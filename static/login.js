function login() {
    var before = document.referrer
    $.ajax({
        type: "POST",
        url: "/login",
        data: {userid: $('#userid').val(), password: $('#password').val()},

        success: function (response) {
            if (response['result'] == 'success') {
                // alert('로그인 완료!')
                window.location.href = before;
            } else {
                // 로그인이 안되면 에러메시지
                alert(response['msg'])
            }
        }
    })
}