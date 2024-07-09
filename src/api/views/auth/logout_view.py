from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = TokenBlacklistSerializer

    @swagger_auto_schema(request_body=TokenBlacklistSerializer, tags=['auth'], responses={
        201: 'Success',
        401: 'Unauthorized',
    })
    def post(self, request):
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(status=201)
