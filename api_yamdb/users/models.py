import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class User(AbstractUser):
    """Пользователь."""

    role = models.SlugField(
        max_length=20,
        default="user"
    )
    bio = models.TextField(
        max_length=200,
        blank=True,
    )
    confirmation_code = models.UUIDField(
        unique=True,
        default=uuid.uuid4
    )

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff or self.is_superuser

    class Meta(object):
        unique_together = ("email",)


@receiver(pre_save, sender=User)
def staff2admin(sender, **kwargs):
    """Перед созранением, если это staff, то меняем ему роль на admin."""
    user = kwargs.get("instance")
    if user:
        if user.is_staff:
            user.role = "admin"
