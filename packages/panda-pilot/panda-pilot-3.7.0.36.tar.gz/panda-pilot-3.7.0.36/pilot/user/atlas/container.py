#!/usr/bin/env python
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Authors:
# - Paul Nilsson, paul.nilsson@cern.ch, 2017-23
# - Alexander Bogdanchikov, Alexander.Bogdanchikov@cern.ch, 2019-20

import json
import os
import pipes
import re
import logging
from typing import Any

# for user container test: import urllib

from pilot.common.errorcodes import ErrorCodes
from pilot.common.exception import PilotException, FileHandlingFailure
from pilot.user.atlas.setup import get_asetup, get_file_system_root_path
from pilot.user.atlas.proxy import get_and_verify_proxy, get_voms_role
from pilot.info import InfoService, infosys
from pilot.util.config import config
from pilot.util.filehandling import (
    grep,
    remove,
    write_file
)

logger = logging.getLogger(__name__)
errors = ErrorCodes()


def do_use_container(**kwargs):
    """
    Decide whether to use a container or not.

    :param kwargs: dictionary of key-word arguments.
    :return: True if function has decided that a container should be used, False otherwise (boolean).
    """

    # to force no container use: return False
    use_container = False

    job = kwargs.get('job', False)
    copytool = kwargs.get('copytool', False)
    if job:
        # for user jobs, TRF option --containerImage must have been used, ie imagename must be set
        if job.imagename and job.imagename != 'NULL':
            use_container = True
            logger.debug('job.imagename set -> use_container = True')
        elif not (job.platform or job.alrbuserplatform):
            use_container = False
            logger.debug('not (job.platform or job.alrbuserplatform) -> use_container = False')
        else:
            queuedata = job.infosys.queuedata
            container_name = queuedata.container_type.get("pilot")
            if container_name:
                use_container = True
                logger.debug('container_name == \'%s\' -> use_container = True', container_name)
            else:
                logger.debug('else -> use_container = False')
    elif copytool:
        # override for copytools - use a container for stage-in/out
        use_container = True
        logger.debug('copytool -> use_container = False')
    else:
        logger.debug('not job -> use_container = False')

    return use_container


def wrapper(executable, **kwargs):
    """
    Wrapper function for any container specific usage.
    This function will be called by pilot.util.container.execute() and prepends the executable with a container command.

    :param executable: command to be executed (string).
    :param kwargs: dictionary of key-word arguments.
    :return: executable wrapped with container command (string).
    """

    workdir = kwargs.get('workdir', '.')
    pilot_home = os.environ.get('PILOT_HOME', '')
    job = kwargs.get('job', None)

    if workdir == '.' and pilot_home != '':
        workdir = pilot_home

    # if job.imagename (from --containerimage <image>) is set, then always use raw singularity/apptainer
    if config.Container.setup_type == "ALRB":  # and job and not job.imagename:
        fctn = alrb_wrapper
    else:
        fctn = container_wrapper
    return fctn(executable, workdir, job=job)


def extract_platform_and_os(platform):
    """
    Extract the platform and OS substring from platform

    :param platform (string): E.g. "x86_64-slc6-gcc48-opt"
    :return: extracted platform specifics (string). E.g. "x86_64-slc6". In case of failure, return the full platform
    """

    pattern = r"([A-Za-z0-9_-]+)-.+-.+"
    found = re.findall(re.compile(pattern), platform)

    if found:
        ret = found[0]
    else:
        logger.warning("could not extract architecture and OS substring using pattern=%s from platform=%s"
                       "(will use %s for image name)", pattern, platform, platform)
        ret = platform

    return ret


def get_grid_image(platform):
    """
    Return the full path to the singularity/apptainer grid image

    :param platform: E.g. "x86_64-slc6" (string).
    :return: full path to grid image (string).
    """

    if not platform or platform == "":
        platform = "x86_64-slc6"
        logger.warning("using default platform=%s (cmtconfig not set)", platform)

    arch_and_os = extract_platform_and_os(platform)
    image = arch_and_os + ".img"
    _path1 = os.path.join(get_file_system_root_path(), "atlas.cern.ch/repo/containers/images/apptainer")
    _path2 = os.path.join(get_file_system_root_path(), "atlas.cern.ch/repo/containers/images/singularity")
    paths = [path for path in [_path1, _path2] if os.path.isdir(path)]
    _path = paths[0]
    path = os.path.join(_path, image)
    if not os.path.exists(path):
        image = 'x86_64-centos7.img'
        logger.warning('path does not exist: %s (trying with image %s instead)', path, image)
        path = os.path.join(_path, image)
        if not os.path.exists(path):
            logger.warning('path does not exist either: %s', path)
            path = ""

    return path


