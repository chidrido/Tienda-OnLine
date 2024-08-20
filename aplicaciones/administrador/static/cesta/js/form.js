let cesta = {
    precio: '',
    cantidad: '',
    id_cli: '',
    id_prod: '',
    cuartos: ''
};
let resultado;

$(function () {
    // recupera el valor del input de la celda cantidad
    $('#datos_cesta tbody').on('change', 'input[name="cant"]', function () {
        console.clear();
        cesta.cantidad = parseInt($(this).val());

        let tr = tblCesta.cell($(this).closest('td, li')).index();
        let dat = tblCesta.row(tr.row).data();

        // obtenemos las variables id_cliente, id, precio, cantidad y precio
        cesta.precio = dat['pvp'];
        cesta.id_prod = dat['id'];
        cesta.id_cli = dat['id_cliente'];

        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                action: 'accion_cant',
                data: cesta,
            },
            dataType: 'json',
            cache: true,
            success: function (response) {
                // console.log('response', response);
                $.each(response, function (key, value) {
                    resultado = value;
                    $('td:eq(5)', tblCesta.row(tr.row).node()).html(resultado['cuenta_subtotal'] + ' €');
                    let total = resultado['total'];
                    $("#total").html(total + ' €');
                });
            },
        }).done(function (data) {
            // console.log(data);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    });

    // Guarda la cesta y envía correo
    $('.guardar').on('click', function (e) {
        e.preventDefault();

        let x_mensaje = document.getElementById("mensaje").value;

        let parametros = {
            'action': 'accion_guardar',
            'mensaje': x_mensaje
        };
        restrict_cesta(window.location.pathname, 'Confirmar la compra!', '¿Desea confirmar la compra?', parametros, function () {

        });

        function restrict_cesta(url, titulo, content, parametros) {
            $.confirm({
                title: titulo,
                content: content,
                columnClass: 'small',
                typeAnimated: true,
                cancelButtonClass: 'btn-primary',
                draggable: true,
                dragWindowBorder: false,
                buttons: {
                    info: {
                        text: "Si",
                        btnClass: 'btn-primary',
                        action: function () {
                            $.ajax({
                                url: window.location.pathname,
                                type: 'POST',
                                data: parametros,
                                dataType: 'json',
                                cache: true,
                                async: false,
                                success: function (response) {

                                },
                            }).done(function (data) {
                                console.log(data);
                                $.each(data, function (key, value) {
                                    if (value == 'error') {
                                        Swal.fire({
                                            icon: 'error',
                                            text: 'Para realizar su pedido con transporte gratuito debe tener una cesta superior a 25 €',
                                        });
                                    } else {
                                        Swal.fire({
                                            icon: 'success',
                                            text: 'Su pedido ha sido recibido correctamente',
                                        });
                                        setTimeout(function (){
                                            location.href = "/adm/super/lista";
                                        }, 3000);
                                    }
                                });
                            }).fail(function (jqXHR, textStatus, errorThrown) {
                                alert(textStatus + ': ' + errorThrown);
                            }).always(function (data) {

                            });
                        }
                    },
                    danger: {
                        text: "No",
                        btnClass: 'btn-red',
                        action: function () {
                            location.href = window.location.pathname;
                        }
                    },
                }
            });
        }

    });

    // funcion que activa el evento del select cuartos
    $('#datos_cesta tbody').on('change', 'select[name="cuartos"]', function () {
        console.clear();
        cesta.cuartos = parseInt($(this).val());
        let cuarto = $(this).val();

        let tr = tblCesta.cell($(this).closest('td, li')).index();
        let dat = tblCesta.row(tr.row).data();
        cesta.precio = dat['pvp'];
        cesta.cantidad = dat['cant'];
        // console.log('cantidad', cesta.cantidad);
        cesta.id_prod = dat['id'];
        cesta.id_cli = dat['id_cliente'];
        cesta.cuartos = cuarto;

        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                action: 'accion_cuartos',
                data: cesta,
            },
            dataType: 'json',
            cache: true,
            success: function (response) {
                console.log('response', response);
                $.each(response, function (key, value) {
                    resultado = value;
                    $('td:eq(5)', tblCesta.row(tr.row).node()).html(resultado['cuenta_subtotal'] + ' €');
                    let total = resultado['total'];
                    $("#total").html(total + ' €');
                });
            },
        }).done(function (data) {
            // console.log(data);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    });

});

