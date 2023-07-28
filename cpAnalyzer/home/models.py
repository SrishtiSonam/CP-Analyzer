from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Member(models.Model):
    rollNo = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    codechef_user = models.CharField(max_length=50)
    codeforces_user = models.CharField(max_length=50)
    leetcode_user = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name
    
class leaderboard(models.Model):
    rollNo = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    total_problems = models.IntegerField() 
    def __str__(self) -> str:
        return self.name 

class codeforces(models.Model):
    username = models.CharField(max_length=100)
    total_problems = models.IntegerField()
    rating = models.IntegerField()
    recently_solved = models.URLField()
    def __str__(self) -> str:
        return self.username 
    
class codechef(models.Model):
    username = models.CharField(max_length=100)
    total_problems = models.IntegerField()
    rating = models.IntegerField()
    recently_solved = models.URLField()
    def __str__(self) -> str:
        return self.username 

class leetcode(models.Model):
    username = models.CharField(max_length=100)
    total_problems = models.IntegerField()
    rating = models.IntegerField()
    recently_solved = models.URLField()
    def __str__(self) -> str:
        return self.username 


class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=16)
    is_verified = models.BooleanField(default=False)
