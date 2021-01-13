from django.urls import path
from app import views

urlpatterns = [
    # 将函数绑定至对应路由
    path('', views.index_page),

    path('add/', views.add_note),

    path('ruin/', views.ruin_note),

    path('ruin/checked/', views.ruin_checked_notes),

    path('ruin/log/', views.ruin_log),

    path('del/', views.del_note),

    path('del/checked/', views.del_checked_notes),

    path('edit/', views.edit_note),

    path('finish/', views.finish_note),

    path('recover/', views.recover_note),

    path('recover/checked/', views.recover_checked_notes)

]
