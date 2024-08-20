// función DataTable para crear la tabla e importar los datos de esta
$(function () {
    $('#datos_favoritos').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        paging: false,
        info: false,
        searching: false,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'busca_datos'              // 'busca_datos' es la variable usada en el método POST
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id_producto.imagen"},
            {"data": "id_producto.nombre"},
            {"data": "id_producto.pvp"},
            {"data": "id_producto.oferta_checkbox"},
            {"data": "id"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + data + '" class="img-fluid d-block mx-auto">';
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                orderable: false,
            },
            {
                targets: [-4],
                class: 'text-center',
                render: function (data, type, row) {
                    return parseFloat(data).toFixed(2) + ' €';
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                render: function (data, type, row) {
                    console.log(data);
                    if (data == true) {
                        return '<span class="badge badge-warning" style="padding: 10px;"><span">Está en OFERTA</span></span>'
                    }else{
                        return ''
                    }
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let boton = '<a href="/adm/favoritos/eliminar/' + row.id + '/"><i class="ti-trash"></i></a> ';
                    return boton;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let boton = '<a href="/adm/favoritos/agregar_cesta/' + row.id_producto.id + '/"><i class="ti-shopping-cart"></i></a> ';
                    return boton;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});