/*USADA EN EL MODAL DE ELIMINAR ANUNCIO*/
$(".btn-delete").click(function(event) {
    $("#id_ad_delete").val($(this).attr("ad"));
    $("#span_ad_name").html($(this).attr("ad-name"));
});