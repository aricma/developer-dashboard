import hashlib
import json
from pathlib import Path
from typing import List, Dict, Optional

import jwt
from yaml import dump, Dumper, load, Loader

from business_logic.errors import AccountAlreadyExists, InvalidCredentials
from business_logic.marshalls import Account, Configuration, _Developer, DevelopersDataFile, Task, TaskDataFile, \
    AccountInfo

JWT_ALGORITHM = "HS256"
JWT_KEY = "SECRET"


class BusinessLogic:

    def __init__(self,
                 path_to_accounts_yml_file: str,
                 path_to_developers_json_file: str,
                 path_to_tasks_json_file: str,
                 ):
        self._path_to_accounts_yml_file = path_to_accounts_yml_file
        self._path_to_developers_json_file = path_to_developers_json_file
        self._path_to_tasks_json_file = path_to_tasks_json_file

    def get_account_for_jwt(self, authentication_token: str) -> Account:
        account_info = AccountInfo(
            **jwt.decode(
                jwt=authentication_token,
                key=JWT_KEY,
                algorithms=[JWT_ALGORITHM]
            )
        )
        return self.get_account_for_email(email=account_info.email)

    def unsafe_register_account(self, name: str, email: str, password: str) -> Account:
        account = self._create_account(name, email, password)
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

    def _create_account(self, name: str, email: str, password: str) -> Account:
        return Account(
            id=self._hash(self._create_account_signature(name, email, password)),
            name=name,
            email=email,
            hashed_password=self._hash_password(password),
            permissions={"READ_MINE"}
        )

    def unsafe_login(self, email: str, password: str) -> str:
        account = self.get_account_for_email(email=email)

        if not account:
            raise InvalidCredentials()

        password_is_valid = self.validate_password_against_account(
            account=account,
            password=password
        )

        if not password_is_valid:
            raise InvalidCredentials()

        return jwt.encode(
            payload={
                "name": account.name,
                "email": account.email,
                "permissions": list(account.permissions)
            },
            key=JWT_KEY,
            algorithm=JWT_ALGORITHM
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
    def _create_account_signature(name: str, email: str, password: str) -> str:
        return f"{name}::{email}::{password}"

    @staticmethod
    def _hash(value: str) -> str:
        return str(hashlib.md5(value.encode("utf-8")).hexdigest())
