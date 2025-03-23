// Alterna a classe 'open-sidebar' no elemento 'sidebar' para exibir/ocultar o menu lateral.
document.getElementById('open_btn').addEventListener('click', function () {
    document.getElementById('sidebar').classList.toggle('open-sidebar');
});