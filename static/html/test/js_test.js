function buttonClick(object, log, data) {
    var currentDate = new Date();

    var date = currentDate.getDate();
    var month = currentDate.getMonth();
    var year = currentDate.getFullYear();

    var dateString = date + "-" + (month + 1) + "-" + year;
    alert(dateString);
    //log.push(["Button Click", dateString]);
}

function test() {
    alert("Connected!");
}