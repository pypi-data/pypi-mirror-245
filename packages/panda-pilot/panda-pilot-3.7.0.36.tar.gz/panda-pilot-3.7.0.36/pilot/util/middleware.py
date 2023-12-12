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
# - Paul Nilsson, paul.nilsson@cern.ch, 2020-23

from os import environ, path, getcwd

from pilot.common.errorcodes import ErrorCodes
from pilot.common.exception import (
    PilotException,
    StageInFailure,
    StageOutFailure,
)
from pilot.util.config import config
from pilot.util.container import execute
from pilot.util.filehandling import (
    copy,
    read_json,
    write_json,
    write_file,
    copy_pilot_source,
)

import logging
logger = logging.getLogger(__name__)
errors = ErrorCodes()


def containerise_general_command(job, container_options, label='command', container_type='container'):
    """
    Containerise a general command by execution in a script that can be run in a container.

    :param job: job object.
    :param label: label (string).
    :param container_options: container options from queuedata (string).
    :param container_type: optional 'container/bash'
    :raises PilotException: for general failures.
    :return:
    """

    cwd = getcwd()

    if container_type == 'container':
        # add bits and pieces needed to run the cmd in a container
        pilot_user = environ.get('PILOT_USER', 'generic').lower()
        user = __import__('pilot.user.%s.container' % pilot_user, globals(), locals(), [pilot_user], 0)
        try:
            cmd = user.create_middleware_container_command(job, job.debug_command, label=label, proxy=False)
        except PilotException as exc:
            raise exc
    else:
        logger.warning('not yet implemented')
        raise PilotException

    try:
        logger.info(f'*** executing {label} (logging will be redirected) ***')
        exit_code, stdout, stderr = execute(cmd, job=job, usecontainer=False)
    except Exception as exc:
        logger.info(f'*** {label} has failed ***')
        logger.warning(f'exception caught: {exc}')
    else:
        if exit_code == 0:
            logger.info(f'*** {label} has finished ***')
        else:
            logger.info(f'*** {label} has failed ***')
        logger.debug(f'{label} script returned exit_code={exit_code}')


def containerise_middleware(job, xdata, queue, eventtype, localsite, remotesite, container_options, external_dir,
                            label='stage-in', container_type='container', rucio_host=''):
    """
    Containerise the middleware by performing stage-in/out steps in a script that in turn can be run in a container.

    Note: a container will only be used for option container_type='container'. If this is 'bash', then stage-in/out
    will still be done by a script, but not containerised.

    Note: this function is tailor made for stage-in/out.

    :param job: job object.
    :param xdata: list of FileSpec objects.
    :param queue: queue name (string).
    :param eventtype:
    :param localsite:
    :param remotesite:
    :param container_options: container options from queuedata (string).
    :param external_dir: input or output files directory (string).
    :param label: optional 'stage-in/out' (string).
    :param container_type: optional 'container/bash' (string).
    :param rucio_host: optiona rucio host (string).
    :raises StageInFailure: for stage-in failures
    :raises StageOutFailure: for stage-out failures
    :return:
    """

    cwd = getcwd()

    # get the name of the stage-in/out isolation script
    script = config.Container.middleware_container_stagein_script if label == 'stage-in' else config.Container.middleware_container_stageout_script

    try:
        cmd = get_command(job, xdata, queue, script, eventtype, localsite, remotesite, external_dir, label=label,
                          container_type=container_type, rucio_host=rucio_host)
    except PilotException as exc:
        raise exc

    if container_type == 'container':
        # add bits and pieces needed to run the cmd in a container
        pilot_user = environ.get('PILOT_USER', 'generic').lower()
        user = __import__('pilot.user.%s.container' % pilot_user, globals(), locals(), [pilot_user], 0)
        try:
            cmd = user.create_middleware_container_command(job, cmd, label=label)
        except PilotException as exc:
            raise exc
    else:
        logger.warning(f'{label} will not be done in a container (but it will be done by a script)')

    try:
        logger.info(f'*** executing {label} (logging will be redirected) ***')
        exit_code, stdout, stderr = execute(cmd, job=job, usecontainer=False)
    except Exception as exc:
        logger.info(f'*** {label} has failed ***')
        logger.warning(f'exception caught: {exc}')
    else:
        if exit_code == 0:
            logger.info(f'*** {label} has finished ***')
        else:
            logger.info(f'*** {label} has failed ***')
            logger.warning(f'stderr:\n{stderr}')
            logger.warning(f'stdout:\n{stdout}')
        logger.debug(f'{label} script returned exit_code={exit_code}')

        # write stdout+stderr to files
        try:
            _stdout_name, _stderr_name = get_logfile_names(label)
            write_file(path.join(job.workdir, _stdout_name), stdout, mute=False)
            write_file(path.join(job.workdir, _stderr_name), stderr, mute=False)
        except PilotException as exc:
            msg = f'exception caught: {exc}'
            if label == 'stage-in':
                raise StageInFailure(msg)
            else:
                raise StageOutFailure(msg)

    # handle errors, file statuses, etc (the stage-in/out scripts write errors and file status to a json file)
    try:
        handle_updated_job_object(job, xdata, label=label)
    except PilotException as exc:
        raise exc


