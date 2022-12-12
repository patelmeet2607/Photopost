from django.shortcuts import render
import base64
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser,FileUploadParser
from rest_framework.views import APIView
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import UserMaster,ImageMaster,LikeMaster
from .serializer import ImageSerializer

class UserLogin(APIView):
    def post(self,request):
        if UserMaster.objects.filter(email=request.data["email"],password=request.data["password"]).exists():
            user_detail=UserMaster.objects.filter(email=request.data["email"]).values()[0]
            user_detail["token"] = "adsajfniwerhcawfjo"
            return Response({'data':user_detail})
        return Response({'error':'Invalid username or password'})

class RegisterView(APIView):

    def post(self,request):

        if UserMaster.objects.filter(email=request.data["email"]).exists():

            return Response({'error':'This Email is already registerd'})

        if request.data["password"] != request.data["confirm_password"]:

            return Response({'error':'Password and confirm password does not match'})

        user=UserMaster.objects.create(email=request.data["email"],firstname=request.data["firstname"],lastname=request.data["lastname"],password=request.data["password"])
        userData = UserMaster.objects.filter(email=request.data["email"]).values()[0]

        return Response({'message': 'successfully registered','data':userData})


class UploadView(APIView):

    queryset = ImageMaster.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        file = request.data['image']
        userid_instance=UserMaster.objects.filter(UserID=request.data["user_id"])[0]
        image = ImageMaster.objects.create(image_url=file, UserID=userid_instance)

        return Response({'data': "Uploaded"})

class GetAllImagesView(APIView):

    def post(self, request, *args, **kwargs):
        imageData=ImageMaster.objects.exclude(UserID=request.data["user_id"]).values()
        for x in range(0, len(imageData)):
            imageData[x]["user"] = UserMaster.objects.filter(UserID=imageData[x]["UserID_id"]).values()[0]
            imageData[x]["likes"] = LikeMaster.objects.filter(ImageID=imageData[x]["ImageID"]).values()

        return Response({'data': imageData})

class GetUserImagesView(APIView):

    def post(self, request, *args, **kwargs):
        imageData=ImageMaster.objects.filter(UserID=request.data["user_id"]).values()
        for x in range(0, len(imageData)):
            imageData[x]["likes"] = LikeMaster.objects.filter(ImageID=imageData[x]["ImageID"]).values()

        return Response({'data': imageData})

class LikeView(APIView):

    def post(self, request, *args, **kwargs):
        imageid_instance=ImageMaster.objects.filter(ImageID=request.data["image_id"])[0]
        userid_instance=UserMaster.objects.filter(UserID=request.data["user_id"])[0]
        image = LikeMaster.objects.create(ImageID=imageid_instance, UserID=userid_instance)

        return Response({'data': "liked an image"})
