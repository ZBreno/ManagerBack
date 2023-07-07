from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from users.models import User
from rest_framework.response import Response
from users.api.serializer import UserSerializer
from rest_framework import status
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)