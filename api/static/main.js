// QRCODE READER FROM https://github.com/nimiq/qr-scanner
import QrScanner from "./qrcode-scanner.js";
QrScanner.WORKER_PATH = './static/qrcode-worker.js';

(function ($) {
    var $document = $(document),
        $showResult = $("#show-result"),
        $fileReader = $("#file-reader"),
        $btnFile = $("#read-from-file"),
        $formSearch = $("#search-form"),
        $termSearch = $("#url"),
        $qrModal = $("#qrcode-camera"),
        $cameraVideo = $("#camera-video"),
        qrScanner = null;

    $document.on("clear-all", (event) => {
        $termSearch.val("");
        $showResult.empty();
    });


    $formSearch.on("submit", function submitForm(e) {
        e.preventDefault();

        $showResult.html("Carregando...")

        var url = $termSearch.val();
        if (url) {
            $.ajax({
                "url": "/",
                "type": "POST",
                "data": JSON.stringify({ "url_qrcode": url }),
                "contentType": "application/json; charset=utf-8",
                "success": function processResponse(data) {
                    $showResult.html(
                        JSON.stringify(data, undefined, 2)
                    ).show();
                    hljs.highlightBlock($showResult[0]);
                },
                "error": function handleError(err) {
                    $showResult.html(
                        err.status + ": " + err.statusText
                    )
                }
            });
        }
        return false;
    });

    $btnFile.on("click", (event) => $fileReader.trigger("click"));

    $fileReader.on("change", (event) => {
        const the_file = event.target && event.target.files ? event.target.files[0] : false;
        if (!the_file) {
            return;
        }
        $document.trigger("clear-all");
        QrScanner.scanImage(the_file)
            .then((result) => {
                $termSearch.val(result);
                $formSearch.trigger("submit");
            })
            .catch(e => alert(e || 'No QR code found.'));
    });


    $qrModal.on("shown.bs.modal", (event) => {
        QrScanner.hasCamera().then(hasCamera => {
            if (!hasCamera) {
                alert("Nenhuma camera encontrada");
            }
        });
        qrScanner = new QrScanner($cameraVideo[0], (result) => {
            $termSearch.val(result);
            $formSearch.trigger("submit");
            $qrModal.modal('hide');
        });
        qrScanner.start();
    });

    $qrModal.on("hide.bs.modal", (event) => {
        qrScanner.destroy();
        qrScanner = null;
    });


})(jQuery)