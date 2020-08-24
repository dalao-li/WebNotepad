import datetime as datetime
import json

from django.shortcuts import render, HttpResponse
from app.models import Note, Log


# Create your views here.

# 主页面

def index_page(request):
    # 获取所有未被删除的文章
    notes = [i for i in Note.objects.exclude(status='D')]
    # 更新记事状态
    for i in notes:
        if i.status != 'F':
            now_status = get_note_status(i.s_time, i.e_time)
            Note.objects.filter(id=i.id).update(status=now_status)

    notes2 = [i for i in Note.objects.filter(status='D')]
    logs = [i for i in Log.objects.all()]
    return render(request, 'index.html', {'note': notes, 'recover_notes': notes2, 'log': logs})


def add_note(request):
    data = json.loads(request.body)
    res = judge_input('add', data)
    # 输入合法
    if res == 1:
        name, text, s_time, e_time, grade = data.values()
        # 获取该记事状态
        now_status = get_note_status(s_time, e_time)
        Note.objects.create(
            name=name, text=text, s_time=s_time, e_time=e_time, grade=grade, status=now_status)
        note = Note.objects.filter(
            name=name, text=text, s_time=s_time, e_time=e_time, grade=grade, status=now_status)[0]
        n_id = note.id
        addLog(n_id, 'A')
    return HttpResponse(json.dumps({'result': res}))


def edit_note(request):
    data = json.loads(request.body)
    res = judge_input('edit', data)
    # 输入合法
    if res == 1:
        n_id, name, text, s_time, e_time, grade = data.values()
        # 获取该记事状态
        now_status = get_note_status(s_time, e_time)
        Note.objects.filter(id=n_id).update(
            name=name, text=text, s_time=s_time, e_time=e_time, grade=grade, status=now_status)
        addLog(n_id, 'E')
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
    addLog(n_id, 'F')
    return HttpResponse(json.dumps({'result': res}))


def del_note(request):
    data = json.loads(request.body)
    n_id = list(data.values())[0]
    res = change_status(n_id, 'D')
    addLog(n_id, 'D')
    return HttpResponse(json.dumps({'result': res}))


# 恢复记事
def recover_note(request):
    data = json.loads(request.body)
    n_id = list(data.values())[0]
    note = Note.objects.filter(id=n_id)[0]
    # 根据进行的时间判断记事的状态
    now_status = get_note_status(note.s_time, note.e_time)
    res = change_status(n_id, now_status)
    addLog(n_id, 'R')
    return HttpResponse(json.dumps({'result': res}))


# 改变记事状态
def change_status(n_id, status):
    Note.objects.filter(id=n_id).update(status=status)
    if Note.objects.filter(id=n_id, status=status).exists():
        return 1
    return -1


# 改变记事优先级
def change_grade(n_id, grade):
    Note.objects.filter(id=n_id).update(grade=grade)
    if Note.objects.filter(id=n_id, grade=grade).exists():
        return 1
    return -1


# 根据时间判断记事状态
def get_note_status(s_time, e_time):
    current_time = datetime.datetime.now()
    # 如果开始与结束时间是str类型,则需进行类型转换
    if type(s_time) == str:
        s_time = change_time_format(s_time)
        e_time = change_time_format(e_time)
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
        name, text, s_time, e_time, grade = data.values()
    elif origin == 'edit':
        id, name, text, s_time, e_time, grade = data.values()
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


# 增加操作日志
def addLog(n_id, operate):
    current_time = datetime.datetime.now()
    Log.objects.create(n_id=n_id, operation=operate, r_time=current_time)
