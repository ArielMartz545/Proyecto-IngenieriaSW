function setSizes(){
    var thumbWidth = $(".slide-thumbs").width();
    $(".thumb").width(thumbWidth);
    $(".thumb").height(thumbWidth);
    var slideImgWidth = $(".slide-img-container").width();
    $(".slide-img-container").height(slideImgWidth);
    $(".slide-thumbs").height(slideImgWidth);
}
$( ".thumb" ).hover(
    function() {
        //Mostrar la imagen miniatura en grande
        $('.slide-img').attr('src',$( this ).attr('src'));
        //Cambiar el alternativo de la imagen
        $('.slide-img').attr('alt','Imagen detalle '+$( this ).attr('id'));
    }, function() {}
);
$( ".thumb" ).click(function(event) {
    event.preventDefault();
    //Mostrar la imagen miniatura en grande
    $('.slide-img').attr('src',$( this ).attr('src'));
    //Cambiar el alternativo de la imagen
    $('.slide-img').attr('alt','Imagen detalle '+$( this ).attr('id'));
});
$( document ).ready(function() {
    setSizes();
});
$( window ).resize(function() {
    setSizes();
});