document.addEventListener("DOMContentLoaded", function () {
    var url = "/static/upload/{{ item_id }}.pdf"; // Altere o caminho do PDF conforme necessário

    var loadingTask = pdfjsLib.getDocument(url);
    loadingTask.promise.then(function (pdf) {
        var scale = 1.5;
        var canvas = document.getElementById("pdfCanvas");
        var context = canvas.getContext("2d");

        for (var pageNumber = 1; pageNumber <= pdf.numPages; pageNumber++) {
            pdf.getPage(pageNumber).then(function (page) {
                var viewport = page.getViewport({ scale: scale });
                canvas.height = viewport.height;
                canvas.width = viewport.width;

                var renderContext = {
                    canvasContext: context,
                    viewport: viewport,
                };

                page.render(renderContext);
            });
        }
    });
});
