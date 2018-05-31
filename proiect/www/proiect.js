document.addEventListener('DOMContentLoaded',function(){
	document.querySelector('#login').addEventListener('click',function(){
		if(login(document.getElementById('username').value,document.getElementById('password').value))
			console.log('succes')
	})
	function loadJSON(callback) {   

		var xobj = new XMLHttpRequest();
			xobj.overrideMimeType("application/json");
		xobj.open('GET', 'http://localhost/Germany_struggles_to_fend_off_assaults_from_Trump', true); // Replace 'my_data' with the path to your file
		xobj.onreadystatechange = function () {
			  if (xobj.readyState == 4 && xobj.status == "200") {
				// Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
				callback(xobj.responseText);
			  }
		};
		xobj.send(null);  
	}
	function init() {
	 loadJSON(function(response) {
	  // Parse JSON string into object
		var actual_JSON = JSON.parse(response);
		console.log(actual_JSON)
	 
	
	
	for(let i=0;i<=3;i++)

		document.getElementById('content').innerHTML += '<div class="column">'+
			'<div id="home_post" style="height:100%;width:100%;border:1px solid #ccc;font:16px/26px Georgia, Garamond, Serif;overflow:auto;">'+
		'<div class="">'+
    '<header class="new-icon">'+
        actual_JSON["title"] +
		
    '</header>'+
	'<img src='+actual_JSON["urlToImage"]+' alt="Mountain View" style="width:100px;height:100px; " align="left">'+
'<ul>'+
        '<li>'+
            '<article align="right">'+
                actual_JSON["description"]+
            '</article>'+
			
        '</li>'+
    '</ul>'+
    '<footer>'+
        '<a href="#">'+
            actual_JSON["url"]+
        '</a>'+
    '</footer>'+
'</div>'+
	'</div>'+
  '</div>'
  });
	}
	init();
	function loadJSON(callback) {   

		var xobj = new XMLHttpRequest();
			xobj.overrideMimeType("application/json");
		xobj.open('GET', 'Hardline_North_Korean_general_to_meet_Pompeo_in_New_York', true); // Replace 'my_data' with the path to your file
		xobj.onreadystatechange = function () {
			  if (xobj.readyState == 4 && xobj.status == "200") {
				// Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
				callback(xobj.responseText);
			  }
		};
		xobj.send(null);  
	}
	
})

function login(user,psw){
	postData('localhost:80/login',{username: user, passwors: psw}) //primul parametru, este link-ul unde ruleaza partea de login, al 2-lea face referire la datele userului
	.then(data =>console.log(data)) //afiseaza datele primite de la server
	.catch(error=>console.error(error)) //afiseaza erorile
}

function postData(url,data){
	return fetch(url,{ //trimite datele catre url / server
		body:JSON.strigify(data), //trimite un json cu proprietatile : body (json la randul sau cu proprietatile din data)
		cache : 'no-cache',
		credentials : 'same-origin',
		headers:{
			'content-type':'application/json'
		},
		method: 'POST'
	})
	.then(response =>response.json())
}