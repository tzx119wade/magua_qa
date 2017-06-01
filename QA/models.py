from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 用户资料
class UserProfile(models.Model):
    # 头像
    avatar = models.ImageField('头像',upload_to='avatar_image',default='avatar_image/ironmen.png')
    belong_to = models.OneToOneField(to=User,related_name='UserProfile',verbose_name='属于')
    # 昵称
    nickname = models.CharField('昵称',max_length=100, blank=True, null=True)
    # 个性签名
    signature = models.CharField('个性签名',max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nickname

# 频道
class Channel(models.Model):
    name = models.CharField('频道',blank=True,null=True,max_length=100,unique=True)
    icon = models.ImageField('图标',upload_to='avatar_image',blank=True,null=True)

    def __str__(self):
        return self.name

# 标签tag
class Tag(models.Model):
    name = models.CharField('标签名',blank=True, null=True,max_length=100,unique=True)

    def __str__(self):
        return self.name

# question
class Question(models.Model):

    title = models.CharField('标题',max_length=400, blank=True, null=True)
    info = models.TextField('问题说明', blank=True, null=True)
    publisher = models.ForeignKey(to=UserProfile, related_name='questions', verbose_name='发布问题的人')
    created_date = models.DateTimeField('发布时间',default=timezone.now)

    # 扩展
    pv_count = models.IntegerField(blank=True,null=True)
    channel = models.ForeignKey(to=Channel,related_name='questions',verbose_name='频道',blank=True,null=True)
    # tags
    tags = models.ManyToManyField(Tag,related_name='questions')

    def __str__(self):
        return self.title

# answer
class Answer(models.Model):
    # 所关联的question
    belong_to = models.ForeignKey(to=Question, related_name='answers',verbose_name='所关联的问题')
    # 撰写问题的人
    publisher = models.ForeignKey(to=UserProfile, related_name='answers', verbose_name='撰写回答的人')
    # 赞同数
    vote_count = models.IntegerField('赞同数',blank=True,null=True)
    # 发布时间
    created_date = models.DateTimeField('发布时间',default=timezone.now)
    # 回答内容
    content = models.TextField('回答内容',blank=True, null=True)

    def __str__(self):
        return self.content[:10]

# tickets
class Ticket(models.Model):
    VOTE_CHOICES = (
        ('like','like'),
        ('unlike','unlike'),
        ('none','none'),
    )
    # choose
    choose = models.CharField(max_length=10, choices=VOTE_CHOICES, blank=True, null=True)
    # belong_to_answer
    belong_to_answer = models.ForeignKey(to=Answer, related_name='tickets')
    # belong_to_userprofile
    belong_to_userprofile = models.ForeignKey(to=UserProfile, related_name='tickets')
    # created_date
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.belong_to_userprofile.nickname
# comment
class Comment(models.Model):
    # content
    content = models.CharField(max_length=500,blank=True,null=True)
    belong_to_userprofile = models.ForeignKey(to=UserProfile, related_name='comments')
    belong_to_answer = models.ForeignKey(to=Answer, related_name='comments',blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    # reply
    reply_to = models.OneToOneField('self',blank=True,null=True)

    def __str__(self):
        return self.belong_to_userprofile.nickname + ':' + self.content[0:20]
