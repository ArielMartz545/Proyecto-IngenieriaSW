var clicked = 0;
$( document ).ready(function() {
    clicked = $("#stars").val();
});
var emptyStar="<i class='far fa-star text-warning'></i>";
var fullStar="<i class='fas fa-star text-warning'></i>"
$(".star").click(function(event){
    event.preventDefault();
    if ($(this).hasClass("star-1")){
        clicked = 1;
        fill(clicked);
    }else if ($(this).hasClass("star-2")){
        clicked = 2;
        fill(clicked);
    }else if ($(this).hasClass("star-3")){
        clicked = 3;
        fill(clicked);
    }else if ($(this).hasClass("star-4")){
        clicked = 4;
        fill(clicked);
    }else if ($(this).hasClass("star-5")){
        clicked = 5;
        fill(clicked);
    }
    $("#stars").val(clicked);
});

$( ".star" ).hover(function(){
    if ($(this).hasClass("star-1")){
        fill(1);
    }else if ($(this).hasClass("star-2")){
        fill(2);
    }else if ($(this).hasClass("star-3")){
        fill(3);
    }else if ($(this).hasClass("star-4")){
        fill(4);
    }else if ($(this).hasClass("star-5")){
        fill(5);
    }
},function(){
    fill(clicked);
});

function fill(n){
    switch(n) {
        case 1:
            $(".star-1").html(fullStar);
            $(".star-2").html(emptyStar);
            $(".star-3").html(emptyStar);
            $(".star-4").html(emptyStar);
            $(".star-5").html(emptyStar);
            break;
        case 2:
            $(".star-1").html(fullStar);
            $(".star-2").html(fullStar);
            $(".star-3").html(emptyStar);
            $(".star-4").html(emptyStar);
            $(".star-5").html(emptyStar);
            break;
        case 3:
            $(".star-1").html(fullStar);
            $(".star-2").html(fullStar);
            $(".star-3").html(fullStar);
            $(".star-4").html(emptyStar);
            $(".star-5").html(emptyStar);
            break;
        case 4:
            $(".star-1").html(fullStar);
            $(".star-2").html(fullStar);
            $(".star-3").html(fullStar);
            $(".star-4").html(fullStar);
            $(".star-5").html(emptyStar);
            break;
        case 5:
            $(".star-1").html(fullStar);
            $(".star-2").html(fullStar);
            $(".star-3").html(fullStar);
            $(".star-4").html(fullStar);
            $(".star-5").html(fullStar);
            break;
        default:
            $(".star-1").html(emptyStar);
            $(".star-2").html(emptyStar);
            $(".star-3").html(emptyStar);
            $(".star-4").html(emptyStar);
            $(".star-5").html(emptyStar);
    }
}