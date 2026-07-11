from rest_framework.serializers import ModelSerializer
from base.models import Room, User, Topic, Resource, Message


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'bio', 'department', 'role', 'student_id', 'github_link', 'linkedin_link']


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class ResourceSerializer(ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

