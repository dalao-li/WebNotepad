from django.db import models
import uuid

# Create your models here.

class Note(models.Model):

    """
    进行中 完成 删除 超时 为开始
    """
    choices = (
        ('U', 'Underway'),
        ('F', 'Finish'),
        ('D', 'Deleted'),
        ('O', 'Overtime'),
        ('P', 'Plan')
    )

    """
    备忘的重要性
    """
    rank = (
        ('I','Important'),
        ('C','Common'),
        ('N','Necessary')
    )
    uuid = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=5)
    text = models.TextField(max_length=20)
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    grade = models.CharField(verbose_name='等级',default='C',choices=rank,max_length=1)
    status = models.CharField(verbose_name='状态', default='U', choices=choices, max_length=1)

# 操作日志表
class Log(models.Model):
    choices = (
        ('A', 'Add'),
        ('E', 'Edit'),
        ('D', 'Delete'),
        ('F', 'Finish'),
        ('R', 'Recover')
    )
    uuid = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    note_id = models.CharField(verbose_name='备忘id', max_length=10000)
    operation = models.CharField(verbose_name='操作', choices=choices, max_length=1)
    record_time = models.DateTimeField(verbose_name='记录时间')
