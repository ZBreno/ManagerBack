from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Department, CheckIn, Employee, Message
from core.api.serializer import DepartmentSerializer, EmployeeSerializer, MessageSerializer, CheckInSerializer
from datetime import datetime, timedelta, date
from django.db.models import Q
from core.api.generate_code import code
from users.models import User

class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['']
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        name = request.query_params.get('name') or ""
        queryset = Department.objects.filter(user=request.user, name__icontains=name)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        employee = Employee.objects.get(id=request.data['head'])
        employee.head= "SIM"

        return Response(serializer.data)
    
    
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        name = request.query_params.get('name') or ""
        try:
            department = Department.objects.get(id=request.query_params.get('department'))
            queryset = Employee.objects.filter(department=department, name__icontains=name)
        except Department.DoesNotExist:
            queryset = Employee.objects.filter(name__icontains=name)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data['code'] = code()
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['department'] = Department.objects.get(id=request.data['department'])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.department = Department.objects.get(id=request.data['department'])
        instance.save()

        return Response(serializer.data)

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

    @action(methods=['get'], detail=True, url_path='messages')
    def messages(self,request, *args, **kwargs):
        employee = Employee.objects.get(id=kwargs['pk'])

        messages = Message.objects.filter(Q(department=employee.department) | Q(employee=employee) | Q(Q(employee__isnull=True), Q(department__isnull=True)))
        queryset = MessageSerializer(messages, many=True)
        return Response(queryset.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='today_yesterday')
    def today_yesterday(self,request,*args, **kwargs):
        employee = Employee.objects.get(id=kwargs['pk'])

        today = datetime.now()
        yesterday = datetime.now() - timedelta(days=1)
        
        checkins = CheckIn.objects.filter(employee=employee)
        checks = []
        for checkin in checkins:
            date = checkin.date - timedelta(hours=2)

            if date.date() == today.date() or date.date() == yesterday.date():
                checks.append(checkin)
                
        data = []
        for checkin in checks:
            data.append({"data" : checkin.date.date().strftime('%d/%m/%Y'), "time" : (checkin.date-timedelta(hours=3)).time().strftime('%H:%M')})

        return Response(data, status=status.HTTP_200_OK)

class CheckInViewSet(generics.CreateAPIView, generics.ListAPIView, generics.RetrieveAPIView, GenericViewSet):
    
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = [permissions.AllowAny]

    @action(methods=['get'], detail=False, url_path='week_checkins')
    def week(self,request, *args, **kwargs):
        dt = datetime.today()
        week = [dt + timedelta(days=i) for i in range(0 - dt.weekday(), 7 - dt.weekday())]

        results = []
        for day in week:
            number = 0
            checkins = CheckIn.objects.all()
            for checkin in checkins:
                if checkin.date.date() == day.date():
                    number += 1
            results.append(number)

        return Response(results, status=status.HTTP_200_OK)
   
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.add_tags(['checkin']) 

class MessageViewSet(generics.CreateAPIView, generics.ListAPIView, generics.RetrieveAPIView, generics.DestroyAPIView ,GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        type = request.query_params.get('type')
        name = request.query_params.get('name') or ""
        print(name)

        if type:
            queryset = Message.objects.filter(Q(employee__name__icontains=name) | Q(manager__name__icontains=name), message_type=type)
        else:
            queryset = Message.objects.filter(Q(employee__name__icontains=name) | Q(manager__name__icontains=name))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'department' in request.data:
            serializer.validated_data['department'] = Department.objects.get(id=request.data['department'])
        if not request.user.__class__.__name__ == "AnonymousUser":
            serializer.validated_data['manager'] = request.user
        if 'employee' in request.data:
            serializer.validated_data['employee'] = Employee.objects.get(id=request.data['employee'])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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

    @action(methods=['get'], detail=False, url_path='news')
    def news(self, request):
        return Response(Message.objects.filter(read=False).count(), status=status.HTTP_200_OK)
