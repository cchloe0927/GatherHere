'use strict'

$(document).ready(function () {
    show_detail_id();
    commentGeting();
});

function open_box() {
    $('#reviewUpload_card').show()
}
function close_box() {
    $('#reviewUpload_card').hide()
}

// 전역변수
const param = window.location.search;
const paramData = new URLSearchParams(param)
const type = paramData.get('type')
const id = paramData.get('id')
//console.log(param, type, id)

function show_detail_id() {
    $.ajax({
    type: "GET",
    url: "/detail/info?type="+type+"&id="+id,
    data: {},
    success: function(response){
        let rows = response['detailID']
        //movie
        let image = rows['image']
        let rank = rows['rank']
        let title = rows['title']
        let star = rows['star']
        let release = rows['release']
        let direction = rows['direction']
        let actor = rows['actor']
        let ageLimit = rows['ageLimit']
        let summary = rows['summary']
        //book
        let author = rows['author']
        //album
        let url = rows['url']
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
                                <p><span style="font-weight: bold">감독</span> &nbsp;&nbsp;${direction}</p>
                                <p><span style="font-weight: bold">출연</span> &nbsp;&nbsp;${actor}</p>
                                <p><span style="font-weight: bold">등급</span> &nbsp;&nbsp;${ageLimit}</p>
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
            temp_html = `<img class="detail_img" src="${url}" />
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

function commentPosting() {
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

function commentGeting() {
    $.ajax({
        type: "GET",
        url: "/detail/comment?type="+type+"&id="+id,
        data: {},
        success: function (response) {
            let rows = response['comments']
            for (let i=0; i<rows.length; i++) {
                //console.log(rows[i])
                let username = rows[i]['username']
                let myStar = rows[i]['myStar']
                let star_img = "⭐️".repeat(myStar)
                let text = rows[i]['text']

                let commentId = rows[i]['commentId'] //코멘트 삭제용

                let temp_html = `<div class="reviewCard_card">
                                    <div>
                                        <div>${username}님 <span>평점 : ${star_img}</span>
                                            <button onclick="commentDelete(${commentId})" type="button" class="reviewCard_card-btn">X</button>
                                        </div>
                                    </div>
                                    <div class="reviewCard_card-text">${text}</div>
                                </div>`
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

