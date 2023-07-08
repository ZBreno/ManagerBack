from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, ImageField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager


class User(AbstractUser):
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None 
    last_name = None  
    email = EmailField(_("email address"), unique=True, max_length=50)
    profile = ImageField(upload_to='profile/')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_absolute_url(self) -> str:
    
        return reverse("users:detail", kwargs={"pk": self.id})