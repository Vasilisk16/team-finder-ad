from django.contrib.auth.models import AbstractUser
from django.db import models

from .avatar import generate_avatar
from .managers import UserManager

USER_NAME_MAX_LENGTH = 124
USER_SURNAME_MAX_LENGTH = 124
USER_PHONE_MAX_LENGTH = 12
USER_ABOUT_MAX_LENGTH = 256


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=USER_NAME_MAX_LENGTH)
    surname = models.CharField(max_length=USER_SURNAME_MAX_LENGTH)
    avatar = models.ImageField(upload_to="avatars/")
    phone = models.CharField(max_length=USER_PHONE_MAX_LENGTH, unique=True)
    github_url = models.URLField(blank=True)
    about = models.CharField(max_length=USER_ABOUT_MAX_LENGTH, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    objects = UserManager()

    class Meta:
        ordering = ["-date_joined"]

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new and not self.avatar:
            self.avatar = generate_avatar(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
