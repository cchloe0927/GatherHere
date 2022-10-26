$(document).ready(function () {
  show_movie()
  // show_book()
  // show_album()
  show_bookmark()
  $('#bmk').hide()
  // }
})

// function reloadDiv() {
//   $('#bmk').load(location.href + ' #bmk');
// }
let bmkcnt = 0

// 즐겨찾기 swiper 고친 거
function resizeDiv() {
  if (bmkcnt % 2 === 1) {
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
          <div class="swiper-slide" id="${id}">
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
          // onclick 시 하트 지우고 DB에서 삭제
          $('#swipeBookmark').on('click', '.heart-like-button', function () {
            // const bmkDiv = $(this).closest('.swiper-slide')
            let contentId = $(this).closest('.swiper-slide').attr('id')
            if ($(this).hasClass("liked")) {
              $(this).removeClass("liked")
              $(this).closest('.swiper-slide').remove();
              del_bookmark(contentType, contentId)
              bmkcnt--
              if (bmkcnt < 1) {
                $('#bmk').hide()
                bmkcnt = 0
              }
            }
          });
          resizeDiv()
        }
      }
    }
  })
}

// function saveLocal(id, content) {
//   localStorage.setItem(id, content)
// }

// function removeLocal(id) {
//   localStorage.removeItem(id)
// }

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
        let contentType = rows[i].type
        let temp_html = `<div class="swiper-slide" id="${id}">
        <div class="detail_info-special--rank">${rank}</div>
        <div class="poster" alt="${title}" style="background-image:url(${image})" onclick="location.href='detail?type=${contentType}&id=${id}'"></div>
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
            // let contentType = bmkDiv.classList[0]
            let contentId = bmkDiv.id

            if (heart.classList.contains("liked")) {
              // 즐겨찾기 취소할 때
              $(".swiper-slide").on("click", heart, function () {
                heart.classList.remove("liked")
              })
              // heart.classList.remove("liked")
              // 즐겨찾기 아래 있는 항목일 때
              contentId = bmkDiv.id
              resizeDiv()
              del_bookmark(contentType, contentId)
              bmkcnt--
              if (bmkcnt < 1) {
                $('#bmk').remove()
              }
            } else { // 즐겨찾기 눌렀을 때
              heart.classList.add("liked")
              $('#bmk').show()
              $('#swipeBookmark').append($(bmkDiv).clone())
              resizeDiv()
              add_bookmark(contentType, contentId)
              bmkcnt++
            }
          }
        })
      }
    }
  })
}

// function show_book() {
//   $('#swipeBook').empty()
//   $.ajax({
//     type: "GET",
//     url: "/main/book",
//     data: {},
//     success: function (response) {
//       let rows = response['show_book']
//       for (let i = 0; i < rows.length; i++) {
//         let title = rows[i].title
//         let author = rows[i].author
//         let star = rows[i].star
//         let id = rows[i].id
//         let image = rows[i].image
//         let rank = rows[i].rank
//         let temp_html = `<div class="book swiper-slide" id="${id}">
//         <div class="detail_info-special--rank">${rank}</div>
//         <div class="poster" alt="${title}" style="background-image:url(${image})" onclick="location.href='detail?type=book&id=${id}'"></div>
//           <h4>${title}</h4>
//           <p class="sumContent">${author}<br>평점: ${star}</p>
//         <div class="heart-like-button">
//         </div></div>`
//         $('#swipeBook').append(temp_html)
//         const heart = document.querySelectorAll(".heart-like-button")
//         heart.forEach((heart) => {
//           heart.onclick = (e) => {
//             const bmkDiv = e.target.parentNode
//             let contentType = bmkDiv.classList[0]
//             let contentId = bmkDiv.id

//             if (heart.classList.contains("liked")) {
//               // 즐겨찾기 취소할 때
//               heart.classList.remove("liked")
//               // $("#bmk").load('main.html' + " #bmk");
//               $(bmkDiv).remove()
//               removeLocal(contentId)
//               if (bmkcnt < 1) {
//                 $('#bmk').remove()
//               }
//               resizeDiv()
//               del_bookmark(contentType, contentId)

//             } else { // 즐겨찾기 눌렀을 때
//               heart.classList.add("liked")
//               $('#bmk').show()
//               $('#swipeBookmark').append($(bmkDiv).clone())
//               resizeDiv()
//               add_bookmark(contentType, contentId)
//               // 로컬 저장 후 불러오기
//               saveLocal(contentId, JSON.stringify(bmkDiv.outerHTML))
//               location.reload(true)
//               // $("#bmk").load('/main' + " #bmk");
//               // event.preventDefault()
//             }
//           }
//         })
//       }
//     }
//   })
// }

// function show_album() {
//   $('#swipeAlbum').empty()
//   $.ajax({
//     type: "GET",
//     url: "/main/album",
//     data: {},
//     success: function (response) {
//       let rows = response['show_album']
//       for (let i = 0; i < rows.length; i++) {
//         let title = rows[i].title
//         let artist = rows[i].artist
//         let star = rows[i].star
//         let id = rows[i].id
//         let image = rows[i].image
//         let rank = rows[i].rank
//         let temp_html = `<div class="album swiper-slide" id="${id}">
//         <div class="detail_info-special--rank">${rank}</div>
//         <div class="poster" alt="${title}" style="background-image:url(${image})" onclick="location.href='detail?type=album&id=${id}'"></div>
//           <h4>${title}</h4>
//           <p class="sumContent">${artist}<br>평점: ${star}</p>
//         <div class="heart-like-button">
//         </div></div>`
//         $('#swipeAlbum').append(temp_html)
//         const heart = document.querySelectorAll(".heart-like-button")
//         heart.forEach((heart) => {
//           heart.onclick = (e) => {
//             const bmkDiv = e.target.parentNode
//             let contentId = bmkDiv.classList[0]
//             let contentType = bmkDiv.id

//             if (heart.classList.contains("liked")) {
//               // 즐겨찾기 취소할 때
//               heart.classList.remove("liked")
//               // $("#bmk").load('main.html' + " #bmk");
//               $(bmkDiv).remove()
//               removeLocal(contentId)
//               if (bmkcnt < 1) {
//                 $('#bmk').hide()
//               }
//               resizeDiv()
//               del_bookmark(contentType, contentId)

//             } else { // 즐겨찾기 눌렀을 때
//               heart.classList.add("liked")
//               $('#bmk').show()
//               $('#swipeBookmark').append($(bmkDiv).clone())
//               resizeDiv()
//               add_bookmark(contentType, contentId)
//               // 로컬 저장 후 불러오기
//               saveLocal(contentId, JSON.stringify(bmkDiv.outerHTML))
//               // $("#bmk").load('/main' + " #bmk");
//               // event.preventDefault()
//             }
//           }
//         })
//       }
//     }
//   })
// }