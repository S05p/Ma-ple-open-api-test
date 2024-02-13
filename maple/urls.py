from django.urls import path, include
from maple import views

app_name= 'maple'
urlpatterns = [
    path('',views.index,name='index'),
    path('equipment/<str:user_name>',views.equipment,name='equipment'),
]
