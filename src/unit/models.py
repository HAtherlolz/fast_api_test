from tortoise import fields, ConfigurationError
from tortoise.models import Model

from src.user.models import User


class Unit(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False, blank=False, default='Name', db_index=True)
    slug = fields.CharField(max_length=255, null=True, unique=True, db_index=True)
    model_name = fields.CharField(max_length=255, null=True, blank=True, db_index=True)
    manufacturer = fields.ForeignKeyField('models.Manufacturer', on_delete=fields.SET_NULL, null=True, blank=True)
    description = fields.TextField(null=True, blank=True)
    features = fields.TextField(null=True, blank=True)
    services = fields.ManyToManyField('models.Service', related_name="unit_services", blank=True, db_index=True)
    owner = fields.ForeignKeyField(
        'models.User', on_delete=fields.CASCADE, related_name='units', null=True, blank=True, db_index=True
    )

    rating = fields.FloatField(default=0, null=True, blank=True, db_index=True)
    views_count = fields.SmallIntField(default=0)
    type_of_work = fields.CharField(max_length=256, db_index=True, default='HOUR')
    time_of_work = fields.CharField(max_length=256, null=True, blank=True, db_index=True)
    phone = fields.CharField(max_length=17, blank=True, null=True)

    minimal_price = fields.FloatField(null=True, blank=True, db_index=True)
    money_value = fields.CharField(max_length=256, default='UAH', blank=True, db_index=True)

    minimal_price_UAH = fields.FloatField(null=True, blank=True, db_index=True)
    minimal_price_USD = fields.FloatField(null=True, blank=True, db_index=True)
    minimal_price_EUR = fields.FloatField(null=True, blank=True, db_index=True)

    payment_method = fields.CharField(max_length=30, default='UAH', blank=True)

    user_type = fields.CharField(max_length=256, default='PRIVATE', db_index=True)

    lat = fields.FloatField(null=True, blank=True, db_index=True)
    lng = fields.FloatField(null=True, blank=True, db_index=True)

    category = fields.ForeignKeyField('models.Category', on_delete=fields.SET_NULL, null=True, blank=True, db_index=True)

    working_start_time = fields.TimeField(null=True, blank=True, db_index=True)
    working_end_time = fields.TimeField(null=True, blank=True, db_index=True)

    count = fields.SmallIntField(default=1, blank=True)

    date_created = fields.DatetimeField(auto_now_add=True, null=True, db_index=True)
    date_updated = fields.DatetimeField(auto_now=True, null=True, db_index=True)
    date_restored = fields.DatetimeField(auto_now_add=True, null=True, db_index=True)

    is_approved = fields.BooleanField(default=None, blank=True, null=True, db_index=True)
    is_archived = fields.BooleanField(default=False, blank=True, db_index=True)

    declined_incomplete = fields.BooleanField(default=False, blank=True, db_index=True)
    declined_censored = fields.BooleanField(default=False, blank=True, db_index=True)
    declined_incorrect_price = fields.BooleanField(default=False, blank=True, db_index=True)
    declined_incorrect_data = fields.BooleanField(default=False, blank=True, db_index=True)
    declined_invalid_img = fields.BooleanField(default=False, blank=True, db_index=True)

    first_name = fields.CharField(max_length=255, null=True, blank=True)
    last_name = fields.CharField(max_length=255, null=True, blank=True)
    middle_name = fields.CharField(max_length=255, null=True, blank=True)
    country = fields.CharField(max_length=255, null=True, blank=True)
    city = fields.CharField(max_length=255, null=True, blank=True)
    street = fields.CharField(max_length=255, null=True, blank=True)
    house = fields.CharField(max_length=15, null=True, blank=True)
    postcode = fields.SmallIntField(null=True, blank=True)
    region = fields.CharField(max_length=255, null=True, blank=True)

    class Meta:
        table = 'main_app_unit'

    def __str__(self):
        return f'{self.id} - {self.owner} - {self.name}'


class ServiceCategory(Model):
    """ Service's categories model """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False, blank=False, default='Other', unique=True, db_index=True)

    class Meta:
        table = 'main_app_servicecategory'

    def __str__(self):
        return f'{self.name}'


class Service(Model):
    """ Model for units' Services table """
    id = fields.IntField(pk=True)
    name = fields.CharField(
        max_length=128, null=False, blank=False, default='Service name', unique=True, db_index=True)
    category = fields.ManyToManyField(
        'models.ServiceCategory', related_name='service_category', db_index=True
    )

    class Meta:
        table = 'main_app_service'

    def __str__(self):
        # categories = [category.name for category in self.category.all()]
        return f'{self.id} {self.name}'


class Category(Model):
    """ Units' categories model """
    id = fields.IntField(pk=True)
    name = fields.CharField(
        max_length=255, null=False, blank=False, default='Category name', unique=True, db_index=True)
    parent = fields.ForeignKeyField('models.Category', on_delete=fields.SET_NULL, null=True, blank=True, db_index=True)
    level = fields.SmallIntField(default=1, null=False, db_index=True)

    class Meta:
        table = 'main_app_category'

    def __str__(self):
        if self.parent and self.parent.parent:
            return f'{self.id}  ...{self.name}'
        if self.parent:
            return f'{self.id}  {self.parent} / {self.name}'
        return f'{self.id} {self.name}'


class Manufacturer(Model):
    """ Manufacturers catalog """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64, db_index=True, unique=True)
    is_custom = fields.BooleanField(default=False)

    def __str__(self):
        return self.name
