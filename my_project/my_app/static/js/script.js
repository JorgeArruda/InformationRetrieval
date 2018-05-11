function handleFiles(event) {
    var file = event.target.files[0];
    console.log("Upload:", file);

    var xhr = new XMLHttpRequest();
    (xhr.upload || xhr).addEventListener('progress', function (event) {
        var done = event.position || event.loaded;
        var total = event.totalSize || event.total;
        console.log('xhr progress: ' + Math.round(done / total * 100) + "%");
    });
    xhr.onreadystatechange = function(){
        if ( xhr.readyState == 4 && xhr.status == 200) {
            console.log(xhr.responseText);
        }
    };
    xhr.open('post', 'sendfile', true);
    var fd = new FormData();
    fd.append('filename', file.name);
    fd.append('file', file);
    xhr.send(fd);
}