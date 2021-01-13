function sendAjax(param, url, callback) {
    $.ajax({
        async: false,
        ache: false,
        type: 'POST',
        url: url,
        //JSON对象转化JSON字符串
        data: JSON.stringify(param),
        //服务器返回的数据类型
        dataType: "json",
        success: function (data) {
            //console.log(data)
            callback(data.result)
        },
        error: function () {
            //错误处理
        }
    })
}


//根据表格生成表格的字典形式
function getNoteDict(formName) {
    const data = {}
    const t = $('#' + formName).serializeArray()
    $.each(t, function () {
        data[this.name] = this.value
    })
    return data
}

//选择与取消选择checkbox
function checkAndCancel(checkboxName) {
    $("input[name='" + checkboxName + "']").each(function () {
        if ($(this).attr("checked")) {
            $(this).removeAttr("checked")
        } else {
            $(this).attr("checked", true)
        }
    })
}

//获取被选中备忘的id
function getCheckedList(checkboxName) {
    const checkList = [];
    $("input[name='" + checkboxName + "']:checkbox:checked").each(function () {
        const checkboxId = this.id
        //根据控件id分离出备忘的id
        const id = checkboxId.split("-")[1]
        //将id转化为int形
        checkList.push(Number(id))
    })
    return checkList
}

function disCallPage(operate, value) {
    const success = {
        "add": "添加成功",
        "edit": "修改成功",
        "finish": "备忘已完成",
        "recover": "选择的备忘已恢复",
        "del": "选择的备忘删除成功",
        "ruin": "选择的备忘彻底删除成功",
        "ruinLog": "记录已经清空"
    }
    const failure = {
        "add": "添加失败",
        "edit": "修改失败",
        "finish": "选择的备忘未完成",
        "recover": "选择的备忘恢复失败",
        "del": "选择的备忘删除失败",
        "ruin": "选择的备忘未彻底删除",
        "ruinLog": "记录未清空"
    }
    if (value === 1) {
        swal({
            title: success[operate], text: "一秒后自动刷新", type: "success", timer: 1500
        }, () => {
            location.reload()
        })
    }
    if (value === -1) {
        swal({
            title: failure[operate], text: "请重试", type: "error"
        })
    }
}

//输入数据合法性判断
function judgeInput(d) {
    if (d['title'] === "" || d['text'] === "") {
        return "-1"
    }
    if (d['startTime'] === "" || d['endTime'] === "") {
        return "-2"
    }
    const currentTime = new Date()
    //结束时间应该大于开始时间
    if (d['startTime'] >= d['endTime']) {
        return "-3"
    }
    return "1"
}

function addNote() {
    const data = {}
    const t = $('#addNoteForm').serializeArray()
    $.each(t, function () {
        data[this.name] = this.value
    })
    const v = judgeInput(data)
    if (v !== "1") {
        const error = {
            "-1": "标题或内容不能为空",
            "-2": "时间不能为空",
            "-3": "开始时间必须大于结束时间",
            "-4": "结束时间必须大于当前时间",
            "-5": "填写内容不能超过指定长度"
        }
        swal(error[v], "请重写填写", "error")
        return
    }
    sendAjax(data, '/app/add/', (value) => {
        if (value === 1) {
            swal({
                title: "添加成功", text: "一秒后自动刷新", type: "success", timer: 1500
            }, () => {
                location.reload()
            })
        }
    })
}


//operate： add , edit
function redactNote(operate, data) {
    sendAjax(data, '/app/' + operate + '/', (value) => {
        if (value === 1) {
            disCallPage(operate, value)
        } else {
            const error = {
                "0": "填写内容不能为空",
                "-1": "开始时间必须大于结束时间",
                "-2": "结束时间必须大于当前时间",
                "-3": "填写内容不能超过指定长度"
            }
            swal(error[value.toString()], "请重写填写", "error")
        }
    })
}

//operate: finish ,del , recover
function changeNote(operate, id) {
    const data = {'id': id}
    sendAjax(data, '/app/' + operate + '/', (value) => {
        disCallPage(operate, value)
    })
}


function redactCheckedNotes(operate) {
    const warn = {
        'del': "请选择需要删除的备忘",
        'recover': "请选择需要恢复的备忘",
        'ruin': "请选择需要彻底删除的备忘"
    }
    const boxName = {
        'del': 'delCheckbox',
        'recover': 'recoverCheckbox',
        'ruin': 'recoverCheckbox'
    }
    var checkList = getCheckedList(boxName[operate])
    if (checkList.length === 0) {
        swal(warn[operate], "请重试", "warning")
        return
    }
    let data = {'ids': checkList}
    if (operate === 'ruin') {
        swal({
                title: "确定要彻底删除选中的" + checkList.length + "件备忘吗？", text: "删除不可恢复", type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "确认",
                cancelButtonText: "取消",
                closeOnConfirm: false,
                closeOnCancel: false
            }, function (isConfirm) {
                if (!isConfirm) {
                    swal({title: "已取消", text: "您取消了删除操作！", type: "warning"})
                    return
                }
                sendAjax(data, '/app/' + operate + '/checked/', (value) => {
                    disCallPage(operate, value)
                })
            }
        )
    } else {
        sendAjax(data, '/app/' + operate + '/checked/', (value) => {
            disCallPage(operate, value)
        })
    }
}


//彻底删除
function ruinNote(id) {
    swal({
            title: "确定要删除该备忘吗？", text: "删除不可恢复", type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "确认",
            cancelButtonText: "取消",
            closeOnConfirm: false,
            closeOnCancel: false
        }, function (isConfirm) {
            if (!isConfirm) {
                swal({title: "已取消", text: "您取消了删除操作！", type: "warning"})
                return
            }
            const data = {'id': id}
            sendAjax(data, '/app/ruin/', (value) => {
                disCallPage('del', value)
            })
        }
    )
}


function ruinLog() {
    const data = {'id': 1}
    sendAjax(data, '/app/ruin/log', (value) => {
        disCallPage('ruinLog', value)
    })
}


