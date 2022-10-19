$(document).ready(function () {
    show_detail_id();
});

function open_box() {
    $('#reviewUpload_card').show()
}

function close_box() {
    $('#reviewUpload_card').hide()
}

function show_detail_id() {
    let url = window.location.href;
    let param = window.location.search;
    let paramData = new URLSearchParams(param)
    let type = paramData.get('type')
    let id = paramData.get('id')
    //console.log(url, param, type, id)

    $.ajax({
    type: "GET",
    url: "/detail/review?type="+type+"&id="+id,
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

