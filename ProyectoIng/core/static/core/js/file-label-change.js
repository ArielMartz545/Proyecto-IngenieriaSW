$('input[type="file"]').change(function(e) {
    var filename ="";
    var len = e.target.files.length;
    for (let i = 0; i < len; i++) {
        if (i != 0){
            filename += ", ";
        }
        filename += shortName(e.target.files[i].name);
    }
    var nextSibling = e.target.nextElementSibling
    nextSibling.innerText = filename
});

function shortName (filename){
    if (filename.length > 15){
        var split = filename.split(".");
        filename = filename.substring(0,10) + "..." + split[split.length-1];
    }
    return filename;
}


  