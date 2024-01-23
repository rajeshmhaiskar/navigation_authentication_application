from django.contrib.auth.models import BaseUserManager


def get_create_superuser_field_names():
    return ['emp_id', 'email', 'password']


class CustomUserManager(BaseUserManager):
    def create_user(self, emp_id, email, password=None, **extra_fields):
        if not emp_id:
            raise ValueError('The Employee ID field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(emp_id=emp_id, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, emp_id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(emp_id, email, password, **extra_fields)

