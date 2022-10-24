'use strict'

$(document).ready(function () {
    banner();
});

function banner() {

    // let temp_html = ``
    //
    let temp_html = `<nav class="navbar navbar-light bg-light header">
                    <a class="header_link" href="/main">
                        GatherHere
                    </a>
                    <div>
                        <button class="header_rightBtn" onclick="location.href='/login'">로그인</button>
                        <button class="header_rightBtn" onclick="location.href='/mypage'">마이페이지</button>
                    </div>
                </nav>`
    //
    // let temp_html = `<nav class="navbar navbar-light bg-light header">
    //             <a class="header_link" href="/main">
    //                 GatherHere
    //             </a>
    //             <div>
    //                 <button class="header_rightBtn" onclick="location.href='/main'">로그아웃</button>
    //                 <button class="header_rightBtn" onclick="location.href='/mypage'">마이페이지</button>
    //             </div>
    //         </nav>`

    $('#banner').append(temp_html)
}
