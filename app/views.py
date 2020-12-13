import json

from django.shortcuts import render, HttpResponse
from app.models import Note, Log
from app.controller import *

# Create your views here.

# 主页面
def index_page(request):
    # 获取所有未被删除的文章
    notes = [i for i in Note.objects.exclude(status='D')]
    # 更新备忘状态
    for i in notes:
        if i.status != 'F':
            # 更新
            now_status = get_status(i.start_time, i.end_time)
            #print(now_status)
            Note.objects.filter(uuid=i.uuid).update(status=now_status)
    recover_notes = [i for i in Note.objects.filter(status='D')]
    logs = [i for i in Log.objects.all()]
    print(notes)
    return render(request, 'index.html', {'notes': notes, 'recover_notes': recover_notes, 'log': logs})

# 添加备忘录
def add_note(request):
    data = json.loads(request.body)
    print(data)
    res = judge_input('add', data)
    # 输入合法
    if res == 1:
        title, text, s_time, e_time, grade = data.values()
        # 获取该备忘状态
        now_status = get_status(s_time, e_time)
        note = Note.objects.create(
            title=title, text=text, start_time=s_time, end_time=e_time, grade=grade, status=now_status)
        #addLog(note.id, 'A')
    return HttpResponse(json.dumps({'result': res}))

# 编辑备忘录
def edit_note(request):
    data = json.loads(request.body)
    res = judge_input('edit', data)
    # 输入合法
    if res == 1:
        n_id, name, text, s_time, e_time, grade = data.values()
        # 获取该备忘状态
        now_status = get_status(s_time, e_time)
        Note.objects.filter(id=n_id).update(
            title=name, text=text, start_time=s_time, end_time=e_time, grade=grade, status=now_status)
        #addLog(n_id, 'E')
    print(res)
    return HttpResponse(json.dumps({'result': res}))


# 彻底删除
def ruin_note(request):
    data = json.loads(request.body)
    n_id = list(data.values())[0]
    Note.objects.filter(id=n_id).delete()
    res = 1
    if Note.objects.filter(id=n_id).exists():
        res = -1
    return HttpResponse(json.dumps({'result': res}))


def ruin_checked_notes(request):
    data = json.loads(request.body)
    note_id_list = list(data.values())[0]
    res = 1
    for i in note_id_list:
        Note.objects.filter(id=i).delete()
        if Note.objects.filter(id=i).exists():
            res = -1
            break
    return HttpResponse(json.dumps({'result': res}))


def finish_note(request):
    data = json.loads(request.body)
    n_id = list(data.values())[0]
    res = change_status(n_id, 'F')
    if res == 1:
        #addLog(n_id, 'F')
        pass
    return HttpResponse(json.dumps({'result': res}))


def del_note(request):
    data = json.loads(request.body)
    n_id = list(data.values())[0]
    res = change_status(n_id, 'D')
    if res == 1:
        #addLog(n_id, 'D')
        pass
    return HttpResponse(json.dumps({'result': res}))


def del_checked_notes(request):
    global res
    data = json.loads(request.body)
    note_id_list = list(data.values())[0]
    for i in note_id_list:
        res = change_status(i, 'D')
        if res == 1:
            #addLog(i, 'D')
            pass
        else:
            break
    return HttpResponse(json.dumps({'result': res}))


# 恢复备忘
def recover_note(request):
    data = json.loads(request.body)
    n_id = list(data.values())[0]
    note = Note.objects.filter(id=n_id)[0]
    # 根据进行的时间判断备忘的状态
    now_status = get_status(note.start_time, note.end_time)
    res = change_status(n_id, now_status)
    if res == 1:
        #addLog(n_id, 'R')
        pass
    return HttpResponse(json.dumps({'result': res}))


# 恢复选中的备忘
def recover_checked_notes(request):
    global res
    data = json.loads(request.body)
    id_list = list(data.values())[0]
    note_list = [i for i in Note.objects.filter(status='D') if i.id in id_list]
    for i in note_list:
        # 根据进行的时间判断备忘的状态
        now_status = get_status(i.start_time, i.end_time)
        res = change_status(i.id, now_status)
        if res == 1:
            # addLog(i.id, 'R')
            pass
        else:
            break
    return HttpResponse(json.dumps({'result': res}))


def ruin_log(request):
    Log.objects.all().delete()
    return HttpResponse(json.dumps({'result': 1}))


# 改变备忘状态
def change_status(n_id, status):
    Note.objects.filter(id=n_id).update(status=status)
    if Note.objects.filter(id=n_id, status=status).exists():
        return 1
    return -1


# 增加操作日志
def addLog(n_id, operate):
    current_time = datetime.datetime.now()
    Log.objects.create(note_id=n_id, operation=operate, record_time=current_time)
