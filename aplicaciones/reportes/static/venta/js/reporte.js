let datos_rango = null;
let datos_ahora = new moment().format('YYYY-MM-DD');


function generar_reporte() {

    let parametros = {
        'action': 'busca_reportes',
        'comienza_datos': datos_ahora,
        'acaba_datos': datos_ahora
    };

    if(datos_rango !== null){
        parametros['comienza_datos'] = datos_rango.startDate.format('YYYY-MM-DD');
        parametros['acaba_datos'] = datos_rango.endDate.format('YYYY-MM-DD');
    }

    // función DataTable para crear la tabla de reportes
    $('#datos_tabla').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parametros,
            dataSrc: ""
        },
        order: false,
        paging: false,
        ordering: false,
        info: false,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = ['20%','40%','20%','20%'];
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: datos_ahora}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }
        ],
        // columns: [
        //     {"data": "id"},
        //     {"data": "nombre"},
        //     {"data": "desc"},
        //     {"data": "desc"},
        // ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return parseFloat(data).toFixed(2) + '€';
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,

            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {
    // implementa el date range picker
    $('input[name="date_range"]').daterangepicker({
        //applyButtonClasses: 'btn-success'   //cambia el color de los botones
        locale: {
            format: 'YYYY-MM-DD',
            separator: ' / ',
            applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
        }
    }).on('apply.daterangepicker', function (ev, picker) {
        datos_rango = picker;
        generar_reporte();
    }).on('cancel.daterangepicker', function(ev, picker) {
        $(this).data('daterangepicker').setStartDate(datos_ahora);
        $(this).data('daterangepicker').setStartDate(datos_ahora);
        datos_rango = picker;
        generar_reporte();
    });
    console.log(datos_ahora);
    generar_reporte();
});