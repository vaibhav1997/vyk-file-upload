from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User  # Default User model
from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from django.core import serializers
# Create your views here.


def Home(request):
    return render(request, 'index.html')


def AdminLogin(request):
    return HttpResponseRedirect('http://127.0.0.1:8000/admin')


def FileuploaderLogin(request):
    return render(request, 'uploaderlogin.html')


def FilerecepientLogin(request):
    return render(request, 'recepientlogin.html')


# Token Issue for uploader
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def UploaderLoginFunc(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    # token, _ = Token.objects.get_or_create(user=user)
    if CustomUser.objects.filter(user=user, user_type="UPLOADER"):
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key},
                        status=HTTP_200_OK)


# Token Issue for recepient
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def RecipientLoginFunc(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    # token, _ = Token.objects.get_or_create(user=user)
    if CustomUser.objects.filter(user=user, user_type="RECEPIENT"):
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key},
                        status=HTTP_200_OK)

# Uploading Files
@csrf_exempt
@api_view(["POST"])
def FileUpload(request):
    current_user = request.user
    current_user = get_object_or_404(CustomUser, user_id=current_user.id)
    print(current_user.id)
    file_uploader = current_user.id

    recipient = request.data.get("recipient")
    reciever = get_object_or_404(CustomUser, user__email=recipient)
    print(reciever.id)

    file_recepient = reciever.id
    file = request.FILES["file"]
    print("Files " + str(file))
    data = {
        'file_uploader': file_uploader,
        'file_recepient': file_recepient,
        'file': file
    }
    file_serializer = FileSerializer(data=data)
    if file_serializer.is_valid():
        file_serializer.save()
        return Response(file_serializer.data, status=HTTP_200_OK)
    else:
        return Response(file_serializer.errors, status=HTTP_400_BAD_REQUEST)

# View data (Uploader)
@csrf_exempt
@api_view(["POST"])
def FileLog(request):
    current_user = request.user
    current_user = get_object_or_404(CustomUser, user_id=current_user.id)
    print(current_user.id)
    data = FileManager.objects.filter(file_uploader_id=current_user.id)

    # return Response(FileSerializer(data, many=True).data)
    ProcessData = FileSerializer(data, many=True).data
    # print(ProcessData)
    for i in ProcessData:
        # print(i["file_recepient"])
        getmail = get_object_or_404(CustomUser, id=i['file_recepient'])
        i["file_recepient"] = getmail.user.email
        # getmail = get_object_or_404(CustomUser, id=i['file_recepient'])
        # print(getmail)
    return Response(ProcessData)

# View data (Reciever)
@csrf_exempt
@api_view(["POST"])
def FileView(request):
    current_user = request.user
    current_user = get_object_or_404(CustomUser, user_id=current_user.id)
    print(current_user.id)
    data = FileManager.objects.filter(file_recepient_id=current_user.id)

    # return Response(FileSerializer(data, many=True).data)
    ProcessData = FileSerializer(data, many=True).data
    # print(ProcessData)
    for i in ProcessData:
        getmail = get_object_or_404(CustomUser, id=i['file_uploader'])
        i["file_uploader"] = getmail.user.email
        # getmail = get_object_or_404(CustomUser, id=i['file_recepient'])
        # print(getmail)
    return Response(ProcessData)
