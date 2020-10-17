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

    // If it exists, bind javascript to plotly
    var myPlot = $('.plotly-graph-div')[0];

    console.log(myPlot)

    myPlot.on('plotly_click', function(data){
        var pts = '';
        for(var i=0; i < data.points.length; i++){
            pts = 'x = '+data.points[i].x +'\ny = '+
                data.points[i].y.toPrecision(4) + '\n\n';
        }
        console.log(pts)
        alert('Closest point clicked:\n\n'+pts);
    });
});

function audioSeek(amount){
    console.log('Current time of audio: ' + audioplayer.currentTime);
    audioplayer.currentTime += amount; 
    console.log('Set time of audio to ' + audioplayer.currentTime);
}