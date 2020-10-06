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



    targetPage = targetPage.slice(1);
    $.ajax({
        url: "/getPage?type=" + targetPage,
        dataType: 'html'
    }).done(function(response) {
        $('.page-content').html(response);
        ready = true;
    });
}

$('.menu-item-id').on('click', renderPageContent);
