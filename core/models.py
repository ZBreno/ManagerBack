from django.db import models
from users.models import User# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=50)
    function = models.CharField(max_length=255)
    contact = models.EmailField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    birth_date = models.DateField()
    head = models.BooleanField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    function = models.CharField(max_length=50)
    finger_print = models.ImageField(upload_to ='finger_prints/', null=True)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.name


class CheckIn(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.date, self.employee

class Message(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ("AVISO", "Aviso"),
        ("ATESTADO", "Atestado"),
        ("JUSTIFICATIVA_DE_FALTA", "Justificativa de falta"),
        ("DEMISSAO", "Demissão"),
        ("PROMOCAO", "Promoção"),
        ("OUTRO", "Outro"),
    ]

    title = models.CharField(max_length=100)
    attachment = models.FileField(upload_to ='attachment/', null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    read = models.BooleanField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    message_type = models.CharField(choices=MESSAGE_TYPE_CHOICES,max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title

