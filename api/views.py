from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAdminUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User,Tasks
from .serializers import AuthSerializer,UserSerializer,TasksSerializer
from django.utils import timezone

class AuthAPIView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        try:
            serializer=AuthSerializer(data=request.data)
            if serializer.is_valid():
                user = authenticate(username=serializer.validated_data.get('phone_number'), password=serializer.validated_data.get('password'))
                if not user:
                    context={
                        "detail":"Invalid Phone number or Password"
                    }
                    return Response(context, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    token, _ = Token.objects.get_or_create(user=user)
                    context={
                        "token":token.key
                    }
                   
                    context.update(UserSerializer(user).data)
                    user.last_login=timezone.now()
                    user.save()
                    return Response(context,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            print (e)
            context={
                "detail":"Something went wrong please try again"
            }
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TasksAPIView(APIView):
    
    def get(self,request,id=None):
        try:
            if id:
                queryset=Tasks.objects.filter(user=request.user,id=id).first()
                serializer=TasksSerializer(queryset)
            else:
                queryset=Tasks.objects.filter(user=request.user)
                serializer=TasksSerializer(queryset,many=True)


            return Response(serializer.data,status=status.HTTP_200_OK)

        
        except Exception as e:
            print (e)
            context={
                "detail":"Something went wrong please try again"
            }
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self,request):
        try:
            serializer=TasksSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data,status=status.HTTP_201_CREATED)

            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print (e)
            context={
                "detail":"Something went wrong please try again"
            }
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self,request,id):
        try:
            queryset=Tasks.objects.filter(user=request.user,id=id).first()
            if not queryset:
                return Response({"detail":"invalid task id"},status=status.HTTP_400_BAD_REQUEST)
            serializer=TasksSerializer(data=request.data,instance=queryset,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)

            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print (e)
            context={
                "detail":"Something went wrong please try again"
            }
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request,id):
        try:
            queryset=Tasks.objects.filter(user=request.user,id=id).first()
            if not queryset:
                return Response({"detail":"invalid task id"},status=status.HTTP_400_BAD_REQUEST)
            
            queryset.delete()
            return Response({"message":"Tasks deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print (e)
            context={
                "detail":"Something went wrong please try again"
            }
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class UserListAPIView(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        try:
            queryset=User.objects.all()
            serializer=UserSerializer(queryset,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            context={
                "detail":"Something went wrong please try again"
            }
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)