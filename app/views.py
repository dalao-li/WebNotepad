import datetime as datetime

# from datetime import datetime
import json

from django.shortcuts import render, HttpResponse
from app.models import Note


# Create your views here.

# 主页面
def main_page(request):
    # 获取所有未被删除的文章
    notes = [i for i in Note.objects.exclude(status='D')]
    # 更新记事状态
    update_note_status(notes)
    return render(request, 'main.html', {'note': notes})


def add_note(request):
    data = json.loads(request.body)
    res = judge_input(data)
    if res == 1:
        name, text, s_time, e_time = data.values()
        Note.objects.create(name=name, text=text, s_time=s_time, e_time=e_time, status='U')
    return HttpResponse(json.dumps({'result': res}))


def edit_note(request):
    data = json.loads(request.body)
    res = judge_input(data)
    if res == 1:
        n_id, name, text, s_time, e_time = data.values()
        Note.objects.filter(id=n_id).update(name=name, text=text, s_time=s_time, e_time=e_time)
    return HttpResponse(json.dumps({'result': res}))


# 彻底删除
def ruin_note(request):
    data = json.loads(request.body)
    n_id = list(data.values())[0]
    Note.objects.filter(id=n_id).delete()
    if Note.objects.filter(id=n_id).exists():
        return HttpResponse(json.dumps({'result': -1}))
    return HttpResponse(json.dumps({'result': 1}))


def finish_note(request):
    data = json.loads(request.body)
    n_id = list(data.values())[0]
    res = change_status(n_id, 'F')
    return HttpResponse(json.dumps({'result': res}))


def del_note(request):
    data = json.loads(request.body)
    n_id = list(data.values())[0]
    res = change_status(n_id, 'D')
    return HttpResponse(json.dumps({'result': res}))


# 改变记事状态
def change_status(n_id, status):
    Note.objects.filter(id=n_id).update(status=status)
    if Note.objects.filter(id=n_id, status=status).exists():
        return 1
    return -1


# 判断记事是否超过结束时间
def update_note_status(notes):
    current_time = datetime.datetime.now()
    # 获取所有未删除记事
    for i in notes:
        if current_time > i.e_time:
            Note.objects.filter(id=i.id).update(status='O')


def judge_input(data):
    for i in data.keys():
        if data[i] == '':
            return 0
    name, text, s_time, e_time = data.values()
    if len(name) > 10 or len(text) > 20:
        return -3
    # 时间不合法
    if e_time < s_time:
        return -1
    # 转换结束时间的格式,方便进行比较
    e_time = e_time.replace('T', ' ')
    e_time += ':00'
    # 结束时间小于当前时间
    if datetime.datetime.strptime(e_time, '%Y-%m-%d %H:%M:%S') < datetime.datetime.now():
        return -2
    return 1
