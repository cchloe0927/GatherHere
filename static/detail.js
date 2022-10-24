'use strict'

$(document).ready(function () {
    show_detail();
    comment_get();
});

function open_box() {
    $('#reviewUpload_card').show()
}
function close_box() {
    $('#reviewUpload_card').hide()
}

// 전역 변수
const param = window.location.search;
const paramData = new URLSearchParams(param)
const type = paramData.get('type')
const id = paramData.get('id')
//console.log(param, type, id)

function show_detail() {
    $.ajax({
    type: "GET",
    url: "/detail/info?type="+type+"&id="+id,
    data: {},
    success: function(response){
        let rows = response['detailID']
        //all
        let image = rows['image']
        let rank = rows['rank']
        let title = rows['title']
        let star = rows['star']
        let release = rows['release']
        let genre = rows['genre']
        let summary = rows['summary']
        //movie
        let direction = rows['direction']
        let actor = rows['actor']
        //book
        let author = rows['author']
        //album
        let artist = rows['artist']
        let company = rows['company']

        let temp_html = ``
        if (type=="movie") {
            temp_html = `<img class="detail_img" src="${image}" />
                            <div class="detail_info">
                                <div class="detail_info-special">
                                    <div class="detail_info-special--rank">${rank}</div>
                                    <h3 id="title" class="detail_info-special--title">${title}</h3>
                                    <h5 class="detail_info-special--star">★${star}</h5>
                                </div>
                                <p><span style="font-weight: bold">개봉일</span> &nbsp;&nbsp;${release}</p>
                                <p><span style="font-weight: bold">장르</span> &nbsp;&nbsp;${genre}</p>
                                <p><span style="font-weight: bold">감독</span> &nbsp;&nbsp;${direction}</p>
                                <p><span style="font-weight: bold">출연</span> &nbsp;&nbsp;${actor}</p>
                                <div><span style="font-weight: bold">줄거리</span>
                                    <p>${summary}</p>
                                </div>
                            </div>`
        } else if (type=="book") {
            temp_html = `<img class="detail_img" src="${image}" />
                            <div class="detail_info">
                                <div class="detail_info-special">
                                    <div class="detail_info-special--rank">${rank}</div>
                                    <h3 id="title" class="detail_info-special--title">${title}</h3>
                                    <h5 class="detail_info-special--star">★ ${star}</h5>
                                </div>
                                <p><span style="font-weight: bold">개봉일</span> &nbsp;&nbsp;${release}</p>
                                <p><span style="font-weight: bold">저자</span> &nbsp;&nbsp;${author}</p>
                                <div><span style="font-weight: bold">줄거리</span>
                                    <p>${summary}</p>
                                </div>
                            </div>`
        } else {
            temp_html = `<img class="detail_img" src="${image}" />
                            <div class="detail_info">
                                <div class="detail_info-special">
                                    <div class="detail_info-special--rank">${rank}</div>
                                    <h3 id="title" class="detail_info-special--title">${title}</h3>
                                    <h5 class="detail_info-special--star">★ ${star}</h5>
                                </div>
                                <p><span style="font-weight: bold">개봉일</span> &nbsp;&nbsp;${release}</p>
                                <p><span style="font-weight: bold">아티스트</span> &nbsp;&nbsp;${artist}</p>
                                <p><span style="font-weight: bold">제작사</span> &nbsp;&nbsp;${company}</p>
                            </div>`
        }

        $('#detail_box').append(temp_html)
    }
  })
}

function comment_post() {
    let title= $('#title').text()

    let myStar = $('#myStar').val()
    let text = $('#text').val()

    let dateList = new Date();
    let year = dateList.getFullYear();
    let month = dateList.getMonth() + 1;
    let day = dateList.getDate();
    let date = year + '.' + month + '.' + day
    //console.log(date)

    $.ajax({
        type: 'POST',
        url: '/detail/comment',
        data: {
            'type': type,
            'id': id,
            'title':title, //mypage용 타이틀 데이터
            'myStar': myStar,
            'text': text,
            'date': date,
        },
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    })
}

function comment_get() {
    $.ajax({
        type: "GET",
        url: "/detail/comment?type="+type+"&id="+id,
        data: {},
        success: function (response) {
            let comments = response['comments']
            let userid = response['user_info']
            //console.log(comments)
            //console.log(userid)

            for (let i=0; i<comments.length; i++) {
                //console.log(rows[i])
                let username = comments[i]['username']
                let myStar = comments[i]['myStar']
                let star_img = "⭐️".repeat(myStar)
                let text = comments[i]['text']

                let commentId = comments[i]['commentId'] //코멘트 삭제용
                let id = comments[i]['id'] //comments['id'] vs userid['userid'] 비교용
                //console.log(id)
                //console.log(userid)

                let temp_html = ``
                if (id == userid) {
                    temp_html = `<div class="reviewCard_card">
                                    <div>
                                        <div>
                                            <span class="reviewCard_card-username">${username}님</span>
                                            <span class="reviewCard_card-mystar">평점 : ${star_img}</span>
                                            <button onclick="commentDelete(${commentId})" type="button" class="reviewCard_card-btn">X</button>
                                        </div>
                                    </div>
                                    <div class="reviewCard_card-text">${text}</div>
                                </div>`
                } else {
                    temp_html = `<div class="reviewCard_card">
                                    <div>
                                        <span class="reviewCard_card-username">${username}님</span>
                                        <span class="reviewCard_card-mystar">평점 : ${star_img}</span>
                                    </div>
                                    <div class="reviewCard_card-text">${text}</div>
                                </div>`
                }
                $('#comment-list').append(temp_html)
            }
        }
    })
}

function commentDelete(commentId) {
    $.ajax({
        type: "POST",
        url: "/detail/comment/delete",
        data: {
            commentId: commentId
        },
        success: function (response) {
            alert(response["msg"])
            window.location.reload()
        }
    });
}

