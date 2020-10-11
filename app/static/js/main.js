function renderPageContent(evt){
    let targetPage;
    var ready = false;
    if(typeof evt === 'string'){
        targetPage = evt;
    }
    else {
        // Ignore are socket stuff for now

        // if(socket){
        //     socket.emit('stop_mosaic');
        // }
        targetPage = $(evt.target).attr('href');
    }

    console.log("blaaa");

    targetPage = targetPage.slice(1);
    $.ajax({
        url: "/getPage?type=" + targetPage,
        dataType: 'html'
    }).done(function(response) {
        $('.page-content').html(response);
        ready = true;
    });
}

function submit_run(evt){
    console.log("called submit")
    // Get data from select fields format is [elementType]#[id]
    let eps = $('select#eps-select').val()
    let discount = $('select#discount-select').val()

    $.ajax({
        url: "/run_ajax",
        data: {'data': JSON.stringify({'eps': eps, 'discount': discount})},
        dataType: 'json'
    }).done(function(response) {
        // do something with results, this shows the response in console
        console.log(response)

        let newVidElm = $('<video id="first-vid" width="480" height="360" controls></video>')
            .append('<source type="video/mp4" />').attr({'src': response[0]});

        $('#first-vid').replaceWith(newVidElm);

    });

}

$('header').on('click', '.menu-item-id', renderPageContent);
// This means call submit_run once the element with id run_btn is clicked within the body element
$('body').on('click', '#run-btn', submit_run);