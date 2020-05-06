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
    $("#price-range-all").click();
    //Mostrar solo los rangos de precio en la moneda seleccionada
    $(".price-range").each(function() {
        //Mantener siempre el Rango de Precio "Todo"
        if($(this).attr('id') == "price-range-all" || $(this).attr('id') == "custom-price-range-item"){
            $(this).attr('currency',currency);
        }else{
            //Mostrar los que tengan la misma moneda, ocultar los demas
            if($(this).attr('currency') == currency){
                $(this).attr('hidden',false);
            }else{
                $(this).attr('hidden',true);
            }
        }
    });
    //Asignar moneda de busqueda
    $("input[name='search_currency']").each(function() {
        $(this).attr('value',currency);
    });
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