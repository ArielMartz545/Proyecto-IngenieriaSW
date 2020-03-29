function setSizes(){
    var imgContainerWidth = $(".profile-img-container").width();
    $(".profile-img-container").height(imgContainerWidth);
}
$( document ).ready(function() {
    setSizes();
});
$( window ).resize(function() {
    setSizes();
});

function copyLink(id){
    const link = $('#'+id).html();
    const el = document.createElement('textarea');
    el.value = link;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
}
//Mostrar un popover debajo por 3000ms luego ocultarlo
$('[data-toggle="popover"]').popover({
    placement: 'bottom',
    //Animacion 300ms para mostrar 100ms para ocultar
    delay : {
        "show" : 300,
        "hide" : 100
    }
}).on('shown.bs.popover', function () {
    setTimeout(function (a) {
        a.popover('hide');
    }, 3000, $(this));
});