def get_middleware_type():
    """
    Return the middleware type from the container type.
    E.g. container_type = 'singularity:pilot;docker:wrapper;container:middleware'
    get_middleware_type() -> 'container', meaning that middleware should be taken from the container. The default
    is otherwise 'workernode', i.e. middleware is assumed to be present on the worker node.

    :return: middleware_type (string)
    """

    middleware_type = ""
    container_type = infosys.queuedata.container_type

    middleware = 'middleware'
    if container_type and container_type != "" and middleware in container_type:
        try:
            container_names = container_type.split(';')
            for name in container_names:
                _split = name.split(':')
                if middleware == _split[0]:
                    middleware_type = _split[1]
        except IndexError as exc:
            logger.warning("failed to parse the container name: %s, %s", container_type, exc)
    else:
        # logger.warning("container middleware type not specified in queuedata")
        # no middleware type was specified, assume that middleware is present on worker node
        middleware_type = "workernode"

    return middleware_type


def extract_atlas_setup(asetup, swrelease):
    """
    Extract the asetup command from the full setup command for jobs that have a defined release.
    export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase;
      source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet;source $AtlasSetup/scripts/asetup.sh
    -> $AtlasSetup/scripts/asetup.sh, export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase; source
         ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet;

    :param asetup: full asetup command (string).
    :param swrelease: ATLAS release (string).
    :return: extracted asetup command, cleaned up full asetup command without asetup.sh (string).
    """

    logger.debug(f'swrelease={swrelease}')
    if not swrelease:
        return '', ''

    try:
        # source $AtlasSetup/scripts/asetup.sh
        asetup = asetup.strip()
        atlas_setup = asetup.split(';')[-1] if not asetup.endswith(';') else asetup.split(';')[-2]
        # export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase;
        #   source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet;
        cleaned_atlas_setup = asetup.replace(atlas_setup, '').replace(';;', ';')
        atlas_setup = atlas_setup.replace('source ', '')
    except AttributeError as exc:
        logger.debug('exception caught while extracting asetup command: %s', exc)
        atlas_setup = ''
        cleaned_atlas_setup = ''

    return atlas_setup, cleaned_atlas_setup


def extract_full_atlas_setup(cmd, atlas_setup):
    """
    Extract the full asetup (including options) from the payload setup command.
    atlas_setup is typically '$AtlasSetup/scripts/asetup.sh'.

    :param cmd: full payload setup command (string).
    :param atlas_setup: asetup command (string).
    :return: extracted full asetup command, updated full payload setup command without asetup part (string).
    """

    updated_cmds = []
    extracted_asetup = ""

    logger.debug(f'cmd={cmd}, atlas_setup={atlas_setup}')

    if not atlas_setup:
        return extracted_asetup, cmd

    try:
        _cmd = cmd.split(';')
        for subcmd in _cmd:
            if atlas_setup in subcmd:
                extracted_asetup = subcmd
            else:
                updated_cmds.append(subcmd)
        updated_cmd = ';'.join(updated_cmds)
    except AttributeError as exc:
        logger.warning('exception caught while extracting full atlas setup: %s', exc)
        updated_cmd = cmd
    logger.debug('updated payload setup command: %s', updated_cmd)

    return extracted_asetup, updated_cmd


def update_alrb_setup(cmd, use_release_setup):
    """
    Update the ALRB setup command.
    Add the ALRB_CONT_SETUPFILE in case the release setup file was created earlier (required available cvmfs).

    :param cmd: full ALRB setup command (string).
    :param use_release_setup: should the release setup file be added to the setup command? (Boolean).
    :return: updated ALRB setup command (string).
    """

    updated_cmds = []
    try:
        _cmd = cmd.split(';')
        for subcmd in _cmd:
            if subcmd.startswith('source ${ATLAS_LOCAL_ROOT_BASE}') and use_release_setup:
                updated_cmds.append('export ALRB_CONT_SETUPFILE="/srv/%s"' % config.Container.release_setup)
            updated_cmds.append(subcmd)
        updated_cmd = ';'.join(updated_cmds)
    except AttributeError as exc:
        logger.warning('exception caught while extracting full atlas setup: %s', exc)
        updated_cmd = cmd
    logger.debug('updated ALRB command: %s', updated_cmd)

    return updated_cmd


