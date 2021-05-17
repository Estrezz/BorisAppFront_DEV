(function(){
    // Compruebo si estoy en la página del detalle de una orden
    if (window.location.pathname.includes('/politica-de-cambios/')) {
        // Almaceno el store_id en una variable.
        let storeId = LS.store.id;
        // Almaceno el order_id en una variable
        //let orderId = document.URL.match(/\d+/)[0];
        // Creo y agrego el nuevo botón
        let referenceNode = document.querySelector('.boris');
        let myButton = document.createElement('a');
        myButton.classList.add('btn','btn-primary', 'btn-small', 'full-width-xs', 'm-top', 'pull-right', 'pull-none-xs');
        //myButton.setAttribute('href',`https://ec2-54-208-172-198.compute-1.amazonaws.com?store_id=${storeId}&order_id=${orderId}`);
        myButton.setAttribute('href',`https://frontprod.borisreturns.com?store_id=${storeId}`);
        myButton.setAttribute('target', '_blank');
        myButton.textContent = 'Cambiar / Devolver un producto';
        referenceNode.append(myButton);
    }
})();
