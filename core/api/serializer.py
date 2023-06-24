from core.models import Department, Employee, CheckIn, Message
from rest_framework import serializers
from datetime import datetime

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(queryset=Department.objects.all(),slug_field='id')
    status = serializers.SerializerMethodField('status_check_in')
    class Meta:
        model = Employee
        fields = '__all__'

    
    
    
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
    class Meta:
        model = Message
        fields = '__all__'