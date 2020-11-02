// Externally there should be a variable named "interactable_elements"

//var interactable_elements = document.getElementById("main-content-X").querySelectorAll("*");
var clickables = [];
var scrollables = [];
var focusables = [];
var all_interactables = [clickables, scrollables, focusables];

// Disable alerts
alert = function() {};

function init_auto_interactions(interactable_elements) {
    for (var i = 0; i < interactable_elements.length; i++) {
        //console.log(interactable_elements[i]);
        if (typeof interactable_elements[i].onclick === 'function') {
            // do something with the element here
            clickables.push(interactable_elements[i]);
            //console.log("Clickable " + interactable_elements[i]);
        } else if (typeof interactable_elements[i].onscroll === 'function') {
            // do something with the element here
            scrollables.push(interactable_elements[i]);
            //console.log("Scrollable " + interactable_elements[i]);
        } else if (typeof interactable_elements[i].onfocus === 'function') {
            // do something with the element here
            focusables.push(interactable_elements[i]);
            //console.log("Focusable " + interactable_elements[i]);
        }
    }
}

//Bot definition
var bot_timer;
var interaction_speed = 1000;

function interact(i, j) { //authomatic event firing function

    if (all_interactables[i].length > 0) {
        var elem = all_interactables[i][j];
        //alert(i + " " + j + " :: " + all_interactables.length + " " + all_interactables[i].length);
        switch (i) {
            case 0:
                elem.click();
                break;
            case 1:
                var scroll_w = Math.floor((Math.random() * elem.scrollWidth) + 1);
                var scroll_h = Math.floor((Math.random() * elem.scrollHeight) + 1);
                elem.scrollTo(scroll_w, scroll_h);
                break;
            case 2:
                elem.focus();
                if (elem.type == "text") {
                    elem.value = Math.floor((Math.random() * 1000) + 1);
                }
                break;
        }
    }
}

function startBot(main_content_name) {
    bot_timer = setInterval(function() {
        interactable_elements = document.getElementById(main_content_name).querySelectorAll("*");
        //console.log(interactable_elements);;
        clickables = [];
        scrollables = [];
        focusables = [];
        all_interactables = [clickables, scrollables, focusables];
        init_auto_interactions(interactable_elements);

        var type_idx = Math.floor(Math.random() * all_interactables.length);
        var elem_idx = Math.floor(Math.random() * all_interactables[type_idx].length);
        var refresh_p = Math.floor(Math.random() * 30);

        if (refresh_p < 1) {
            console.log("refresh!");
            window.location.reload();

        } else {
            interact(type_idx, elem_idx);
        }

    }, interaction_speed, "JavaScript"); // Measure in milisecond
}

function stopBot() {
    clearInterval(bot_timer);
}