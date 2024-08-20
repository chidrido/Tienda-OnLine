$(function () {

    //ajax para añadir el producto a Cesta
    $('.agregar_cesta').click(function (e) {
        let variable = $(this).attr('value');
        e.preventDefault();
        let parameters = {
            'action': 'busca_id',
            id: variable,
        };
        modal_alert(window.location.pathname, 'Cesta de Compra', '¿Quieres añadir este producto a la Cesta?', parameters, function () {
            location.href = '{{ lista_url }}';
        });
    });

    //ajax para obtener los datos del modal del producto
    $('.btn_modal').click(function (e) {
        let var_prod = $(this).attr('value');                             // obtiene id del producto
        console.log(var_prod);

        $.ajax({                                                        // llamamos a ajax
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'mirar_producto',
                id: var_prod,
            },
            dataType: 'json',
            cache: true,
            // devuelve los datos al modal del producto
            success: function (response) {
                $.each(response, function (key, value) {
                    resultado = value;
                    let producto = resultado['id'];
                    console.log(producto);
                    let nombre = resultado['nombre'];
                    let precio = resultado['pvp'];
                    let imagen = resultado['imagen'];
                    let desc = resultado['desc'];

                    $("#nombre").html(nombre);
                    $("#precio").html(precio + ' €');
                    $("#imagen").html(imagen);
                    $("#mi_imagen").attr("src", imagen);
                    $("#desc").html(desc);
                    $("#id_prod").html(producto);
                });
            },
        }).done(function (data) {
            console.log(data);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });

    });

    // ajax para eliminar producto del modal cesta
    $('.removecantidad').click(function (e) {
        let variable = $(this).attr('value');
        e.preventDefault();
        let parameters = {
            'action': 'borra_prod',
            id: variable,
        };
        modal_alert(window.location.pathname, 'Cesta de Compra', '¿Quieres eliminar el producto de la Cesta?', parameters, function () {
            location.href = '{{ lista_url }}';
        });
    });

    //ajax para añadir a favoritos
    $('.btn_agregarFavoritos').click(function (e) {
        let var_fav = $(this).attr('value');                             // obtiene id del producto

        e.preventDefault();
        let parameters = {
            'action': 'añadir_favoritos',
            id: var_fav,
        };
        modal_alert(window.location.pathname, 'Favoritos', '¿Quieres añadir este producto a Favoritos?', parameters, function () {
            location.href = '{{ lista_url }}';
        });
    });
});