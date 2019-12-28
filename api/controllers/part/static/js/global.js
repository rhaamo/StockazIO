$(document).ajaxError(function (event, request, settings) {
    show_alert("error", "Ajax query failed", "");
});

function show_message(name, title, message) {
    console.log("Showing message " + message);

    var $dialog_master = $('#dialog-master');
    var $dialog = $dialog_master.clone();
    $dialog.attr("id", "dialog-" + name);
    $dialog.attr("title", title);
    $dialog.html(message);

    $dialog_master.append($dialog);

    $dialog.dialog({
        close: function (event, ui) {
            $(this).dialog("close");
            $(this).remove();
        }
    });

}

function show_alert(type, title, message) {
    $.alert(message, {
        autoClose: true,
        closeTime: 3000,
        type: type,
        position: ['top-right'],
        title: title,
        isOnly: false
    })
}

// Javascript to enable link to tab
var url = document.location.toString();
if (url.match('#')) {
    $('.nav-tabs a[href=#' + url.split('#')[1] + ']').tab('show');
}

// Change hash for page-reload
$('.nav-tabs a').on('shown.bs.tab', function (e) {
    window.location.hash = e.target.hash;
});


// Document Viewer by Modal
$('#contentBody').on("click", ".modalViewerOpen", function () {
    var item = $(this);
    var _datas = $(this).data();

    // Sanity check
    if (_datas.type != "text" && _datas.type != "image" && _datas.type != "pdf") {
        console.log("File Viewer: Unknown type " + _datas.type);
        return false;
    }
    // Pop modal
    $('#modalViewer').modal();
    // Set title
    $('#modalViewerLabel').html("File viewer: " + _datas.filename);
    // Display content
    if (_datas.type == "text") {
        $('#modalViewerBody').html('<pre id="modalViewerPreText"></pre>');
        $('#modalViewerPreText').load(_datas.resource);
    } else if (_datas.type == "image") {
        var str = '<center><img src="' + _datas.resource + '" alt="' + _datas.filename + '" /></center>';
        $('#modalViewerBody').html(str);
    } else if (_datas.type == "pdf") {
        // Inject pdfJS resources
        var str = '<object data="' + _datas.resource + '" type="application/pdf" width="870" height="400">'+
                'alt : <a href="' + _datas.resource + '">' + _datas.resource + '</a></object>';
        $('#modalViewerBody').html(str);
    }

    return false;
});

$('#modalViewer').on('hidden.bs.modal', function (e) {
    // cleanup body, title, resources
    $('#modalViewerResources').html("");
    $('#modalViewerLabel').html("");
    $('#modalViewerBody').html("");
});

