function search(event) {
    //console.log(event)
    if (event.key == 'Enter') {
        console.log('we click this key', event.key);
        let keyword = $('#input').val()
        
        $.ajax({
            type: "GET",
            url: "/search?keyword="+keyword,
            data: {},
            success: function (response) {
                let keyword  = response['keyword']
                if(keyword == null){
                    alert("검색과 일치하는 내용이 없습니다.")
                }else{
                    console.log(keyword)
                    window.location.href = 'detail?type='+keyword['type']+'&id='+keyword['id']
                }
            }
        })
    }
}