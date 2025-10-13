from django.db import models


# Create your models here.

class patientdata(models.Model):
   
    GENDER_CHOICES=[
        ('M','Male'),
        ('F','Female'),
        ('O','Others'),
      ]
    RH_CHOICES=[
        ('+','positive'),
        ('-','negative'),
     ]
    name=models.CharField(max_length=20)
    age=models.IntegerField()
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES) 
    bloodgroup=models.CharField(max_length=10)
    rhoptions=models.CharField(max_length=1,choices=RH_CHOICES)
    unit=models.IntegerField()
    location=models.TextField()
    hospital=models.CharField(max_length=100)
    ifany=models.TextField()



class userdetail(models.Model):
    username=models.CharField(max_length=20)
    email=models.EmailField(max_length=254)
    password=models.CharField(max_length=128)

class patientuser(models.Model):
    p_name = models.CharField(max_length=50)
    p_email = models.EmailField(unique=True)
    p_password = models.CharField(max_length=128)

    

class Donordetail(models.Model):

    GENDER_CHOICES=[
        ('M','Male'),
        ('F','Female'),
        ('O','Others'),
      ]
    RH_CHOICES=[
        ('+','positive'),
        ('-','negative'),
     ]
    username=models.CharField(max_length=20)
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES) 
    age=models.IntegerField()
    bloodgroup=models.CharField(max_length=10)
    rhoptions=models.CharField(max_length=1,choices=RH_CHOICES)
    unit=models.IntegerField()
    location=models.TextField()
    idproof=models.FileField(upload_to='idproof/')
    mc=models.FileField(upload_to='medical_certificate/')
    image=models.ImageField(upload_to='image/')
    patient = models.ForeignKey(
        'patientdata', on_delete=models.SET_NULL, null=True, blank=True, related_name='donors'
    )


      

    