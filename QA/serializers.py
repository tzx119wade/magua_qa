from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile,Question,Answer,Channel,Ticket,Comment

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20,min_length=6)
    password = serializers.CharField(max_length=20,min_length=6)
    remember = serializers.CharField()

# 注册的序列化器
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20,min_length=6)
    password = serializers.CharField(max_length=20,min_length=6)
    email = serializers.EmailField()

# UserProfile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

# question序列化器
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        depth = 1

# answer序列化器
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        depth = 1

# Channel
class ChannelSerializer(serializers.ModelSerializer):
    class Meta :
        model = Channel
        fields = "__all__"

# add-question
class AddQuestionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=300,min_length=10)
    info = serializers.CharField(max_length=1000,min_length=10)
    channel_name = serializers.CharField(max_length=100,min_length=2)
    tags = serializers.CharField(max_length=100)

# question & answer
class ChannelRestulSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    answer = serializers.DictField(required=False)
    question = serializers.DictField(required=False)
    q_id = serializers.IntegerField()

# search
class SearchSerializer(serializers.Serializer):
    search_text = serializers.CharField(max_length=100)

# detail answers
class DetailAnswerSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=50)
    signature = serializers.CharField(max_length=50)
    avatar = serializers.CharField(max_length=300)
    voters_count = serializers.IntegerField()
    voters = serializers.ListField(required=False)
    content = serializers.CharField()
    created_date = serializers.DateTimeField(format='%m-%d-%Y %H:%M:%S')
    comments_count = serializers.IntegerField()
    answer_id = serializers.IntegerField()
    choose = serializers.CharField(max_length=10)
    comment_show = serializers.IntegerField()
    comments = serializers.ListField()

# ticket
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        depth = 1

# comment
class CommentSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%m-%d-%Y %H:%M:%S')
    class Meta:
        model = Comment
        fields = "__all__"
        depth = 2
