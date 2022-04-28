import string
from datetime import date
from random import randint
from typing import List

from mimesis import Field, Schema
from mimesis.locales import Locale
from yaoya.models.user import User, UserRole
from yaoya.repositories.base import NotFoundError


class UserMemoryRepository:
    def __init__(self) -> None:
        self.users: List[User] = []

    def get_all(self) -> List[User]:
        return self.users

    def get_by_id(self, user_id: str) -> User:
        users = [user for user in self.users if user.user_id == user_id]
        if len(users) == 0:
            raise NotFoundError(user_id)

        return users[0]

    def insert(self, user: User) -> None:
        self.users.append(user)


def get_dummy_users(n: int, role: UserRole) -> List[User]:
    _ = Field(locale=Locale.JA)
    schema = Schema(
        schema=lambda: {
            "user_id": _("random.generate_string", str_seq=string.ascii_lowercase, length=randint(5, 10)),
            "name": _("full_name", reverse=True),
            "birthday": _("date", start=1950, end=2010),
            "email": _("email", domains=["sample.com"]),
        }
    )
    users = [
        User(
            user_id=data["user_id"],
            name=data["name"],
            birthday=data["birthday"],
            email=data["email"],
            role=role,
        )
        for data in schema.create(n)
    ]
    return users


def dummy_users_insert(user_repository: UserMemoryRepository, n: int, role: UserRole) -> None:
    for user in get_dummy_users(n, role):
        user_repository.insert(user)


def dummy_guest_insert(user_repository: UserMemoryRepository) -> User:
    user = User(user_id="guest", name="ゲストユーザ", birthday=date(2000, 1, 1), email="guest@sample.com", role="guest")
    user_repository.insert(user)
    return user


def dummy_owner_insert(user_repository: UserMemoryRepository) -> User:
    user = User(user_id="owner", name="オーナーユーザ", birthday=date(2000, 1, 1), email="owner@sample.com", role="owner")
    user_repository.insert(user)
    return user


def dummy_admin_insert(user_repository: UserMemoryRepository) -> User:
    user = User(user_id="admin", name="管理者ユーザ", birthday=date(2000, 1, 1), email="admin@sample.com", role="admin")
    user_repository.insert(user)
    return user
