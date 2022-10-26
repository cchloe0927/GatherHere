$(document).ready(function () {
    listing_bookmark();
    listing_comment();
});
let comment_count = 0;
let b_cnt =0;
function listing_bookmark() {
    $.ajax({
        type: 'GET',
        url: '/mypage/bookmark',
        data: {},
        success: function (response) {
            let rows = response['bookmarks']
            if(rows[0] != null){
                for (let i = 0; i < rows.length; i++) {
                    b_cnt++
                    let id = rows[i]['id']
                    let title = rows[i]['title']
                    let image = rows[i]['image']
                    let star = rows[i]['star']
                    let type = rows[i]['type']
                    let creator = null
                    if (type == 'movie') {
                        creator = rows[i]['direction']
                    } else if (type == 'book') {
                        creator = rows[i]['author']
                    } else if (type == 'album') {
                        creator = rows[i]['artist']
                    }
                    let temp_html = `
                        <div id='bmk_card' class="swiper-slide" id="${id}">
                            <div class="poster" alt="${title}" 
                                style="background-image:url(${image})" 
                                onclick="location.href='detail?type=${type}&id=${id}'">
                            </div>
                            <h4>${title}</h4>
                            <p class="sumContent">${creator}<br>평점: ${star}</p>
                        <div class="heart-like-button liked" href="#" id="${id}" 
                        onclick="delete_bookmark(${id}, '${type}')"></div>
                        </div>`
                    console.log(type)
                    $('#swipeBookmark').append(temp_html)
                } console.log(b_cnt)
                if(b_cnt) $('#bmk').hide()
            } else {
                $('#bmk').hide()
            }
        }
    })
}

let c_cnt = 0
function listing_comment() {
    $.ajax({
        type: 'GET',
        url: '/mypage/comment',
        data: {},
        success: function (response) {
            let rows = response['comments']
            for (i = 0; i < rows.length; i++) {
                c_cnt++
                let username = rows[i]['username']
                let text = rows[i]['text']
                let myStar = rows[i]['myStar']
                let star_img = "⭐️".repeat(myStar)

                let commentId = rows[i]['commentId'] //코멘트 삭제용
                let title = rows[i]['title']

                // let mystar = rows[i]['myStar']
                let date = rows[i]['date']

                let temp_html = `
                    <div id="cmt_card" class="reviewCard_card mypage_comment">
                        <div>
                            <h4>${title}</h4>
                            <div>${username}님 <span>평점 : ${star_img}</span>
                                <div class="delete_btn_mypage"
                                onclick="commentDelete(${commentId})">
                                <span class="cp_bar"></span>
                                </div>
                            </div>
                        </div>
                        <div class="reviewCard_card-text">${text}</div>
                        <div class="mypage_date">${date}</div>
                    </div>`
                $('#comment-list').append(temp_html)
            }
            if(c_cnt < 1) $('#cmt').hide()
        },error: function () {
            $('#cmt').hide()
        }
    })
}

function delete_bookmark(id, type) {
    b_cnt--;
    console.log(id, type)
    if(b_cnt <= 0){
        $('#bmk').hide();
    }
    $.ajax({
        type: "POST",
        url: "/del_bookmark",
        data: {
            id: id,
            type: type
        },
        success: function (response) {
            $('#bmk_card').remove();
        }
    });
}


function commentDelete(commentId) {
    alert('button active')
    c_cnt--;
    if(c_cnt <=0){
        $('#cmt').hide()
    }
    $.ajax({
        type: "POST",
        url: "/detail/comment/delete",
        data: {
            commentId: commentId
        },
        success: function (response) {
            $('#cmt_card').remove()
        }
    });
}
