import json
from django.http.response import HttpResponse
from .models import   User , project
from .serializers import  projectserializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins
from rest_framework import generics
from django.shortcuts import redirect
import requests
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate , login

def main_page(request):
    user = User.objects.create_user(
            email="mj6@gmail.com",
            name = "jai_manan",
            year = "2",
            password = "20312018",
  )
    
    user.save()
    return HttpResponse(user)
def login2(request):
    email="mj6@gmail.com"
    password = "20312018"
    user = User.objects.filter(email=email)
    

    if user:
        user = authenticate(email=email,password = password)
        request.user = user
        login(request,user)
        return redirect("/todo/regester")


    return redirect(user)

@csrf_exempt
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
        

# def project(request):
#     return ("hi")
    # stu = RegesteredUser.objects.all()
    # print(stu)
    # searilizer = RegesteredUserserial(stu , many=True)
    # json_data = JSONRenderer().render(searilizer.data)
    # return JsonResponse(searilizer.data,safe=False)
# @csrf_exempt
# @api_view(['GET', 'POST'])
# def regester(request):
#     response1 = request.data
#     r = requests.get(url = "https://channeli.in/open_auth/get_user_data/", headers={"Authorization": f"{response1['token_type']} {response1['access_token']}"})
#     # if request.method == 'GET':
    #     snippets = RegesteredUser.objects.all()
    #     serializer = RegesteredUserserial(snippets, many=True)
    #     return JsonResponse(serializer.data, safe=False)
    # elif request.method == 'POST':
    #     data = {"name": "Manann", "year": 2, "email": "mananjain1234.ujn@gmail.com", "enrollment": 20312018}
    #     print (request.POST.get("name"))
    #     serializer = RegesteredUserserial(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=201)
    #     return JsonResponse(serializer.errors, status=400)

# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = RegesteredUser.objects.all()
#     serializer_class = RegesteredUserserial

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class project(generics.ListCreateAPIView):
    queryset = project.objects.all()
    serializer_class = projectserializer


# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = RegesteredUser.objects.all()
#     serializer_class = RegesteredUser

