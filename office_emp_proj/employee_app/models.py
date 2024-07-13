from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    department_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    salary = models.IntegerField(default=0)
    
    def __str__(self):
        return '%s %s'%(self.first_name, self.last_name)