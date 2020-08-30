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
            callback(data.result)
        },
        error: function () {
            //错误处理
        }
    })
}

function redactNote(operator, data) {
    const titDict = {
        "add": "添加成功",
        "edit": "修改成功"
    }
    sendAjax(data, '/app/' + operator + '/', (value) => {
        if (value === 1) {
            swal({
                title: titDict[operator], text: "", type: "success", timer: 1000
            }, function () {
                location.reload()
            })
            return
        }
        const error = {
            "0": "填写内容不能为空",
            "-1": "开始时间必须大于结束时间",
            "-2": "结束时间必须大于当前时间",
            "-3": "填写内容不能超过指定长度"
        }
        swal(error[value.toString()], "请重写填写", "error")
    })

}

function delNote(id) {
    const data = {'id': id}
    sendAjax(data, '/app/del/', (value) => {
        if (value === 1) {
            swal({
                title: "删除成功", text: "", type: "success", timer: 1000
            }, () => {
                location.reload()
            })
        }
        if (value === -1) {
            swal("删除失败", "请重试", "error")
        }
    })
}

//获取被选中记事的id
function getCheckedList(checkboxName) {
    var checkList = []
    $("input[name='" + checkboxName + "']:checkbox:checked").each(function () {
        //由于复选框一般选中的是多个,所以可以循环输出
        var checkboxId = this.id
        //根据控件id分离出记事的id
        var id = checkboxId.split("-")[1]
        //将id转化为int形
        checkList.push(Number(id))
    })
    return checkList
}

function delCheckedNotes() {
    var checkList = getCheckedList('delCheckbox')
    if (checkList.length === 0) {
        swal("请选择需要删除的记事", "请重试", "warning")
        return
    }
    data = {'ids': checkList}
    sendAjax(data, '/app/del/checked/', (value) => {
        if (value === 1) {
            swal({
                title: "删除成功", text: "", type: "success", timer: 1000
            }, () => {
                location.reload()
            })
        }
        if (value === -1) {
            swal("删除失败", "请重试", "error")
        }
    })
}

//彻底删除
function ruinNote(id) {
    swal({
            title: "确定要删除该记事吗？", text: "删除不可恢复", type: "warning",
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
            const data = {'id': id,}
            sendAjax(data, '/app/ruin/', (value) => {
                if (value === 1) {
                    swal({
                        title: "删除成功", text: "", type: "success", timer: 1000
                    }, () => {
                        location.reload()
                    })
                }
                if (value === -1) {
                    swal("删除失败", "请重试", "error")
                }
            })
        }
    )
}

function ruinCheckedNotes() {
    var checkList = getCheckedList('ruinCheckbox')
    if (checkList.length === 0) {
        swal("请选择需要删除的记事", "请重试", "warning")
        return
    }
    swal({
            title: "确定要删除选中的" + len + "件记事吗？", text: "删除不可恢复", type: "warning",
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
            const data = {'ids': checkList}
            sendAjax(data, '/app/ruin/checked', (value) => {
                if (value === 1) {
                    swal({
                        title: "选中的记事已删除", text: "", type: "success", timer: 1000
                    }, () => {
                        location.reload()
                    })
                }
                if (value === -1) {
                    swal("删除失败", "请重试", "error")
                }
            })
        }
    )
}

function finishNote(id) {
    const data = {'id': id}
    sendAjax(data, '/app/finish/', (value) => {
        if (value === 1) {
            swal({
                title: "记事已完成", text: "", type: "success", timer: 1000
            }, () => {
                location.reload()
            })
        }
        if (value === -1) {
            swal("网络异常", "请重试", "error")
        }
    })
}


function recoverNote(id) {
    const data = {'id': id}
    sendAjax(data, '/app/recover/', (value) => {
        if (value === 1) {
            swal({
                title: "记事已恢复", text: "", type: "success", timer: 1000
            }, () => {
                location.reload()
            })
        }
        if (value === -1) {
            swal("网络异常", "请重试", "error")
        }
    })
}

function recoverCheckedNotes() {
    var checkList = []
    $("input[name='ruinCheckbox']:checkbox:checked").each(function () {
        //根据控件id分离出记事的id
        var id = this.id.split("-")[1]
        checkList.push(Number(id))
    })
    if (checkList.length === 0) {
        swal("请选择需要恢复的记事", "请重试", "warning")
        return
    }
    data = {'ids': checkList}
    sendAjax(data, '/app/recover/checked/', (value) => {
        if (value === 1) {
            swal({
                title: "选中的记事已全部恢复", text: "", type: "success", timer: 1000
            }, () => {
                location.reload()
            })
        }
        if (value === -1) {
            swal("网络异常", "请重试", "error")
        }
    })
}


