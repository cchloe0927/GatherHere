$(document).ready(function () {
  // 메인 슬라이드
  let swiper = new Swiper(".mySwiper", {
    slidesPerView: 3,
    spaceBetween: 10,
    // Responsive breakpoints
    breakpoints: {
      // when window width is >= 
      120: {
        slidesPerView: 1,
        slidesPerGroup: 1,
        spaceBetween: 10,
      },
      380: {
        slidesPerView: 2,
        slidesPerGroup: 2,
        spaceBetween: 10,
      },
      760: {
        slidesPerView: 3,
        slidesPerGroup: 3,
        spaceBetween: 10,
      },
      1024: {
        slidesPerView: 4,
        slidesPerGroup: 4,
        spaceBetween: 10,
      },
      1280: {
        slidesPerView: 5,
        slidesPerGroup: 5,
        spaceBetween: 10,
      },
      1600: {
        slidesPerView: 6,
        slidesPerGroup: 6,
        spaceBetween: 10,
      }
    },
    loop: true,
    loopAdditionalSlides: 1,
    loopFillGroupWithBlank: true,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  }
  )
  show_bookmark()
  show_movie()
  show_book()
  show_album()
  $('#bmk').hide()
})

// 바디에서 즐겨찾기에 추가한 항목의 갯수를 세는 임시 변수
let bmkcnt = 0

// 로컬 스토리지에 올라간 항목과 같은 바디 항목의 하트를 채색
function paintHeart(id) {
  for (let i = 0; i < localStorage.length; i++) {
    let key = localStorage.key(i);
    if ($(`#${id}`).attr('id') === key) {
      $(`#${key}`).children('.heart-like-button').addClass('liked')
    }
  }
}

// 로컬 스토리지에서 지워진 항목과 같은 바디 항목의 하트를 지움
function eraseHeart(id, divType) {
  for (let i = 0; i < localStorage.length; i++) {
    let key = localStorage.key(i);
    if ($(`#${id}`).attr('id') === key) {
      $(`#${divType}`).find(`#${key}`).children('.heart-like-button').removeClass('liked')
    }
  }
}

function markHeart() {
  const hearts = document.querySelectorAll(".heart-like-button")
  hearts.forEach((heart) => {
    heart.onclick = (e) => {
      console.log(e.target.parentNode.id);
      // 클릭한 개체의 div
      const bmkDiv = e.target.parentNode
      let type = e.target.parentNode.classList[0]
      let contentId = e.target.parentNode.id

      if (heart.classList.contains("liked")) { // 즐겨찾기 취소할 때
        heart.classList.remove("liked")
        resizeDiv()
        del_bookmark(type, contentId)
        localStorage.removeItem(contentId)
        // body에서 눌러도 삭제하기
        $(`#bmk`).find(`#${contentId}`).remove()
        bmkReset()

      } else { // 즐겨찾기 눌렀을 때
        heart.classList.add("liked")
        $('#bmk').show()
        $('#swipeBookmark').append($(bmkDiv).clone())
        $('#bmk').find('.detail_info-special--rank').remove()
        resizeDiv()
        add_bookmark(type, contentId)
        localStorage.setItem(contentId, 'liked')
        bmkcnt++
      }
    }
  })
}

/* function markHeart2(swipeSth) {
  $(`#swipeMovie`).on('click', '.heart-like-button', function () {
    let contentId = $(this).closest('.swiper-slide').attr('id')
    contentType = this.parentNode.classList[0]

    // 즐겨찾기 취소
    if ($(this).hasClass("liked")) {
      $(this).removeClass("liked")
      $(this).closest('.swiper-slide').remove()
      resizeDiv()
      del_bookmark(contentType, contentId)
      eraseHeart(contentId, contentType)
      localStorage.removeItem(contentId)
      bmkReset()

    } else if ($(this).attr('class').not("liked")) {
      console.log('not is working')
      // 즐겨찾기 추가
      $('#bmk').show
      $(this).addClass("liked")
      $('#swipeBookmark').append($(bmkDiv).clone())
      $('#bmk').find('.detail_info-special--rank').remove()
      resizeDiv()
      add_bookmark(contentType, contentId)
      localStorage.setItem(contentId, 'liked')
      bmkcnt++
    }
  });
} */

