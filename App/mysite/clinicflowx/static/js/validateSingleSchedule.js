function checkSingleSchedule(){
	var checkname = checkName();
	var checktime = checkTime();
	var checkvisit = checkVisiting();
	return (checkname && checktime && checkvisit)
}

function checkName(){// validate name
	var namepattern = /^([a-zA-Z0-9,.!?@#$%^& ]+)$/; 
/*	name pattern, between 2 to 100 character*/
	var name = document.forms["patientinfo_form"]["Name"].value; // get value from html
	if (name =="" || name ==null){ // if value is empty
		document.getElementById("name").style.borderColor ="red"; 
		document.getElementById("name_error_alert").innerHTML = "Name is required";
		document.getElementById("name_error_alert").style.color ="red";
		return false;
	}else if(!namepattern.test(name)){ // if pattern is wrong
		document.getElementById("name").style.borderColor ="red";
		document.getElementById("name_error_alert").innerHTML = "Pattern error, unexpected character";
		document.getElementById("name_error_alert").style.color ="red";
		return false;
	}
	else{ // close the alert and return true
		document.getElementById("name").style.borderColor ="#5d93d1";
		document.getElementById("name_error_alert").innerHTML = "";
		return true;
		
	}
	
}

function checkTime(){
	var timepattern=/^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/;
	var time = document.forms["patientinfo_form"]["Time"].value; 
	if (time =="" || time ==null){ // if value is empty
		document.getElementById("time").style.borderColor ="red"; 
		document.getElementById("time_error_alert").innerHTML = "Time is required";
		document.getElementById("time_error_alert").style.color ="red";
		return false;
	}else if(!timepattern.test(time)){ // if pattern is wrong
		document.getElementById("time").style.borderColor ="red";
		document.getElementById("time_error_alert").innerHTML = "Pattern error, please follow the pattern hh:mm ex. 23:59";
		document.getElementById("time_error_alert").style.color ="red";
		return false;
	}
	else{ // close the alert and return true
		document.getElementById("time").style.borderColor ="#5d93d1";
		document.getElementById("time_error_alert").innerHTML = "";
		return true;
		
	}
}

function checkVisiting(){
	var visits = document.forms["patientinfo_form"]["Providers"];
	var len = visits.length
	var visitany = false;
	for (var i=0; i<len;i++){
		visitany = visitany || visits[i].checked;
	}
	if (visitany==false){
		document.getElementById("visit_error_alert").innerHTML = "Visit purpose can't be empty";
		document.getElementById("visit_error_alert").style.color ="red";
	}else{
		document.getElementById("visit_error_alert").innerHTML = "";
	}
	return visitany;
}