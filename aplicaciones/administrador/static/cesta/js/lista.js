let tblCesta;

$(function () {
    tblCesta = $('#datos_cesta').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        paging: false,
        info: false,
        searching: false,
        select: {
            style:    'os',
            selector: 'td:first-child'
        },
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'busca_datos_cesta',              // 'busca_datos' es la variable usada en el método POST
            },
            dataSrc: "",

        },
        columns: [
            {"data": "imagen"},
            {"data": "nombre"},
            {"data": "lista_cuartos"},
            {"data": "pvp"},
            {"data": "cant"},
            {"data": "subtotal"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let icono_basura = '<a href="/adm/cesta/eliminar/' + row.id + '/"><i class="ti-trash remove-icon"></i></a> ';
                    return icono_basura;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    return parseFloat(data).toFixed(2) + ' €';
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + data + '">';
                }
            },
            {
                targets: [-4],
                class: 'text-center',
                render: function (data, type, row) {
                    return parseFloat(data).toFixed(2) + ' €';
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                render: function (data, type, row) {
                    console.log(data)
                    if(data == 'cuarto') {
                        return "<select class='pilihan form-control form-control-sm input-sm' name='cuartos'>" +
                            "<option value='cuarto'>1/4 Kg</option>" +
                            "<option value='medio'>1/2 Kg</option>" +
                            "<option value='unidad'>1 Kg</option>" +
                            "</select>";
                    }else if(data == 'medio'){
                        return "<select class='pilihan form-control form-control-sm input-sm' name='cuartos'>" +
                            "<option value='medio'>1/2 Kg</option>" +
                            "<option value='cuarto'>1/4 Kg</option>" +
                            "<option value='unidad'>1 Kg</option>" +
                            "</select>";
                    }else if(data == 'unidad'){
                        return "<select class='pilihan form-control form-control-sm input-sm' name='cuartos'>" +
                            "<option value='unidad'>1 Kg</option>" +
                            "<option value='medio'>1/2 Kg</option>" +
                            "<option value='cuarto'>1/4 Kg</option>" +
                            "</select>";
                    }else{
                        return ""
                    }
                }
            },
            {
                targets: [-6],
                class: 'text-center',
            },
            {
                targets: [-7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + data + '" class="img-fluid d-block mx-auto">';
                }
            },
        ],
        rowCallback(row, data, displayNum, displayIndex, dataIndex) {
            // console.log('row', row);
            // console.log('data', data);
            $(row).find('input[name="cant"]').TouchSpin({
                min: 1,
                max: 1000000000,
                step: 1
            });
        },
    });

});