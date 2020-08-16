from django.db import models


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

    name = models.CharField(verbose_name='标题', max_length=5)
    text = models.TextField(verbose_name='内容', max_length=20)
    s_time = models.DateTimeField(verbose_name='开始时间')
    e_time = models.DateTimeField(verbose_name='结束时间')
    status = models.CharField(verbose_name='状态', default='U', choices=choices, max_length=1)
