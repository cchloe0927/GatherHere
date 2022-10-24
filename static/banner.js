'use strict'

$(document).ready(function () {
    // banner();
    $('#banner').load("./banner.html")
});


function logout(){
    document.cookie = 'Authorization' + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    location.href = '/main';
}

function banner() {

    let temp_html = `<nav class="navbar navbar-light bg-light header">
                    <a class="header_link" href="/main">
                        GatherHere
                    </a>
                    <div>
                        {% if username %}
                            {{ username }}
                            <button class="header_rightBtn" onclick="logout()">로그아웃</button>
                        {% endif %}
                        {% if not username %}
                            <button class="header_rightBtn" onclick="location.href='/login'">로그인</button>
                            <button class="header_rightBtn">마이페이지</button>
                        {% endif %}
                        <button class="header_rightBtn" onclick="location.href='/mypage'">마이페이지</button>
                    </div>
                </nav>`

    // $('#banner').append(temp_html)
    $('#banner').load("/banner.html")
}