def update_for_user_proxy(_cmd, cmd, is_analysis=False, queue_type=''):
    """
    Add the X509 user proxy to the container sub command string if set, and remove it from the main container command.
    Try to receive payload proxy and update X509_USER_PROXY in container setup command
    In case payload proxy from server is required, this function will also download and verify this proxy.

    :param _cmd: container setup command (string).
    :param cmd: command the container will execute (string).
    :param is_analysis: True for user job (Boolean).
    :param queue_type: queue type (e.g. 'unified') (string).
    :return: exit_code (int), diagnostics (string), updated _cmd (string), updated cmd (string).
    """

    exit_code = 0
    diagnostics = ""

    #x509 = os.environ.get('X509_USER_PROXY', '')
    x509 = os.environ.get('X509_UNIFIED_DISPATCH', os.environ.get('X509_USER_PROXY', ''))
    logger.debug(f'using X509_USER_PROXY={x509}')
    if x509 != "":
        # do not include the X509_USER_PROXY in the command the container will execute
        cmd = cmd.replace(f"export X509_USER_PROXY={x509};", '')
        # add it instead to the container setup command:

        # download and verify payload proxy from the server if desired
        proxy_verification = os.environ.get('PILOT_PROXY_VERIFICATION') == 'True' and os.environ.get('PILOT_PAYLOAD_PROXY_VERIFICATION') == 'True'
        if proxy_verification and config.Pilot.payload_proxy_from_server and is_analysis and queue_type != 'unified':
            voms_role = get_voms_role(role='user')
            exit_code, diagnostics, x509 = get_and_verify_proxy(x509, voms_role=voms_role, proxy_type='payload')
            if exit_code != 0:  # do not return non-zero exit code if only download fails
                logger.warning('payload proxy verification failed')

        # add X509_USER_PROXY setting to the container setup command
        _cmd = f"export X509_USER_PROXY={x509};" + _cmd

    return exit_code, diagnostics, _cmd, cmd


def set_platform(job, alrb_setup):
    """
    Set thePlatform variable and add it to the sub container command.

    :param job: job object.
    :param alrb_setup: ALRB setup (string).
    :return: updated ALRB setup (string).
    """

    if job.alrbuserplatform:
        alrb_setup += 'export thePlatform=\"%s\";' % job.alrbuserplatform
    elif job.preprocess and job.containeroptions:
        alrb_setup += 'export thePlatform=\"%s\";' % job.containeroptions.get('containerImage')
    elif job.imagename:
        alrb_setup += 'export thePlatform=\"%s\";' % job.imagename
    elif job.platform:
        alrb_setup += 'export thePlatform=\"%s\";' % job.platform

    return alrb_setup


def get_container_options(container_options):
    """
    Get the container options from AGIS for the container execution command.
    For Raythena ES jobs, replace the -C with "" (otherwise IPC does not work, needed by yampl).

    :param container_options: container options from AGIS (string).
    :return: updated container command (string).
    """

    is_raythena = os.environ.get('PILOT_ES_EXECUTOR_TYPE', 'generic') == 'raythena'

    opts = ''
    # Set the singularity/apptainer options
    if container_options:
        # the event service payload cannot use -C/--containall since it will prevent yampl from working
        if is_raythena:
            if '-C' in container_options:
                container_options = container_options.replace('-C', '')
            if '--containall' in container_options:
                container_options = container_options.replace('--containall', '')
        if container_options:
            opts += '-e \"%s\"' % container_options
    else:
        # consider using options "-c -i -p" instead of "-C". The difference is that the latter blocks all environment
        # variables by default and the former does not
        # update: skip the -i to allow IPC, otherwise yampl won't work
        if is_raythena:
            pass
            # opts += 'export ALRB_CONT_CMDOPTS=\"$ALRB_CONT_CMDOPTS -c -i -p\";'
        else:
            opts += '-e \"-C\"'

    return opts


