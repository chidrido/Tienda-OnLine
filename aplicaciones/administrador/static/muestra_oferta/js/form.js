$(function () {

    $('a').click(function (e) {
        let variable = $(this).attr('value');                             // obtiene id del producto
        console.log('indice : ' + variable);

        $.ajax({                                                        // llamamos a ajax
            url: window.location.pathname,
            type: 'POST',
            data: {
                id: variable,
            },
            dataType: 'json',
            cache: true,
            success: function (response) {
                console.log(response);
                $.each(response, function (key, value) {
                    resultado = value;
                    console.log('resultado : ', resultado);
                    let nombre = resultado['nombre'];
                    let precio = resultado['pvp'];
                    let imagen = resultado['imagen'];
                    let desc = resultado['desc'];

                    $("#nombre").html(nombre);
                    $("#precio").html(precio + ' €');
                    $("#imagen").html(imagen);
                    $("#mi_imagen").attr("src", imagen);
                    $("#desc").html(desc);

                });

            },
        }).done(function (data) {
            // console.log(data);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });

    });
    $('#btn_agregarFavoritos').on('click', function (){
       alert("a");
    });
});