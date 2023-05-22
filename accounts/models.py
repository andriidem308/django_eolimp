from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None):
        if not email:
            raise ValueError('User must have an email address!')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.set_first_name(first_name)
        user.set_last_name(last_name)

        user.save(using=self._db)

        return user

    def create_teacher_user(self, email, username, password, first_name, last_name):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.staff = True
        user._teacher = True

        user.save(using=self._db)
        return user

    def create_student_user(self, email, password, first_name, last_name):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.staff = True
        user._student = True

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(
            email,
            password=password
        )

        user.staff = True
        user.admin = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='username',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='first name',
        max_length=255,
        null=True
    )
    last_name = models.CharField(
        verbose_name='last name',
        max_length=255,
        null=True
    )

    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    _teacher = models.BooleanField(default=False)
    _student = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_email(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_teacher(self):
        return self._teacher

    @property
    def is_student(self):
        return self._student

    objects = UserManager()