def alrb_wrapper(cmd: str, workdir: str, job: Any = None) -> str:
    """
    Wrap the given command with the special ALRB setup for containers
    E.g. cmd = /bin/bash hello_world.sh
    ->
    export thePlatform="x86_64-slc6-gcc48-opt"
    export ALRB_CONT_RUNPAYLOAD="cmd'
    setupATLAS -c $thePlatform

    :param cmd (string): command to be executed in a container.
    :param workdir: (not used)
    :param job: job object.
    :return: prepended command with singularity/apptainer execution command (string).
    """

    if not job:
        logger.warning('the ALRB wrapper did not get a job object - cannot proceed')
        return cmd

    queuedata = job.infosys.queuedata
    container_name = queuedata.container_type.get("pilot")  # resolve container name for user=pilot
    if container_name:
        # first get the full setup, which should be removed from cmd (or ALRB setup won't work)
        _asetup = get_asetup()
        _asetup = fix_asetup(_asetup)
        # get_asetup()
        # -> export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase;source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
        #     --quiet;source $AtlasSetup/scripts/asetup.sh
        # atlas_setup = $AtlasSetup/scripts/asetup.sh
        # clean_asetup = export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase;source
        #                   ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet;
        atlas_setup, clean_asetup = extract_atlas_setup(_asetup, job.swrelease)
        full_atlas_setup = get_full_asetup(cmd, 'source ' + atlas_setup) if atlas_setup and clean_asetup else ''

        # do not include 'clean_asetup' in the container script
        if clean_asetup and full_atlas_setup:
            cmd = cmd.replace(clean_asetup, '')
            # for stand-alone containers, do not include the full atlas setup either
            if job.imagename:
                cmd = cmd.replace(full_atlas_setup, '')

        # get_asetup(asetup=False)
        # -> export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase;source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet;

        # get simplified ALRB setup (export)
        alrb_setup = get_asetup(alrb=True, add_if=True)
        alrb_setup = fix_asetup(alrb_setup)

        # get_asetup(alrb=True)
        # -> export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase;
        # get_asetup(alrb=True, add_if=True)
        # -> if [ -z "$ATLAS_LOCAL_ROOT_BASE" ]; then export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase; fi;

        # add user proxy if necessary (actually it should also be removed from cmd)
        exit_code, diagnostics, alrb_setup, cmd = update_for_user_proxy(alrb_setup, cmd, is_analysis=job.is_analysis(), queue_type=job.infosys.queuedata.type)
        if exit_code:
            job.piloterrordiag = diagnostics
            job.piloterrorcodes, job.piloterrordiags = errors.add_error_code(exit_code)
        # set the platform info
        alrb_setup = set_platform(job, alrb_setup)

        # add the jobid to be used as an identifier for the payload running inside the container
        # it is used to identify the pid for the process to be tracked by the memory monitor
        if 'export PandaID' not in alrb_setup:
            alrb_setup += f"export PandaID={job.jobid};"

        # add TMPDIR
        cmd = "export TMPDIR=/srv;export GFORTRAN_TMPDIR=/srv;" + cmd
        cmd = cmd.replace(';;', ';')

        # get the proper release setup script name, and create the script if necessary
        release_setup, cmd = create_release_setup(cmd, atlas_setup, full_atlas_setup, job.swrelease,
                                                  job.workdir, queuedata.is_cvmfs)

        # prepend the docker login if necessary
        # does the pandasecrets dictionary contain any docker login info?
        pandasecrets = str(job.pandasecrets)
        if pandasecrets and "token" in pandasecrets and \
                has_docker_pattern(pandasecrets, pattern=r'docker://[^/]+/'):
            # if so, add it do the container script
            logger.info('adding sensitive docker login info')
            cmd = add_docker_login(cmd, job.pandasecrets)

        # correct full payload command in case preprocess command are used (ie replace trf with setupATLAS -c ..)
        if job.preprocess and job.containeroptions:
            cmd = replace_last_command(cmd, job.containeroptions.get('containerExec'))

        # write the full payload command to a script file
        container_script = config.Container.container_script
        _cmd = obscure_token(cmd)  # obscure any token if present
        if _cmd:
            logger.info(f'command to be written to container script file:\n\n{container_script}:\n\n{_cmd}\n')
        else:
            logger.warning('will not show container script file since the user token could not be obscured')
        try:
            write_file(os.path.join(job.workdir, container_script), cmd, mute=False)
            os.chmod(os.path.join(job.workdir, container_script), 0o755)  # Python 2/3
        # except (FileHandlingFailure, FileNotFoundError) as exc:  # Python 3
        except (FileHandlingFailure, OSError) as exc:  # Python 2/3
            logger.warning(f'exception caught: {exc}')
            return ""

        # also store the command string in the job object
        job.command = cmd

        # add atlasLocalSetup command + options (overwrite the old cmd since the new cmd is the containerised version)
        cmd = add_asetup(job, alrb_setup, queuedata.is_cvmfs, release_setup, container_script, queuedata.container_options)

        # add any container options if set
        execargs = job.containeroptions.get('execArgs', None)
        if execargs:
            cmd += ' ' + execargs
        logger.debug(f'\n\nfinal command:\n\n{cmd}\n')
    else:
        logger.warning('container name not defined in CRIC')

    return cmd


def obscure_token(cmd: str) -> str:
    """
    Obscure any user token from the payload command.

    :param cmd: payload command (str)
    :return: updated command (str).
    """

    try:
        match = re.search(r'-p (\S+);', cmd)
        if match:
            cmd = cmd.replace(match.group(1), '********')
    except (re.error, AttributeError, IndexError):
        logger.warning('an exception was thrown while trying to obscure the user token')
        cmd = ''

    return cmd


