from .serializers import LoginSerializer,RegisterSerializer,UserProfileSerializer,QuestionSerializer, AnswerSerializer,ChannelSerializer,AddQuestionSerializer,ChannelRestulSerializer, SearchSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .models import UserProfile,Question,Answer,Channel,Tag
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Max

# 登录
@api_view(['POST'])
@csrf_exempt
def login_site(request):
    serializers = LoginSerializer(data=request.data)

    # 先做序列化验证
    if serializers.is_valid():
        username = serializers.initial_data['username']
        password = serializers.initial_data['password']
        remember = serializers.initial_data['remember']

        # 查询用户
        user = authenticate(username=username,password=password)
        if user is not None:
            # 是否需要记住密码
            if remember == 'false':
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
            # 生成token
            token = Token.objects.create(user=user)

            body = {
                'msg':'login is ok',
                'token':token.key,
                'data':serializers.data,
            }
            return Response(body, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

#注册
@api_view(['POST'])
def register_site(request):

    serializers = RegisterSerializer(data=request.data)
    if serializers.is_valid():
        # 取数据
        username = serializers.initial_data['username']
        password = serializers.initial_data['password']
        email = serializers.initial_data['email']

        # 创建user对象
        user = User.objects.create_user(username=username,password=password,email=email)
        # 创建profile对象
        userprofile = UserProfile.objects.create(belong_to=user,nickname=username)

        # 创建token
        token = Token.objects.create(user=user)
        body = {
            'token':token.key,
        }
        print ('token is ',token.key)
        return Response(body, status=status.HTTP_200_OK)

    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# 获取userprofile
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def userprofile(request):

    if request.auth :
        userprofile = request.user.UserProfile
        serializers = UserProfileSerializer(userprofile,many=False)
        return Response(serializers.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

# 获取问题
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def get_question(request):
    # 如果用户通过验证
    if request.auth:
        userprofile = UserProfile.objects.get(belong_to=request.user)
        queryset = Question.objects.filter(publisher=userprofile)
        # 把查询后的结果交给序列化器进行编码，转成json格式
        serializers = QuestionSerializer(queryset,many=True)
        body = {
            'count':queryset.count(),
            'result':serializers.data,
        }
        return Response(body,status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

# 获取回答
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def get_answer(request):
    # 验证用户
    if request.auth:
        # 查询该用户下的锁哟回答
        quseryset = Answer.objects.filter(publisher=request.user.UserProfile)
        # 编码
        serializers = AnswerSerializer(quseryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


# home-获取频道列表
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def get_channel(request):
    print (request.auth,request.user)
    if request.auth :
        all_channel = Channel.objects.all()
        serializers = ChannelSerializer(all_channel,many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

# home-获取频道下的对应回答内容
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def get_channel_answers(request,id,qid):

    # 转格式
    qid = int(qid)

    if request.auth:
        # 查询数据
        channel = Channel.objects.get(id=id)
        # 查询频道下的所有问题
        result_questions = []
        questions = list(channel.questions.all().order_by('-created_date'))
        # 通过查看ID来判断是属于首次请求，还是加载下一页
        if qid != 1:
            # 说明是在请求加载下一页
            # 找到对应ID的question，并且构造一个新的数组，数组的第一位就是这个ID所代表的question
            for question in questions:
                if question.id == qid:
                    index = questions.index(question)
                    result_questions = questions[index+1 : ]
        else:
            # 说明是第一次请求
            result_questions = questions

        queryset = []
        for question in result_questions:
        # 构建answer类型的数据
            if question.answers.count() > 0:
                answer_list = sorted(question.answers.all(), key=lambda x : x.vote_count, reverse=True)
                item = {
                    'code':1,
                    'answer':{
                        'question_title':answer_list[0].belong_to.title,
                        'avatar':answer_list[0].publisher.avatar.url,
                        'nickname':answer_list[0].publisher.nickname,
                        'signature':answer_list[0].publisher.signature,
                        'vote_count':answer_list[0].vote_count,
                        'content':answer_list[0].content,
                        },
                    'q_id' : question.id,
                }
                queryset.append(item)
            else:
                # 构建question类型的数据
                item = {
                        'code' : 2,
                        'question' : {
                            'title':question.title,
                            'nickname' : question.publisher.nickname,
                            'avatar' : question.publisher.avatar.url,
                            'signature' : question.publisher.signature,
                            },
                        'q_id' : question.id,
                }
                queryset.append(item)

        # 构造分页器
        page_robot = Paginator(queryset,3)
        page_data = page_robot.page(1)
        # 判断还有没有下一页
        if page_data.has_next():
            has_next = 1
        else :
            has_next = 0

        # 对数据进行json编码
        serializers = ChannelRestulSerializer(page_data,many=True)
        body = {
            'data':serializers.data,
            'has_next':has_next,
                }
        return Response(body, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

# home-Post New Question
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def post_new_question(request):

    if request.auth :
        # 取数据
        serializers = AddQuestionSerializer(data=request.data)
        if serializers.is_valid():
            title = serializers.initial_data['title']
            info = serializers.initial_data['info']
            channel_name = serializers.initial_data['channel_name']
            # 处理tags
            tags = serializers.initial_data['tags']
            new_tags = tags.split(' ')
            # 创建tag对象
            tag_ob = []
            for item in new_tags:
                tag = Tag.objects.create(name = item)
                tag_ob.append(tag)

            # 根据channel_name查询channel对象
            channel = Channel.objects.get(name=channel_name)
            # 发起请求的UserProfile
            userprofile = request.user.UserProfile
            # 创建question对象
            question = Question.objects.create(title=title, info=info, channel=channel, publisher=userprofile)
            question.tags = tag_ob
            question.save()
            # 返回所创建的question对象
            item = {
                'code':2,
                'question' : {
                    'title' : question.title,
                    'nickname' : question.publisher.nickname,
                    'avatar' : question.publisher.avatar.url,
                    'signature' : question.publisher.signature,
                },
                'q_id' : question.id,
            }
            # json 编码
            result_serializer = ChannelRestulSerializer(data=item)
            if result_serializer.is_valid():
                return Response(result_serializer.data, status=status.HTTP_200_OK)
            else:
                body = {
                    'msg':'添加question的时候出现序列化错误',
                    'error':result_serializer.errors,
                }
                return Response(body, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


# search接口
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def search(request,search_text,page_num):
    if request.auth :
        # 获取数据
        print ('search_text is ',search_text)
        # 查询所有符合标准的question
        questions = Question.objects.filter(title__icontains=search_text)
        all_answer = []
        if questions.count()>0:
            for question in questions:
                if question.answers.count() > 0:
                    all_answer_list = list(sorted(question.answers.all(),key=lambda x:x.vote_count,reverse=True))
                    max_vote_count_answer = all_answer_list[0]
                    all_answer.append(max_vote_count_answer)

            # 判断有没有回答数据,对查询集进行编码，返回200 OK
            if len(all_answer) > 0:
                # 构造分页器，处理分页
                page_robot = Paginator(all_answer,2)
                # 判断页码是否有效
                try:
                    page_data = page_robot.page(page_num)
                except EmptyPage:
                    body = {
                        'msg':'EmptyPage',
                    }
                    return Response(body, status=status.HTTP_404_NOT_FOUND)

                # 判断还有没有下一页
                if page_data.has_next():
                    has_next = 1
                else:
                    has_next = 0

                answerserializer = AnswerSerializer(page_data, many=True)
                body = {
                    'has_next':has_next,
                    'data':answerserializer.data,
                }
                return Response(body,status=status.HTTP_200_OK)
            else:
                body = {
                    'code':1,
                    'msg':'没有找到合适的回答',
                }
                return Response(body, status=status.HTTP_400_BAD_REQUEST)
        else:
            body = {
                'code':2,
                'msg':'没有找到相关的问题',
            }
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
