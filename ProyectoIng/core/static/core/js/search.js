$( ".price-range" ).click(function(event) {
    event.preventDefault();
    $( ".price-range" ).removeClass( "bg-secondary text-white" );
    $(this).addClass("bg-secondary text-white");
    var min = $(this).attr("min");
    var max = $(this).attr("max");
    $("input[name='min']").each(function() {
        $(this).attr('value',min);
    });
    $("input[name='max']").each(function() {
        $(this).attr('value',max);
    });
    if($(this).attr("id") != "custom-price-range-item"){
        $("#custom-price-range-item").attr("hidden",true);
        $("#custom-price-range-item").attr("min","");
        $("#custom-price-range-item").attr("max","");
        $("#custom-price-range-item").html("");
    }
    //Cerrar filtro de precios luego de seleccionar uno
    //$("#prices-collapser").click();
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
        text="Menos de "+currency+max;
    }else if (max==0 || (max==0 && min==0)){
        text="Arriba de "+currency+min;
    }else{
        text=currency+min+"-"+max;
    }
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
    $("input[name='l']").each(function() {
        $(this).attr('value',location);
    });
    //Cerrar filtro de lugares luego de seleccionar uno
    //$("#locations-collapser").click();
});