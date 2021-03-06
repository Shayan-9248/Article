from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Permission, _user_get_permissions
from django.db.models.signals import post_save
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=77)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    special_user = models.DateTimeField(default=timezone.now)
    permission = models.ManyToManyField(Permission, related_name='users')


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_user_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'user')

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'all')

    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        return False
    is_special_user.boolean = True
    is_special_user.short_description = 'Special User'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.user.username


def user_profile_save(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile(user=kwargs['instance'])
        user_profile.save()

post_save.connect(user_profile_save, sender=User)