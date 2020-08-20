import datetime as datetime
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


# 回收站页面
def recover_page(request):
    notes = [i for i in Note.objects.filter(status='D')]
    return render(request, 'recover.html', {'note': notes})


def add_note(request):
    data = json.loads(request.body)
    res = judge_input('add', data)
    if res == 1:
        name, text, s_time, e_time = data.values()
        # 获取该记事状态
        now_status = get_note_status(s_time, e_time)
        Note.objects.create(name=name, text=text, s_time=s_time, e_time=e_time, status=now_status)
    return HttpResponse(json.dumps({'result': res}))


def edit_note(request):
    data = json.loads(request.body)
    res = judge_input('edit', data)
    # 输入合法
    if res == 1:
        n_id, name, text, s_time, e_time = data.values()
        # 获取该记事状态
        now_status = get_note_status(s_time, e_time)
        Note.objects.filter(id=n_id).update(name=name, text=text, s_time=s_time, e_time=e_time, status=now_status)
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


# 恢复记事
def recover_note(request):
    data = json.loads(request.body)
    n_id = list(data.values())[0]
    note = Note.objects.filter(id=n_id)[0]
    # 根据进行的时间判断记事的状态
    now_status = get_note_status(note.s_time, note.e_time)
    res = change_status(n_id, now_status)
    return HttpResponse(json.dumps({'result': res}))


# 改变记事状态
def change_status(n_id, status):
    Note.objects.filter(id=n_id).update(status=status)
    if Note.objects.filter(id=n_id, status=status).exists():
        return 1
    return -1


# 批量更新记事状态
def update_note_status(notes):
    # 获取所有记事
    for i in notes:
        now_status = get_note_status(i.s_time, i.e_time)
        Note.objects.filter(id=i.id).update(status=now_status)


# 判断记事状态
def get_note_status(s_time, e_time):
    current_time = datetime.datetime.now()
    # 如果开始与结束时间是str类型,则需进行类型转换
    if type(s_time) == str:
        e_time = change_time_format(e_time)
        s_time = change_time_format(s_time)
    # 进行中
    if s_time < current_time < e_time:
        return 'U'
    # 超时
    elif current_time > e_time:
        return 'O'
    # 未开始
    elif current_time < s_time:
        return 'P'


# 判断前端输入格式
def judge_input(origin, data):
    global name, text, e_time, s_time
    for i in data.keys():
        if data[i] == '':
            return 0
    if origin == 'add':
        name, text, s_time, e_time = data.values()
    elif origin == 'edit':
        id, name, text, s_time, e_time = data.values()
    if len(name) > 10 or len(text) > 20:
        return -3
    # 时间不合法
    if e_time < s_time:
        return -1
    # 转换结束时间的格式,方便进行比较
    e_time = change_time_format(e_time)
    # 结束时间小于当前时间
    if e_time < datetime.datetime.now():
        return -2
    return 1


# 将str类型的时间格式转换为datetime类型
def change_time_format(time):
    time = time.replace('T', ' ')
    time += ':00'
    return datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
