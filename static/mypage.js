const param = window.location.search;
const paramData = new URLSearchParams(param)
const type = paramData.get('type')
const id = paramData.get('id')

$(document).ready(function () {
    listing_bookmark();
    listing_comment();
});

function listing_bookmark() {
    $.ajax({
        type: 'GET',
        url: '/bookmark',
        data: {},
        success: function (response) {
            let rows = response['bookmarks']
            for (let i = 0; i < rows.length; i++) {
                let title = rows[i]['title']
                let image = rows[i]['image']
                let star = rows[i]['star']
                let type = rows[i]['type']
                let creator = null
                if (type == 'movie') {
                    creator = rows[i]['direction']
                } else if (type == 'book') {
                    creator = rows[i]['author']
                } else if (type == 'album') {
                    creator = rows[i]['artist']
                }
                // let temp_html = `
                //     <div class="swiper-slide" onclick="location.href='detail?type=movie&id=${id}'">
                //         <div class="col">
                //         <a class ="Link" href="https://www.naver.com">
                //             <div class="card h-100">
                //                 <img src="${image}"
                //                      class="card-img-top">
                //                 <div class="card-body">
                //                     <h5 class="card-title">${title}</h5>
                //                     <p>평점 : ${star}</p>
                //                     <p>${creator}</p>
                //                 </div>
                //             </div>
                //             </a>
                //         </div>
                //     </div>`
                let temp_html = `
                    <div class="swiper-slide" onclick="location.href='detail?type=movie&id=${id}'">
                        <img src="${image}" alt="${title}">
                        <div>
                        <div class="contentDesc">
                          <h4>${title}</h4>
                          <p>${creator}<br>평점: ${star}</p>
                        </div>
                        </div>
                    </div>`
                $('#swipeMovie').append(temp_html)
            }
        }
    })
}

function listing_comment() {
    $.ajax({
        type: 'GET',
        url: '/comment',
        data: {},
        success: function (response) {
            console.log(response['comments'])
            let rows = response['comments']
            for (i = 0; i < rows.length; i++) {
                let username = rows[i]['username']
                let text = rows[i]['text']
                let myStar = rows[i]['myStar']
                let star_img = "⭐️".repeat(myStar)

                let commentId = rows[i]['commentId'] //코멘트 삭제용
                let title = rows[i]['title']
                // let mystar = rows[i]['myStar']
                // let date = rows[i]['date']

                // let temp_html = `
                //             <div class="card">
                //
                //                 <div class="card-body">
                //                     <blockquote class="blockquote mb-0">
                //                         <p>${comment}</p>
                //                         <footer class="blockquote-footer">${nickname}</footer>
                //                         <p>${contents}</p>
                //                         <p>평점 : ${mystar}</p>
                //                         <p>${date}</p>
                //                     </blockquote>
                //                 </div>
                //             </div>`
                let temp_html = `<div class="reviewCard_card">
                                    <div>
                                        <div>${username}님 <span>평점 : ${star_img}</span>
                                            <button onclick="commentDelete(${commentId})" type="button" class="reviewCard_card-btn">X</button>
                                        </div>
                                    </div>
                                    <div class="reviewCard_card-text">${text}</div>
                                </div>`
                $('#comment-list').append(temp_html)
            }
        }
    })
}


// Initialize Swiper
let swiper = new Swiper(".mySwiper", {
        slidesPerView: 3,
        spaceBetween: 10,
        // Responsive breakpoints
        breakpoints: {
            // when window width is >= 320px
            180: {
                slidesPerView: 1,
                slidesPerGroup: 1,
                spaceBetween: 10,
            },
            320: {
                slidesPerView: 2,
                slidesPerGroup: 2,
                spaceBetween: 10,
            },
            // when window width is >= 480px
            480: {
                slidesPerView: 3,
                slidesPerGroup: 3,
                spaceBetween: 10,
            },
            // when window width is >= 640px
            720: {
                slidesPerView: 4,
                slidesPerGroup: 4,
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

