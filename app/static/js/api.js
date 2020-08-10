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
        success: function (data)  {
            callback(data.result)
        },
        error: function ()  {
            //错误处理
        }
    })
}

function addNote(data) {
    for (var k in data) {
        if (data.hasOwnProperty(k) && data[k] === "") {
            swal("填写内容不能为空", "请重写填写", "error")
            return
        }
    }
    sendAjax(data, '/app/add/', (value) => {
        if (value === 1) {
            swal({title: "添加成功", text: "", type: "success", timer: 2000}, () => {
                location.href = '/app/'
            })
        }
        if (value === 0) {
            swal("填写内容不能为空", "请重写填写", "error")
        }
    })
}


function delNote(n_id) {
    swal({
            title: "确定要删除该记事吗？", text: "删除不可恢复", type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "确认", cancelButtonText: "取消",
            closeOnConfirm: false,
            closeOnCancel: false
        },
        (isConfirm) => {
            if (!isConfirm) {
                swal({title: "已取消", text: "您取消了删除操作！", type: "warning"})
                return
            }
            var data = {'id': n_id}
            sendAjax(data, '/app/del/', (value) => {
                if (value === 1) {
                    swal({title: "删除成功", text: "", type: "success", timer: 2000}, () => {
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


function finishNote(n_id) {
    var data = {
        'n_id': n_id,
        'status': 'F'
    }
    sendAjax(data, '/app/change/', (value) => {
        if (value === 1) {
            swal({title: "记事已完成", text: "", type: "success", timer: 2000}, () => {
                location.reload()
            })
        }
        if (value === -1) {
            swal("网络异常", "请重试", "error")
        }
    })
}


function modifyNote(data) {
     for (var k in data) {
        if (data.hasOwnProperty(k) && data[k] === "") {
            swal("填写内容不能为空", "请重写填写", "error")
            return
        }
    }
    sendAjax(data, '/app/modify/', (value) => {
        if (value === 1) {
            swal({title: "修改成功", text: "", type: "success", timer: 2000}, () => {
                location.href = '/app/'
            })
        }
        if (value === 0) {
            swal("填写内容不能为空", "请重写填写", "error")
        }
    })
}


