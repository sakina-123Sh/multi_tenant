import os
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import pandas as pd
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




class UpdateExcelAPIView(APIView):
    def post(self, request):
        # Extract file from request
        file_obj = request.FILES.get('file')

        # Check if the file object is received
        if not file_obj:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Save the uploaded file temporarily
            path = default_storage.save('tmp/' + str(uuid.uuid4()), ContentFile(file_obj.read()))

            # Full path for the uploaded file
            temp_file_path = os.path.join(default_storage.location, path)

            # Read the Excel file
            df = pd.read_excel(temp_file_path)

            # Replace all empty cells in "SalesMan" column with "shaukat ali"
            df['SalesMan'].fillna('shaukat ali', inplace=True)

            # Convert 'OrderDate' column to datetime format
            df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')

            # Replace all cells in "OrderDate" column with date format "DD/MM/20YY"
            df['OrderDate'] = df['OrderDate'].dt.strftime('%d/%m/%Y')

            # Generate a unique output file name
            output_file_name = f"output_{uuid.uuid4()}.xlsx"
            output_file_path = os.path.join('/home/shaukatali/Desktop/', output_file_name)  # Replace with your output directory

            # Create a new Excel file with updated data
            df.to_excel(output_file_path, index=False)

            # Cleanup the temporary file
            default_storage.delete(path)

            # Return success response with output file path
            return Response({'message': 'Excel file updated successfully', 'output_file': output_file_path}, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Cleanup the temporary file in case of failure
            if 'temp_file_path' in locals():
                default_storage.delete(path)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
