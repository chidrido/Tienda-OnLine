// crea la DataTable de la cesta de compra con su buscador 'tblProductos'
let tblProductos;
let tblBuscarProductos;
let ventas = {
    items: {
        cliente: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        pvp: 0.00,
        total: 0.00,
        productos: []
    },
    calcula_factura: function () {
        let subtotal = 0.00;
        $.each(this.items.productos, function (pos, dict) {
            dict.pos = pos;
            dict.subtotal = dict.cant * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
    },
    add: function (item) {
        this.items.productos.push(item);
        this.list();
    },
    // crea la tabla del cajero
    list: function () {
        this.calcula_factura();
        tblProductos = $('#tblProductos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.productos,
            columns: [
                {"data": "id"},
                {"data": "nombre"},
                {"data": "cat.nombre"},
                {"data": "pvp"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="eliminar" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2) + ' €';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2) + ' €';
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    step: 1
                });

            },
            initComplete: function (settings, json) {

            }
        });
    },
};

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    if (!Number.isInteger(repo.id)) {
        return repo.text;
    }

    let option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.nombre + '<br>' +
        '<b>Categoría:</b> ' + repo.cat.nombre + '<br>' +
        '<b>PVP:</b> <span class="badge badge-warning">' + repo.pvp + '&nbsp€</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {

    // crea la función select2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    // función date_joined para crear el almanaque
    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });

    //función TouchSpin
    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        ventas.calcula_factura();
    })
        .val(0.12);

    // busqueda de clientes
    $('select[name="cliente"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'buscar_clientes'
                };
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },

        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
    });

    // activa evento modal cliente con botón
    $('.btnAgregarCliente').on('click', function () {
        $('#modalCliente').modal('show');
    });

    // limpia el modal crear cliente
    $('#modalCliente').on('hidden.bs.modal', function () {
        $('#frmCliente').trigger('reset');
    });

    // cierra el modal
    $('.btnCerrar').on('click', function () {
        $('#modalCliente').modal('hide');
    });

    // evento cliente form
    $('#frmCliente').on('submit', function (e) {
        e.preventDefault();
        let parameters = new FormData(this);
        parameters.append('action', 'crear_cliente');
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Confirma crear cliente?', parameters, function (response) {
            $('#modalCliente').modal('hide');
        });
    });

    //elimina productos de la cesta
    $('.btnBorrarTodo').on('click', function () {
        if (ventas.items.productos.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            ventas.items.productos = [];
            ventas.list();
        }, function () {

        });
    });

    // eventos de 'cant' (cantidad)
    $('#tblProductos tbody')
        .on('click', 'a[rel="eliminar"]', function () {
            let tr = tblProductos.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?', function () {
                ventas.items.productos.splice(tr.row, 1);
                ventas.list();
            }, function () {

            });
        })
        .on('change', 'input[name="cant"]', function () {
            console.clear();
            let cant = parseInt($(this).val());
            let tr = tblProductos.cell($(this).closest('td, li')).index();
            ventas.items.productos[tr.row].cant = cant;
            ventas.calcula_factura();
            $('td:eq(5)', tblProductos.row(tr.row).node()).html('€' + ventas.items.productos[tr.row].subtotal.toFixed(2));
        });


    //función limpiar búsqueda del artículo de la cesta
    /*$('.btnLimpiarBusqueda').on('click', function () {
        $('input[name="buscarProducto"]').val('').focus();
        $('input[name="buscar_codigo"]').val('').focus();
    });*/

    //buscador de productos
    $('.btnBuscarProducto').on('click', function () {
        tblBuscarProductos = $('#tblBuscarProductos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'busca_productos',
                    'term': $('select[name="buscar_nombre"]').val()
                },
                dataSrc: ""
            },
            columns: [
                {"data": "nombre"},
                {"data": "cat.nombre"},
                {"data": "pvp"},
                {"data": "imagen"},
                {"data": "stock"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2) + ' €';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 40px; height: 40px;">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a rel="add" class="btn btn-success btn-xs btn-flat"><i class="fas fa-plus"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            },


        });
        $('#modalBuscador').modal('show');
    });

    //buscador de productos con ajax
    /*('input[name="buscarProducto"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'busca_productos',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            ui.item.cant = 1;
            ui.item.subtotal = 0.00;
            ventas.add(ui.item);
            $(this).val('');
        }
    });*/

    // eventos del buscador de productos
    $('#tblBuscarProductos tbody')
        .on('click', 'a[rel="add"]', function () {
            let tr = tblBuscarProductos.cell($(this).closest('td, li')).index();
            let producto = tblBuscarProductos.row(tr.row).data();
            producto.cant = 1;
            producto.subtotal = 0.00;
            ventas.add(producto);
        });

    // event submit
    $('#frmVenta').on('submit', function (e) {
        e.preventDefault();

        if (ventas.items.productos.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        ventas.items.date_joined = $('input[name="date_joined"]').val();
        ventas.items.cliente = $('select[name="cliente"]').val();
        let parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('ventas', JSON.stringify(ventas.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
            alert_action('Notificación', '¿Quiere imprimir la factura?', function () {
                window.open('/adm/ventas/factura/pdf/' + response.id + '/', '_blank');
                location.href = '/adm/ventas/lista/';
            }, function () {
                location.href = '/adm/ventas/lista/';
            });
        });
    });

    // ventas.list();

    // select por nombre
    $('select[name="buscar_codigo"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'busca_productos_por_codigo'
                };
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        let data = e.params.data;
        if(!Number.isInteger(data.id)){
            return false;
        }
        data.cant = 1;
        data.subtotal = 0.00;
        ventas.add(data);
        $(this).val('').trigger('change.select2');
    });

    // select por nombre
    $('select[name="buscar_nombre"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'busca_productos_select'
                };
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        let data = e.params.data;
        if(!Number.isInteger(data.id)){
            return false;
        }
        data.cant = 1;
        data.subtotal = 0.00;
        ventas.add(data);
        $(this).val('').trigger('change.select2');
    });
});