from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class Battalion(models.TextChoices):
    ALON = "Alon", "Alon"
    GEFEN = "Gefen", "Gefen"
    NAHSHON = "Nahshon", "Nahshon"
    BROSH = "Brosh", "Brosh"
    EREZ = "Erez", "Erez"
    HADAS = "Hadas", "Hadas"
    DOLEV = "Dolev", "Dolev"


class Rank(models.TextChoices):
    TSOER = "Tso'er", "Tso'er"
    SAGAM = "Sagam", "Sagam"
    SEGEN = "Segen", "Segen"
    SEREN = "Seren", "Seren"
    RAV_SEREN = "Rav-Seren", "Rav-Seren"
    SAAL = "Sa'al", "Sa'al"
    ALAM = "Alam", "Alam"



class UserRole(models.TextChoices):
    BATTALION_COMMANDER = "BC", "Battalion Commander"
    PLATOON_COMMANDER = "PC", "Platoon Commander"
    TEAM_COMMANDER = "TC", "Team Commander"
    CADET = "CAD", "Cadet"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("must_change_password", False)
        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    rank = models.CharField(max_length=20, choices=Rank.choices, default=Rank.TSOER)

    course_num = models.PositiveIntegerField()
    role = models.CharField(max_length=8, choices=UserRole.choices)

    battalion = models.CharField(max_length=20, choices=Battalion.choices)
    platoon = models.PositiveIntegerField(null=True, blank=True)
    team = models.PositiveIntegerField(null=True, blank=True)

    must_change_password = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "rank", "course_num", "role", "battalion"]

    def __str__(self):
        return f"{self.full_name} <{self.email}>"
