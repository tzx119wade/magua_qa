from django.conf.urls import url
from .views import proflie, login,home
from .api import login_site, register_site, userprofile,get_question,get_answer,get_channel,get_channel_answers, post_new_question
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^profile/',proflie,name='proflie'),
    url(r'^login/', login, name='login'),
    url(r'^home/', home, name='home'),



    # api
    url(r'^api/login', login_site),
    url(r'^api/register', register_site),
    url(r'^api/userprofile', userprofile),
    url(r'^api/question', get_question),
    url(r'^api/answer', get_answer),
    url(r'^api/channel$',get_channel),
    url(r'^api/channel/(?P<id>\d+)/(?P<page>\d+)',get_channel_answers),
    url(r'^api/addquestion',post_new_question),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
