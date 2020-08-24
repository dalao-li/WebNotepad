from django.urls import path
from app import views

urlpatterns = [
    # 将函数绑定至对应路由
    path('', views.index_page),

    path('add/', views.add_note),

    path('ruin/', views.ruin_note),

    path('del/', views.del_note),

    path('edit/', views.edit_note),

    path('finish/', views.finish_note),

    path('recover/', views.recover_note)

]