// 바디에서 지운 즐겨찾기와 같은 항목을 즐겨찾기에서도 삭제하기
function heartClick(mType, contentId, divType) {
  resizeDiv()
  del_bookmark(mType, contentId)
  eraseHeart(contentId, divType)
  localStorage.removeItem(contentId)
  $(`#bmk`).find(`#${contentId}`).remove()
  bmkReset()
}

// 로컬 스토리지가 비워졌을 경우 bmkcnt를 0으로 돌림 (즐겨찾기 감추기 위함)
function bmkReset() {
  bmk--
  if (localStorage.length < 1) {
    $('#bmk').hide()
    bmkcnt = 0
  }
}

// 즐겨찾기 swiper append 시 슬라이더 화살표 안 생기는 버그 해결
function resizeDiv() {
  if (bmkcnt % 2 === 1) {
    $('.swiper').width('96.001vw')
  } else {
    $('.swiper').width('96vw')
  }
}

// DB에 바디 즐겨찾기 누른 개체 추가
function add_bookmark(type, id) {
  $.ajax({
    type: "POST",
    url: "/bookmark/add",
    data: {
      type: type,
      id: id,
    },
    success: function (response) {
    }
  })
}

// DB에서 바디 즐겨찾기 누른 개체 삭제
function del_bookmark(type, id) {
  $.ajax({
    type: "POST",
    url: "/bookmark/del",
    data: {
      type: type,
      id: id,
    },
    success: function (response) {
    }
  })
}

// 즐겨찾기(#bmk) 내에서 일어나는 모든 이벤트
function show_bookmark() {
  $.ajax({
    type: 'GET',
    url: '/bookmark',
    data: {},
    success: function (response) {
      // 로컬 스토리지 비우기
      localStorage.clear()

      // 로그인 시 DB에서 즐겨찾기 항목 불러오기
      let rows = response['bookmarks']
      if (rows[0] != null) {
        bmkcnt = rows.length
        $('#bmk').show()
        for (let i = 0; i < rows.length; i++) {
          let id = rows[i]['id']
          let title = rows[i]['title']
          let image = rows[i]['image']
          let star = rows[i]['star']
          let contentType = rows[i]['type']
          let creator = null
          if (contentType == 'movie') {
            creator = rows[i]['direction']
          } else if (contentType == 'book') {
            creator = rows[i]['author']
          } else if (contentType == 'album') {
            creator = rows[i]['artist']
          }
          let temp_html = `
          <div class="${contentType} swiper-slide" id="${id}">
              <div class="poster" alt="${title}" 
                  style="background-image:url(${image})" 
                  onclick="location.href='detail?type=${contentType}&id=${id}'">
              </div>
              <h4>${title}</h4>
              <p class="sumContent">${creator}<br>평점: ${star}</p>
          <div class="heart-like-button liked" href="#" id="${id}" 
          ></div>
          </div>`
          $('#swipeBookmark').append(temp_html)

          // 로컬 스토리지에 하트 칠한 항목 추가
          localStorage.setItem(`${id}`, 'liked')

          // 하트 버튼 클릭 시 하트 지우고 DB에서 삭제
          // 동적 이벤트 바인딩을 위해 jQuery .on() 사용
          $('#swipeBookmark').on('click', '.heart-like-button', function () {
            let contentId = $(this).closest('.swiper-slide').attr('id')
            contentType = this.parentNode.classList[0]
            if ($(this).hasClass("liked")) {
              $(this).removeClass("liked")
              $(this).closest('.swiper-slide').remove()
              resizeDiv()
              del_bookmark(contentType, contentId)
              eraseHeart(contentId, contentType)
              localStorage.removeItem(contentId)
              bmkReset()
            }
          });
        }
      } else {
        // 로그인 아닐 시 로컬 스토리지를 비움
        localStorage.clear()
      }
    }
  })
}

