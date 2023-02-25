from tortoise import fields
from tortoise.models import Model

from src.user.models import User
from src.track.models import Track

from .services import delete_file_to_s3


class PlayList(Model):
    """ Model for playlists """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, index=True)
    description = fields.CharField(max_length=1000)
    poster = fields.CharField(max_length=2000)
    is_hidden = fields.BooleanField(default=False)
    owner: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        'models.User', related_name='play_list', on_delete=fields.CASCADE
    )
    track: fields.ManyToManyRelation['Track'] = fields.ManyToManyField(
        'models.Track', through='playlist_track', null=True, related_name='playlists'
    )

    async def delete(self):
        await delete_file_to_s3(self.poster)
        super.delete()

    def __str__(self):
        return self.name