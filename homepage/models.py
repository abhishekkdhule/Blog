from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Articles(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.CharField(max_length=2000)
    wantpublic=models.BooleanField(default=True)
    heading=models.CharField(max_length=100,blank=True,null=True)
    img=models.ImageField(upload_to="homepage/static/images/",blank=True,null=True)

    def __str__(self):
        return self.user.username

    def __id__(self):
        return  self.user.username