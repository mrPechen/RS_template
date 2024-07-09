from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.serializers import EmailField, CharField
from rest_framework.views import APIView

from api.models import Account
from api.serializers.base_serializers.base_patch_serializer_conf import BasePatchSerializer


class RegistrationView(APIView):
    class InputSerializer(BasePatchSerializer):
        email = EmailField(required=False)
        phone = CharField(required=False)

        class Meta:
            model = Account
            fields = ['username', 'password', 'email', 'phone']
            ref_name = 'Registration input serializer'

        def create(self, validated_data):
            user = Account.objects.create_user(**validated_data)
            user.set_encrypted_password(validated_data['password'])
            return user

    @swagger_auto_schema(request_body=InputSerializer, tags=['auth'], responses={
        201: 'Success'
    })
    def post(self, request):
        data = request.data
        serializer = self.InputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)
