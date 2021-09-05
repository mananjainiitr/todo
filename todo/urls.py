from django.urls import path 
from todo import views
urlpatterns = [
    path('channeli',views.student_detail),
    path('login',views.student),
    path('project',views.project.as_view()),
    path('project/<int:project_id>',views.list.as_view()),
    path('project/<int:project_id>/<int:list_id>',views.card.as_view()),
    
]