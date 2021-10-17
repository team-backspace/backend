from tortoise import fields
from tortoise.models import Model
from dataclasses import dataclass
from typing import List
from ast import literal_eval


@dataclass
class Reaction:
    id: str
    emoji: str
    count: int
    react_users: List[int]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "emoji": self.emoji,
            "count": self.count,
            "react_users": self.react_users,
        }


class ReactionsField(fields.TextField):
    def to_db_value(self, value: List[Reaction], _) -> str:
        return str([reaction.to_dict() for reaction in value])

    def to_python_value(self, value: str) -> List[Reaction]:
        dict_value = literal_eval(value)
        return [
            Reaction(
                id=data["id"],
                emoji=data["emoji"],
                count=data["count"],
                react_users=data["react_users"],
            )
            for data in dict_value
        ]


class Project(Model):
    id = fields.TextField(pk=True)
    name = fields.TextField(default="새 작품")
    description = fields.TextField(null=True, default="방금 생성된 빈 작품")
    author = fields.OneToOneField("model.ProfileUser")
    project_type = fields.TextField(default="blank")
    source_url = fields.TextField(default="")
    timestamp = fields.DatetimeField()
    reactions = ReactionsField(default=[])
