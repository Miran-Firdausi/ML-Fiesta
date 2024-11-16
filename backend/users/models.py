from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# Custom manager for the CustomUser model
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

        # Superusers have no username field requirement, we use email as the identifier
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.TextField(max_length=255)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