def add_docker_login(cmd: str, pandasecrets: dict) -> dict:
    """
    Add docker login to user command.

    The pandasecrets dictionary was found to contain login information (username + token). This function
    will add it to the payload command that will be run in the user container.

    :param cmd: payload command (str)
    :param pandasecrets: panda secrets (dict)
    :return: updated payload command (str).
    """

    pattern = r'docker://[^/]+/'
    tmp = json.loads(pandasecrets)
    docker_tokens = tmp.get('DOCKER_TOKENS', None)
    if docker_tokens:
        try:
            docker_token = json.loads(docker_tokens)
            if docker_token:
                token_dict = docker_token[0]
                username = token_dict.get('username', None)
                token = token_dict.get('token', None)
                registry_path = token_dict.get('registry_path', None)
                if username and token and registry_path:
                    # extract the registry (e.g. docker://gitlab-registry.cern.ch/) from the path
                    try:
                        match = re.search(pattern, registry_path)
                        if match:
                            cmd = f'docker login {match.group(0)} -u {username} -p {token}; ' + cmd
                        else:
                            logger.warning(f'failed to extract registry from {registry_path}')
                    except re.error as regex_error:
                        err = str(regex_error)
                        entry = err.find('token')
                        err = err[:entry]  # cut away any token
                        logger.warning(f'error in regular expression: {err}')
                else:
                    logger.warning(
                        'either username, token, or registry_path was not set in DOCKER_TOKENS dictionary')
            else:
                logger.warning('failed to convert DOCKER_TOKENS str to dict')
        except json.JSONDecodeError as json_error:
            err = str(json_error)
            entry = err.find('token')
            err = err[:entry]  # cut away any token
            logger.warning(f'error decoding JSON data: {err}')
    else:
        logger.warning('failed to read DOCKER_TOKENS key from panda secrets')

    return cmd


def add_asetup(job, alrb_setup, is_cvmfs, release_setup, container_script, container_options):
    """
    Add atlasLocalSetup and options to form the final payload command.

    :param job: job object.
    :param alrb_setup: ALRB setup (string).
    :param is_cvmfs: True for cvmfs sites (Boolean).
    :param release_setup: release setup (string).
    :param container_script: container script name (string).
    :param container_options: container options (string).
    :return: final payload command (string).
    """

    # this should not be necessary after the extract_container_image() in JobData update
    # containerImage should have been removed already
    if '--containerImage' in job.jobparams:
        job.jobparams, container_path = remove_container_string(job.jobparams)
        if job.alrbuserplatform:
            if not is_cvmfs:
                alrb_setup += 'source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c %s' % job.alrbuserplatform
        elif container_path != "":
            alrb_setup += 'source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c %s' % container_path
        else:
            logger.warning('failed to extract container path from %s', job.jobparams)
            alrb_setup = ""
        if alrb_setup and not is_cvmfs:
            alrb_setup += ' -d'
    else:
        alrb_setup += 'source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh '
        if job.platform or job.alrbuserplatform or job.imagename:
            alrb_setup += '-c $thePlatform'
            if not is_cvmfs:
                alrb_setup += ' -d'

    # update the ALRB setup command
    alrb_setup += ' -s %s' % release_setup
    alrb_setup += ' -r /srv/' + container_script
    alrb_setup = alrb_setup.replace('  ', ' ').replace(';;', ';')

    # add container options
    alrb_setup += ' ' + get_container_options(container_options)
    alrb_setup = alrb_setup.replace('  ', ' ')
    cmd = alrb_setup

    # correct full payload command in case preprocess command are used (ie replace trf with setupATLAS -c ..)
    #if job.preprocess and job.containeroptions:
    #    logger.debug('will update cmd=%s', cmd)
    #    cmd = replace_last_command(cmd, 'source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c $thePlatform')
    #    logger.debug('updated cmd with containerImage')

    return cmd


def get_full_asetup(cmd, atlas_setup):
    """
    Extract the full asetup command from the payload execution command.
    (Easier that generating it again). We need to remove this command for stand-alone containers.
    Alternatively: do not include it in the first place (but this seems to trigger the need for further changes).
    atlas_setup is "source $AtlasSetup/scripts/asetup.sh", which is extracted in a previous step.
    The function typically returns: "source $AtlasSetup/scripts/asetup.sh 21.0,Athena,2020-05-19T2148,notest --makeflags='$MAKEFLAGS';".

    :param cmd: payload execution command (string).
    :param atlas_setup: extracted atlas setup (string).
    :return: full atlas setup (string).
    """

    pos = cmd.find(atlas_setup)
    cmd = cmd[pos:]  # remove everything before 'source $AtlasSetup/..'
    pos = cmd.find(';')
    cmd = cmd[:pos + 1]  # remove everything after the first ;, but include the trailing ;

    return cmd


