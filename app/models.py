from django.db import models


# Create your models here.

class Note(models.Model):
    choices = (
        ('U', 'Underway'),
        ('F', 'Finish'),
        ('D', 'Deleted')
    )

    name = models.CharField(verbose_name='标题', help_text='请输入记事标题', max_length=5)
    text = models.TextField(verbose_name='内容', help_text='请输入记事内容', max_length=20)
    s_time = models.DateTimeField(verbose_name='开始时间', help_text='请选择开始时间')
    e_time = models.DateTimeField(verbose_name='结束时间', help_text='请选择结束时间')
    status = models.CharField(verbose_name='状态', help_text='请选择状态', default='U', choices=choices, max_length=1)


