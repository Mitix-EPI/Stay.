function myfakePopUp() {
    var today = new Date();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var dateTime = date+' '+time;
    console.log("coucou " + dateTime);
    alert("myPopUp")
}

function myPopUp(timer) {
    //si le timer est bon alors
    alert("Validation de Présence")
}

myfakePopUp()