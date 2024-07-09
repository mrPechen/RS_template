from django.db import models
from django.contrib.auth.models import AbstractUser
from cryptography.fernet import Fernet
from django.conf import settings


f = Fernet(settings.BINARY_CODE)


class Account(AbstractUser):
    class Meta:
        db_table = 'account'
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    class Role(models.TextChoices):
        User = "user", "User"
        Mentor = "mentor", "Mentor"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.User)
    phone = models.CharField(blank=True, null=True)
    email = models.EmailField(blank=True)
    crypto_password = models.BinaryField(blank=True, null=True)

    def set_encrypted_password(self, raw_password):
        encrypted_password = f.encrypt(raw_password.encode())
        self.crypto_password = encrypted_password
        self.save()

    def get_decode_password(self):
        if self.crypto_password:
            decrypted_password = f.decrypt(bytes(self.crypto_password))
            return decrypted_password.decode()
        return None

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
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True, blank=True, related_name='mentored_users')

    def __str__(self):
        return self.account.username
