from django.shortcuts import render
from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


# Create your views here.


# doing manual serialization

# def studentsView(request):
#     students = Student.objects.all()
#     student_list = list(students.values())
#     return JsonResponse(student_list, safe = False)

# automatic serialization from drf

@api_view(['GET', 'POST'])
def studentsView(request):
    if request.method == 'GET':
        #get all the data from the students table
        student = Student.objects.all()
        serializer = StudentSerializer(student, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)   
    
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
def studentDetailView(resquest, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if resquest.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif resquest.method == 'PUT':
        serializer = StudentSerializer(student, data=resquest.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        