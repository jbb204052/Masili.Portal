import os
from django.contrib.auth.models import User
from django.db import models
from apps.authentication.helper import OverwriteStorage

###################### DB MODELS ######################

def photo_path(path):
    def _func(instance, filename):
        return os.path.join(path, str(instance.id) + '.png')
    # return _func


class Profile(models.Model):
    types = (
        ['RESIDENT', 'RESIDENT'],
        ['ADMIN', 'ADMIN'],
        ['SUPERADMIN', 'SUPERADMIN'],
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_resident = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    photo = models.ImageField(upload_to=photo_path('profile_pics'), blank=True, default='profile_pics/default.jpg', storage=OverwriteStorage())

    def __str__(self):
        return self.user.email

    def delete(self, *args, **kwargs):
        self.photo.delete()
        super().delete(*args, **kwargs)


