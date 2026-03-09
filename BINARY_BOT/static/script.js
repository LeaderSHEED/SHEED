// PAIR LIST

const pairs = [

"AUDUSD",
"EURUSD",
"GBPUSD",
"USDJPY",
"USDCHF",
"USDCAD",
"NZDUSD",
"EURJPY",
"GBPJPY",
"AUDJPY"

];


// LOAD PAIRS TO SUGGESTION

const datalist = document.getElementById("pairs");

pairs.forEach(pair => {

let option = document.createElement("option");
option.value = pair;

datalist.appendChild(option);

});


// VARIABLES

let cooldown = false;
let timerInterval;


// GET SIGNAL

function getSignal(){

if(cooldown){
alert("Wait for next signal");
return;
}

let pair = document.getElementById("pair").value.toUpperCase();

if(pair === ""){
alert("Select Pair");
return;
}


// BUY SELL RANDOM

let signal = Math.random() > 0.5 ? "BUY" : "SELL";


// LIVE ENTRY TIME (NEXT MINUTE)

let now = new Date();

let h = now.getHours();
let m = now.getMinutes() + 1;

if(m >= 60){
m = 0;
h++;
}

if(h >= 24){
h = 0;
}

h = h < 10 ? "0"+h : h;
m = m < 10 ? "0"+m : m;

let entryTime = h + ":" + m;


// PROBABILITY

let prob = Math.floor(Math.random()*10)+80;


// RESULT BOX

let result = document.getElementById("result");

let signalBox = `
<div style="font-weight:bold">PAIR : ${pair}</div>

<div class="signal-box ${signal.toLowerCase()}">
${signal}
</div>

<div class="entry">ENTRY TIME : ${entryTime}</div>

<div class="prob">PROBABILITY : ${prob}%</div>

<div class="timer" id="timer">Next signal in 60s</div>
`;

result.innerHTML = signalBox;


// HISTORY

let history = document.getElementById("history");

let newHistory = document.createElement("div");

newHistory.className = "suggest";

newHistory.innerText = `${pair} - ${signal} (${entryTime})`;

history.prepend(newHistory);


// COOLDOWN TIMER

cooldown = true;

let timeLeft = 30;

let timer = document.getElementById("timer");

timerInterval = setInterval(function(){

timeLeft--;

timer.innerText = "Next signal in " + timeLeft + "s";

if(timeLeft <= 0){

clearInterval(timerInterval);

cooldown = false;

timer.innerText = "You can get next signal";

}

},1000);

}