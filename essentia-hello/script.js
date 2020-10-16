let essentiaExtractor;
let audioURL = "https://freesound.org/data/previews/328/328857_230356-lq.mp3";
let audioData;
// fallback for cross-browser Web Audio API BaseAudioContext
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = new AudioContext();

$(document).ready(function () {
    // Now let's load the essentia wasm back-end
    EssentiaWASM().then(async function (WasmModule) {
        essentiaExtractor = new EssentiaExtractor(WasmModule);
        extract();
    });
});

async function extract(frameSize=4096, hopSize=2048) {
    audioData = await essentiaExtractor.getAudioChannelDataFromURL(audioURL, audioCtx, 0);
    let audioFrames = essentiaExtractor.FrameGenerator(audioData, frameSize, hopSize);
    let hpcpgram = [];
    for (var i=0; i<audioFrames.size(); i++) {
      hpcpgram.push(essentiaExtractor.hpcpExtractor(essentiaExtractor.vectorToArray(audioFrames.get(i))));
    }
}
