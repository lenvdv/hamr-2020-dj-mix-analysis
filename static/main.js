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
        var x = data.points[0].x
        console.log('Clicked on '+x);
        audioJumpTo(x);
    });
});

function audioJumpTo(time_as_ratio){
    // Jump to a time in the audio
    //   time_to_ratio should be a _relative_ starting point,
    //   0.0 being the start of the audio, 0.5 being halfway, 1.0 being the end.
    var time = time_as_ratio * audioplayer.duration;
    console.log('Current time of audio: ' + audioplayer.currentTime);
    console.log('Duration of audio: ' + audioplayer.duration);
    audioplayer.currentTime = time;
    console.log('Set time of audio to ' + audioplayer.currentTime);
}

function audioSeek(amount){
    // Jump forwards or backwards in the music by increments of "amount" seconds. Amount can be negative.
    console.log('Current time of audio: ' + audioplayer.currentTime);
    audioplayer.currentTime += amount; 
    console.log('Set time of audio to ' + audioplayer.currentTime);
}