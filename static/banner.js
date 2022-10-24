'use strict'

$(document).ready(function () {
    banner();
});

function banner() {

    let temp_html = `<nav class="navbar navbar-light bg-light header">
                    <a class="header_link" href="#">
                        GatherHere
                    </a>
                    <div>
                        <button class="header_rightBtn">로그인</button>
                        <button class="header_rightBtn">마이페이지</button>
                    </div>
                </nav>`

    $('#banner').append(temp_html)
}
