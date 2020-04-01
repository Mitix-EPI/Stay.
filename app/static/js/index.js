function myPopUp(timer) {
    var today = new Date();
    var date = today.getHours() + ":" + today.getMinutes();

    console.log("ta mère");
    console.log(date);
    console.log(timer);
    if (date == timer) {
        if (alert("Validation de Présence")) {}
        else {
            window.location.reload();
        }
    }
}

function refreshData(timer)
{
    x = 40;
    myPopUp(timer);
    setInterval(refreshData, x * 1000);
}

// console.log(timer);