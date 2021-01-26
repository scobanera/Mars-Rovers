/* Main Javascrip file for the web app.
 *
 * The JS is responsible for displaying the grid according to the backend information.
 * No logic regarding rovers position is included here.
 */

var server = "https://navigation-dot-scobanera-mars-rover-ibm.rj.r.appspot.com/"
var activeRovers = {}; // List of rovers currently positioned at a certain cell in the grid.

$(document).ready(function() {
	getGridSize();
	printGrid();
});

function getGridSize() {
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", server + "grid/size", false);
	xhttp.send();

	var response = JSON.parse(xhttp.responseText);
	document.getElementById("grid-rows").value = parseInt(response.max_y) - 1;
	document.getElementById("grid-columns").value = parseInt(response.max_x) - 1;
}

/*
 * Prints the grid according to the existing number of rows and columns.
 */
function printGrid() {
	var rows = document.getElementById("grid-rows").value;
	var columns = document.getElementById("grid-columns").value;

	var grid = document.getElementById("grid");
	grid.innerHTML = "";

	// The upper right coordinate 'x', correspon to a total of 'x + 1' columns. 
	let totalColumns = parseInt(columns) + 1;
	grid.style.gridTemplateColumns = "repeat(" + totalColumns + ", auto)";

	var row, column;
	for(row = rows; row >= 0; row--){
		for(column = 0; column <= columns; column++){
			let newCell = document.createElement("div");
			newCell.id = "cell" + row + column;
			if (activeRovers[newCell.id] == null){
				newCell.innerText = " ";
			} else {
				newCell.innerText = activeRovers[newCell.id].join(" - ");
			}
			
			grid.appendChild(newCell);
		}
	}
}

/*
 * Resizes the grid to the selected number of rows and columns.
 *
 * After resizing the grid, existing rovers are removed from the grid. Althoug resizing
 * a grid doesn't neccearly impact the rovers, it is assumed that they return to their
 * base position until they are launched again according to the new grid system.
 */
function resizeGrid() {
	var body = {};
	body["max_x"] = parseInt(document.getElementById("grid-columns").value) + 1;
	body["max_y"] = parseInt(document.getElementById("grid-rows").value) + 1;

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			printGrid();
		}
	};
	xhttp.open("POST", server + "grid/resize", true);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send(JSON.stringify(body));

	deleteRovers();
}

/*
 * Creates a rover at the selected position and specified direction.
 */
function createRover() {
	var body = {};
	body["pos_x"] = document.getElementById("new-x").value;
	body["pos_y"] = document.getElementById("new-y").value;
	body["direction"] = document.getElementById("new-dir").value;

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var response = JSON.parse(xhttp.responseText);

			appendRoverCommandPanel(body, response["id"]);
			setActiveRover("cell" + body["pos_y"] + body["pos_x"], body["direction"]);
			printGrid();
		}
	};

	xhttp.open("POST", server + "rovers/create", true);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send(JSON.stringify(body));
}

/*
 * Append the rover to the list of active rovers.
 *
 * @param {string} cell Cell code where the rover has to be placed
 * @param {string} direction Rover direction.
 */
function setActiveRover(cell, direction) {
	if(activeRovers[cell] != null){
		activeRovers[cell].push(direction);
	} else {
		activeRovers[cell] = [direction];
	}	
}

/*
 * Removes the rover from its current position. Rover has to be present on indicated cell.
 *
 * @param {string} code Cell code where the rover is currently placed.
 * @param {string} direction Rover direction.
 */
function removeActiveRover(cell, direction) {
	let roverIndex = activeRovers[cell].indexOf(direction);
	activeRovers[cell].splice(roverIndex, 1);
}

/*
 * Create a command panel for the new Rover.
 *
 * @param {dict} rover Rover containing its coordinates and current direction.
 * @param {string} rover_id
 */
function appendRoverCommandPanel(rover, rover_id){
	let panel = document.createElement("div");
	panel.id = rover_id;

	let startPosition = document.createElement("p");
	startPosition.setAttribute("id", "start-" + rover_id);
	startPosition.innerText = "Start position: Column: " + rover["pos_x"] + " - Row: " + rover["pos_y"] + " - Dir: " + rover["direction"];

	let commandInput = document.createElement("input");
	commandInput.setAttribute("type", "text");
	commandInput.setAttribute("id", "command-" + rover_id);

	let commandExecution = document.createElement("input");
	commandExecution.setAttribute("id", "reposition-" + rover_id);
	commandExecution.setAttribute("type", "button");
	commandExecution.setAttribute("value", "Execute");
	commandExecution.onclick = function() {repositionRover(rover_id, rover);};

	panel.appendChild(startPosition);
	panel.appendChild(commandInput);
	panel.appendChild(commandExecution);

	document.getElementById("rovers-list").appendChild(panel);
}

/*
 * Move the rover to a new position after executing the user commands.
 *
 * @param {string} rover_id
 * @param {dict} origin Initial rover position.
 */
function repositionRover(rover_id, origin) {
	var body = {};
	body["id"] = rover_id;
	body["commands"] = document.getElementById("command-" + rover_id).value;

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var response = JSON.parse(xhttp.responseText);
			// TODO(scobanera): avoid the mapping by using a consistent name in the server response.
			response["pos_x"] = response["x"];
			response["pos_y"] = response["y"];


			appendRoverDestination(rover_id, response);
			removeActiveRover("cell" + origin["pos_y"] + origin["pos_x"], origin["direction"]);
			document.getElementById("reposition-" + rover_id).onclick = function() {repositionRover(rover_id, response);};
			setActiveRover("cell" + response["y"] + response["x"], response["direction"]);
			printGrid();
		}
	};

	let endpoint = "rovers/" + rover_id + "/move";
	xhttp.open("POST", server + endpoint,  true);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send(JSON.stringify(body));
}


function appendRoverDestination(rover_id, destination){
	var roverPanel = document.getElementById(rover_id);

	var endPositionId = "end-position-" + rover_id;
	var endPosition = document.getElementById(endPositionId);

	// First time a command is executed the element needs to be created.
	if (endPosition == null){
		var endPosition = document.createElement("p");
		endPosition.id = endPositionId;
		roverPanel.appendChild(endPosition);
	}

	endPosition.innerText = "End position: Column: " + destination["x"] + " - Row: " + destination["y"] + " - Dir: " + destination["direction"];
}

function deleteRovers() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			alert("Rovers have been removed from the plateau.");
		}
	};

	xhttp.open("POST", server + "rovers/delete",  true);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send();

	document.getElementById('rovers-list').innerText = '';
	activeRovers = {}
	printGrid();
}