// Using code from https://wavesurfer-js.org/example/audio-element/

// Create an instance
var wavesurfer;
var fileinput;

// Init & load audio file
document.addEventListener('DOMContentLoaded', function() {

    // Init
    wavesurfer = WaveSurfer.create({
        container: document.querySelector('#waveform'),
        waveColor: '#A8DBA8',
        progressColor: '#3B8686',
        // backend: 'MediaElement',
    });

    wavesurfer.once('ready', function() {
        console.log('Using wavesurfer.js ' + WaveSurfer.VERSION);
    });

    wavesurfer.on('error', function(e) {
        console.warn(e);
    });

    fileinput = document.querySelector('#file-input')
    fileinput.onchange = loadFileOfUser;
    console.log('Changed onchange');


    // fetch('./resources/hybridminds.json')
    // .then(response => {
    //     if (!response.ok) {
    //         throw new Error('HTTP error ' + response.status);
    //     }
    //     return response.json();
    // })
    // .then(peaks => {
    //     console.log(
    //         'loaded peaks! sample_rate: ' + peaks.sample_rate
    //     );

    //     // load peaks into wavesurfer.js
    //     wavesurfer.load(
    //         './resources/hybridminds.mp3', peaks.data);
    //     // document.body.scrollTop = 0;
    // })
    // .catch(e => {
    //     console.error('error', e);
    // });

    // toggle play button
    document
        .querySelector('[data-action="play"]')
        .addEventListener('click', seekToDummyTime); //wavesurfer.playPause.bind(wavesurfer));
});

function loadFileOfUser(e){
    uploadAudioFileFromMenu(e.target, null);
}

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

function seekToDummyTime(){
    var vid = $("#audio-div")[0];
    console.log(vid.currentTime);
    vid.currentTime = 20; 
    console.log('Setting to 20!')
}