from django.urls import path 
from todo import views
urlpatterns = [
    path('channeli',views.student_detail),
    path('login',views.student),
    path('get',views.main_page),
    path('in',views.login2),
    path('project',views.project.as_view()),
]