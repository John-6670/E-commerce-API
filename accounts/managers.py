from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, **user_data):
        email = user_data.get('email')
        phone_number = user_data.get('phone_number')

        if not email and not phone_number:
            raise ValueError('Email or Phone Number must be set')

        email = self.normalize_email(email)
        user = self.model(**user_data)
        user.set_password(user_data.get('password'))
        user.save(using=self._db)
        return user

    def create_superuser(self, **user_data):
        user = self.create_user(**user_data)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
