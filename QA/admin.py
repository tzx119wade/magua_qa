from django.contrib import admin
from .models import UserProfile,Question,Answer,Channel,Tag

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Channel)
admin.site.register(Tag)
