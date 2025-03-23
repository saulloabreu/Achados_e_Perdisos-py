
// JavaScript responsavel pelo Upload dos formularios
function chooseFile() {
    document.getElementById("fileInput").click();
}

document.getElementById("fileInput").addEventListener("change", function() {
    uploadFile();
});

function uploadFile() {
    var fileInput = document.getElementById("fileInput");
    var file = fileInput.files[0];

    if (file) {
        var formData = new FormData();
        formData.append("fileToUpload", file);

        fetch("/upload", {
            method: "POST",
            body: formData
        })
        .then(function(response) {
            if (response.ok) {
                alert("Upload concluído com sucesso!");
            } else {
                alert("Falha ao fazer o upload do arquivo.");
            }
        })
        .catch(function(error) {
            console.error("Erro durante o upload do arquivo:", error);
        });
    } else {
        alert("Selecione um arquivo para fazer upload.");
    }
}