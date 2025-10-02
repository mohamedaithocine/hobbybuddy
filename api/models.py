from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.utils import timezone

class CustomUserManager(UserManager):
    def _create_user(self, email, username, first_name, last_name, date_of_birth, password, **extra_fields):
        if not email:
            raise ValueError('Please enter a valid email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email=None, username=None, first_name=None, last_name=None, date_of_birth=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, username, first_name, last_name, date_of_birth, password, **extra_fields)

    def create_superuser(self, email=None, username=None, first_name=None, last_name=None, date_of_birth=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, username, first_name, last_name, date_of_birth, password, **extra_fields)
    
class hobbies(models.Model):
    hobby = models.CharField(max_length=255, blank=True, default='')
    # users = models.ManyToManyField('user', blank=True)

    class Meta:
        verbose_name = 'Hobby'
        verbose_name_plural = 'Hobbies'

    def as_dict(self):
        return {
            'hobby': self.hobby
        }

    def __str__(self):
        return self.hobby

class user(AbstractUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    username = models.CharField(max_length=255, blank=True, default='', unique=True)
    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    date_of_birth = models.DateField(blank=True, null=True)

    hobbies = models.ManyToManyField(hobbies, blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    # EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'date_of_birth']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]

    def calculate_age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)) # checks if birthday has passed this year
    
    def as_dict(self):

        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'hobbies': [hobby.hobby for hobby in self.hobbies.all()],
            'date_joined': self.date_joined,
            'last_login': self.last_login,
            'age': self.calculate_age()
        }

class friends(models.Model):
    friend_request_from = models.ForeignKey(user, related_name='friend_request_from', on_delete=models.CASCADE)
    friend_request_to = models.ForeignKey(user, related_name='friend_request_to', on_delete=models.CASCADE)
    friendship_status = models.CharField(
        max_length=10,
        choices={('pending', 'Pending'), ('accepted', 'Accepted')},
        default='pending'
    )

    class Meta:
        verbose_name = 'Friend'
        verbose_name_plural = 'Friends'

    def as_dict(self):
        return {
            'id': self.id,
            'friend_request_from': self.friend_request_from.as_dict(),
            'friend_request_to': self.friend_request_to.as_dict(),
            'friendship_status': self.friendship_status
        }


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
