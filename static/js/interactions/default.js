try {
    var a = log["history"];
} catch (err) {
    var log = { "history": [], "main_time": 0, "focus_time": 0, "interaction_time": 0, "hidden_content_time": 0, "shown_content_time": 0 };

    include_interaction_testing_tools

    //Main Time
    var tmp_main_t = 0;
    var main_timer;
    var control_t = 0;

    function start_main_time() {
        //console.log(tmp_main_t);

        if (control_t == 0) {
            //console.log("start timer");
            main_timer = setInterval(function() {
                //console.log(tmp_main_t / 100);
                tmp_main_t++;
                control_t++;
            }, 10, "JavaScript"); // Measure in milisecond
        }
    }

    function main_time() {
        return tmp_main_t;
    }

    function stop_main_time() {
        clearInterval(main_timer);
    }

    //Foculs Time
    var tmp_focus_t = 0;
    var focus_timer;

    function elementInViewport(myElement) {
        var bounding = myElement.getBoundingClientRect();
        var myElementHeight = myElement.offsetHeight;
        var myElementWidth = myElement.offsetWidth;
        if (bounding.top >= -myElementHeight &&
            bounding.left >= -myElementWidth &&
            bounding.right <= (window.innerWidth || document.documentElement.clientWidth) + myElementWidth &&
            bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight) + myElementHeight) {
            return true;
        } else {
            return false;
        }
    }

    function start_focus_time(mechanic_id) {
        if (control_t == 0) {
            focus_timer = setInterval(function() {
                if (elementInViewport(document.getElementById(mechanic_id))) {
                    tmp_focus_t++;
                }

            }, 10, "JavaScript"); // Measure in seconds
        }

    }

    function focus_time() {
        return tmp_focus_t;
    }

    function stop_focus_time() {
        clearInterval(focus_timer);
    }

    //Interaction Time
    var tmp_interaction_t = 0;

    function increase_interaction_time(increment) {
        tmp_interaction_t = Math.min(tmp_interaction_t + increment, tmp_focus_t);
    }

    function interaction_time() {
        return tmp_interaction_t;
    }

    //Locked Time
    var tmp_locked_t = 0;
    var locked_timer;

    function start_locked_time() {
        if (control_t == 0) {
            locked_timer = setInterval(function() {
                tmp_locked_t++;
            }, 10, "JavaScript"); // Measure in milisecond
        }
    }

    function locked_time() {
        return tmp_locked_t;
    }

    function stop_locked_time() {
        clearInterval(locked_timer);
    }

    //Unlocked Time
    var tmp_unlocked_t = 0;
    var unlocked_timer;

    function start_unlocked_time() {
        unlocked_timer = setInterval(function() {
            tmp_unlocked_t++;
        }, 10, "JavaScript"); // Measure in milisecond
    }

    function unlocked_time() {
        return tmp_unlocked_t;
    }

    function stop_unlocked_time() {
        clearInterval(unlocked_timer);
    }

    // Server log saving checkpoint
    var timer;

    function sendLogs(log_data, username, mechanic_index) {
        //alert(mechanic_index);
        //alert(log_data['history']);
        //console.log(main_time() / 100);
        log_data['main_time'] = main_time() / 100;
        log_data['focus_time'] = Math.min(focus_time(), main_time()) / 100;
        log_data['interaction_time'] = interaction_time();
        log_data['hidden_content_time'] = locked_time() / 100;
        log_data['shown_content_time'] = unlocked_time() / 100;

        //alert(log_data['main_time']);
        fetch('http://127.0.0.1:8080/api/g_mechanics/' + mechanic_index + '/', { //if window is closing,  fetch answer fails, but it makes the put method!
                method: 'PUT',
                body: JSON.stringify({
                    "user": username,
                    "log": log_data
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(function(response) {
                if (response.ok) {
                    //alert(log["hidden_content_time"]);
                    return response.text()
                } else {
                    throw "Error on the Ajax call";
                }
            })
            .then(function(texto) {
                console.log("OK");
                log['history'] = [];
                tmp_main_t = 0;
                tmp_focus_t = 0;
                tmp_interaction_t = 0;
                tmp_locked_t = 0;
                tmp_unlocked_t = 0;

            })
            .catch(function(err) {
                console.log(err);
            });
    }

    function start_logs(log_data, username, mechanic_index, update_time) { //use as dynamic_user, dynamic_mechanic_index

        //console.log(tmp_main_t);
        if (control_t == 0) {
            // console.log("control");
            window.onbeforeunload = function() {
                sendLogs(log_data, username, mechanic_index);
                return null;
            }
            timer = setInterval(function() {
                sendLogs(log_data, username, mechanic_index);
            }, update_time * 1000, "JavaScript"); // Update statistics on server each 15 seconds 
        }
    }
}