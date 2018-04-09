function create_character_selector(character_list) {
	var myDiv = document.getElementById("characterDiv");

	//Create and append select list
	var selectList = document.createElement("select");
	selectList.id = "characterSelect";
	myDiv.appendChild(selectList);

	//Create and append the options
	for (var i = 0; i < character_list.length; i++) {
	    var option = document.createElement("option");
	    option.value = character_list[i][0];
	    option.text = character_list[i][1];
	    selectList.appendChild(option);
	}
	selectList.addEventListener("change", character_info);

}

function import_characters(){

	var req = new XMLHttpRequest();
	req.responseType = 'json';
	req.open('GET', 'character_list', true);
	req.onload  = function() {
	   var characters = req.response;
	   create_character_selector(characters);
	};
	req.send(null);

};

function character_info(){
	var character_id = document.getElementById("characterSelect").value;
    var req = new XMLHttpRequest();
	req.responseType = 'json';
	url = "character_info?character_id=" + character_id
    req.open("GET", url, true);
    req.onload = function() {
	   var info = req.response;
	  	var modal = document.getElementById('myModal');
		modal.style.display = "block";
		var span = document.getElementsByClassName("close")[0];
		span.onclick = function() {
		    modal.style.display = "none";
		}
		window.onclick = function(event) {
		    if (event.target == modal) {
		        modal.style.display = "none";
		    }
		}
		document.getElementById("modal_text").innerHTML = info;
     };
	req.send(null);

};

$( document ).ready(function() {
    import_characters();
});