from djongo import models

class AdminAccounts(models.Model):
    _id=models.ObjectIdField(unique=True)
    firstname = models.CharField(max_length=255)
    lastname= models.CharField(max_length=255)
    rollno=models.CharField(max_length=200)   
    password=models.CharField(max_length=200)   
    email=models.CharField(max_length=150)  
    profile_img=models.CharField(max_length=200)
    cover_pic=models.CharField(max_length=200)
    department=models.CharField(max_length=200)
    admin=models.CharField(max_length=200)
    objects=models.DjongoManager()

class StudentAccounts(models.Model):
    _id=models.ObjectIdField(unique=True)
    firstname = models.CharField(max_length=255)
    lastname= models.CharField(max_length=255)
    rollno=models.CharField(max_length=200)   
    password=models.CharField(max_length=200)   
    email=models.CharField(max_length=150)  
    profile_img=models.CharField(max_length=200)
    cover_pic=models.CharField(max_length=200)
    department=models.CharField(max_length=200)
    objects=models.DjongoManager()
    
class ClubsAccounts(models.Model):
    _id=models.ObjectIdField(unique=True)
    studentobjectid=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    club=models.CharField(max_length=200)
    objects=models.DjongoManager()
    
class Updates(models.Model):
    _id=models.ObjectIdField(unique=True)
    department=models.CharField(max_length=200)
    date=models.CharField(max_length=200)
    urltext=models.CharField(max_length=200)
    url=models.CharField(max_length=200)
    objects=models.DjongoManager()

class Quiz(models.Model):
    _id=models.ObjectIdField(unique=True)
    date=models.CharField(max_length=100)
    title=models.CharField(max_length=1000)  
    quiz=models.JSONField(max_length=100)
    club=models.CharField(max_length=100)
    objects=models.DjongoManager()
    
class Quizresult(models.Model):
    _id=models.ObjectIdField(unique=True)
    date=models.CharField(max_length=100) 
    idd=models.CharField(max_length=100) 
    title=models.CharField(max_length=1000)  
    quizresult=models.JSONField(max_length=100)
    score=models.CharField(max_length=1000) 
    objects=models.DjongoManager()

    