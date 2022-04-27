import string
from datetime import date
from random import randint

from mimesis import Field, Schema
from mimesis.locales import Locale
from yaoya.models.user import User, UserRole
from yaoya.repositories.base import MemoryStore


class UserMemoryStore(MemoryStore):
    def get_by_id(self, user_id: str) -> User:
        df = self._df
        user = df[df["user_id"] == user_id].to_dict("records")[0]
        return User(
            user_id=user["user_id"],
            name=user["name"],
            birthday=user["birthday"],
            email=user["email"],
            role=user["role"],
        )

    def insert(self, user_id: str, name: str, birthday: date, email: str, role: UserRole) -> None:
        row = dict(
            user_id=user_id,
            name=name,
            birthday=birthday,
            email=email,
            role=role,
        )
        super().insert(row)


def user_mock_insert(user_store: UserMemoryStore, n: int, role: UserRole) -> None:
    _ = Field(locale=Locale.JA)
    schema = Schema(
        schema=lambda: {
            "user_id": _("random.generate_string", str_seq=string.ascii_lowercase, length=randint(5, 10)),
            "name": _("full_name", reverse=True),
            "birthday": _("date", start=1950, end=2010),
            "email": _("email", domains=["sample.com"]),
        }
    )
    for user in schema.create(n):
        user_store.insert(user["user_id"], user["name"], user["birthday"], user["email"], role)
