from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser 
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.
# Base user manager for having a custom user table
class UserManager(BaseUserManager):
    def create_user(self, email,name,year, password=None): #creates a normal user
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name = name,
            year = year,
        )
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_staffuser(self, email,name,year, password): #creates a staff user
        user = self.create_user(
            email,
            password=password,
            name = name,
            year = year,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email,name,year, password): #creates a super user
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            name = name,
            year = year,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

# Model for custom user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    name = models.CharField(max_length=40)
    year = models.IntegerField()
    is_active = models.BooleanField(default=True) #active status
    staff = models.BooleanField(default=False)    #staff status
    admin = models.BooleanField(default=False)    #admin status
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["name","year"] 

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property                                     #property tag to call directly
    def is_staff(self): 
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    objects = UserManager()

#model for adding a project

class project(models.Model):
    projtitle = models.CharField(max_length=50)
    wiki = models.TextField()
    member = models.ManyToManyField(User)

    
class list(models.Model):
    listtitle = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    project = models.ForeignKey(to=project, on_delete=models.CASCADE)

class card(models.Model):
    cardtitle = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    list = models.ForeignKey(to=list, on_delete=models.CASCADE)
    assigned_member = models.ManyToManyField(User)
    