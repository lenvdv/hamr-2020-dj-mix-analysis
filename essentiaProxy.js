let essentiaExtractor;
// fallback for cross-browser Web Audio API BaseAudioContext
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = new AudioContext();

$(document).ready(function() {
    // instantiate Essentia
    EssentiaWASM().then(async function (WasmModule) {
        essentiaExtractor = new EssentiaExtractor(WasmModule);
    });
});


async function getTempoAsync(audioURL, callbackFunction, frameSize = 40960, hopSize = 20480) {

    let audioData = await essentiaExtractor.getAudioChannelDataFromURL(audioURL, audioCtx, 0);
    let audioFrames = essentiaExtractor.FrameGenerator(audioData, frameSize, hopSize);

    for (var i=0; i<audioFrames.size(); i++) {
        essentiaExtractor.hpcpExtractor(essentiaExtractor.vectorToArray(audioFrames.get(i)));
    }
}


