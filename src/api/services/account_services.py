from django.db import transaction

from api.models import Account, User, Mentor


class AccountService:

    @classmethod
    @transaction.atomic
    def update(cls, instance, validated_data):
        password = validated_data.pop('password', None)
        new_mentored_users = validated_data.pop('mentored_users', None)
        new_role = validated_data.pop('role', None)
        role = Account.Role

        if new_role and new_role != instance.role:
            if instance.role == role.Mentor:
                if instance.mentor:
                    instance.mentor.delete()
                User.objects.create(account=instance)
            elif instance.role == role.User:
                if instance.user:
                    instance.user.delete()
                Mentor.objects.create(account=instance)
            instance.role = new_role

        if password:
            instance.set_password(password)
            instance.set_encrypted_password(password)

        if new_mentored_users and instance.role == role.Mentor:
            instance.mentor.mentored_users.clear()
            new_mentored_users = User.objects.filter(mentor=None, account__id__in=new_mentored_users)
            instance.mentor.mentored_users.set(new_mentored_users)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
