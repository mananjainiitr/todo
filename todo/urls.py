from django.urls import path , include
from requests.api import get, request 
from todo import views
from rest_framework.routers import DefaultRouter

router1 = DefaultRouter()
router2 = DefaultRouter()
router3 = DefaultRouter()
router1.register('project',views.projectViewset,basename="project")
router2.register('list',views.listViewset,basename="project")
router3.register('card',views.cardViewset,basename="card")

urlpatterns = [
    path('viewsets/',include(router1.urls)),
    path('viewsets/project/id/<int:id>/',include(router2.urls)),
    path('viewsets/project/id/<int:id1>/list/id/<int:id2>/',include(router3.urls)),
    path('channeli',views.student_detail),
    path('login',views.student),   
]