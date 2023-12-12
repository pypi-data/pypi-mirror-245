import json
import os
from typing import Dict, Protocol, List, Any
from shutil import copytree

MAX_RETRY = 2


class Validators(Protocol):
    @staticmethod
    def validate(directory: str) -> bool:
        ...


class ABBValidator:
    @staticmethod
    def validate(directory: str) -> bool:
        """Check if ABB Rapid program structure exists in given folder

        Parameters
        ----------
        directory : str
            Directory of ABB Backup

        Returns
        -------
        bool
            True if directory is valid.
        """
        if not os.path.isdir(os.path.join(directory, 'RAPID')):
            print("Unable to find 'RAPID'.")
            return False
        elif not os.path.isdir(os.path.join(directory, 'RAPID\\TASK 1')):
            print("Unable to find 'TASK 1'.")
            return False
        elif not os.path.isdir(os.path.join(directory, 'RAPID\\TASK 2')):
            print("Unable to find 'TASK 2'.")
            return False
        return True


class GITValidator:
    @staticmethod
    def validate(directory: str) -> bool:
        """Check if git structure exists in given folder

        Parameters
        ----------
        directory : str
            Directory of git

        Returns
        -------
        bool
            True if directory is valid.
        """
        if not os.path.isdir(os.path.join(directory, '.git')):
            print("Unable to find 'GIT REPO'.")
            return False
        return True


class DummyValidator:
    @staticmethod
    def validate(directory: str) -> bool:
        """Dummy placeholder.

        Returns
        -------
        bool
            Always returns True
        """
        return True


class UserResponse:
    @staticmethod
    def get_user_confirmation(msg: str) -> bool:
        """Get user confirmation for proceeding.

        Parameters
        ----------
        msg : str
            Message to display to the user.

        Returns
        -------
        bool
            Wether user confirms or not.
        """
        return input(f'{msg} y/[n]: ').upper() in ['Y', 'YES']

    @staticmethod
    def get_user_input(msg: str) -> str | None:
        global MAX_RETRY
        retry = 0

        while retry <= MAX_RETRY:
            retry += 1
            resp = input(msg).strip()
            if len(resp) >= 3:
                return resp
            print('Please type a word of min 3 characters.')
        print('Exceeded max retries.')
        quit()


class CreateConfig:
    __slots__ = [
        '_work_dir',
        '_config_file',
        '_config_fle_name',
        '_config_fle_path',
    ]

    def __init__(self) -> None:
        self._work_dir = os.path.dirname(os.path.realpath(__file__))

        self._config_file: Dict[str, Any] = {}
        self._config_fle_name = 'config.json'
        self._config_fle_path = os.path.join(
            self._work_dir,
            self._config_fle_name
        )

    @property
    def check_config(self) -> bool:
        """Check if configuration file exists.

        Returns
        -------
        bool
            True if file exists, else False.
        """
        return os.path.exists(self._config_fle_path)

    @staticmethod
    def __check_dir(msg: str, validator: Validators) -> str | None:
        """Check if directory exists

        Parameters
        ----------
        msg : str
            _description_
        validator : Validators
            _description_

        Returns
        -------
        str | None
            _description_
        """
        global MAX_RETRY
        retry = 0

        while retry <= MAX_RETRY:
            retry += 1

            _dir = os.path.normpath(input(msg).replace('"', ''))
            if os.path.isdir(_dir) and validator.validate((_dir)):
                return _dir
            print('Please check your directory.')
        print('Max retry exceeded. Please check your directory.')
        return None

    def __write_config(self) -> None:
        """Write configuration file."""
        print('Creating configuration file.')
        with open(self._config_fle_path, 'w') as config_file:
            json.dump(self._config_file, config_file)

    def __get_directories(self) -> None:
        """Get directories for transferring backup."""

        _msg = "Enter 'ABB Backup' directory: "
        if (_dir := self.__check_dir(_msg, ABBValidator)):
            self._config_file['abb_backup_dir'] = _dir

        _msg = "Enter 'GIT' root directory: "
        if (_dir := self.__check_dir(_msg, GITValidator)):
            self._config_file['git_root_dir'] = _dir

        _msg = "Enter directory for copying backup: "
        if (_dir := self.__check_dir(_msg, DummyValidator)):
            self._config_file['git_rapid_dir'] = _dir

    def __get_dir_names(self, dirs: List[str]) -> None:
        for _dir in dirs:
            self._config_file['dir_names'][_dir] = UserResponse.get_user_input(
                f'Change name of {_dir} to : ')

    def __get_abb_dirs(self) -> None:
        abb_dir = self._config_file['abb_backup_dir']
        if not os.path.isdir(abb_dir):
            raise FileNotFoundError

        task_list = os.listdir(os.path.join(abb_dir, 'RAPID'))

        if not self._config_file.get('dir_names'):
            self._config_file['dir_names'] = {}

        print('Default task name: Right_arm, Left_arm')

        msg = 'Do you wish to provide custom name for the ' +\
            'tasks, if "no", name will be assigned automatically?'

        if UserResponse.get_user_confirmation(msg):
            self.__get_dir_names(dirs=task_list)
        else:
            default_task = ['TASK 1', 'TASK 2']
            if (new_task := list(set(task_list) - set(default_task))):
                self.__get_dir_names(dirs=new_task)
            self._config_file['dir_names']['TASK 1'] = 'Right_arm'
            self._config_file['dir_names']['TASK 2'] = 'Left_arm'

    def generate_config(self) -> None:
        self.__get_directories()
        self.__get_abb_dirs()
        self.__write_config()


class TransferBackup:
    __slots__ = [
        '_work_dir',
        '_config_file',
        '_config_fle_name',
        '_config_fle_path',
    ]

    def __init__(self) -> None:
        self._work_dir = os.path.dirname(os.path.realpath(__file__))

        self._config_file: Dict[str, Any] = {}
        self._config_fle_name = 'config.json'
        self._config_fle_path = os.path.join(
            self._work_dir,
            self._config_fle_name
        )

    def __read_config(self) -> None:
        """Read configuration file."""
        try:
            with open(self._config_fle_path, 'r') as config_file:
                self._config_file = json.load(config_file)
        except FileNotFoundError:
            print('Unable to find configuration file. ')
            quit()

    def __copy_folders(self) -> None:
        abb_backup_dir = self._config_file['abb_backup_dir']
        git_rapid_dir = self._config_file['git_rapid_dir']

        for source, destination in self._config_file['dir_names'].items():
            copytree(
                src=f'{abb_backup_dir}\\RAPID\\{source}',
                dst=f'{git_rapid_dir}\\{destination}',
                dirs_exist_ok=True
            )

    def transfer_backup(self) -> None:
        self.__read_config()
        self.__copy_folders()


def main():
    config = CreateConfig()
    transfer = TransferBackup()

    if not config.check_config:
        print('Configuration file is missing.')
        msg = 'Do you wish to proceed with config creation?'
        if UserResponse.get_user_confirmation(msg):
            config.generate_config()
        else:
            print('Cannot work without configuration file.')
            quit()
    else:
        transfer.transfer_backup()


main()
