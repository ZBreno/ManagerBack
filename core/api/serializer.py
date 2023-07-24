from core.models import Department, Employee, CheckIn, Message
from rest_framework import serializers
from datetime import datetime, timedelta
from users.api.serializer import UserSerializer

class DepartmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    head = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True, required=False)
    class Meta:
        model = Department
        fields = ['id','name','assignment','contact','location','head','user']

    def get_head(self, instance):
        try:
            head = instance.employees.get(head="SIM")
            return f"{head.name}"
        except Employee.DoesNotExist:
            return None

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
            dateBR = checkin.date - timedelta(hours=3)
            data_checkin = checkin.date.date()
            data_checkinSerialiaze = dateBR.strftime("%d/%m/%y às %H:%M:%S") 
           
           
       
            if(data_atual == data_checkin):
                checked = True
                return {'checkin': checked, 'date': data_checkinSerialiaze }
            
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