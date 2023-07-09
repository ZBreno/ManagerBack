from core.models import Department, Employee, CheckIn, Message
from rest_framework import serializers
from datetime import datetime
from users.api.serializer import UserSerializer

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','name','assignment','contact','location']

class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    status = serializers.SerializerMethodField('status_check_in')
    class Meta:
        model = Employee
        fields = ['id','name', 'email','birth_date','head','department','assignment','finger_print','code','phone', 'status']
    
    def status_check_in(self, instance):

        data_atual = datetime.now().date()
        checked = False
        employee = instance.id
  
        try:
            checkin = CheckIn.objects.filter(employee=employee).latest("id")
            data_checkin = checkin.date.date()
            data_checkinSerialiaze = checkin.date
       
            if(data_atual == data_checkin):
                checked = True
                return {'checkin': checked, 'date': data_checkinSerialiaze}
            
            return {'checkin': checked}
        
        except:
            return {'checkin': checked}

class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    manager = UserSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id','title', 'department', 'attachment', 'manager', 'read', 'message_type', 'description','employee']