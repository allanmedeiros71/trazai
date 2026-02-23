from django.db import models
from django.contrib.auth.models import AbstractUser

class FamilyGroup(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    family_group = models.ForeignKey(FamilyGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    def __str__(self):
        return self.username