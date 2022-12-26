# from tortoise.signals import pre_save
#
# from .models import User, settings
#
#
# @pre_save(User)
# async def set_default_avatar(sender: type[User], instance: User, created: bool) -> None:
#     """ Set a default avatar to user when created """
#     if created:
#         instance.avatar = settings.AWS_BUCKET_DEFAULT_AVATAR_PATH
#         await instance.save()
