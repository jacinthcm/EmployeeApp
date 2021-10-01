import csv
import pandas as pd
from django.shortcuts import render
from django.contrib.auth import login as django_login, logout as django_logout
# Create your views here.
from rest_framework import generics, permissions, viewsets
from rest_framework.views import APIView
from django.views.generic.list import ListView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, EmployeeSerializer, UploadCsvSerializer
from .models import Employee

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data,
                         "token": token.key}, status=200)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        django_logout(request)
        return Response(status=204)


class UploadView(APIView):
    serializer_class = UploadCsvSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        employee_csv = request.data.get("csv", "")
        employee_data = pd.read_csv(employee_csv, sep=',')
        row_count = employee_data.shape[0]
        column_count = employee_data.shape[1]
        if row_count > 20:
            return Response({"error": "Invalid csv file. Must not contain more than 20 rows"}, status=201)
        elif column_count < 5:
            return Response({"error": "Invalid csv file. Must contain 5 columns minimum"}, status=201)
        else:
            for i in range(len(employee_data)):
               created = Employee.objects.get_or_create(
                   code=employee_data.iloc[i][0],
                   name=employee_data.iloc[i][1],
                   department=employee_data.iloc[i][2],
                   age=employee_data.iloc[i][3],
                   experience=employee_data.iloc[i][4],
               )

            return Response({"message": "Employee data added successfully"}, status=201)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = (TokenAuthentication,)