def get_script_path(script):
    """
    Return the path for the script.

    :param script: script name (string).
    :return: path (string).
    """

    srcdir = environ.get('PILOT_SOURCE_DIR', '.')
    _path = path.join(srcdir, 'pilot/scripts')
    if not path.exists(_path):
        _path = path.join(srcdir, 'pilot3')
        _path = path.join(_path, 'pilot/scripts')
    _path = path.join(_path, script)
    if not path.exists(_path):
        _path = ''

    return _path


def get_command(job, xdata, queue, script, eventtype, localsite, remotesite, external_dir, label='stage-in',
                container_type='container', rucio_host=''):
    """
    Get the middleware container execution command.

    Note: this function is tailor made for stage-in/out.

    :param job: job object.
    :param xdata: list of FileSpec objects.
    :param queue: queue name (string).
    :param script: name of stage-in/out script (string).
    :param eventtype:
    :param localsite:
    :param remotesite:
    :param external_dir: input or output files directory (string).
    :param label: optional 'stage-[in|out]' (string).
    :param container_type: optional 'container/bash' (string).
    :param rucio_host: optional rucio host (string).
    :return: stage-in/out command (string).
    :raises PilotException: for stage-in/out related failures
    """

    if label == 'stage-out':
        filedata_dictionary = get_filedata_strings(xdata)
    else:
        filedata_dictionary = get_filedata(xdata)

        # write file data to file
        status = write_json(path.join(job.workdir, config.Container.stagein_replica_dictionary), filedata_dictionary)
        if not status:
            diagnostics = 'failed to write replica dictionary to file'
            logger.warning(diagnostics)
            raise PilotException(diagnostics)

    # copy pilot source into container directory, unless it is already there
    diagnostics = copy_pilot_source(job.workdir)
    if diagnostics:
        raise PilotException(diagnostics)

    final_script_path = path.join(job.workdir, script)
    environ['PYTHONPATH'] = environ.get('PYTHONPATH') + ':' + job.workdir
    script_path = path.join('pilot/scripts', script)
    full_script_path = path.join(path.join(job.workdir, script_path))
    copy(full_script_path, final_script_path)

    if container_type == 'container':
        # correct the path when containers have been used
        final_script_path = path.join('.', script)
        workdir = '/srv'
    else:
        # for container_type=bash we need to add the rucio setup
        pilot_user = environ.get('PILOT_USER', 'generic').lower()
        user = __import__('pilot.user.%s.container' % pilot_user, globals(), locals(), [pilot_user], 0)
        try:
            final_script_path = user.get_middleware_container_script('', final_script_path, asetup=True)
        except PilotException:
            final_script_path = 'python %s' % final_script_path
        workdir = job.workdir

    cmd = "%s -d -w %s -q %s --eventtype=%s --localsite=%s --remotesite=%s --produserid=\"%s\" --jobid=%s" % \
          (final_script_path, workdir, queue, eventtype, localsite, remotesite, job.produserid.replace(' ', '%20'), job.jobid)

    if label == 'stage-in':
        cmd += " --eventservicemerge=%s --usepcache=%s --usevp=%s --replicadictionary=%s" % \
               (job.is_eventservicemerge, job.infosys.queuedata.use_pcache, job.use_vp, config.Container.stagein_replica_dictionary)
        if external_dir:
            cmd += ' --inputdir=%s' % external_dir
    else:  # stage-out
        cmd += ' --lfns=%s --scopes=%s --datasets=%s --ddmendpoints=%s --guids=%s' % \
               (filedata_dictionary['lfns'], filedata_dictionary['scopes'], filedata_dictionary['datasets'],
                filedata_dictionary['ddmendpoints'], filedata_dictionary['guids'])
        if external_dir:
            cmd += ' --outputdir=%s' % external_dir

    cmd += ' --taskid=%s' % job.taskid
    cmd += ' --jobdefinitionid=%s' % job.jobdefinitionid
    cmd += ' --catchall=\'%s\'' % job.infosys.queuedata.catchall
    cmd += ' --rucio_host=\'%s\'' % rucio_host

    if container_type == 'bash':
        cmd += '\nexit $?'

    return cmd


