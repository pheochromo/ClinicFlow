function checkSearchingDate(){
	var testtime1= checkDate("timebound1","time1","time1_error_alert");
	var testtime2= checkDate("timebound2","time2","time2_error_alert");
	return (testtime1 && testtime2);
 
}



function checkDate(inputname, id, errorid){ //validate date 
	var datepattern1= /^\d{1,2}\/\d{1,2}\/\d{4}$/; // date pattern mm/dd/yyyy
	var datepattern2= /^\d{4}\-\d{1,2}\-\d{1,2}$/;
	
	//var datepattern="(?:19|20)[0-9]{2}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-9])|(?:(?!02)(?:0[1-9]|1[0-2])-(?:30))|(?:(?:0[13578]|1[02])-31))";
	var date = document.forms["searching_form"][inputname].value; // get value from html 
	if (date =="" || date==null){ // if input is empty 
		document.getElementById(id).style.borderColor ="#5d93d1";
		//document.getElementById(id).style.borderColor ="green";
		document.getElementById(errorid).innerHTML = "";
		return true;
	}
	var separate;
	var mm;
	var dd;
	var yyyy;
	if(datepattern1.test(date)){
		 separate = date.split("/"); // split mm/dd/yyyy to different variable 
		 mm = parseInt(separate[0]); //month 
		 dd = parseInt(separate[1]); // day
		 yyyy = parseInt(separate[2]); //year 
	}else if(datepattern2.test(date)){
		separate = date.split("-"); // split yyyy-mm-dd to different variable 
		 mm = parseInt(separate[1]); //month 
		 dd = parseInt(separate[2]); // day
		 yyyy = parseInt(separate[0]); //year 
		 //window.alert(str(yyyy)+str(mm)+str(dd));

	}
	else{ // doesn't match with pattern 
		document.getElementById(id).style.borderColor ="red";
		document.getElementById(errorid).style.color ="red";
		document.getElementById(errorid).innerHTML = "Please match yyyy-mm-dd pattern";
		return false;
	}
	
	if (yyyy <1000 || yyyy>3000 || mm <=0 || mm >=13){ // if one of the value of year or month doesn't make sense 
		document.getElementById(id).style.borderColor ="red";
		document.getElementById(errorid).innerHTML = "year or month value doesn't make sense";
		document.getElementById(errorid).style.color ="red";
		return false;
	}
	var dayofmonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]; // each month have different number of days
	if (yyyy%400==0 || (yyyy%4==0 && yyyy%100 !=0 )){
		dayofmonth[1] =29; // Feburary has 29th day.
	}
	if (dd <=0 || dd>dayofmonth[mm-1]){ // if the day value doesn't make sense 
		document.getElementById(id).style.borderColor ="red";
		document.getElementById(errorid).innerHTML = "day value doesn't make sense";
		document.getElementById(errorid).style.color ="red";
		return false;
	}else{ // clean the alert and return true 
		document.getElementById(id).style.borderColor ="#5d93d1";
		document.getElementById(errorid).innerHTML = "";
		return true;
	}
}