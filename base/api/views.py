from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room, Resource
from .serializers import RoomSerializer, ResourceSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/rooms/:id/resources'
    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    dept = request.GET.get('dept')
    course = request.GET.get('course')
    rooms = Room.objects.all()
    if dept:
        rooms = rooms.filter(host__department__icontains=dept)
    if course:
        rooms = rooms.filter(course_code__icontains=course)
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getRoomResources(request, pk):
    resources = Resource.objects.filter(room__id=pk)
    serializer = ResourceSerializer(resources, many=True)
    return Response(serializer.data)

