(function(){
    // Compruebo si estoy en la página del detalle de una orden
    if (window.location.pathname.includes('/account/orders/')) {
        // Almaceno el store_id en una variable.
        let storeId = LS.store.id;
        // Almaceno el order_id en una variable
        let orderId = document.URL.match(/\d+/)[0];
        // Creo y agrego el nuevo botón
        let referenceNode = document.querySelector('.full-width-container');
        let myButton = document.createElement('a');
        myButton.classList.add('btn','btn-primary', 'btn-small', 'full-width-xs', 'm-top', 'pull-right', 
'pull-none-xs');
        myButton.setAttribute('href',`https://ec2-54-208-172-198.compute-1.amazonaws.com?store_id=${storeId}&order_id=${orderId}`);
        myButton.setAttribute('target', '_blank');
        myButton.textContent = 'Devolver un producto';
        referenceNode.append(myButton);
    }
})();
