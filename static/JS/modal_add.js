// modal_add.js

// Aguarda o carregamento completo do DOM
document.addEventListener("DOMContentLoaded", function () {
    // Seleciona os elementos do DOM
    const form = document.querySelector("form");
    const modal = document.querySelector(".popup");
    const buttonClose = document.querySelector(".button-red-modal");

    // Adiciona um listener ao formulário para lidar com o envio
    if (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault(); // Previne o comportamento padrão de envio do formulário
            const formData = new FormData(form);

            // Envia os dados do formulário via fetch
            fetch(form.action, {
                method: form.method,
                body: formData
            })
            .then(response => response.json()) // Converte a resposta para JSON
            .then(data => {
                modal.classList.add("open-popup"); // Abre o modal
                document.getElementById("item-id").textContent = data.id; // Atualiza o ID no modal
            })
            .catch(error => console.error("Erro ao enviar o formulário:", error)); // Trata erros
        });
    }

    // Fecha o modal ao clicar no botão de fechar
    if (buttonClose) {
        buttonClose.onclick = function () {
            modal.classList.remove("open-popup"); // Remove a classe que exibe o modal
            window.location.href = window.indexUrl; // Redireciona para a página inicial
        };
    }
});

// Função para redirecionar ao índice
function redirectToIndex() {
    window.location.href = window.indexUrl;
}