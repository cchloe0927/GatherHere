$(document).ready(function () {
  show_movie()
  show_book()
  show_album()
  $('#bmk').hide()
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
        let temp_html = `<div class="swiper-slide" id="${id}">
        <div class="poster" alt="${title}" style="background-image:url(${image})" onclick="location.href='detail?type=movie&id=${id}'"></div>
          <h4>${title}</h4>
          <p class="sumContent">감독: ${direction}<br>평점: ${star}</p>
        <div class="heart-like-button"></div>
        </div>`
        $('#swipeMovie').append(temp_html)
        const heart = document.querySelectorAll(".heart-like-button")
        heart.forEach((heart) => {
          heart.onclick = (e) => {
            const bmkDiv = e.target.parentNode
            if (heart.classList.contains("liked")) {
              heart.classList.remove("liked")
              $(bmkDiv).remove()
              $('#swipeMovie').append(bmkDiv)
            } else {
              heart.classList.add("liked")
              $('#bmk').show()
              $('#swipeBookmark').append(bmkDiv)
              // console.log(e.path[1]);
              // console.log(e.path[1].classList.length);
              // 즐겨찾기 swiper 슬라이드 안 넘어가는 문제 파악하는 중
            }
          }
        })
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
          <h4>${title}</h4>
          <p class="sumContent">${author}<br>평점: ${star}</p>
        <div class="heart-like-button">
        </div></div>`
        $('#swipeBook').append(temp_html)
        const heart = document.querySelectorAll(".heart-like-button")
        heart.forEach((heart) => {
          heart.onclick = (e) => {
            const bmkDiv = e.target.parentNode
            if (heart.classList.contains("liked")) {
              heart.classList.remove("liked")
              $(bmkDiv).remove()
              $('#swipeBook').append(temp_html)
            } else {
              heart.classList.add("liked")
              $('#bmk').show()
              $('#swipeBookmark').append(bmkDiv)
            }
          }
        })
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
        <div class="poster" alt="${title}" style="background-image:url(${image})" onclick="location.href='detail?type=book&id=${id}'"></div>
          <h4>${title}</h4>
          <p class="sumContent">${artist}<br>평점: ${star}</p>
        <div class="heart-like-button">
        </div></div>`
        $('#swipeAlbum').append(temp_html)
        const heart = document.querySelectorAll(".heart-like-button")
        heart.forEach((heart) => {
          heart.onclick = (e) => {
            const bmkDiv = e.target.parentNode
            if (heart.classList.contains("liked")) {
              heart.classList.remove("liked")
              $(bmkDiv).remove()
              $('#swipeAlbum').append(temp_html)
            } else {
              heart.classList.add("liked")
              $('#bmk').show()
              $('#swipeBookmark').append(bmkDiv)
            }
          }
        })
      }
    }
  })
}