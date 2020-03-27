function setThumbSize(){
    var width = $("#img-thumb-container").width();
    $(".img-thumb").width(width);
    $(".img-thumb").height(width);
}
function setBoxSize(){
    var width = $("#img-box-container").width();
    $("#img-box-container").height(width);
}
$( ".img-thumb" ).hover(
    function() {
        $('.img-detail').attr('src',$( this ).attr('src'));
    }, function() {}
);
$( ".img-thumb" ).hover(
    function() {
        $('.img-detail').attr('src',$( this ).attr('src'));
    }, function() {}
);
$( ".img-thumb" ).click(function(event) {
    event.preventDefault();
    $('.img-detail').attr('src',$( this ).attr('src'));
});
$( document ).ready(function() {
    setThumbSize();
    setBoxSize();
});
$( window ).resize(function() {
    setThumbSize();
    setBoxSize();
});