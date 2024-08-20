$(function () {
    let select_action = 'busca_datos';
    let select_cat = '';
    let estado;
    let producto = '';
    let bool;

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    // función para el select categorías
    $('#select_cat').on('change', function () {
        select_cat = document.getElementById('select_cat').value;
        select_action = "busca_datos_categoria";

        selectorCategoria();
    });

    selectorCategoria();

    function selectorCategoria() {

        $('#datos_tabla').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': select_action,
                    'estado': estado,
                    'producto': producto,
                    'datos': select_cat
                },
                dataSrc: ""
            },
            columns: [
                {"data": "codigo"},
                {"data": "nombre"},
                {"data": "subcat.nombre"},
                {"data": "imagen"},
                {"data": "pvp"},
                {"data": "stock"},
                {"data": "oferta_checkbox"},
                {"data": "especial"},
                {"data": "activo"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-8],
                    class: 'text-center',
                    orderable: false,
                },
                {
                    targets: [-7],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 40px; height: 40px;">';
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2) + ' €';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if (data > 0) {
                            return '<span class="badge badge-success">' + data + '</span>'
                        }
                        return '<span class="badge badge-danger">' + data + '</span>'
                    }
                },
                {
                    targets: [-4],
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
                        return '<input type="checkbox" name="oferta_checkbox" value="' + row.oferta_checkbox + '" ' + bool + '>';
                    }
                },
                {
                    targets: [-3],
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
                        return '<input type="checkbox" name="oferta_especial" value="' + row.oferta_checkbox + '" ' + bool + '>';
                    }
                },
                {
                    targets: [-2],
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
                        return '<input type="checkbox" name="activos" value="' + row.activo + '" ' + bool + '>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a href="/adm/producto/editar/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/adm/producto/eliminar/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            },
        });
    }

    // función para los checkbox de oferta
    $('#datos_tabla tbody').on('change', 'input[name="oferta_checkbox"]', function () {
        let checked = this.checked;
        let valor = "";
        $(this).parents("tr").find("td:eq(0)").each(function () {
            valor = $(this).html();
        });
        let parametros = {
            'action': 'selecciona_checkbox',
            'checked': checked,
            'valor': valor,
        };
        modal_noRedirect(window.location.pathname, 'Añadir/quitar Ofertas', '¿Quieres añadir/quitar de Ofertas', parametros, function () {
            location.href = "/adm/producto/lista/";
        });
    });

    // función para los checkbox especial
    $('#datos_tabla tbody').on('change', 'input[name="oferta_especial"]', function () {
        let checked = this.checked;
        let valor = "";
        $(this).parents("tr").find("td:eq(0)").each(function () {
            valor = $(this).html();
        });
        let parametros = {
            'action': 'selecciona_checkbox_ayala',
            'checked': checked,
            'valor': valor,
        };
        modal_noRedirect(window.location.pathname, 'Añadir/quitar Ayala', '¿Quieres añadir/quitar Producto Ayala?', parametros, function () {
            location.href = "/adm/producto/lista/";
        });
    });

    // función para los checkbox activados/desactivados
    $('#datos_tabla tbody').on('change', 'input[name="activos"]', function () {
        let checked = this.checked;
        let valor = "";
        $(this).parents("tr").find("td:eq(0)").each(function () {
            valor = $(this).html();
        });
        let parametros = {
            'action': 'selecciona_checkbox_activos',
            'checked': checked,
            'valor': valor,
        };
        modal_noRedirect(window.location.pathname, 'Activar/Desactivar', '¿Quieres Activar/Desactivar el producto?', parametros, function () {
            location.href = "/adm/producto/lista/";
        });
    });
});
