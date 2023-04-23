from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class WalletUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_premium_user = models.BooleanField(
        default=False,
        verbose_name="premium user",
        help_text="Select the checkbox to enjoy premium features.!",
    )
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="auth_users_groups",  # unique related_name
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="auth_users_permissions",  # unique related_name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    def __str__(self):
        return self.get_full_name()
