from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns =[
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('appointment/', views.appointment, name='appointment'),
    path('blog/', views.blog, name='blog'),
    path('team/', views.team, name='team'),
    path('show_appointments/', views.retrieve_appointments, name='show_appointments'),
    path('delete/<int:id>', views.delete_appointment, name="delete_appointment"),
    path('edit/<int:appointment_id>', views.update_appointment, name="update_appointment"), 
    path('pay/', views.pay, name='pay' ),
    path('stk/', views.stk, name='stk'), # send the stk push prompt
    path('token/', views.token, name='token'), # generate the token for that particular transaction  
]