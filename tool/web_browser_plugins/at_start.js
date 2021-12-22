TestPrint()

function TestPrint1() {
	console.log("at_start1.js");
}

function TestPrint2() {
	console.log("at_start1.js");
}

function TestPrint() {
	if (true) {
		TestPrint1();
	}
	else {
		TestPrint2();

	}
	console.log("at_start.js");
}
