from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import user_data
from .serializers import userSeralizer
from .forms import LoginForm
from rest_framework import permissions
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F, Count, JSONField
from django.db.models.functions import Length, Cast



# Create your views here.
class UserActions(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        id = request.GET.get('id')
        if id:
            response_data = list(user_data.objects.filter(id = id).values())
        else:
            response_data = list(user_data.objects.values())
        return Response(response_data, status = status.HTTP_200_OK)
    
    def post(self, request):
        try:
            with transaction.atomic():
                serializer_data = userSeralizer(data = request.data)
                if serializer_data.is_valid():
                    res = serializer_data.save()
                    if res == 'Success':
                        user_data.objects.filter(Email = request.data.get('Email')).update(Password = request.data.get('Password'))
                        user = User.objects.create(username=request.data.get('Email'))
                        user.email = request.data.get('Email')
                        user.set_password(request.data.get('Password'))  # Set the password as needed
                        user.save()
                        return Response(status = status.HTTP_200_OK)
                    return Response([{'msg' : res}],status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response([{'msg' : 'Invalid data'}],status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response([{'msg' : e}],status = status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        id = request.GET.get('id')
        user_data.objects.filter(id = id).delete()
        return Response(status = status.HTTP_200_OK)
        
    def put(self, request):
        try:
            validated_data = userSeralizer(data = request.data)
            if validated_data.is_valid():
                instance = user_data.objects.get(id = request.data.get('id'))
                serializer_data = userSeralizer()
                res = serializer_data.update(instance, validated_data)
                if res == 'Success':
                    return Response([{'msg' : res}],status = status.HTTP_200_OK)
                else:
                    return Response([{'msg' : res}],status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response([{'msg' : 'Invalid data'}],status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response([{'msg' : e}],status = status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request):
        try:
            instance = user_data.objects.get(id = request.data.get('id'))
            shortened_urls = []
            if instance.shortened_urls:
                shortened_urls = list(instance.shortened_urls)
            shortened_urls.append(request.data.get('id'))
        except Exception as e:
            return Response([{'msg' : e}],status = status.HTTP_400_BAD_REQUEST)
        
class userLogin(APIView):
    def get(self, request):
        loginform = LoginForm()
        return render(request, "login.html", {"form": loginform})
    
    def post(self,request):
        data = request.data

        username = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/reg')
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)   
class userLogout(APIView):
    def get(self, request):
        logout(request)
        return redirect('/login')
    
class adminPanel(APIView):
    def get(self, request):
        userData = user_data.objects.annotate(num_items=Count(Cast('shortened_urls', output_field=JSONField()))).values()
        # details = []
        # import pdb;pdb.set_trace()
        # for data in details:
        #     data['num_items'] = len(data['shortened_urls'])
        return render(request, "list.html", {"data": userData})