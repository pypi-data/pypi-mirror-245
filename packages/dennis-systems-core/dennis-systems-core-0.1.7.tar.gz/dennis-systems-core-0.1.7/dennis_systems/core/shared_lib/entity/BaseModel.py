from django.db.models import Model


class BaseModel(Model):
    class Meta:
        abstract = True  # specify this model as an Abstract Model
        app_label = 'base_model'
