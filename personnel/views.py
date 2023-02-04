from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from .models import Department, Personnel
from .serializers import DepartmentSerializer, PersonnelSerializer, DepartmentPersonnelSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly, IsOwnerAndStafforReadOnly
from rest_framework import status
from rest_framework.response import Response

class DepartmentView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]


class PersonnelView(ListCreateAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.request.user.is_staff:
            personal = self.perform_create(serializer)
            data = {
                "message": f"Personal {personal.first_name} created successfully..",
                "personnel": serializer.data
            }
        else:
            data = {
                "message": f"Yo do not have authorization to perform this action..",
            }
            headers = self.get_success_headers(data)
            return Response(data, status=status.HTTP_401_UNAUTHORIZED, headers=headers)
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        
    def perform_create(self, serializer):
        person = serializer.save()
        person.create_user_id = self.request.user.id
        person.save()
        return person


class PersonnelGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    # permission_classes = [IsAuthenticated, IsOwnerAndStafforReadOnly]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff and (instance.create_user == self.request.user):
            return self.update(request, *args, **kwargs)
        else:
            data = {
                "message": f"Yo do not have authorization to perform this action..",
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return self.destroy(request, *args, **kwargs)
        else:
            data = {
                "message": f"Yo do not have authorization to perform this action..",
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class DepartmentPersonnelView(ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentPersonnelSerializer

    def get_queryset(self):
        name = self.kwargs["department"]
        return Department.objects.filter(name__iexact=name)

class CustomDepartmentPersonnelView(RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentPersonnelSerializer
    lookup_field = 'name'