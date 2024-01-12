from pathlib import Path
from typing import Optional, Dict, List

import jwt
from yaml import dump, Dumper

from business_logic.utils import hash_string_value, read_yml_file_content
from business_logic.errors import InvalidCredentialsError, AccountAlreadyExistsError
from business_logic.serializer.misc import Account, AccountInfo, Configuration
from server.errors import MissingAccountForAuthenticationToken

JWT_ALGORITHM = "HS256"
JWT_KEY = "SECRET"


class AuthenticationBusinessLogic:
    def __init__(self, path_to_accounts_yml_file: str):
        self._path_to_accounts_yml_file = path_to_accounts_yml_file

    def unsafe_register_account(self, name: str, email: str, password: str) -> Account:
        account = self._create_account(name, email, password)
        self._unsafe_store_accounts(accounts=[account])
        return account

    def unsafe_login(self, email: str, password: str) -> str:
        account = self.get_account_for_email(email=email)

        if not account:
            raise InvalidCredentialsError()

        password_is_valid = self.validate_password_against_account(
            account=account, password=password
        )

        if not password_is_valid:
            raise InvalidCredentialsError()

        return self.unsafe_create_authentication_token(account)

    def get_account_for_email(self, email: str) -> Optional[Account]:
        for account in self._get_accounts_from_file().values():
            if account.email == email:
                return account
        return None

    def validate_password_against_account(
        self, account: Account, password: str
    ) -> bool:
        return account.hashed_password == self._hash_password(password)

    def get_account_for_jwt(self, authentication_token: str) -> Optional[Account]:
        account_info = AccountInfo(
            **jwt.decode(
                jwt=authentication_token, key=JWT_KEY, algorithms=[JWT_ALGORITHM]
            )
        )
        return self.get_account_for_email(email=account_info.email)

    def unsafe_refresh_authentication_token(self, old_authentication_token: str) -> str:
        account: Optional[Account] = self.get_account_for_jwt(old_authentication_token)
        if not account:
            raise MissingAccountForAuthenticationToken()
        return self.unsafe_create_authentication_token(account)

    def _get_accounts_from_file(self) -> Dict[str, Account]:
        file_path = Path(self._path_to_accounts_yml_file)
        if file_path.is_file():
            file_content = read_yml_file_content(file_path)
            configuration = Configuration(**file_content)
        else:
            configuration = Configuration(**{"accounts": {}})

        return configuration.accounts

    def _create_account(self, name: str, email: str, password: str) -> Account:
        return Account(
            id=hash_string_value(self._create_account_signature(name, email, password)),
            name=name,
            email=email,
            hashed_password=self._hash_password(password),
            permissions={"READ_MINE"},
        )

    def _unsafe_store_accounts(self, accounts: List[Account]) -> None:
        file_path = Path(self._path_to_accounts_yml_file)
        if file_path.is_file():
            file_content = read_yml_file_content(file_path)
            configuration = Configuration(**file_content)
        else:
            configuration = Configuration(**{"accounts": {}})

        for account in accounts:
            if account.id in configuration.accounts:
                raise AccountAlreadyExistsError(account)
            configuration.accounts[account.id] = account

        new_file_content = dump(configuration.model_dump(), Dumper=Dumper)

        with open(file_path, "w") as writer:
            writer.write(new_file_content)

    @staticmethod
    def _hash_password(password: str) -> str:
        return hash_string_value(password)

    @staticmethod
    def _create_account_signature(name: str, email: str, password: str) -> str:
        return f"{name}::{email}::{password}"

    @staticmethod
    def unsafe_create_authentication_token(account: Account) -> str:
        return jwt.encode(
            payload={
                "name": account.name,
                "email": account.email,
                "permissions": list(account.permissions),
            },
            key=JWT_KEY,
            algorithm=JWT_ALGORITHM,
        )
