from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Tasks
from rest_framework.views import APIView
from .serializers import TasksSerializer

@api_view(['GET', 'POST'])
def tasksView(request):
    if request.method == 'GET':
        data = Tasks.objects.all()
        serializer = TasksSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TasksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def tasksViewDetailed(request, pk):
    try:
        task = Tasks.objects.get(id=pk)
    except Tasks.DoesNotExist:
        return Response({'error': 'Todo not found'}, status=404)
    
    if request.method == 'GET':
        serializer = TasksSerializer(task)
        return Response(serializer.data)
    
    elif request.method in ['PATCH', 'PUT']:
        serializer = TasksSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=204)


