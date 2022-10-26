$(document).ready(function () {
  show_movie()
  show_book()
  show_album()
  $('.heart-like-button').hide()
  if (localStorage.length > 0) {
    $('#bmk').show()
    // 로컬에 저장된 즐겨찾기 전부 append
    for (let i = 0; i < localStorage.length; i++) {
      $('#swipeBookmark').prepend(JSON.parse(localStorage.getItem(localStorage.key(i))))
    }
  } else {
    $('#bmk').hide()
    // $('bodyWrap').show()
  }
})

// document.querySelectorAll('.heart-like-button').addEventListener((click) => {
//   window.location.reload(true);
// })

// 즐겨찾기 스와이퍼 고친 거
function resizeDiv() {
  if (localStorage.length % 2 === 1) {
    $('.swiper').width('96.001vw')
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
      // console.log(response['result'])
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
      // console.log(response['result'])
    }
  })
}

function show_bookmark() {
  $.ajax({
    type: 'GET',
    url: '/mypage/bookmark',
    data: {},
    success: function (response) {
      console.log(response);
    }
  })
}

function saveLocal(id, content) {
  localStorage.setItem(id, content)
}

function getLocal(id) {
  const data = JSON.parse(localStorage.getItem(id))
  console.log('data', data);
}

function removeLocal(id) {
  localStorage.removeItem(id)
}

let testarr = []

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
        let rank = rows[i].rank
        let temp_html = `<div class="movie swiper-slide" id="${id}">
        <div class="detail_info-special--rank">${rank}</div>
        <div class="poster" alt="${title}" style="background-image:url(${image})" onclick="location.href='detail?type=movie&id=${id}'"></div>
          <h4>${title}</h4>
          <p class="sumContent">감독: ${direction}<br>평점: ${star}</p>
        <div class="heart-like-button"></div>
        </div>`
        $('#swipeMovie').append(temp_html)
        const heart = document.querySelectorAll(".heart-like-button")
        heart.forEach((heart) => {
          heart.onclick = (e) => {
            // 클릭한 개체의 div
            const bmkDiv = e.target.parentNode
            let contentType = bmkDiv.classList[0]
            let contentId = bmkDiv.id

            if (heart.classList.contains("liked")) {
              // 즐겨찾기 취소할 때
              heart.classList.remove("liked")
              // $("#bmk").load('main.html' + " #bmk");
              $(bmkDiv).remove()
              removeLocal(contentId)
              if (localStorage.length < 1) {
                $('#bmk').hide()
              }
              resizeDiv()
              del_bookmark(contentType, contentId)

            } else { // 즐겨찾기 눌렀을 때
              heart.classList.add("liked")
              $('#bmk').show()
              $('#swipeBookmark').append($(bmkDiv).clone())
              resizeDiv()
              add_bookmark(contentType, contentId)
              // 로컬 저장 후 불러오기
              saveLocal(contentId, JSON.stringify(bmkDiv.outerHTML))
              // $("#bmk").load('/main' + " #bmk");
              // event.preventDefault()
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
        let rank = rows[i].rank
        let temp_html = `<div class="book swiper-slide" id="${id}">
        <div class="detail_info-special--rank">${rank}</div>
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
              // 즐겨찾기 취소할 때
              heart.classList.remove("liked")
              // $("#bmk").load('main.html' + " #bmk");
              $(bmkDiv).remove()
              removeLocal(contentId)
              if (localStorage.length < 1) {
                $('#bmk').hide()
              }
              resizeDiv()
              del_bookmark(contentType, contentId)

            } else { // 즐겨찾기 눌렀을 때
              heart.classList.add("liked")
              $('#bmk').show()
              $('#swipeBookmark').append($(bmkDiv).clone())
              resizeDiv()
              add_bookmark(contentType, contentId)
              // 로컬 저장 후 불러오기
              saveLocal(contentId, JSON.stringify(bmkDiv.outerHTML))
              // $("#bmk").load('/main' + " #bmk");
              // event.preventDefault()
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
        let rank = rows[i].rank
        let temp_html = `<div class="album swiper-slide" id="${id}">
        <div class="detail_info-special--rank">${rank}</div>
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
              // 즐겨찾기 취소할 때
              heart.classList.remove("liked")
              // $("#bmk").load('main.html' + " #bmk");
              $(bmkDiv).remove()
              removeLocal(contentId)
              if (localStorage.length < 1) {
                $('#bmk').hide()
              }
              resizeDiv()
              del_bookmark(contentType, contentId)

            } else { // 즐겨찾기 눌렀을 때
              heart.classList.add("liked")
              $('#bmk').show()
              $('#swipeBookmark').append($(bmkDiv).clone())
              resizeDiv()
              add_bookmark(contentType, contentId)
              // 로컬 저장 후 불러오기
              saveLocal(contentId, JSON.stringify(bmkDiv.outerHTML))
              // $("#bmk").load('/main' + " #bmk");
              // event.preventDefault()
            }
          }
        })
      }
    }
  })
}