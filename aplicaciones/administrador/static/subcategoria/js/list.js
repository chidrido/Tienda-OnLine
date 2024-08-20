$(function () {
    let select_cat = '';
    let select_action = 'busca_datos';

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    // Llama al selector de categorías
    $('#select_cat').on('change', function () {
        select_cat = document.getElementById('select_cat').value;
        select_action = "busca_datos_subcategoria";
        tabla_oferta();
    });

    tabla_oferta();

    function tabla_oferta() {
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
                    'datos': select_cat
                },
                dataSrc: ""
            },
            columns: [
                {"data": "id"},
                {"data": "nombre"},
                {"data": "cat"},
                {"data": "desc"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a href="/adm/oferta/editar/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/adm/oferta/eliminar/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
    }
});
