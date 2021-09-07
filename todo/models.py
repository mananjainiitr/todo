from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser 
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from ckeditor.fields import RichTextField
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
    """
        Custom user table for regestering the user
        fields email , name , year , is_active , staff , admin 

    """
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

    @property                                     #property tag to call directly is staff
    def is_staff(self): 
        return self.staff

    @property                                     #property tag to call directly is admin
    def is_admin(self):
        return self.admin

    objects = UserManager()

#model for adding a project

class project(models.Model):
    """
        Custom user table for regestering the user
        fields projtitle , wiki , member
        
    """
    projtitle = models.CharField(max_length=50)
    wiki = RichTextField()
    member = models.ManyToManyField(User)
    creator = models.EmailField(default="admin@gmail.com")
    def __str__(self):
        return self.projtitle

#model for adding a list
    
class listOfProject(models.Model):

    """
        Custom user table for regestering the user
        fields listtitle , desc , is_completed , start_date , due_date , project_id
        
    """
    listtitle = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    is_completed = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    project_id = models.ForeignKey(to=project, on_delete=models.CASCADE)

    def __str__(self):
        return self.listtitle

#model for adding a card

class cardOfList(models.Model):
    """
        Custom user table for regestering the user
        fields cardtitle , desc , is_completed , start_date , due_date , list_id , assigned_members
        
    """
    cardtitle = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    start_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    list_id = models.ForeignKey(to=listOfProject, on_delete=models.CASCADE)
    assigned_member = models.ManyToManyField(User)

    def __str__(self):
        return self.cardtitle
    