from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.shortcuts import get_object_or_404
from .models import Classroom
from .serializers import ClassroomSerializer

class ClassroomListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        # If you want to filter by user (if Classroom has a user relation)
        # classrooms = request.user.classrooms.all()
        
        # If classrooms aren't user-specific, get all
        classrooms = Classroom.objects.all()
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ClassroomSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            # If you want to associate with user
            # serializer.save(user=request.user)
            
            # If no user association needed
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#class ClassroomCreateView(APIView):
    #permission_classes = [AllowAny]  # Permite acceso público
    #authentication_classes = []  # ⚠️ Desactiva JWT para esta vista

    #def post(self, request, format=None):
        #serializer = ClassroomSerializer(data=request.data)
        #if serializer.is_valid():
         #   serializer.save()
          #  return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassroomDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        # If you want to filter by user
        # return get_object_or_404(Classroom, pk=pk, user=self.request.user)
        
        # If no user filter needed
        return get_object_or_404(Classroom, pk=pk)
    
    def get(self, request, pk, format=None):
        classroom = self.get_object(pk)
        serializer = ClassroomSerializer(classroom)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        classroom = self.get_object(pk)
        serializer = ClassroomSerializer(classroom, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        classroom = self.get_object(pk)
        classroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)