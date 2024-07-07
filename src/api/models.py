from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    class Meta:
        db_table = 'account'
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    class Role(models.TextChoices):
        User = "user", "User"
        Agency = "mentor", "Mentor"

    role = models.CharField(max_length=50, choices=Role.choices)
    phone = models.CharField(blank=True, null=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.username


class Mentor(models.Model):
    class Meta:
        db_table = 'mentor'
        verbose_name = "Mentor"
        verbose_name_plural = "Mentors"

    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='mentor')

    def __str__(self):
        return self.account.username


class User(models.Model):
    class Meta:
        db_table = 'user'
        verbose_name = "User"
        verbose_name_plural = "Users"

    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='user')
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True, blank=True, related_name='mentored_user')

    def __str__(self):
        return self.account.username
