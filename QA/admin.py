from django.contrib import admin
from .models import UserProfile,Question,Answer,Channel,Tag,Comment,Ticket

# 管理器
class  QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','title','publisher','channel','created_date')
    list_per_page = 20

class  UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','nickname','belong_to','signature',)
    list_per_page = 20

class  AnswerAdmin(admin.ModelAdmin):
    list_display = ('id','publisher','belong_to','vote_count','created_date')
    list_per_page = 20

class  ChannelAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_per_page = 20

class  TagAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_per_page = 20

class  CommentAdmin(admin.ModelAdmin):
    list_display = ('id','belong_to_userprofile','content','created_date')
    list_per_page = 20

class  TicketAdmin(admin.ModelAdmin):
    list_display = ('id','belong_to_userprofile','choose','created_date')
    list_per_page = 20

# Register your models here.
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(Channel,ChannelAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Ticket,TicketAdmin)
