try {
    var b = init_test(1);
} catch (err) {
    //Click
    function init_test(i) {
        i++;
    }

    function format_log(data) {
        console.log("Interaction!");
        var time = new Date().getTime();
        var date = new Date(time);
        //alert("Interaction!");
        data.register['history'].push([{
            "timestamp": date.toString(),
            "type": data.type,
            "level": data.level,
            "description": data.message
        }]);
    }

    function log_click(data) {
        increase_interaction_time(data.itime);
        format_log(data);
    }

    var input_t = 0;
    var input_timer;

    function log_input(data) { // We don't care about multithreading: first occurs input in and then input out
        if (data.type == "InputIn") {
            console.log("Input In");
            input_timer = setInterval(function() {
                input_t++;
            }, 1000, "JavaScript"); // Measure in seconds
        } else if (data.type == "InputOut") {
            console.log("Input Out");
            clearInterval(input_timer);
            increase_interaction_time(input_t);
            input_t = 0;
        }
        format_log(data);

    }
}