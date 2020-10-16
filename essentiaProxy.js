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
        essentiaExtractor.hpcpExtractor();
    }
}

async function getEnergy(audioURL, callbackFn, frameSize = 2048, hopSize = 2048) {
    // load audio file from an url
    audioCtx.resume();
    let audioData = await essentiaExtractor.getAudioChannelDataFromURL(audioURL, audioCtx, 0);

    // modifying default extractor settings
    essentiaExtractor.frameSize = frameSize;
    essentiaExtractor.hopSize = hopSize;
    // settings specific to an algorithm

    // Now generate overlapping frames with given frameSize and hopSize
    // You could also do it using pure JS to avoid arrayToVector and vectorToArray conversion
    let audioFrames = essentiaExtractor.FrameGenerator(audioData, frameSize, hopSize);
    let entropies = [];
    for (var i=0; i<audioFrames.size(); i++) {
        console.log('Processing frame ' + i + ' of ' + audioFrames.size());
        // essentiaExtractor.EnergyBandRatio
        let spectrum = essentiaExtractor.Spectrum(audioFrames.get(i), frameSize);
        let entropy = essentiaExtractor.Entropy(spectrum['spectrum']);
        entropies.push(entropy['entropy']);
    }

    console.log(entropies)
    // plot the feature
    plotArray(entropies);
}

function plotArray(arr){
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 60},
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#myDataViz")
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

  // Now I can use this dataset:
  function bla(data) {

    // Add X axis --> it is a date format
    var x = d3.scaleLinear()
      .domain([0, data.length])
      .range([ 0, width ]);
    svg.append("g")
      .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
      .domain([0, d3.max(data, function(d) { return +d.value; })])
      .range([ height, 0 ]);
    svg.append("g")
      .call(d3.axisLeft(y));

    console.log('Data: '+data);

    // Add the line
    svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("d", d3.line()
        .x(function(d, i) { return x(i) })
        .y(function(d, i) { return y(d.value) })
        )
    }

    bla(arr);
}