def handle_updated_job_object(job, xdata, label='stage-in'):
    """
    Handle updated job object fields.

    :param job: job object.
    :param xdata: list of FileSpec objects.
    :param label: 'stage-in/out' (string).
    :return:
    :raises: StageInFailure, StageOutFailure
    """

    dictionary_name = config.Container.stagein_status_dictionary if label == 'stage-in' else config.Container.stageout_status_dictionary

    # read the JSON file created by the stage-in/out script
    if path.exists(path.join(job.workdir, dictionary_name + '.log')):
        dictionary_name += '.log'
    file_dictionary = read_json(path.join(job.workdir, dictionary_name))

    # update the job object accordingly
    if file_dictionary:
        # get file info and set essential parameters
        for fspec in xdata:
            try:
                fspec.status = file_dictionary[fspec.lfn][0]
                fspec.status_code = file_dictionary[fspec.lfn][1]
                if label == 'stage-in':
                    fspec.turl = file_dictionary[fspec.lfn][2]
                    fspec.ddmendpoint = file_dictionary[fspec.lfn][3]
                else:
                    fspec.surl = file_dictionary[fspec.lfn][2]
                    fspec.turl = file_dictionary[fspec.lfn][3]
                    fspec.checksum[config.File.checksum_type] = file_dictionary[fspec.lfn][4]
                    fspec.filesize = file_dictionary[fspec.lfn][5]
            except Exception as exc:
                msg = f"exception caught while reading file dictionary: {exc}"
                logger.warning(msg)
                if label == 'stage-in':
                    raise StageInFailure(msg)
                else:
                    raise StageOutFailure(msg)

        # get main error info ('error': [error_diag, error_code])
        error_diag = file_dictionary['error'][0]
        error_code = file_dictionary['error'][1]
        if error_code:
            job.piloterrorcodes, job.piloterrordiags = errors.add_error_code(error_code, msg=error_diag)
    else:
        msg = f"{label} file dictionary not found"
        logger.warning(msg)
        if label == 'stage-in':
            raise StageInFailure(msg)
        else:
            raise StageOutFailure(msg)


def get_logfile_names(label):
    """
    Get the proper names for the redirected stage-in/out logs.

    :param label: 'stage-[in|out]' (string)
    :return: 'stage[in|out]_stdout' (string), 'stage[in|out]_stderr' (string).
    """

    if label == 'stage-in':
        _stdout_name = config.Container.middleware_stagein_stdout
        _stderr_name = config.Container.middleware_stagein_stderr
    else:
        _stdout_name = config.Container.middleware_stageout_stdout
        _stderr_name = config.Container.middleware_stageout_stderr
    if not _stdout_name:
        _stdout_name = 'stagein_stdout.txt' if label == 'stage-in' else 'stageout_stdout.txt'
    if not _stderr_name:
        _stderr_name = 'stagein_stderr.txt' if label == 'stage-in' else 'stageout_stderr.txt'

    return _stdout_name, _stderr_name


