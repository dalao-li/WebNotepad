import datetime


# 根据时间判断备忘状态
def get_status(s_time, e_time):
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
        id, name, text, start_time, e_time, grade = data.values()
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



