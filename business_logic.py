import hashlib
import json
from pathlib import Path
from typing import List, Dict, Optional

from yaml import dump, Dumper, load, Loader

from errors import AccountAlreadyExists
from marshalls import Account, Configuration, _Developer, DevelopersDataFile, Task, TaskDataFile
from models import AccountRequest


class BusinessLogic:

    def __init__(self,
                 path_to_accounts_yml_file: str,
                 path_to_developers_json_file: str,
                 path_to_tasks_json_file: str,
                 ):
        self._path_to_accounts_yml_file = path_to_accounts_yml_file
        self._path_to_developers_json_file = path_to_developers_json_file
        self._path_to_tasks_json_file = path_to_tasks_json_file

    def unsafe_register_account(self, request: AccountRequest) -> Account:
        account = self._create_account(account_request=request)
        self._unsafe_store_accounts(accounts=[account])
        return account

    def _unsafe_store_accounts(self, accounts: List[Account]) -> None:
        file_path = Path(self._path_to_accounts_yml_file)
        if file_path.is_file():
            file_content = self._read_yml_file_content(file_path)
            configuration = Configuration(**file_content)
        else:
            configuration = Configuration(**{
                "accounts": {}
            })

        for account in accounts:
            if account.id in configuration.accounts:
                raise AccountAlreadyExists(account)
            configuration.accounts[account.id] = account

        new_file_content = dump(configuration.model_dump(), Dumper=Dumper)

        with open(file_path, "w") as writer:
            writer.write(new_file_content)

    def unsafe_read_developer_data(self) -> List[_Developer]:
        file_path = Path(self._path_to_developers_json_file)
        file_content = self._read_json_file_content(file_path)

        return DevelopersDataFile(**file_content).developers

    def unsafe_read_task_data(self) -> List[Task]:
        file_path = Path(self._path_to_tasks_json_file)
        file_content = self._read_json_file_content(file_path)

        return TaskDataFile(**file_content).tasks

    def _create_account(self, account_request: AccountRequest) -> Account:
        return Account(
            id=self._hash(self._create_account_signature(account_request)),
            name=account_request.name,
            email=account_request.email,
            hashed_password=self._hash_password(account_request.password),
            permissions={"READ_MINE"}
        )

    def get_account_for_email(self, email: str) -> Optional[Account]:
        for account in self._get_accounts_from_file().values():
            if account.email == email:
                return account
        return None

    def validate_password_against_account(self, account: Account, password: str) -> bool:
        return account.hashed_password == self._hash_password(password)

    def _get_accounts_from_file(self) -> Dict[str, Account]:
        file_path = Path(self._path_to_accounts_yml_file)
        if file_path.is_file():
            file_content = self._read_yml_file_content(file_path)
            configuration = Configuration(**file_content)
        else:
            configuration = Configuration(**{
                "accounts": {}
            })

        return configuration.accounts

    def _hash_password(self, password: str) -> str:
        return self._hash(password)

    @staticmethod
    def _read_json_file_content(value: Path) -> dict:
        with open(value, "r") as reader:
            return json.loads(reader.read())

    @staticmethod
    def _read_yml_file_content(value: Path) -> dict:
        with open(value, "r") as reader:
            return load(reader.read(), Loader=Loader)

    @staticmethod
    def _create_account_signature(account_request: AccountRequest) -> str:
        return f"{account_request.name}::{account_request.email}::{account_request.password}"

    @staticmethod
    def _hash(value: str) -> str:
        return str(hashlib.md5(value.encode("utf-8")).hexdigest())
