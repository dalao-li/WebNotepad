import datetime
import json

from django.shortcuts import render, HttpResponse
from app.models import Note, Record


# Create your views here.

# 主页面
def main_page(request):
    # TODO
    pass


def record_page(request):
    # TODO
    pass


def del_page(request):
    # TODO
    pass


def add_note(request):
    data = json.loads(request.body)
    name, text, s_time, e_time = data.values()
    Note.objects.create(name=name, s_time=s_time, e_time=e_time, status='U')
    note = Note.objects.filter(name=name, s_time=s_time, e_time=e_time, status='U').last()
    Record.objects.create(n_id=note.id, time=datetime.datetime.now(), status='A')
    return HttpResponse(json.dumps({'result': 1}))


def del_note(request):
    data = json.loads(request.body)
    n_id = list(data.values())[0]
    Note.objects.filter(n_id=n_id).update(status='D')
    Record.objects.create(n_id=n_id, time=datetime.datetime.now(), status='D')
    return HttpResponse(json.dumps({'result': 1}))


def modify_note(request):
    data = json.loads(request.body)
    n_id,name, text, s_time, e_time = data.values()
    Note.objects.filter(n_id=n_id).update(name=name,s_time=s_time,e_time=e_time)
    Record.objects.create(n_id=n_id, time=datetime.datetime.now(), status='M')
    return HttpResponse(json.dumps({'result': 1}))


def ruin_note(request):
    data = json.loads(request.body)
    n_id = list(data.values())[0]
    Note.objects.filter(n_id=n_id).delete()
    Record.objects.create(n_id=n_id, time=datetime.datetime.now(), status='R')
    return HttpResponse(json.dumps({'result': 1}))


def change_note_status(request):
    data = json.loads(request.body)
    n_id, status = data.values()
    Note.objects.filter(n_id=n_id).update(status=status)
    Record.objects.create(n_id=n_id, time=datetime.datetime.now(), status=status)
    return HttpResponse(json.dumps({'result': 1}))