def replace_last_command(cmd, replacement):
    """
    Replace the last command in cmd with given replacement.

    :param cmd: command (string).
    :param replacement: replacement (string).
    :return: updated command (string).
    """

    cmd = cmd.strip('; ')
    last_bit = cmd.split(';')[-1]
    cmd = cmd.replace(last_bit.strip(), replacement)

    return cmd


def create_release_setup(cmd, atlas_setup, full_atlas_setup, release, workdir, is_cvmfs):
    """
    Get the proper release setup script name, and create the script if necessary.

    This function also updates the cmd string (removes full asetup from payload command).

    :param cmd: Payload execution command (string).
    :param atlas_setup: asetup command (string).
    :param full_atlas_setup: full asetup command (string).
    :param release: software release, needed to determine Athena environment (string).
    :param workdir: job workdir (string).
    :param is_cvmfs: does the queue have cvmfs? (Boolean).
    :return: proper release setup name (string), updated cmd (string).
    """

    release_setup_name = '/srv/my_release_setup.sh'

    # extracted_asetup should be written to 'my_release_setup.sh' and cmd to 'container_script.sh'
    content = 'echo \"INFO: sourcing %s inside the container. ' \
              'This should not run if it is a ATLAS standalone container\"' % release_setup_name
    if is_cvmfs and release and release != 'NULL':
        content, cmd = extract_full_atlas_setup(cmd, atlas_setup)
        if not content:
            content = full_atlas_setup
        content = 'retCode=0\n' + content

    content += '\nretCode=$?'
    # add timing info (hours:minutes:seconds in UTC)
    # this is used to get a better timing info about setup
    content += '\ndate +\"%H:%M:%S %Y/%m/%d\"'  # e.g. 07:36:27 2022/06/29
    content += '\nif [ $? -ne 0 ]; then'
    content += '\n    retCode=$?'
    content += '\nfi'
    content += '\nreturn $retCode'

    logger.debug('command to be written to release setup file:\n\n%s:\n\n%s\n', release_setup_name, content)
    try:
        write_file(os.path.join(workdir, os.path.basename(release_setup_name)), content, mute=False)
    except FileHandlingFailure as exc:
        logger.warning('exception caught: %s', exc)

    return release_setup_name, cmd.replace(';;', ';')


## DEPRECATED, remove after verification with user container job
def remove_container_string(job_params):
    """ Retrieve the container string from the job parameters """

    pattern = r" \'?\-\-containerImage\=?\ ?([\S]+)\ ?\'?"
    compiled_pattern = re.compile(pattern)

    # remove any present ' around the option as well
    job_params = re.sub(r'\'\ \'', ' ', job_params)

    # extract the container path
    found = re.findall(compiled_pattern, job_params)
    container_path = found[0] if found else ""

    # Remove the pattern and update the job parameters
    job_params = re.sub(pattern, ' ', job_params)

    return job_params, container_path


def container_wrapper(cmd, workdir, job=None):
    """
    Prepend the given command with the singularity/apptainer execution command
    E.g. cmd = /bin/bash hello_world.sh
    -> singularity_command = singularity exec -B <bindmountsfromcatchall> <img> /bin/bash hello_world.sh
    singularity exec -B <bindmountsfromcatchall>  /cvmfs/atlas.cern.ch/repo/images/singularity/x86_64-slc6.img <script>
    Note: if the job object is not set, then it is assumed that the middleware container is to be used.
    Note 2: if apptainer is specified in CRIC in the container type, it is assumes that the executable is called
    apptainer.

    :param cmd: command to be prepended (string).
    :param workdir: explicit work directory where the command should be executed (needs to be set for Singularity) (string).
    :param job: job object.
    :return: prepended command with singularity execution command (string).
    """

    if job:
        queuedata = job.infosys.queuedata
    else:
        infoservice = InfoService()
        infoservice.init(os.environ.get('PILOT_SITENAME'), infosys.confinfo, infosys.extinfo)
        queuedata = infoservice.queuedata

    container_name = queuedata.container_type.get("pilot")  # resolve container name for user=pilot
    logger.debug("resolved container_name from queuedata.container_type: %s", container_name)

    if container_name == 'singularity' or container_name == 'apptainer':
        logger.info("singularity/apptainer has been requested")

        # Get the container options
        options = queuedata.container_options
        if options != "":
            options += ","
        else:
            options = "-B "
        options += "/cvmfs,${workdir},/home"
        logger.debug("using options: %s", options)

        # Get the image path
        if job:
            image_path = job.imagename or get_grid_image(job.platform)
        else:
            image_path = config.Container.middleware_container

        # Does the image exist?
        if image_path:
            # Prepend it to the given command
            quote = pipes.quote(f'cd $workdir;pwd;{cmd}')
            cmd = f"export workdir={workdir}; {container_name} --verbose exec {options} {image_path} " \
                  f"/bin/bash -c {quote}"
            #cmd = "export workdir=" + workdir + "; singularity --verbose exec " + options + " " + image_path + \
            #      " /bin/bash -c " + pipes.quote("cd $workdir;pwd;%s" % cmd)

            # for testing user containers
            # singularity_options = "-B $PWD:/data --pwd / "
            # singularity_cmd = "singularity exec " + singularity_options + image_path
            # cmd = re.sub(r'-p "([A-Za-z0-9.%/]+)"', r'-p "%s\1"' % urllib.pathname2url(singularity_cmd), cmd)
        else:
            logger.warning("singularity/apptainer options found but image does not exist")

        logger.info("updated command: %s", cmd)

    return cmd


