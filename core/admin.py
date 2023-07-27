from django.contrib import admin
from core.models import CheckIn, Department,  Employee, Message, User
# Register your models here.
admin.site.register(Department)
admin.site.register(CheckIn)
admin.site.register(Employee)
admin.site.register(Message)
admin.site.register(User)