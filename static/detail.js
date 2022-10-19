$(document).ready(function () {
    show_detail_id();
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

        let image = rows['image']
        let rank = rows['rank']
        let title = rows['title']
        let star = rows['star']
        let release = rows['release']
        let direction = rows['direction']
        let actor = rows['actor']
        let ageLimit = rows['ageLimit']
        let summary = rows['summary']

        let temp_html = `<img class="detail_img" src="${image}" />
                            <div class="detail_info">
                                <div class="detail_info-special">
                                    <div class="detail_info-special--rank">${rank}</div>
                                    <h3 class="detail_info-speacial--title">${title}</h3>
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
        $('#detail_box').append(temp_html)
    }
  })
}

function commentPosing() {
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

