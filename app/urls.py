from django.urls import path
from app import views

urlpatterns = [
    # 将函数绑定至对应路由
    path('', views.main_page),

    path('add/',views.add_note),

    path('change/',views.change_note_status)


]

