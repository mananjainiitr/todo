from django.contrib.auth.models import Permission
from rest_framework import permissions
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
       

class projectViewset(viewsets.ViewSet):
    '''Listing/Creating/Updating/Deleting of project'''
    permission_classes = [IsAuthenticated]
    def list(self,request):
        queryset = project.objects.all()
        seralizer = projectserializer(queryset,many=True)
        return Response(seralizer.data)
        

    def create(self, request):
        var = request.data
        var["creator"]=request.user.email
        serializer = projectserializer(data=var)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status= HTTP_201_CREATED)
        return Response(serializer.errors,status= HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        proj = project.objects.get(pk=pk)
        serializer = projectserializer(proj,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status= HTTP_201_CREATED)
        return Response(serializer.errors,status= HTTP_400_BAD_REQUEST)

    def retrive(self,request,pk=None):
        queryset = project.objects.all
        proj = get_object_or_404(queryset,pk=pk)
        serializer = projectserializer(proj)
        return Response(serializer.data)
    
    def destroy(self,request,pk=None):
        proj = project.objects.get(pk=pk)
        serializer = projectserializer(proj)
        proj.delete()
        return Response(serializer.data)
        

class listViewset(viewsets.ViewSet):
    '''Listing/Creating/Updating/Deleting of list'''
    
    def list(self,request,id):
        queryset = listOfProject.objects.filter(project_id=id)
        seralizer = listserializer(queryset,many=True)
        return Response(seralizer.data)

    def create(self, request , id):
        var = request.data
        var["project_id"]=id
        serializer = listserializer(data=var)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status= HTTP_201_CREATED)
        return Response(serializer.errors,status= HTTP_400_BAD_REQUEST)

    def update(self, request,id,pk):       
        list = listOfProject.objects.get(pk=pk)
        var = request.data
        var["project_id"]=id
        serializer = listserializer(list,data=var)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status= HTTP_201_CREATED)
        return Response(serializer.errors,status= HTTP_400_BAD_REQUEST)

    def retrive(self,request,id,pk=None):
        queryset = listOfProject.objects.all
        list_obj = get_object_or_404(queryset,pk=pk)
        serializer = listserializer(list_obj)
        return Response(serializer.data)
    
    def destroy(self,request,pk=None):
        obj = listOfProject.objects.get(pk=pk)
        serializer = listserializer(obj)
        obj.delete()
        return Response(serializer.data)

class cardViewset(viewsets.ViewSet):
    '''Listing/Creating/Updating/Deleting of card'''
   

    def list(self,request,id1,id2):    
        queryset = cardOfList.objects.filter(list_id=id2)
        seralizer = cardserializer(queryset,many=True)
        return Response(seralizer.data)

    def create(self, request,id1,id2):       
        var = request.data
        var["list_id"] = id2
        serializer = cardserializer(data=var)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status= HTTP_201_CREATED)
        return Response(serializer.errors,status= HTTP_400_BAD_REQUEST)

    def update(self, request,pk,id1,id2):    
        var = request.data
        var["list_id"] = id2
        list = listOfProject.objects.get(pk=pk)
        serializer = cardserializer(list,data=var)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status= HTTP_201_CREATED)
        return Response(serializer.errors,status= HTTP_400_BAD_REQUEST)

    def retrive(self,request,id1,id2,pk=None):    
        queryset = cardOfList.objects.all
        card_obj = get_object_or_404(queryset,pk=pk)
        serializer = listserializer(card_obj)
        return Response(serializer.data)
    
    def destroy(self,request,pk=None):
        obj = cardOfList.objects.get(pk=pk)
        serializer = cardserializer(obj)
        obj.delete()
        return Response(serializer.data)