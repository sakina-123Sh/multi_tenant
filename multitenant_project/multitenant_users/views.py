from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer

class SignUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(f"Received email: {email}, password: {password}")

        if email and password:
            user = User.objects.filter(email=email).first()
            print(f"Retrieved user: {user}")

            if user:
                print(f"User password from database: {user.password}")

                # Check if the password matches
                if user.password == password:
                    # Authentication successful
                    print("Authentication successful")
                    return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
                else:
                    # Password does not match
                    print("Password does not match")
            else:
                # User does not exist
                print("User does not exist")

        # Invalid credentials
        print("Invalid credentials")
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


