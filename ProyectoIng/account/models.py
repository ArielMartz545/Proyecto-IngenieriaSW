from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, address, birth_date, password=None):
        if not email:
            raise ValueError("Debes ingresar tu correo para registrarte")
        if not first_name:
            raise ValueError("Debes ingresar tu nombre para registrarte")
        if not last_name:
            raise ValueError("Debes ingresar tu apellido para registrarte")
        if not phone_number:
            raise ValueError("Debes ingresar número de teléfono para registrarte")
        if not address:
            raise ValueError("Debes ingresar tu direccion para registrarte")
        if not birth_date:
            raise ValueError("Debes ingresar tu fecha de nacimiento para registrarte")
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            address = address,
            birth_date = birth_date
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, address, birth_date, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            address = address,
            birth_date = birth_date,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Correo electrónico',
        max_length=100,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Nombre',
        max_length=50,
    )
    last_name = models.CharField(
        verbose_name='Apellido',
        max_length=50,
    )
    phone_number = models.CharField(
        verbose_name='Número de teléfono',
        max_length=20,
    )
    address = models.TextField(
        verbose_name='Dirección'
    )
    birth_date = models.DateField(
        verbose_name='Fecha de nacimiento'
    )
    date_joined = models.DateTimeField(
        verbose_name='Fecha de registro',
        auto_now_add=True
    )
    last_login = models.DateTimeField(
        verbose_name='Último acceso',
        auto_now=True
    )
    is_admin = models.BooleanField(
        default=False
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=False
    )
    is_superuser = models.BooleanField(
        default=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone_number','address','birth_date']

    objects = AccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
