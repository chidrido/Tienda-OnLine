$(function () {
    let select_action = 'busca_datos';
    let id = ';'
    let bool;

    $('select[name="subcategorias"]').on('change', function () {
        id = $(this).val();
        select_action = 'busca_productos';
        selectorSubCategoria();
    });

    // función que muestra todos los productos
    $('.btn_todo').on('click', function () {
        select_action = 'busca_todo';
        selectorSubCategoria();
    });

    selectorSubCategoria();

    function selectorSubCategoria() {
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
                    'id': id
                },
                dataSrc: ""
            },
            columns: [
                {"data": "id"},
                {"data": "nombre"},
                {"data": "imagen"},
                {"data": "pvp"},
                {"data": "cuartos"},
                {"data": "especial"},
                {"data": "oferta_checkbox"},
                {"data": "activo"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-8],
                    class: 'text-center',
                },
                {
                    targets: [-7],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 35px; height: 35px;">';
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                    orderable: false,
                },
                {
                    targets: [-5],
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
                        return '<input type="checkbox" name="cuartos" value="' + row.cuartos + '" ' + bool + '>';
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
                        return '<input type="checkbox" name="especial" value="' + row.especial + '" ' + bool + '>';
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
                        return '<input type="checkbox" name="oferta" value="' + row.oferta_checkbox + '" ' + bool + '>';
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
                        return '<input type="checkbox" name="activar" value="' + row.activo + '" ' + bool + '>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a href="/adm/gestiona/editar/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/adm/gestiona/eliminar/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
    }

});
