from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Tasks, Tags
from rest_framework.views import APIView
from .serializers import TasksSerializer, TagSerializer
from django.db.models import Q

"""
@api_view(['GET', 'POST'])
def tasksView(request):
    if request.method == 'GET':
        data = Tasks.objects.all()
        tag = request.GET.get('tag')

        if tag:
            tasks = Tasks.objects.filter(tags__name=tag)
        else:
            tasks = Tasks.objects.all()

        serializer = TasksSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TasksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PATCH', 'DELETE'])
def tasksViewDetailed(request, pk):
    try:
        task = Tasks.objects.get(id=pk)
    except Tasks.DoesNotExist:
        return Response({'error': 'Todo not found'}, status=404)
    
    if request.method == 'GET':
        serializer = TasksSerializer(task)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = TasksSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def tagsView(request):
    if request.method == 'GET':
        tags = Tags.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
"""


# -----------------------------
# TODOS LIST + CREATE
# -----------------------------
@api_view(['GET', 'POST'])
def tasksView(request):

    # GET → Alle Tasks oder gefiltert nach Tag
    if request.method == 'GET':
        """
        # Query Parameter holen: /api/todos/?tag=work
        tag = request.GET.get('tag')

        tasks = Tasks.objects.all()
        
        if tag:
            # Filter: Tasks, die ein Tag mit diesem Namen haben
            tasks = Tasks.objects.filter(tags__name=tag).distinct()
        
        
        if tag: 
            for tag in tag:
                tasks = tasks.filter(tags__name=tag)

        tasks = tasks.distinct()
        """

        tags = request.GET.getlist('tags')

        tasks = Tasks.objects.all()

        if tags:
            query = Q()
            for tag in tags:
                query |= Q(tags__name__iexact=tag)
            tasks = tasks.filter(query)

        tasks = tasks.distinct()

        serializer = TasksSerializer(tasks, many=True)
        return Response(serializer.data)

    # POST → neuen Task erstellen
    elif request.method == 'POST':
        serializer = TasksSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# -----------------------------
# TODO DETAIL (GET, UPDATE, DELETE)
# -----------------------------
@api_view(['GET', 'PATCH', 'DELETE'])
def tasksViewDetailed(request, pk):

    try:
        task = Tasks.objects.get(id=pk)
    except Tasks.DoesNotExist:
        return Response({'error': 'Todo not found'}, status=404)

    # GET → einzelner Task
    if request.method == 'GET':
        serializer = TasksSerializer(task)
        return Response(serializer.data)

    # PATCH → teilweise updaten
    elif request.method == 'PATCH':
        serializer = TasksSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # DELETE → löschen
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=204)


# -----------------------------
# TAGS LIST + CREATE
# -----------------------------
@api_view(['GET', 'POST'])
def tagsView(request):

    # GET → alle Tags
    if request.method == 'GET':
        tags = Tags.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    # POST → neuen Tag erstellen
    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# -----------------------------
# TAG DELETE
# -----------------------------
@api_view(['GET', 'DELETE'])
def tagDetailView(request, pk):
    try:
        tag = Tags.objects.get(id=pk)
    except Tags.DoesNotExist:
        return Response({'error': 'Tag not found'}, status=404)

    # GET → Tag anzeigen
    if request.method == 'GET':
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    # DELETE → Tag löschen
    elif request.method == 'DELETE':
        tag.delete()
        return Response(status=204)

