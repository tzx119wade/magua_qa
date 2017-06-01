from django.conf.urls import url
from .views import proflie, login,home,search_view,detail_view
from .api import login_site, register_site, userprofile,get_question,get_answer,get_channel,get_channel_answers, post_new_question,search,detail_answers,vote
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^profile/',proflie,name='proflie'),
    url(r'^login/', login, name='login'),
    url(r'^home/', home, name='home'),
    url(r'^search', search_view, name='search_view'),
    url(r'^detail', detail_view, name='detail_view'),



    # api
    url(r'^api/login', login_site),
    url(r'^api/register', register_site),
    url(r'^api/userprofile', userprofile),
    url(r'^api/question$', get_question),
    url(r'^api/question/(?P<id>\d+)',get_question),
    url(r'^api/answer$', get_answer),
    url(r'^api/answer/(?P<qid>\d+)', detail_answers),
    url(r'^api/channel$',get_channel),
    url(r'^api/channel/(?P<id>\d+)/(?P<qid>\d+)',get_channel_answers),
    url(r'^api/addquestion',post_new_question),
    url(r'^api/search/(?P<search_text>\S+)/(?P<page_num>\d+)',search),
    url(r'^api/vote',vote),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
