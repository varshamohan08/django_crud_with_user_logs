from django.db import models
from django.db.models.fields import TextField, EmailField
from django.db.models import JSONField
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class user_data(AbstractBaseUser):
    first_name = TextField(blank= False, null= False)
    last_name = TextField()
    Email = EmailField(blank= False, null= False, unique=True)#(required and unique)
    Password = TextField(blank= False, null= False, default='test')#(required, password should have atleast 1 special character, 1 uppercase, 1 number, minlength 8)
    shortened_urls = JSONField(null=True)
    # REQUIRED_FIELDS = ['Email','Password']
    USERNAME_FIELD = 'Email'

# class login_user(AbstractBaseUser):
#     username = EmailField(blank= False, null= False, unique=True)
#     password = TextField(blank= False, null= False)
#     # REQUIRED_FIELDS = ['username','password']
#     USERNAME_FIELD = 'username'



[
{
    "id":2,
    "first_name" : "varsha",
    "last_name" : "m",
    "Email" : "varsha@g.com",
    "Password" : "varsha"
}
]