def create_root_container_command(workdir, cmd):
    """

    :param workdir:
    :param cmd:
    :return:
    """

    command = 'cd %s;' % workdir
    content = get_root_container_script(cmd)
    script_name = 'open_file.sh'

    try:
        status = write_file(os.path.join(workdir, script_name), content)
    except PilotException as exc:
        raise exc
    else:
        if status:
            # generate the final container command
            x509 = os.environ.get('X509_UNIFIED_DISPATCH', os.environ.get('X509_USER_PROXY', ''))
            if x509:
                command += 'export X509_USER_PROXY=%s;' % x509
            command += 'export ALRB_CONT_RUNPAYLOAD=\"source /srv/%s\";' % script_name
            _asetup = get_asetup(alrb=True)  # export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase;
            _asetup = fix_asetup(_asetup)
            command += _asetup
            command += 'source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c CentOS7'

    logger.debug('container command: %s', command)

    return command


def fix_asetup(asetup):
    """
    Make sure that the command returned by get_asetup() contains a trailing ;-sign.

    :param asetup: asetup (string).
    :return: updated asetup (string).
    """

    if asetup and not asetup.strip().endswith(';'):
        asetup += '; '

    return asetup


def create_middleware_container_command(job, cmd, label='stagein', proxy=True):
    """
    Create the container command for stage-in/out or other middleware.

    The function takes the isolated middleware command, adds bits and pieces needed for the containerisation and stores
    it in a script file. It then generates the actual command that will execute the middleware script in a
    container.

    new cmd:
      lsetup rucio davis xrootd
      old cmd
      exit $?
    write new cmd to stage[in|out].sh script
    create container command and return it

    :param job: job object.
    :param cmd: command to be containerised (string).
    :param label: 'stage-[in|out]|setup' (string).
    :param proxy: add proxy export command (Boolean).
    :return: container command to be executed (string).
    """

    command = 'cd %s;' % job.workdir

    # add bits and pieces for the containerisation
    middleware_container = get_middleware_container(label=label)
    content = get_middleware_container_script(middleware_container, cmd, label=label)

    # store it in setup.sh
    if label == 'stage-in':
        script_name = 'stagein.sh'
    elif label == 'stage-out':
        script_name = 'stageout.sh'
    else:
        script_name = 'general.sh'

    # for setup container
    container_script_name = 'container_script.sh'
    try:
        logger.debug('command to be written to container setup file \n\n%s:\n\n%s\n', script_name, content)
        status = write_file(os.path.join(job.workdir, script_name), content)
        if status:
            content = 'echo \"Done\"'
            logger.debug('command to be written to container command file \n\n%s:\n\n%s\n', container_script_name,
                         content)
            status = write_file(os.path.join(job.workdir, container_script_name), content)
    except PilotException as exc:
        raise exc
    else:
        if status:
            # generate the final container command
            if proxy:
                x509 = os.environ.get('X509_USER_PROXY', '')
                if x509:
                    command += 'export X509_USER_PROXY=%s;' % x509
            if not label == 'setup':  # only for stage-in/out; for setup verification, use -s .. -r .. below
                command += 'export ALRB_CONT_RUNPAYLOAD=\"source /srv/%s\";' % script_name
                if 'ALRB_CONT_UNPACKEDDIR' in os.environ:
                    command += 'export ALRB_CONT_UNPACKEDDIR=%s;' % os.environ.get('ALRB_CONT_UNPACKEDDIR')
            command += fix_asetup(get_asetup(alrb=True))  # export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase;
            if label == 'setup':
                # set the platform info
                command += 'export thePlatform=\"%s\";' % job.platform
            command += 'source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh -c %s' % middleware_container
            if label == 'setup':
                command += f' -s /srv/{script_name} -r /srv/{container_script_name}'
            else:
                command += ' ' + get_container_options(job.infosys.queuedata.container_options)
            command = command.replace('  ', ' ')

    logger.debug('container command: %s', command)

    return command


