import logging
import os
from contextlib import suppress
from pathlib import Path

from common_helper_process import execute_shell_command_get_return_code

from helperFunctions.config import load_config
from helperFunctions.install import apt_remove_packages, apt_install_packages, apt_upgrade_system, apt_update_sources, \
    apt_autoremove_packages, apt_clean_system, InstallationError, pip3_install_packages


def install_pip(python_command):
    logging.info('Installing {} pip'.format(python_command))
    for command in ['wget https://bootstrap.pypa.io/get-pip.py', 'sudo -EH {} get-pip.py'.format(python_command), 'rm get-pip.py']:
        output, return_code = execute_shell_command_get_return_code(command)
        if return_code != 0:
            raise InstallationError('Error in pip installation for {}:\n{}'.format(python_command, output))


def main(distribution):
    xenial = distribution == 'xenial'

    apt_install_packages('apt-transport-https')

    logging.info('Updating system')
    apt_update_sources()
    apt_upgrade_system()
    apt_autoremove_packages()
    apt_clean_system()

    # update submodules
    git_output, git_code = execute_shell_command_get_return_code('(cd ../../ && git submodule foreach "git pull")')
    if git_code != 0:
        raise InstallationError('Failed to update submodules\n{}'.format(git_output))

    # make bin dir
    with suppress(FileExistsError):
        os.mkdir('../bin')

    # install python3 and general build stuff
    apt_install_packages('python3', 'python3-dev', 'build-essential', 'automake', 'autoconf', 'libtool', 'git', 'unzip')
    if not xenial:
        pip3_install_packages('testresources')

    # get a bugfree recent pip version
    apt_remove_packages('python3-pip', 'python3-setuptools', 'python3-wheel')
    apt_autoremove_packages()
    install_pip('python3')

    # install python2
    apt_install_packages('python', 'python-dev')
    apt_remove_packages('python-pip')
    apt_autoremove_packages()
    install_pip('python2')

    # install general python dependencys
    apt_install_packages('libffi-dev', 'libfuzzy-dev')
    pip3_install_packages('pytest==3.5.1', 'pytest-cov', 'pytest-pep8', 'pylint', 'python-magic', 'xmltodict', 'yara-python==3.7.0', 'appdirs')

    config = load_config('main.cfg')
    data_folder = config.get('unpack', 'data_folder')
    os.makedirs(str(Path(data_folder, 'files')), exist_ok=True)
    os.makedirs(str(Path(data_folder, 'reports')), exist_ok=True)

    return 0
