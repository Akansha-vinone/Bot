from django.db import models
# from django.contrib.auth.hashers import make_password

class Register(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def set_password(self,new_password):
        self.password = new_password
