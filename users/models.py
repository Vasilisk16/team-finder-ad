import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from .avatar import generate_avatar


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        if not extra_fields.get("phone"):
            extra_fields["phone"] = f"+7900{uuid.uuid4().hex[:7]}"
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("name", "Admin")
        extra_fields.setdefault("surname", "User")
        if not extra_fields.get("phone"):
            extra_fields["phone"] = f"+7900{uuid.uuid4().hex[:7]}"
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to="avatars/")
    phone = models.CharField(max_length=12, unique=True)
    github_url = models.URLField(blank=True)
    about = models.CharField(max_length=256, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new and not self.avatar:
            self.avatar = generate_avatar(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
