from tortoise.models import Model
from tortoise import fields


class ProfileUser(Model):
    id = fields.TextField(pk=True)
    name = fields.TextField(default="새 유저")
    bio = fields.TextField(null=True, default="새로운 유저를 환영해주세요!")
    profile_url = fields.TextField(null=True, default="")
    banner_url = fields.TextField(null=True, default="")


class AnonymousUser(Model):
    id = fields.TextField(pk=True)
    name = fields.TextField()
    profile_url = fields.TextField(null=True, default="")


class LoginUser(Model):
    email = fields.TextField(pk=True)
    user_id = fields.TextField()
