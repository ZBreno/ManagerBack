from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Department, CheckIn, Employee, Message
from core.api.serializer import DepartmentSerializer, EmployeeSerializer, MessageSerializer, CheckInSerializer

class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

class CheckInViewSet(ModelViewSet):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False, url_path='message_unread')
    def count_message_read(self, request):
        queryset = self.queryset.filter(read=False)
        messages_unread = queryset.count()
        return Response({'total de mensagens não lidas': messages_unread})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.read = True
        instance.save()
        serializer = self.get_serializer(instance)
        
        return Response(serializer.data)
