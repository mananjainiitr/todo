from django.http.response import HttpResponse
from .models import   User , project , list
from .serializers import  listserializer, projectserializer ,cardserializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from django.shortcuts import redirect
import requests
from django.contrib.auth import authenticate , login
from todo import models

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
            return redirect("/todo/project")
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
            return redirect("/todo/project")
        return redirect("/todo/project")

class project(generics.ListCreateAPIView):
    queryset = project.objects.all()
    serializer_class = projectserializer

class list(generics.ListCreateAPIView):
    queryset = list.objects.all()
    serializer_class = listserializer

class card(generics.ListCreateAPIView):
    queryset = models.card.objects.all()
    serializer_class = cardserializer

# class list(generics.ListCreateAPIView):
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["data"] = 
#         return context
    
#     project_i = models.project.objects.get(id = 7)
#     queryset = models.list.objects.filter(project_id  = project_i)
#     serializer_class = listserializer

