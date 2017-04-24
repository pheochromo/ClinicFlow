function checkChangeProvider() {
    var providerpattern = /^([a-zA-Z0-9,._/- ]+)$/;
    var provider = document.forms["setting-form"]["Provider_List"].value; // get value from html
    if (provider == "" || provider == null) { // if value is empty
        document.getElementById("provider-list").style.borderColor = "red";
        document.getElementById("provider-list_error_alert").innerHTML = "Provider is required";
        document.getElementById("provider-list_error_alert").style.color = "red";
        return false;
    } else if (!providerpattern.test(provider)) { // if pattern is wrong
        document.getElementById("provider-list").style.borderColor = "red";
        document.getElementById("provider-list_error_alert").innerHTML = "Pattern error, Please follow the example 'Provider1/Provider2/'";
        document.getElementById("provider-list_error_alert").style.color = "red";
        return false;
    } else { // close the alert and return true
        document.getElementById("provider-list").style.borderColor = "#5d93d1";
        document.getElementById("provider-list_error_alert").innerHTML = "";
        return true;
    }
}


function checkDate() { //validate date
    var datepattern1 = /^\d{1,2}\/\d{1,2}\/\d{4}$/; // date pattern mm/dd/yyyy
    var datepattern2 = /^\d{4}\-\d{1,2}\-\d{1,2}$/;
    if (checkChangeProvider() == false) {
        return false;
    }
    //var datepattern="(?:19|20)[0-9]{2}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-9])|(?:(?!02)(?:0[1-9]|1[0-2])-(?:30))|(?:(?:0[13578]|1[02])-31))";
    var date = document.forms["setting-form"]["Schedule_Date"].value; // get value from html
    if (date == "" || date == null) { // if input is empty
        document.getElementById("date").style.borderColor = "red";
        document.getElementById("date_error_alert").style.color = "red";
        document.getElementById("date_error_alert").innerHTML = "Date is required";
        return false;
    }
    var separate;
    var mm;
    var dd;
    var yyyy;
    if (datepattern1.test(date)) {
        separate = date.split("/"); // split mm/dd/yyyy to different variable
        mm = parseInt(separate[0]); //month
        dd = parseInt(separate[1]); // day
        yyyy = parseInt(separate[2]); //year
    } else if (datepattern2.test(date)) {
        separate = date.split("-"); // split yyyy-mm-dd to different variable
        mm = parseInt(separate[1]); //month
        dd = parseInt(separate[2]); // day
        yyyy = parseInt(separate[0]); //year
        //window.alert(str(yyyy)+str(mm)+str(dd));

    } else { // doesn't match with pattern
        document.getElementById("date").style.borderColor = "red";
        document.getElementById("date_error_alert").style.color = "red";
        document.getElementById("date_error_alert").innerHTML = "Please match yyyy-mm-dd pattern";
        return false;
    }

    if (yyyy < 1000 || yyyy > 3000 || mm <= 0 || mm >= 13) { // if one of the value of year or month doesn't make sense
        document.getElementById("date").style.borderColor = "red";
        document.getElementById("date_error_alert").innerHTML = "year or month value doesn't make sense";
        document.getElementById("date_error_alert").style.color = "red";
        return false;
    }
    var dayofmonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]; // each month have different number of days
    if (yyyy % 400 == 0 || (yyyy % 4 == 0 && yyyy % 100 != 0)) {
        dayofmonth[1] = 29; // Feburary has 29th day.
    }
    if (dd <= 0 || dd > dayofmonth[mm - 1]) { // if the day value doesn't make sense
        document.getElementById("date").style.borderColor = "red";
        document.getElementById("date_error_alert").innerHTML = "day value doesn't make sense";
        document.getElementById("date_error_alert").style.color = "red";
        return false;
    } else { // clean the alert and return true
        document.getElementById("date").style.borderColor = "#5d93d1";
        document.getElementById("date_error_alert").innerHTML = "";
        return true;
    }
}
