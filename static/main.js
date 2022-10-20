$(document).ready(function () {
  show_movie()
  show_book()
  show_album()
})

function show_movie() {
  $('#swipeMovie').empty()
  $.ajax({
    type: "GET",
    url: "/main/movie",
    data: {},
    success: function (response) {
      let rows = response['show_movie']
      for (let i = 0; i < rows.length; i++) {
        let title = rows[i].title
        let direction = rows[i].direction
        let star = rows[i].star
        let id = rows[i].id
        let image = rows[i].image
        let temp_html = `<div class="swiper-slide">
        <div class="poster" alt="${title}" style="background-image:url(${image})" onclick="location.href='detail?type=movie&id=${id}'"></div>
        <div>
        <div class="contentDesc">
          <h4>${title}</h4>
          <p class="sumContent">감독: ${direction}<br>평점: ${star}</p>
        </div>
        </div>
        <a class="heart" href="#">💖</a>`

        $('#swipeMovie').append(temp_html)
      }
    }
  })
}

function show_book() {
  $('#swipeBook').empty()
  $.ajax({
    type: "GET",
    url: "/main/book",
    data: {},
    success: function (response) {
      let rows = response['show_book']
      for (let i = 0; i < rows.length; i++) {
        let title = rows[i].title
        let author = rows[i].author
        let star = rows[i].star
        let id = rows[i].id
        let image = rows[i].image
        let temp_html = `<div class="swiper-slide">
        <div class="poster" alt="${title}" style="background-image:url(${image})" onclick="location.href='detail?type=book&id=${id}'"></div>
        <div>
        <div class="contentDesc">
          <h4>${title}</h4>
          <p class="sumContent">${author}<br>평점: ${star}</p>
        </div>
        </div>
        <a class="heart" href="#">💖</a>`
        $('#swipeBook').append(temp_html)
      }
    }
  })
}

function show_album() {
  $('#swipeAlbum').empty()
  $.ajax({
    type: "GET",
    url: "/main/album",
    data: {},
    success: function (response) {
      let rows = response['show_album']
      for (let i = 0; i < rows.length; i++) {
        let title = rows[i].title
        let artist = rows[i].artist
        let star = rows[i].star
        let id = rows[i].id
        let image = rows[i].image
        let temp_html = `<div class="swiper-slide">
        <div class="posterAlbum" alt="${title}" style="background-image:url(${image})" onclick="location.href='detail?type=album&id=${id}'"></div>
        <div>
        <div class="contentDesc">
          <h4>${title}</h4>
          <p class="sumContent">${artist}<br>평점: ${star}</p>
        </div>
        </div>
        <a class="heart" href="#">💖</a>`
        $('#swipeAlbum').append(temp_html)
      }
    }
  })
}