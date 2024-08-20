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
            {"data": "id"},
            {"data": "full_name"},
            {"data": "username"},
            {"data": "date_joined"},
            {"data": "imagen"},
            {"data": "groups"},
            {"data": "id"},
        ],
        columnDefs: [
            // {
            //     targets: [-3],
            //     class: 'text-center',
            //     orderable: false,
            // },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let html = '';
                    $.each(row.groups, function (key, value){
                       html+='<span class="badge badge-success">'+value.name+'</span> ';
                    });
                    return html;
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" class="img-fluid mx-auto d-block" style="width: 30px; height: 30px;">';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="/usuario/editar/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/usuario/eliminar/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});