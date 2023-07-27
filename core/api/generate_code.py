from random import randint
from core.models import Employee

def code():
    number = randint(10000, 999999)
    try:
        Employee.objects.get(code=number)
        return code()
    except Employee.DoesNotExist:
        return number