def get_root_container_script(cmd):
    """
    Return the content of the root container script.

    :param cmd: root command (string).
    :return: script content (string).
    """

    # content = 'lsetup \'root 6.20.06-x86_64-centos7-gcc8-opt\'\npython %s\nexit $?' % cmd
    # content = f'date\nlsetup \'root pilot\'\ndate\npython {cmd}\nexit $?'
    content = f'date\nlsetup \'root pilot\'\ndate\nstdbuf -oL bash -c \"python {cmd}\"\nexit $?'
    logger.debug(f'root setup script content:\n\n{content}\n\n')

    return content


def get_middleware_container_script(middleware_container, cmd, asetup=False, label=''):
    """
    Return the content of the middleware container script.
    If asetup is True, atlasLocalSetup will be added to the command.

    :param middleware_container: container image (string).
    :param cmd: isolated stage-in/out command (string).
    :param asetup: optional True/False (boolean).
    :return: script content (string).
    """

    sitename = 'export PILOT_RUCIO_SITENAME=%s; ' % os.environ.get('PILOT_RUCIO_SITENAME')
    if label == 'setup':
        # source $AtlasSetup/scripts/asetup.sh AtlasOffline,21.0.16,notest --platform x86_64-slc6-gcc49-opt --makeflags='$MAKEFLAGS'
        content = cmd[cmd.find('source $AtlasSetup'):]
    elif 'rucio' in middleware_container:
        content = sitename
        content += f'export ATLAS_LOCAL_ROOT_BASE={get_file_system_root_path()}/atlas.cern.ch/repo/ATLASLocalRootBase; '
        content += "alias setupATLAS=\'source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh\'; "
        content += "setupATLAS -3; "
        content = 'lsetup \"python pilot-default\";python3 %s ' % cmd  # only works with python 3
    else:
        content = 'export ALRB_LOCAL_PY3=YES; '
        if asetup:  # export ATLAS_LOCAL_ROOT_BASE=/cvmfs/..;source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet;
            _asetup = get_asetup(asetup=False)
            _asetup = fix_asetup(_asetup)
            content += _asetup
        if label == 'stagein' or label == 'stageout':
            content += sitename + 'lsetup rucio davix xrootd; '
            content += 'python3 %s ' % cmd
        else:
            content += cmd
    if not asetup:
        content += '\nexit $?'

    logger.debug('middleware container content:\n%s', content)

    return content


def get_middleware_container(label=None):
    """
    Return the middleware container.

    :param label: label (string).
    :return: path (string).
    """

    if label and label == 'general':
        return 'CentOS7'

    if label == 'setup':
        path = '$thePlatform'
    elif 'ALRB_CONT_UNPACKEDDIR' in os.environ:
        path = config.Container.middleware_container_no_path
    else:
        path = config.Container.middleware_container
        if path.startswith('/') and not os.path.exists(path):
            logger.warning('requested middleware container path does not exist: %s (switching to default value)', path)
            path = 'CentOS7'
    logger.info('using image: %s for middleware container', path)

    return path


def has_docker_pattern(line, pattern=None):
    """
    Does the given line contain a docker pattern?

    :param line: panda secret (string)
    :param pattern: regular expression pattern (raw string)
    :return: True or False (bool).
    """

    found = False

    if line:
        # if no given pattern, look for a general docker registry URL
        url_pattern = get_url_pattern() if not pattern else pattern
        match = re.search(url_pattern, line)
        if match:
            logger.warning('the given line contains a docker token')
            found = True

    return found


def get_docker_pattern() -> str:
    """
    Return the docker login URL pattern for secret verification.

    Example: docker login <registry URL> -u <username> -p <token>

    :return: pattern (raw string).
    """

    return (
        fr"docker\ login\ {get_url_pattern()}\ \-u\ \S+\ \-p\ \S+;"
    )


def get_url_pattern() -> str:
    """
    Return the URL pattern for secret verification.

    :return: pattern (raw string).
    """

    return (
        r"docker?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\."
        r"[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
    )


def verify_container_script(path):
    """
    If the container_script.sh contains sensitive token info, remove it before creating the log.

    :param path: path to container script (string).
    """

    if os.path.exists(path):
        url_pattern = r'docker\ login'  # docker login <registry> -u <username> -p <token>
        lines = grep([url_pattern], path)
        if lines:
            has_token = has_docker_pattern(lines[0], pattern=url_pattern)
            if has_token:
                logger.warning(f'found sensitive token information in {path} - removing file')
                remove(path)
            else:
                logger.debug(f'no sensitive information in {path}')
        else:
            logger.debug(f'no sensitive information in {path}')
