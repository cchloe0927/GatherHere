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
                if(type == 'movie'){
                    creator = rows[i]['director']
                }
                else if(type == 'book'){
                    creator = rows[i]['author']
                }
                else if(type == 'album'){
                    creator = rows[i]['artist']
                }
                console.log('title')
                let temp_html = `
                    <div class="col">
                        <div class="card h-100">
                            <img src="${image}"
                                 class="card-img-top">
                            <div class="card-body">
                                <h5 class="card-title">${title}</h5>
                                <p>${star}</p>
                                <p>${creator}</p>
                            </div>
                        </div>
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


        }
    })
}
