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
        error: function (data) {
            //错误处理
        }
    })
}

function addRecord() {
    var d = {}
    var t = $('#recordForm').serializeArray()
    //表单是否存在空值
    var isNull = false
    $.each(t, function () {
        if (this.value === "") {
            isNull = true
            addCallback(0)
            // return false才代表退出each()函数
            return false
        }
        d[this.name] = this.value
    })
    //若存在空值则不发送ajax
    if (isNull) {
        return
    }
    sendAjax(d, '/app/add/', addCallback)
}

function addCallback(value) {
    if (value === 1) {
        swal({
            title: "提交成功",
            text: "",
            type: "success",
            timer: 2000
        }, function () {
            location.href = '/app/'
        })
    }
    if (value === 0) {
        swal("填写内容不能为空", "请重写填写", "error")
    }
    if (value === -1) {
        swal({
            title: "该学生体温已提交",
            text: "请勿重复提交",
            type: "warning"
        }, function () {
            $('#recordForm')[0].reset()
        })
    }
}

function delRecord(num) {
    swal({
            title: "确定要删除该记录吗",
            text: "删除后将无法恢复，请谨慎操作！",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "确认",
            cancelButtonText: "取消",
            closeOnConfirm: false,
            closeOnCancel: false
        },
        function (isConfirm) {
            if (!isConfirm) {
                swal({
                    title: "已取消",
                    text: "您取消了删除操作！",
                    type: "warning"
                })
                return
            }
            var data = {'num': num}
            sendAjax(data, '/app/del/', delCallback)
        }
    )
}

function delCallback(value) {
    if (value === 1) {
        swal({
            title: "删除成功",
            text: "",
            type: "success",
            timer: 2000
        }, function () {
            location.reload()
        })
    }
    if (value === -1) {
        swal("删除失败", "请重试", "error")
    }
}