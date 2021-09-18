(function(){
    // Compruebo si estoy en la página del detalle de una orden
    if (window.location.pathname.includes('/politica-de-cambios/')) {
        var paragraph = document.getElementById("politica");
		var text = document.createTextNode("This just got added");
		paragraph.appendChild(text);
    }
})();
