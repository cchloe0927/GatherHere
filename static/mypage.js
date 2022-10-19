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
            console.log(rows)

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
                let temp_html = `
                    <div class="col">
                    <a class ="Link" href="https://www.naver.com">
                        <div class="card h-100">
                            <img src="${image}"
                                 class="card-img-top">
                            <div class="card-body">
                                <h5 class="card-title">${title}</h5>
                                <p>평점 : ${star}</p>
                                <p>${creator}</p>
                            </div>
                        </div>
                        </a>
                    </div>`
                $('#cards-box').append(temp_html)
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
                let nickname = rows[i]['username']
                let comment = rows[i]['text']
                let contents = rows[i]['title']
                let mystar = rows[i]['myStar']
                let date = rows[i]['date']
                let temp_html = `
                            <div class="card">

                                <div class="card-body">
                                    <blockquote class="blockquote mb-0">
                                        <p>${comment}</p>
                                        <footer class="blockquote-footer">${nickname}</footer>
                                        <p>${contents}</p>
                                        <p>평점 : ${mystar}</p>
                                        <p>${date}</p>
                                    </blockquote>
                                </div>
                            </div>
                        `
                $('#comment-list').append(temp_html)
            }
        }
    })
}
