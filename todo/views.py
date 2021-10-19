from django.contrib.auth.models import Permission
from django.core.checks.messages import Error
from django.http.response import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirectBase, JsonResponse
from requests.api import request
from rest_framework import permissions ,status 
from rest_framework.decorators import permission_classes , action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from .models import   User , project , listOfProject,cardOfList
from .serializers import  dashcardserializer, dashprojserializer, listserializer, projectserializer ,cardserializer, userserializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import  viewsets
from django.shortcuts import redirect
import requests
from django.contrib.auth import authenticate , login
from todo import models
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .permissions import AdminPermition, IsAdminOrMember, IsAdminOrMember_c, IsAdminOrMember_l, NotAcessable
from todo import serializers
from django.db.models import Q
def student_detail(request):
    if request.method == 'GET':
        url = "https://channeli.in/oauth/authorise/?client_id=STTrMkmTfDZEuFoDKj45uM6YEN4FXXXByWzltpRg&redirect_uri=http://127.0.0.1:8000/todo/login&state=RANDOM_STATE_STRING"
        response = redirect(url)
        return response

def student(request):
        code = request.GET.get("code")
        data = {'client_id':'STTrMkmTfDZEuFoDKj45uM6YEN4FXXXByWzltpRg',
        'client_secret':'rCDoILOftTynFi1YFGp97yCwAcSFeAWx8jkPvdOJEmSPVAuuhzUABjS8YUXy1LuQi0Wm3biIHuzqskoEFUyzHxqOc5O2HnDpvVXTWYyPO0hZtyztbNQ0bGnEb24e4PY9', 
        'grant_type':'authorization_code',
        'redirect_uri':'http://127.0.0.1:8000/todo/login',
        'code':code
        }
        response = requests.post("https://channeli.in/open_auth/token/", data = data)        
        response1 = response.json()
        r = requests.get(url = "https://channeli.in/open_auth/get_user_data/", headers={"Authorization": f"{response1['token_type']} {response1['access_token']}"})      
        response_data = r.json()
        email=response_data["contactInformation"]["instituteWebmailAddress"]
        name = response_data["person"]["fullName"]
        year = response_data["student"]["currentYear"]
        roles = response_data["person"]["roles"][1]["role"]
        user = User.objects.filter(email = email).exists()
        if roles == "Maintainer":
            if user :
                user = User.objects.get(email = email)
                login(request,user)
                return redirect("/todo/viewsets/project")
            else :
                user = User.objects.create_user(
                email=email,
                name = name,
                year = year,
                )
                user.save()
                user = User.objects.get(email = email)
                login(request,user)
                return redirect("/todo/viewsets/project")
        else:
            return HttpResponse("you are not member of IMG")

        
       
#viewset for displaying list of projects

class projectViewset(viewsets.ModelViewSet):
    '''Listing/Creating/Updating/Deleting of project'''
    queryset = project.objects.all()
    serializer_class = projectserializer
    permission_classes = [IsAuthenticated,]
    def perform_create(self, serializer):        
        serializer.save(creator=self.request.user)
    
    def get_permissions(self):
        if self.request.method in ('GET', 'POST'):
            self.permission_classes = [IsAuthenticated,]
        elif self.request.method in ('PUT', 'PATCH', 'DELETE'):
                self.permission_classes = [IsAdminOrMember]

        return super(projectViewset, self).get_permissions()

#list viewset for displaying list of list

class listViewset(viewsets.ModelViewSet):
    '''Listing/Creating/Updating/Deleting of list'''  
    serializer_class = listserializer
    def get_queryset(self,*args,**kwargs):
        """get list of list"""

        id = self.kwargs.get("id")
        
        queryset = listOfProject.objects.filter(project_id=id)
        proj = project.objects.filter(id=id).exists()
        if proj :
            return queryset
        else:
            raise Http404

    def perform_create(self, serializer , *args,**kargs):
        """create the list"""

        id = self.kwargs.get("id")
        proj = project.objects.get(id = id)
        if self.request.user.admin or (self.request.user in proj.member.all()) or (proj.creator.email in self.request.user.email):
            serializer.save(project_id=proj,creator=self.request.user)
        else:
            raise Http404
     
    def update(self,request,*args,**kargs):
        """update the list"""

        id = self.kwargs.get("id")
        print(self.request)
        obj = project.objects.get(id = id)
        
        partial = kargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer, *args, **kwargs):
        """update the list"""

        id = self.kwargs.get("id")    
        proj = project.objects.get(id = id)
        serializer.save(project_id=proj)
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated,]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
                self.permission_classes = [IsAdminOrMember_l,IsAuthenticated]
        return super(listViewset, self).get_permissions()
       
# card viewset for displaying cards in list  

class cardViewset(viewsets.ModelViewSet):
    '''Listing/Creating/Updating/Deleting of card'''
    serializer_class = cardserializer
    def get_queryset(self,*args,**kargs):
        """display list of card"""
        p_id = self.kwargs.get("id1")
        id = self.kwargs.get("id2")
        queryset = cardOfList.objects.filter(list_id=id)
        proj = project.objects.filter(id=p_id).exists()
        lis = listOfProject.objects.get(id = id)
        print(p_id)
        print(lis.project_id)
        if p_id == lis.project_id.id :
            return queryset
        else:
            raise Http404
 
    def perform_create(self, serializer , *args,**kargs):
        """create cards"""

        id = self.kwargs.get("id2")
        print("po")
        print(id)
        lst = listOfProject.objects.get(id = id)
        proj = project.objects.get(id = lst.project_id.id)
        if self.request.user.admin or (self.request.user in proj.member.all()) or (proj.creator.email in self.request.user.email):
            serializer.save(list_id=lst,creator=self.request.user)
        else:
            raise Http404

    def update(self,request,*args,**kargs):
        """Update cards"""

        partial = kargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
   
    def perform_update(self, serializer, *args, **kwargs):
        """update cards"""

        id = self.kwargs.get("id2")
        lst = listOfProject.objects.get(id = id)
        serializer.save(list_id=lst)

    def get_permissions(self):
        if self.request.method in ('GET', 'POST'):
            self.permission_classes = [IsAuthenticated,]
        elif self.request.method in ('PUT', 'PATCH', 'DELETE'):
                self.permission_classes = [IsAdminOrMember_c,IsAuthenticated]
        return super(cardViewset, self).get_permissions()

#Admin only data of user

class userViewset(viewsets.ModelViewSet):
    serializer_class = userserializer
    queryset = User.objects.all()
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [NotAcessable]            
        else:
            self.permission_classes = [IsAuthenticated,AdminPermition]
        return super(userViewset, self).get_permissions()

#display dashboard to user project data viewset

class dashProjectViewset(viewsets.ModelViewSet):
    serializer_class = dashprojserializer
    def get_queryset(self,*args,**kargs):
        id = self.request.user.email
        queryset = project.objects.filter(Q(member__email__contains = id )|Q(creator = self.request.user))
        return queryset

#display dashboard to user card data viewset

class dashCardViewset(viewsets.ModelViewSet):
    serializer_class = dashcardserializer
    def get_queryset(self,*args,**kargs):
        id = self.request.user.email
        queryset = cardOfList.objects.filter(assigned_member__email__contains = id)
        return queryset