$(function () {
    $('#import_csv').on('click', function (e) {
        e.preventDefault();
        let parametros = {
            'action': 'importar_csv',
        };
        console.log(parametros);
        modal_alert(window.location.pathname, 'Importar CSV', '¿Confirma importar CSV?', parametros, function () {
            location.href = window.location.pathname;
        });
    });
});

