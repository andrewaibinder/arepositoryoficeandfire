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
	var name = document.getElementById("characterSelect").value;
	var year = document.getElementById("yearValue").value;
    var req = new XMLHttpRequest();
	req.responseType = 'json';
	url = "character_info?character_id=" + name + "&year_gap=" + year
    req.open("GET", url, true);
    req.onload = function() {
	   var info = req.response;
	   console.log(info);
     };
	req.send(null);

};

$( document ).ready(function() {
    import_characters();
});