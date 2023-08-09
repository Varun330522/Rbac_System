from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.


class Role(models.Model):
    role_name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.role_name


class Action(models.Model):
    action_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.action_name


class RoleActionMapping(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.role} - {self.action}"


class Users(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    tokens = models.JSONField(blank=True, null=True)

    def generate_token(self):
        refresh = RefreshToken.for_user(self)
        self.tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        self.save()

    def __str__(self):
        return self.username


class API(models.Model):
    api_name = models.CharField(max_length=100, unique=True)
    endpoints = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    methods = models.CharField(max_length=100)

    def __str__(self):
        return self.api_name


class ApiUserMapping(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    api = models.ForeignKey(API, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}-{self.api}"
