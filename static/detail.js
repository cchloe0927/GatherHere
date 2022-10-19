
// $(document).ready(function () {
//     detail_movie();
// });

function open_box() {
    $('#reviewUpload_card').show()
}

function close_box() {
    $('#reviewUpload_card').hide()
}

function detail_movie() {
    let type = "movie"
    let id= 187831

    $.ajax({
    type: "GET",
    url: "/detail/review?type="+type+"&id="+id,
    data: {},
    success: function(response){
       console.log(response)
    }
  })
}

