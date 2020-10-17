// Using code from https://wavesurfer-js.org/example/audio-element/

// Create objects
var audioplayer;

// Init & load audio file
document.addEventListener('DOMContentLoaded', function() {

    // Initialize the audio player
    audioplayer = $("#audio-div")[0];

    // Bind event handlers to seek buttons
    var SEEK_AMOUNT = 30;
    $("#audio-seek-forward")[0].addEventListener('click', () => {audioSeek(SEEK_AMOUNT)});
    $("#audio-seek-backward")[0].addEventListener('click', () => {audioSeek(-SEEK_AMOUNT)});

    // Bind event handler to upload button
    $("#file-input")[0].onchange = e => {uploadAudioFileFromMenu(e.target, null)};
});

function uploadAudioFileFromMenu(fileContainer, onLoadExtractor) {
    let reader = new FileReader();
    var blob;

    blob = fileContainer.files[0]

    reader.readAsBinaryString(blob);
    checkUploadFileExtension(blob);

    // if ((blob.size / 1024 / 1024) > FILE_UPLOAD_SIZE_LIMIT) {
    //     alert("Too big file to process! Please a upload a audio file less than " + FILE_UPLOAD_SIZE_LIMIT + "mb!");
    //     throw "Excedees maximum upload file size limit " + FILE_UPLOAD_SIZE_LIMIT + "mb!";
    // }
   
    addToAudioPlayer(blob);
    getTempoAsync(URL.createObjectURL(blob))
    // if (myAppSettings.audioLoaded) { removeAudioButtons() };
  
    // var blobUrl = URL.createObjectURL(blob);
    // here we do the feature extraction and plotting offline using the callback function
    // onLoadExtractor(blobUrl);
}

function checkUploadFileExtension(blob, allowedExtensions=["wav", "mp3", 'ogg']) {
    var filename_split = blob.name.split(".")
    var fileExt = filename_split[filename_split.length - 1];
    fState = $.inArray(fileExt, allowedExtensions) > -1;
    if (!fState) {
        alert('Incompatible audio file format! Only the following file formats are supported at the moment: \n [' + allowedExtensions.join(", ") + ', ]');
        throw "uploaded un-supported audio file format";
    }
}

function addSourceToAudioPlayer(url) {
    $("#audio-source").attr("src", url);
    $("#audio-div")[0].pause();
    $("#audio-div")[0].load();
    $("#audio-div")[0].oncanplaythrough = $("#audio-div")[0].pause();
    // myAppSettings.audioLoaded = true;
}


function addToAudioPlayer(blob) {
    var blobUrl = URL.createObjectURL(blob);
    addSourceToAudioPlayer(blobUrl);
}

function audioSeek(amount){
    console.log('Current time of audio: ' + audioplayer.currentTime);
    audioplayer.currentTime += amount; 
    console.log('Set time of audio to ' + audioplayer.currentTime);
}