$(document).ready(function () {
  show_movie()
  show_book()
  show_album()
  $('#bmk').hide()
})

// 즐겨찾기 스와이퍼 고친 거
function resizeDiv() {
  if (cnt % 2 === 1) {
    $('.swiper').width('96.01vw')
  } else {
    $('.swiper').width('96vw')
  }
}

function add_bookmark(type, id) {
  $.ajax({
    type: "POST",
    url: "/add_bookmark",
    data: {
      type: type,
      id: id,
    },
    success: function (response) {
      console.log(response['result'])
    }
  })
}

function del_bookmark(type, id) {
  $.ajax({
    type: "POST",
    url: "/del_bookmark",
    data: {
      type: type,
      id: id,
    },
    success: function (response) {
      console.log(response['result'])
    }
  })
}

function add_bookmark(type, id) {
  $.ajax({
    type: "POST",
    url: "/add_bookmark",
    data: {
      type: type,
      id: id,
    },
    success: function (response) {
      console.log(response['result'])
    }
  })
}

let cnt = 0

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
        let temp_html = `<div class="movie swiper-slide" id="${id}">
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
            // 클릭한 개체의 아이디
            let contentType = bmkDiv.classList[0]
            let contentId = bmkDiv.id

            if (heart.classList.contains("liked")) {
              heart.classList.remove("liked")
              $(bmkDiv).remove()
              $('#swipeMovie').append(bmkDiv)
              cnt -= 1
              if (cnt < 1) {
                $('#bmk').hide()
              }
              resizeDiv()
              del_bookmark(contentType, contentId)
            } else {
              heart.classList.add("liked")
              $('#bmk').show()
              $('#swipeBookmark').append(bmkDiv)
              cnt += 1
              resizeDiv()
              add_bookmark(contentType, contentId)
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
        let temp_html = `<div class="book swiper-slide" id="${id}">
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
            let contentType = bmkDiv.classList[0]
            let contentId = bmkDiv.id

            if (heart.classList.contains("liked")) {
              heart.classList.remove("liked")
              $(bmkDiv).remove()
              $('#swipeBook').append(bmkDiv)
              cnt -= 1
              if (cnt < 1) {
                $('#bmk').hide()
              }
              resizeDiv()
              del_bookmark(contentType, contentId)
            } else {
              $('#bmk').show()
              heart.classList.add("liked")
              $('#bmk').show()
              $('#swipeBookmark').append(bmkDiv)
              cnt += 1
              resizeDiv()
              add_bookmark(contentType, contentId)
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
        let temp_html = `<div class="album swiper-slide" id="${id}">
        <div class="poster" alt="${title}" style="background-image:url(${image})" onclick="location.href='detail?type=album&id=${id}'"></div>
          <h4>${title}</h4>
          <p class="sumContent">${artist}<br>평점: ${star}</p>
        <div class="heart-like-button">
        </div></div>`
        $('#swipeAlbum').append(temp_html)
        const heart = document.querySelectorAll(".heart-like-button")
        heart.forEach((heart) => {
          heart.onclick = (e) => {
            const bmkDiv = e.target.parentNode
            let contentId = bmkDiv.classList[0]
            let contentType = bmkDiv.id

            if (heart.classList.contains("liked")) {
              heart.classList.remove("liked")
              $(bmkDiv).remove()
              $('#swipeAlbum').append(bmkDiv)
              cnt -= 1
              if (cnt < 1) {
                $('#bmk').hide()
              }
              resizeDiv()
              del_bookmark(contentType, contentId)
            } else {
              heart.classList.add("liked")
              $('#bmk').show()
              $('#swipeBookmark').append(bmkDiv)
              cnt += 1
              resizeDiv()
              add_bookmark(contentType, contentId)
            }
          }
        })
      }
    }
  })
}