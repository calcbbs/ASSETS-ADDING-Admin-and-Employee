from django.db import models

# Create your models here.
class Login_Table(models.Model):
    Userid = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=120,null = False,blank=False)
    name = models.CharField(max_length = 120,null = False,blank = False)
    Admin = 'Admin'
    Employee = 'Employee'
    role_choice = (
        (Admin,'Admin'),
        (Employee,'Employee'),
    )
    role = models.CharField(
        max_length = 8,
        choices = role_choice,
        default = Employee
    )

    def __str__(self):
        return self.name

class Assets_Table(models.Model):
    Laptop = 'Laptop'
    Mouse = 'Mouse'
    Monitor = 'Monitor'
    CPU = 'CPU'
    Headset = 'Headset'
    MobilePhone = 'Mobile-Phone'

    Asset_Choice = (
        (Laptop,'Laptop'),
        (Mouse,'Mouse'),
        (Monitor,'Monitor'),
        (CPU,'CPU'),
        (Headset,'Headset'),
        (MobilePhone,'Mobile Phone')
    )
    ASSETID = models.CharField(max_length = 120, default = 'AS000', unique=True)
    DEVICE = models.CharField(
        max_length = 13,
        choices = Asset_Choice,
        default = Laptop
    )
    MANUFACTURE = models.DateField(auto_now = False,auto_now_add = False)
    SNO = models.IntegerField(default = 000)
    WARRANTYEXPIRY = models.DateField(auto_now = False,auto_now_add = False)

    def __str__(self):
        return self.ASSETID + ' ' + self.DEVICE

class Assets_Employee_Table(models.Model):
    Assetid = models.CharField(max_length = 120, default = 'AS000')
    Employeeid = models.IntegerField(null=False,blank=False)

    def __str__(self):
        return self.Assetid + ' ' + str(self.Employeeid)

class Employee_Table(models.Model):
    Employee_ID = models.IntegerField(unique=True,null=False,blank=False)
    First_Name = models.CharField(max_length=60)
    Last_Name = models.CharField(max_length=60)
    Company_Name = models.CharField(max_length=120,default = 'iTalent')
    Employee_Email = models.EmailField(max_length = 100,null = False, blank = False,default = ' ')

    def __str__(self):
        return self.First_Name + ' ' + self.Last_Name + '-' + str(self.Employee_ID)