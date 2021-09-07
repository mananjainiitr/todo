from django.contrib.auth.models import Permission
from django.http.response import HttpResponseRedirectBase, JsonResponse
from rest_framework import permissions ,status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .models import   User , project , listOfProject,cardOfList
from .serializers import  listserializer, projectserializer ,cardserializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import  viewsets
from django.shortcuts import redirect
import requests
from django.contrib.auth import authenticate , login
from todo import models
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .permissions import IsAdminOrMember
from todo import serializers
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
        password = "passcode"
        user = authenticate(email=email, password=password)
        if user != None:
            login(request,user)
            return redirect("/todo/viewsets/project")
        elif user == None:
            user = User.objects.create_user(
            email=email,
            name = name,
            year = year,
            password = "passcode",
            )
            user.save()
            user = authenticate(email=email, password=password)
            login(request,user)
            return redirect("/todo/viewsets/project")
        return redirect("/todo/viewsets/project")
       

class projectViewset(viewsets.ModelViewSet):
    '''Listing/Creating/Updating/Deleting of project'''
    queryset = project.objects.all()
    serializer_class = projectserializer
    # permission_classes = [IsAdminOrMember]
    def perform_create(self, serializer):        
        serializer.save(creator=self.request.user.email)
class listViewset(viewsets.ModelViewSet):
    '''Listing/Creating/Updating/Deleting of list'''
    # permission_classes = [IsAdminOrMember]
    serializer_class = listserializer
    
    def get_queryset(self,*args,**kargs):
        id = self.kwargs.get("id")
        queryset = listOfProject.objects.filter(project_id=id)
        return queryset

    def perform_create(self, serializer , *args,**kargs):
        id = self.kwargs.get("id")
        proj = project.objects.get(id = id)
        serializer.save(project_id=proj)
    def update(self,request,*args,**kargs):
        partial = kargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    def perform_update(self, serializer, *args, **kwargs):
        id = self.kwargs.get("id")
        proj = project.objects.get(id = id)
        serializer.save(project_id=proj)
    


class cardViewset(viewsets.ModelViewSet):
    '''Listing/Creating/Updating/Deleting of card'''
    serializer_class = cardserializer
    # permission_classes = [IsAdminOrMember]
    def get_queryset(self,*args,**kargs):
        id = self.kwargs.get("id2")
        queryset = cardOfList.objects.filter(list_id=id)
        return queryset
 
    def perform_create(self, serializer , *args,**kargs):
        id = self.kwargs.get("id2")
        lst = listOfProject.objects.get(id = id)
        serializer.save(list_id=lst)

    def update(self,request,*args,**kargs):
        partial = kargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer, *args, **kwargs):
        id = self.kwargs.get("id2")
        lst = listOfProject.objects.get(id = id)
        serializer.save(list_id=lst)