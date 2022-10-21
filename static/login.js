function login() {
    var before = document.referrer
    $.ajax({
        type: "POST",
        url: "/login",
        data: {userid: $('#userid').val(), password: $('#password').val()},

        success: function (response) {
            if (response['result'] == 'success') {
                // 이 토큰을 mytoken이라는 키 값으로 쿠키에 저장
                $.cookie('mytoken', response['token']);
                $.cookie('username', response['username']);
                // alert('로그인 완료!')
                window.location.href = before;
            } else {
                // 로그인이 안되면 에러메시지
                alert(response['msg'])
            }
        }
    })
}