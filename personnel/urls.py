from django.urls import path
from .views import DepartmentView, PersonnelView, PersonnelGetUpdateDelete, DepartmentPersonnelView, CustomDepartmentPersonnelView

urlpatterns = [
    path('department/', DepartmentView.as_view()),
    path('personnel/', PersonnelView.as_view()),
    path('personnel/<int:pk>/', PersonnelGetUpdateDelete.as_view()),
    # path('department/<str:department>/', DepartmentPersonnelView.as_view()),
    path('department/<str:name>/', CustomDepartmentPersonnelView.as_view()),
]