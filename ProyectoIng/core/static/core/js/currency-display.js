$( ".currency-display" ).click(function(event) {
    event.preventDefault();
    $( ".currency-display" ).removeClass( "bg-secondary text-white" );
    $(this).addClass("bg-secondary text-white");
    var currency = $(this).attr('currency');
    var classShow = ".price-"+currency; 
    var classHide = ".price-"; 
    $(".currency-display").each(function() {
        if ($(this).attr('currency') != currency) {
            classHide += $(this).attr('currency');
        }
    });
    $(classShow).attr('hidden', false);
    $(classHide).attr('hidden', true);
    //$("#currency-collapser").click();
});

function setSelectedCurrency(){
    $(".currency-display").each(function() {
        if ($(this).attr('selected')) {
            $(this).click();
        }
    });
}

$( document ).ready(function() {
    setSelectedCurrency();
});