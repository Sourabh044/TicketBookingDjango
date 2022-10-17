from django.contrib.auth.base_user import BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            mobile = mobile,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, mobile=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            mobile=mobile,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
