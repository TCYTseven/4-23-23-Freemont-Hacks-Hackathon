var sec = 0;
var min = 0;
var hrs = 0;

var interval;

function twoDigits(digit) {
	if(digit < 10) {
		return('0' + digit)
	} else {
		return(digit)
	}
}

function start() {
	if (!interval) {
		counter()
		interval = setInterval(counter, 1000)
	}
}

function pause() {
	clearInterval(interval)
	interval = null
}

function restart() {
	clearInterval(interval)
	interval = null
	sec = 0;
	min = 0;
	hrs = 0;
	document.getElementById('text_cronometro').innerText = '00:00:00'
}

function counter() {
	sec++

	if(sec == 60) {
		min++
		sec = 0

		if(min == 60) {
			hrs++
			min = 0
		}
	}

	document.getElementById('text_cronometro').innerText = twoDigits(hrs) + ':' + twoDigits(min) + ':' + twoDigits(sec)
}
