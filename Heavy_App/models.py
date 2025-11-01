from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.core.validators import MinValueValidator , MaxValueValidator , RegexValidator

# Create your models here.

# The manager handles how we create users and superusers
class HeavyUserManager(BaseUserManager):
    
    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError("Email is (-REQUIRED-)")
        email=self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
# Method to create superusers (admins)
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        return self.create_user(email,password,**extra_fields)
    
    def get_by_natural_key(self, email):
        return self.get(email=email)




#Custom User Model
class HeavyUser(AbstractBaseUser,PermissionsMixin):
    objects = HeavyUserManager()
    #age- limit
    age_validator = [MinValueValidator(16),MaxValueValidator(99)]
    #phone- limit & format 
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    username = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    age = models.PositiveIntegerField(validators=age_validator)
    country = models.CharField(max_length=50)
    state  = models.CharField(max_length=50 , blank=True,null=True)
    phone_number = models.CharField(validators=[phone_validator] , max_length=16,blank=True,null=True)
    email = models.EmailField(unique=True)
    

    #Fitness profile
    weight = models .FloatField(blank=True,null=True)
    height = models.FloatField(blank=True,null=True)

    EXPERIANCE_LEVEL = [
        ('beginner','Beginner'),
        ('intermediate','Intermediate'),
        ('advanced','Advanced'),
        ('alpha','alpha'),
    ]
    experiance_level = models.CharField(max_length=20,choices=EXPERIANCE_LEVEL, blank=True)
    intrests = models.TextField(blank=True)

    #system field

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    

    #manager & Auth

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name", "lname","age","country", "state"]

    class Meta:
        db_table = "heavy_app_heavyuser"


    def __str__(self):
        return self.email

    