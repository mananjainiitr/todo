from django.urls import path , include
from requests.api import get, request 
from todo import views
from rest_framework.routers import DefaultRouter

router1 = DefaultRouter()
router2 = DefaultRouter()
router3 = DefaultRouter()
router4 = DefaultRouter()
router5 = DefaultRouter()
router1.register('project',views.projectViewset,basename="project")
router2.register('list',views.listViewset,basename="project")
router3.register('card',views.cardViewset,basename="card")
router4.register('info',views.userViewset,basename="user")
router5.register('card',views.dashCardViewset,basename="dash_card")
router5.register('project',views.dashProjectViewset,basename="dash_proj")

urlpatterns = [
    path('viewsets/',include(router1.urls)),
    path('viewsets/project/id/<int:id>/',include(router2.urls)),
    path('viewsets/project/id/<int:id1>/list/id/<int:id2>/',include(router3.urls)),
    path('user/',include(router4.urls)),
    path('dashbord/',include(router5.urls)),
    path('channeli',views.student_detail),
    path('login',views.student),
]