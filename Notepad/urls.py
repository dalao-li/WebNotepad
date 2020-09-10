from django.urls import path, include
from django.views import static
from django.conf import settings
from django.conf.urls import url
from app import views

urlpatterns = [
    path('app/', include('app.urls')),
    path('', views.index_page),
    
    # 部署时访问静态文件
    url(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'),
]