def get_filedata(data):
    """
    Return a dictionary with LFNs, guids, scopes, datasets, ddmendpoints, etc.
    Note: this dictionary will be written to a file that will be read back by the stage-in script inside the container.
    Dictionary format:
        { lfn1: { 'guid': guid1, 'scope': scope1, 'dataset': dataset1, 'ddmendpoint': ddmendpoint1,
                  'filesize': filesize1, 'checksum': checksum1, 'allowlan': allowlan1, 'allowwan': allowwan1,
                  'directaccesslan': directaccesslan1, 'directaccesswan': directaccesswan1, 'istar': istar1,
                  'accessmode': accessmode1, 'storagetoken': storagetoken1}, lfn2: .. }
    :param data:
    :type data:
    :return:
    :rtype:
    """

    file_dictionary = {}
    for fspec in data:
        try:
            _type = 'md5' if ('md5' in fspec.checksum and 'adler32' not in fspec.checksum) else 'adler32'
            file_dictionary[fspec.lfn] = {'guid': fspec.guid,
                                          'scope': fspec.scope,
                                          'dataset': fspec.dataset,
                                          'ddmendpoint': fspec.ddmendpoint,
                                          'filesize': fspec.filesize,
                                          'checksum': fspec.checksum.get(_type, 'None'),
                                          'allowlan': fspec.allow_lan,
                                          'allowwan': fspec.allow_wan,
                                          'directaccesslan': fspec.direct_access_lan,
                                          'directaccesswan': fspec.direct_access_wan,
                                          'istar': fspec.is_tar,
                                          'accessmode': fspec.accessmode,
                                          'storagetoken': fspec.storage_token}
        except Exception as exc:
            logger.warning(f'exception caught in get_filedata(): {exc}')

    return file_dictionary


def get_filedata_strings(data):
    """
    Return a dictionary with comma-separated list of LFNs, guids, scopes, datasets, ddmendpoints, etc.

    :param data: job [in|out]data (list of FileSpec objects).
    :return: {'lfns': lfns, ..} (dictionary).
    """

    lfns = ""
    guids = ""
    scopes = ""
    datasets = ""
    ddmendpoints = ""
    filesizes = ""
    checksums = ""
    allowlans = ""
    allowwans = ""
    directaccesslans = ""
    directaccesswans = ""
    istars = ""
    accessmodes = ""
    storagetokens = ""
    for fspec in data:
        lfns = fspec.lfn if lfns == "" else lfns + ",%s" % fspec.lfn
        guids = fspec.guid if guids == "" else guids + ",%s" % fspec.guid
        scopes = fspec.scope if scopes == "" else scopes + ",%s" % fspec.scope
        datasets = fspec.dataset if datasets == "" else datasets + ",%s" % fspec.dataset
        ddmendpoints = fspec.ddmendpoint if ddmendpoints == "" else ddmendpoints + ",%s" % fspec.ddmendpoint
        filesizes = str(fspec.filesize) if filesizes == "" else filesizes + ",%s" % fspec.filesize
        _type = 'md5' if ('md5' in fspec.checksum and 'adler32' not in fspec.checksum) else 'adler32'
        checksums = fspec.checksum.get(_type, 'None') if checksums == "" else checksums + ",%s" % fspec.checksum.get(_type)
        allowlans = str(fspec.allow_lan) if allowlans == "" else allowlans + ",%s" % fspec.allow_lan
        allowwans = str(fspec.allow_wan) if allowwans == "" else allowwans + ",%s" % fspec.allow_wan
        directaccesslans = str(fspec.direct_access_lan) if directaccesslans == "" else directaccesslans + ",%s" % fspec.direct_access_lan
        directaccesswans = str(fspec.direct_access_wan) if directaccesswans == "" else directaccesswans + ",%s" % fspec.direct_access_wan
        istars = str(fspec.is_tar) if istars == "" else istars + ",%s" % fspec.is_tar
        _accessmode = fspec.accessmode if fspec.accessmode else 'None'
        accessmodes = _accessmode if accessmodes == "" else accessmodes + ",%s" % _accessmode
        _storagetoken = fspec.storage_token if fspec.storage_token else 'None'
        storagetokens = _storagetoken if storagetokens == "" else storagetokens + ",%s" % _storagetoken

    return {'lfns': lfns, 'guids': guids, 'scopes': scopes, 'datasets': datasets, 'ddmendpoints': ddmendpoints,
            'filesizes': filesizes, 'checksums': checksums, 'allowlans': allowlans, 'allowwans': allowwans,
            'directaccesslans': directaccesslans, 'directaccesswans': directaccesswans, 'istars': istars,
            'accessmodes': accessmodes, 'storagetokens': storagetokens}


def use_middleware_script(container_type):
    """
    Should the pilot use a script for the stage-in/out?
    Check the container_type (from queuedata) if 'middleware' is set to 'container' or 'bash'.

    :param container_type: container type (string).
    :return: Boolean (True if middleware should be containerised).
    """

    return True if container_type == 'container' or container_type == 'bash' else False
