// contiene lista de ventas
// y también contiene funcion checkbox-pedidos
let tblVentas;
let select_checkbox = 'busca_datos';

function format(d) {
    let html = '<table class="table">';
    html += '<thead class="thead-dark">';
    html += '<tr><th scope="col">Producto</th>';
    html += '<th scope="col">Categoría</th>';
    html += '<th scope="col">Precio</th>';
    html += '<th scope="col">Cantidad</th>';
    html += '<th scope="col">Subtotal</th></tr>';
    html += '</thead>';
    html += '<tbody>';
    $.each(d.det, function (key, value) {
        html += '<tr>'
        html += '<td>' + value.prod.nombre + '</td>'
        html += '<td>' + value.prod.cat.nombre + '</td>'
        html += '<td>' + value.precio + '</td>'
        html += '<td>' + value.cant + '</td>'
        html += '<td>' + value.subtotal + '</td>'
        html += '</tr>';
    });
    html += '</tbody>';
    return html;
}

$(function () {
    let bool;

    tabla_pedidos();

    function tabla_pedidos() {
        tblVentas = $('#datos_tabla').DataTable({
            responsive: true,
            // scrollX: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': select_checkbox
                },
                dataSrc: ""
            },
            columns: [
                // {
                //     "className": 'dt-control',
                //     "orderable": false,
                //     "data": null,
                //     "defaultContent": ''
                // },
                {"data": "pedido_checkbox"},
                {"data": "id"},
                {"data": "cliente.first_name"},
                {"data": "cliente.last_name"},
                {"data": "date_joined"},
                {"data": "cliente.direccion"},
                {"data": "cliente.telefono"},
                {"data": "subtotal"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-9],
                    checkboxes: {
                        selectRow: true,
                    },
                    class: 'text-center',
                    orderable: false,
                    className: 'select-checkbox',
                    render: function (data, type, row) {
                        if (data == true) {
                            bool = 'checked';
                        } else {
                            bool = '';
                        }
                        return '<input type="checkbox" value="' + row.pedido_checkbox + '" ' + bool + '>';
                    }
                },
                {
                    targets: [-3, -5, -8],
                    class: 'text-center',
                    orderable: false,
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2) + ' €';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a href="/adm/ventas/eliminar/' + row.id + '/" style="margin-right: 2px;" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                        buttons += '<a href="/adm/ventas/editar/' + row.id + '/" style="margin-right: 2px;" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a>';
                        buttons += '<a rel="detalles" style="margin-right: 2px;" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a>';
                        buttons += '<a href="/adm/ventas/factura/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a>';

                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
    }

    // eventos de 'cant' (cantidad)
    $('#datos_tabla tbody')
        .on('click', 'a[rel="detalles"]', function () {
            let tr = tblVentas.cell($(this).closest('td, li')).index();
            let data = tblVentas.row(tr.row).data();
            $.each(data.det, function (key, value) {
                resultado = value;
                $("#mensaje_nota").html(resultado['mensaje']);
            });
            $('#tblDetalle').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'busqueda_detalles_producto',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "prod.nombre"},
                    {"data": "prod.cat.nombre"},
                    {"data": "precio"},
                    {"data": "cant"},
                    {"data": "cuartos"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return parseFloat(data).toFixed(2) + ' €';
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            if (data == '0.5') {
                                return '1/2 K'
                            } else if (data == '0.25') {
                                return '1/4 K'
                            } else if (data == '1') {
                                return '1 K'
                            } else {
                                return data
                            }
                        }
                    },
                    {
                        targets: [-3, -4, -5],
                        class: 'text-center',
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#miModeloDetalle').modal('show');
        })
        .on('click', 'td.dt-control', function () {
            let tr = $(this).closest('tr');
            let row = tblVentas.row(tr);
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                row.child(format(row.data())).show();
                tr.addClass('shown');
            }
        });

    // función para los checkbox
    $('#datos_tabla').on('change', 'input[type="checkbox"]', function () {
        let checked = this.checked;
        let id = "";
        $(this).parents("tr").find("td:eq(1)").each(function () {
            id = $(this).html();
        });

        let parametros = {
            'action': 'checkbox_pedidos',
            'checked': checked,
            'id': id,
        };
        let content = 'Confirme el pedido!';
        modal_alert(window.location.pathname, 'Confirmar!', 'Confirmar Agregar/Quitar pedido', parametros, content, function () {
            location.href = window.location.pathname;
        });


    });

    $('#selecciona_checkbox').on('click', function () {
        select_checkbox = document.getElementById('selecciona_checkbox').value;
        console.log(select_checkbox);

        tabla_pedidos();
    });

});




