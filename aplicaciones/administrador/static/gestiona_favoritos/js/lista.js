// función DataTable para crear la tabla e importar los datos de esta
$(function () {
    $('#datos_tabla').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'busca_datos'              // 'busca_datos' es la variable usada en el método POST
            },
            dataSrc: ""
        },
        columns: [
            {"data": "codigo"},
            {"data": "nombre"},
            {"data": "cat"},
            {"data": "subcat"},
            {"data": "total"},
            {"data": "total"},

        ],
        columnDefs: [
            // {
            //         targets: [-3],
            //         class: 'text-center',
            //         orderable: false,
            //         render: function (data, type, row) {
            //             return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 35px; height: 35px;">';
            //         }
            // },
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
                    let buttons = '<a href="/adm/categoria/editar/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/adm/categoria/eliminar/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});