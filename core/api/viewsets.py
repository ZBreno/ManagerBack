from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Department, CheckIn, Employee, Message
from core.api.serializer import DepartmentSerializer, EmployeeSerializer, MessageSerializer, CheckInSerializer
from datetime import datetime

class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
   

    @action(methods=['get'], detail=False, url_path='last_five')
    def last_five(self, request, *args, **kwargs):
        last_five = []
    
        for employee in Employee.objects.all():
            queryset = CheckIn.objects.filter(employee_id=employee.id)
            last_five.append({'nome': employee.name, 'qtd': queryset.count()})

        last_five = sorted(last_five, key=lambda d: d['qtd'])[:5]

        return Response(last_five)
    

    @action(methods=['get'], detail=False, url_path='un_checked')
    def un_checked(self, request, *args, **kwargs):
        
        unchecked_employees = []
    
        for employee in Employee.objects.all():

            employee = EmployeeSerializer(employee).data
            print(not employee)

            if(not bool(employee['status']['checkin'])):
                print(employee)
                unchecked_employees.append(employee)
        

        return Response(unchecked_employees)
    

    @action(methods=['get'], detail=False, url_path='percent')
    def percent(self, request, *args, **kwargs):
        queryset = Employee.objects.all()
        qtd_employee = queryset.count()
        data_atual = datetime.now().date()
        checkin = CheckIn.objects.filter(date__date=data_atual)
        percent = (checkin.count() / qtd_employee) * 100

        print('quanditdade de funcionario', qtd_employee, 'quanditdade de checkin', checkin.count())
        return Response({'percent' : f'{int(percent)}%'})


class CheckInViewSet(generics.CreateAPIView, generics.ListAPIView, generics.RetrieveAPIView, GenericViewSet):
    
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = [permissions.IsAuthenticated]
   
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.add_tags(['checkin']) 

class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False, url_path='message_unread')
    def count_message_read(self, request):
        queryset = self.queryset.filter(read=False)
        messages_unread = queryset.count()
        return Response({'total': messages_unread})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.read = True
        instance.save()
        serializer = self.get_serializer(instance)
        
        return Response(serializer.data)