function show_movie() {
  $('#swipeMovie').empty()
  $.ajax({
    type: "GET",
    url: "/movie",
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

        // DB에서 가져온 항목을 swiper #swipeMovie 아래에 append
        let temp_html = `<div class="movie swiper-slide" id="${id}">
        <div class="detail_info-special--rank">${rank}</div>
        <div class="poster" alt="${title}" style="background-image:url(${image})" onclick="location.href='detail?type=movie&id=${id}'"></div>
          <h4>${title}</h4>
          <p class="sumContent">감독: ${direction}<br>평점: ${star}</p>
        <div class="heart-like-button" onclick="heartClick('movie', ${id}, 'swipeMovie')"></div>
        </div>`
        $('#swipeMovie').append(temp_html)

        // 즐겨찾기에 하트 채색된 항목과 같은 게 로컬 스토리지에 있으면 찾아서 채색
        paintHeart(id)
        // markHeart2(swipeMovie)
        const hearts = document.querySelectorAll(".heart-like-button")
        hearts.forEach((heart) => {
          heart.onclick = (e) => {
            // 클릭한 개체의 div
            const bmkDiv = e.target.parentNode
            let mType = bmkDiv.classList[0]
            let contentId = bmkDiv.id

            if (heart.classList.contains("liked")) { // 즐겨찾기 취소할 때
              heart.classList.remove("liked")
              resizeDiv()
              del_bookmark(mType, contentId)
              localStorage.removeItem(contentId)
              // body에서 눌러도 삭제하기
              $(`#bmk`).find(`#${contentId}`).remove()
              bmkReset()

            } else { // 즐겨찾기 눌렀을 때
              heart.classList.add("liked")
              $('#bmk').show()
              $('#swipeBookmark').append($(bmkDiv).clone())
              $('#bmk').find('.detail_info-special--rank').remove()
              resizeDiv()
              add_bookmark(mType, contentId)
              localStorage.setItem(contentId, 'liked')
              bmkcnt++
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
    url: "/book",
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
        // let bType = rows[i].type

        let temp_html = `<div class="book swiper-slide" id="${id}">
        <div class="detail_info-special--rank">${rank}</div>
        <div class="poster" alt="${title}" style="background-image:url(${image})" onclick="location.href='detail?type=book&id=${id}'"></div>
          <h4>${title}</h4>
          <p class="sumContent">${author}<br>평점: ${star}</p>
          <div class="heart-like-button" onclick="heartClick('book', ${id}, 'swipeBook')"></div>
          </div>`
        $('#swipeBook').append(temp_html)
        paintHeart(id)
        const heart = document.querySelectorAll(".heart-like-button")
        heart.forEach((heart) => {
          heart.onclick = (e) => {
            // 클릭한 개체의 div
            const bmkDiv = e.target.parentNode
            let bType = bmkDiv.classList[0]
            let contentId = bmkDiv.id

            if (heart.classList.contains("liked")) {
              // 즐겨찾기 취소할 때
              heart.classList.remove("liked")
              resizeDiv()
              del_bookmark(bType, contentId)
              localStorage.removeItem(contentId)
              $(`#bmk`).find(`#${contentId}`).remove()

              bmkReset()

            } else { // 즐겨찾기 눌렀을 때
              heart.classList.add("liked")
              $('#bmk').show()
              $('#swipeBookmark').append($(bmkDiv).clone())
              $('#bmk').find('.detail_info-special--rank').remove()
              resizeDiv()
              add_bookmark(bType, contentId)
              localStorage.setItem(contentId, 'liked')
              bmkcnt++
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
    url: "/album",
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
          <div class="heart-like-button" onclick="heartClick('album', ${id}, 'swipeAlbum')"></div>
          </div>`
        $('#swipeAlbum').append(temp_html)
        paintHeart(id)
        const heart = document.querySelectorAll(".heart-like-button")
        heart.forEach((heart) => {
          heart.onclick = (e) => {
            // 클릭한 개체의 div
            const bmkDiv = e.target.parentNode
            let aType = bmkDiv.classList[0]
            let contentId = bmkDiv.id

            if (heart.classList.contains("liked")) {
              // 즐겨찾기 취소할 때
              heart.classList.remove("liked")
              resizeDiv()
              del_bookmark(aType, contentId)
              localStorage.removeItem(contentId)
              $(`#bmk`).find(`#${contentId}`).remove()

              bmkReset()

            } else { // 즐겨찾기 눌렀을 때
              heart.classList.add("liked")
              $('#bmk').show()
              $('#swipeBookmark').append($(bmkDiv).clone())
              $('#bmk').find('.detail_info-special--rank').remove()
              resizeDiv()
              add_bookmark(aType, contentId)
              localStorage.setItem(contentId, 'liked')
              bmkcnt++
            }
          }
        })
      }
    }
  })
}