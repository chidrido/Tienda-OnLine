$(function (){
    let bool;

    tabla_importados();

    function tabla_importados() {
        $('#datos_tabla').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            select: {
                style: 'os',
                selector: 'td:first-child'
            },
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'busca_datos',
                },
                dataSrc: ""
            },
            columns: [
                {"data": "codigo"},
                {"data": "nombre"},
                {"data": "cat.nombre"},
                {"data": "subcat.nombre"},
                {"data": "imagen"},
                {"data": "pvp"},
                {"data": "stock"},
                {"data": "oferta_checkbox"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" style="width: 40px; height: 40px;">';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
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
                        return '<input type="checkbox" value="' + row.oferta_checkbox + '" ' + bool + '>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a href="/adm/importar/editar/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/adm/importar/eliminar/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            },
        });
    }

    // función para los checkbox
    $('#datos_tabla').on('change', 'input[type="checkbox"]', function () {
        let checked = this.checked;
        let codigo = "";
        let nombre = "";
        let categoria = "";
        let subcategoria = "";
        let imagen = "";
        let pvp = "";
        let stock = "";

        $(this).parents("tr").find("td:eq(0)").each(function () {
            codigo = $(this).html();
        });
        $(this).parents("tr").find("td:eq(1)").each(function () {
            nombre = $(this).html();
        });
        $(this).parents("tr").find("td:eq(2)").each(function () {
            categoria = $(this).html();
        });
        $(this).parents("tr").find("td:eq(3)").each(function () {
            subcategoria = $(this).html();
        });
        $(this).parents("tr").find("td:eq(4)").each(function () {
            imagen = $(this).children('img').first().attr('src');
        });
        $(this).parents("tr").find("td:eq(5)").each(function () {
            pvp = $(this).html();
        });
        $(this).parents("tr").find("td:eq(6)").each(function () {
            stock = $(this).html();
        });

        let parametros = {
            'action': 'checkbox_importar',
            'checked': checked,
            'codigo': codigo,
            'nombre': nombre,
            'categoria': categoria,
            'subcategoria': subcategoria,
            'imagen': imagen,
            'pvp': pvp,
            'stock': stock,
        };
        let content = 'Confirme el pedido!';
        modal_alert(window.location.pathname, 'Confirmar!', '¿Añadimos a la Tienda?',parametros, content, function(){
            location.href = window.location.pathname;
        });


    });
});
