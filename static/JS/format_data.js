// Importação do Moment.js via CDN (opcional se já estiver no HTML)
document.addEventListener("DOMContentLoaded", function () {
    var dataCells = document.querySelectorAll('td[data-date]');

    dataCells.forEach(function (cell) {
        var data = cell.getAttribute('data-date');
        var dataFormatada = moment(data, 'YYYY-MM-DD').format('DD/MM/YYYY');
        cell.setAttribute('data-formatted-date', dataFormatada);
        cell.innerText = dataFormatada;
    });
});



// Retornar ao Menu Principal
function redirectToIndex() {
    window.location.href = "/"; // Redireciona para a página inicial ("/")
}