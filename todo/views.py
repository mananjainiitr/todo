from django.contrib.auth.models import Permission
from django.core.checks.messages import Error
from django.core.exceptions import BadRequest, ValidationError
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirectBase, JsonResponse
from requests.api import request
from rest_framework import permissions ,status
from rest_framework import authentication 
from rest_framework.decorators import authentication_classes, permission_classes , action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from .models import   User , project , listOfProject,cardOfList
from .serializers import  ProjectValidator, dashcardserializer, dashprojserializer, dataserializer, listserializer, projectserializer ,cardserializer, userdataserializer, userserializer
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
from rest_framework.authtoken.models import Token, TokenProxy
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
def student_detail(request):
    if request.method == 'GET':
        url = "https://channeli.in/oauth/authorise/?client_id=STTrMkmTfDZEuFoDKj45uM6YEN4FXXXByWzltpRg&redirect_uri=http://127.0.0.1:8000/todo/login&state=RANDOM_STATE_STRING"
        response = redirect(url)
        return response

def student(request):
        code = request.GET.get("code")
        print(code)
        data = {'client_id':'STTrMkmTfDZEuFoDKj45uM6YEN4FXXXByWzltpRg',
        'client_secret':'rCDoILOftTynFi1YFGp97yCwAcSFeAWx8jkPvdOJEmSPVAuuhzUABjS8YUXy1LuQi0Wm3biIHuzqskoEFUyzHxqOc5O2HnDpvVXTWYyPO0hZtyztbNQ0bGnEb24e4PY9', 
        'grant_type':'authorization_code',
        'redirect_uri':'http://127.0.0.1:8000/todo/login',
        'code':code
        }
        response = requests.post("https://channeli.in/open_auth/token/", data = data)  
        # print(response)      
        response1 = response.json()
        # print(response1); 
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
                data1 = {}
                data1['token'] = Token.objects.get(user=user).key
                print (data1)
                # return JsonResponse(data1)
                return redirect("http://localhost:3000/todo/project?Token=Token "+data1['token'])
            else :
                user = User.objects.create_user(
                email=email,
                name = name,
                year = year,
                )
                user.save()
                user = User.objects.get(email = email)
                Token.objects.create(user=user)
                login(request,user)
                data1 = {}
                data1['token'] = Token.objects.get(user=user).key
                # return Response (data1)
                return redirect("http://localhost:3000/todo/project?Token=Token "+data1['token'])
        else:
            return HttpResponse("you are not member of IMG")

        
       
#viewset for displaying list of projects

class projectViewset(viewsets.ModelViewSet):
    '''Listing/Creating/Updating/Deleting of project'''
    queryset = project.objects.all()
    serializer_class = projectserializer
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated,]
    def perform_create(self, serializer):        
        serializer.save(creator=self.request.user)
    
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.authentication_classes = [TokenAuthentication]
            self.permission_classes = [IsAuthenticated,]
            print("hi")
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
                self.permission_classes = [IsAdminOrMember]

        return super(projectViewset, self).get_permissions()

#list viewset for displaying list of list

class listViewset(viewsets.ModelViewSet):
    '''Listing/Creating/Updating/Deleting of list'''  
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    # permission_classes = [IsAuthenticated,]
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
        projects = project.objects.get(id=id)
        lists = listOfProject.objects.filter(project_id = projects,listtitle=self.request.data['listtitle']).exists()
        print(not(lists))
        # print (self.request.data['listtitle'])
        if(not(lists)):
            if self.request.user.admin or (self.request.user in proj.member.all()) or (proj.creator.email in self.request.user.email):
                serializer.save(project_id=proj,creator=self.request.user)
            else:
                raise Http404
        else:
            raise BadRequest("invalid request")
     
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
        projects = project.objects.get(id=id)
        lists = listOfProject.objects.filter(project_id = projects,listtitle=self.request.data['listtitle']).exists()
        lis = listOfProject.objects.get(id = self.kwargs.get("pk")).listtitle
        if (lis == self.request.data['listtitle']):
            lists = False
        # print(lis)
        # print(lis)
        if (not(lists)):
            serializer.save(project_id=proj)
        else :
            raise BadRequest("invalid data")
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated,]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
                self.permission_classes = [IsAdminOrMember_l,IsAuthenticated]
        return super(listViewset, self).get_permissions()
       
# card viewset for displaying cards in list  

class cardViewset(viewsets.ModelViewSet):
    '''Listing/Creating/Updating/Deleting of card'''
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    # permission_classes = [IsAuthenticated,]
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
        cards = cardOfList.objects.filter(list_id = lst,cardtitle=self.request.data['cardtitle']).exists()
        if (not(cards)):
            proj = project.objects.get(id = lst.project_id.id)
            if self.request.user.admin or (self.request.user in proj.member.all()) or (proj.creator.email in self.request.user.email):
                serializer.save(list_id=lst,creator=self.request.user)
            else:
                raise Http404
        else:
            raise BadRequest('invalid request')

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
        cards = cardOfList.objects.filter(list_id = lst,cardtitle=self.request.data['cardtitle']).exists()
        car = cardOfList.objects.get(id = self.kwargs.get("pk")).cardtitle
        if(car == self.request.data['cardtitle']):
            cards = False
        if (not(cards)):
            serializer.save(list_id=lst)
        else:
            raise BadRequest('invalid request')


    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated,]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
                self.permission_classes = [IsAdminOrMember_c,IsAuthenticated]
        return super(cardViewset, self).get_permissions()

#Admin only data of user

class userViewset(viewsets.ModelViewSet):
    serializer_class = userserializer
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [NotAcessable]            
        else:
            self.permission_classes = [IsAuthenticated,AdminPermition]
        return super(userViewset, self).get_permissions()

#display dashboard to user project data viewset

class dashProjectViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated,]
    serializer_class = dashprojserializer
    def get_queryset(self,*args,**kargs):
        id = self.request.user.email
        queryset = project.objects.filter(Q(member__email__contains = id )|Q(creator = self.request.user))
        return queryset

#display dashboard to user card data viewset

class dashCardViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated,]
    serializer_class = dashcardserializer
    def get_queryset(self,*args,**kargs):
        id = self.request.user.email
        queryset = cardOfList.objects.filter(assigned_member__email__contains = id)
        return queryset

class dataview(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated,]
    serializer_class = dataserializer
    queryset = User.objects.all()

class mydataview(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated,]
    serializer_class = userdataserializer
    def get_queryset(self,*args,**kargs):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset

class validateProject(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated,]
    serializer_class = ProjectValidator
    def get_queryset(self,*args,**kargs):
        queryset = project.objects.filter(projtitle = self.kwargs.get("title"))
        return queryset