from django.db import models
from django.core.validators import FileExtensionValidator


class Test(models.Model):
    file = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        verbose_name='採点ファイル',
        validators=[FileExtensionValidator(['pdf', ])],
    )


# Create your models here.
