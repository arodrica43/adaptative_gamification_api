function log_click(data) {
    var time = new Date().getTime();
    var date = new Date(time);
    alert(date.toString());
    data.register.push([date.toString(), data.message]);
    //alert(data.register);
}

function test() {
    alert("Connected!");
}