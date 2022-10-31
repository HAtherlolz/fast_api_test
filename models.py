import io
import os
import uuid
from typing import IO

from tortoise import fields, ConfigurationError
from tortoise.models import Model


# TEXTCHARS = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
#
#
# def is_binary_file(file_path: str):
#     with open(file_path, 'rb') as f:
#         content = f.read(1024)
#         return bool(content.translate(None, TEXTCHARS))
#
#
# class FileField(fields.TextField):
#     def __init__(self, *, upload_root: str, **kwargs):
#         super().__init__(**kwargs)
#         self.upload_root = upload_root
#         if not os.path.exists(self.upload_root):
#
#             raise ConfigurationError('No such directory: {}'.format(self.upload_root))
#
#     def _is_binary(self, file: IO):
#         return not isinstance(file, io.TextIOBase)
#
#     def to_db_value(self, value: IO, instance):
#         is_binary = self._is_binary(value)
#         if hasattr(value, 'name'):
#             name = value.name
#         else:
#             name = str(uuid.uuid4())
#
#         if os.path.isfile(os.path.join(self.upload_root, name)):
#             name = '{}-{}'.format(str(uuid.uuid4()), name)
#
#         mode = 'w' if not is_binary else 'wb'
#
#         path = os.path.join(self.upload_root, name)
#
#         with open(path, mode) as f:
#             f.write(value.read())
#
#         return path
#
#     def to_python_value(self, value: str):
#         if is_binary_file(value):
#             mode = 'rb'
#             buffer = io.BytesIO()
#         else:
#             mode = 'r'
#             buffer = io.StringIO()
#
#         buffer.name = os.path.split(value)[-1]
#
#         with open(value, mode) as f:
#             buffer.write(f.read())
#
#         buffer.seek(0)
#         return buffer


class City(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50, unique=True)
    file = fields.CharField(2000, blank=True, null=True)
    timezone = fields.DateField()


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50)
    email = fields.CharField(50, unique=True)
    password = fields.CharField(50)
    date_created = fields.DateField(add_auto_now=True)
    date_updated = fields.DateField(auto_now=True)
    city = fields.ForeignKeyField('models.City', related_name='user', null=True)


