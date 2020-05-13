$( document ).ready(function() {
    //Cargar las variables anteriores para mejorar UX
    var search_q = $("#search_var_q").html();
    var search_c = $("#search_var_c").html();
    var search_l = $("#search_var_l").html();
    var search_r = $("#search_var_r").html();
    var search_currency = $("#search_var_currency").html();
    var search_min = $("#search_var_min").html();
    var search_max = $("#search_var_max").html();
    //Cargar el mismo Rating de busqueda
    $(".search-r-option").each(function() {
        if($(this).val() == search_r){
            $(this).attr('selected',true);
        }
    });
    //Cargar la misma Query de busqueda
    $("input[name='search_q']").each(function() {
        $(this).attr('value',search_q);
    });
    //Cargar la misma Category de busqueda
    $(".search-c-option").each(function() {
        if($(this).val() == search_c){
            $(this).attr('selected',true);
        }
    });
    //Cargar la misma Location de busqueda
    $(".location").each(function() {
        if($(this).attr('location') == search_l){
            //Ya hay funcion encargada de seleccionar Location al hacer click
            $(this).click();
        }
    });
    $(".search-l-option").each(function() {
        if($(this).attr('value') == search_l){
            $(this).attr('selected',true);
        }
    });
    //Cargar la misma Currency de busqueda
    $(".currency-display").each(function() {
        if($(this).attr('currency') == search_currency){
            //Ya hay funcion encargada de seleccionar la Currency al hacer click
            $(this).click();
        }
    });
    //Cargar el mismo Price Range de busqueda
    var custom_price_range = true;
    $(".price-range").each(function() {
        if($(this).attr('min') == search_min
        && $(this).attr('max') == search_max){
            //Ya hay funcion encargada de seleccionar Price Range al hacer click
            custom_price_range = false;
            $(this).click();
        }
    });
    if (custom_price_range){
        $("#custom-min-price").attr("value", search_min);
        $("#custom-max-price").attr("value", search_max);
        $("#btn-custom-price").click();
    }
});

$( ".price-range" ).click(function(event) {
    event.preventDefault();
    $( ".price-range" ).removeClass( "bg-secondary text-white" );
    $(this).addClass("bg-secondary text-white");
    var min = $(this).attr("min");
    var max = $(this).attr("max");
    $("input[name='search_min']").each(function() {
        $(this).attr('value',min);
    });
    $("input[name='search_max']").each(function() {
        $(this).attr('value',max);
    });
    if($(this).attr("id") != "custom-price-range-item"){
        $("#custom-price-range-item").attr("hidden",true);
        $("#custom-price-range-item").attr("min","");
        $("#custom-price-range-item").attr("max","");
        $("#custom-price-range-item").html("");
    }
    $(".search-p-option").each(function() {
        if($(this).attr('min') == min && $(this).attr('max') == max){
            $(this).attr("selected",true);
        }else{
            $(this).attr("selected",false);
        }
    });
    //Cerrar filtro de precios luego de seleccionar uno
    //$("#prices-collapser").click();
});

$( "select[name='search_c']" ).change(function(event) {
    var search_c = $(this).children("option:selected").val();
    $(".search-c-option").each(function() {
        if($(this).val() == search_c){
            $(this).attr("selected",true);
        }else{
            $(this).attr("selected",false);
        }
    });
});

$( "select[name='search_p']" ).change(function(event) {
    var search_min = $(this).children("option:selected").attr('min');
    var search_max = $(this).children("option:selected").attr('max');
    $(".price-range").each(function() {
        if($(this).attr('min') == search_min
        && $(this).attr('max') == search_max){
            $(this).click();
        }
    });
});

$( "select[name='search_l']" ).change(function(event) {
    var search_l = $(this).children("option:selected").val();
    $(".location").each(function() {
        if($(this).attr('location') == search_l){
            //Ya hay funcion encargada de seleccionar Location al hacer click
            $(this).click();
        }
    });
});

$( "select[name='search_r']" ).change(function(event) {
    var search_r = $(this).children("option:selected").val();
    $("input[name='search_r']").each(function() {
        $(this).attr('value',search_r);
    });
});

$( "#btn-custom-price" ).click(function(event) {
    event.preventDefault();
    $( ".price-range" ).removeClass( "bg-secondary text-white" );
    var min = $("#custom-min-price").val();
    var max = $("#custom-max-price").val();
    if(min==""){
        min=0;
    }
    if(max==""){
        max=0;
    }
    var currency = $("#custom-price-range-item").attr("currency");
    var currency_text = currency == 1 ? "L" : "$";
    $("#custom-min-price").val("");
    $("#custom-max-price").val("");
    if((max-min)<0 && max!=0){
        //Invertir valores si el usuario los ingreso al reves.
        var temp = min;
        min = max;
        max= temp;
    }
    var text="";
    if(min == 0 && max != 0){
        text="Menos de "+currency_text+max;
    }else if (max==0 || (max==0 && min==0)){
        text="Arriba de "+currency_text+min;
    }else{
        text=currency_text+min+"-"+max;
    }
    $("#search-p-option-custom").attr('selected',true);
    $("#search-p-option-custom").html(text);
    $("#custom-price-range-item").attr("hidden",false);
    $("#custom-price-range-item").attr("min",min);
    $("#custom-price-range-item").attr("max",max);
    $("#custom-price-range-item").html(text);
    $("#custom-price-range-item").click();
});
$('#custom-min-price').keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    //Se presiono Enter
	if(keycode == '13'){
		$("#btn-custom-price").click();	
	}
});
$('#custom-max-price').keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    //Se presiono Enter
	if(keycode == '13'){
		$("#btn-custom-price").click();	
	}
});

$( ".location" ).click(function(event) {
    event.preventDefault();
    $( ".location" ).removeClass( "bg-secondary text-white" )
    $(this).addClass("bg-secondary text-white");
    var location = $(this).attr("location");
    $("input[name='search_l']").each(function() {
        $(this).attr('value',location);
    });
    $(".search-l-option").each(function() {
        if($(this).val() == location){
            $(this).attr("selected",true);
        }else{
            $(this).attr("selected",false);
        }
    });
    //Cerrar filtro de lugares luego de seleccionar uno
    //$("#locations-collapser").click();
});