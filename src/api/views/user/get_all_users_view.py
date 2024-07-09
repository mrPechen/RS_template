from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.models import Account


class GetUsersView(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(ModelSerializer):
        account_id = ReadOnlyField(source='id')
        login = ReadOnlyField(source='username')
        mentor_id = ReadOnlyField(source='user.mentor.id')

        class Meta:
            model = Account
            fields = ['account_id', 'login', 'mentor_id']

    def get(self, request):
        instance = Account.objects.all()
        serializer = self.OutputSerializer(instance, many=True)
        return Response(data=serializer.data, status=200)
