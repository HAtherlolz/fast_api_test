from tortoise import fields, ConfigurationError
from tortoise.models import Model

from .services import delete_file_to_s3, settings


class User(Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(25, blank=True, null=True)
    last_name = fields.CharField(25, blank=True, null=True)
    email = fields.CharField(50, unique=True)
    password = fields.CharField(100)
    avatar = fields.CharField(1000, blank=True, null=True)
    date_created = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=False)

    class PydanticMeta:
        exclude = ('password', 'track', 'is_active', 'album')

    async def delete(self):
        if self.avatar != settings.AWS_BUCKET_DEFAULT_AVATAR_PATH:
            await delete_file_to_s3(self.avatar)
        super.delete()

    def __str__(self):
        return self.email
