$(document).ready(function () {
    $.ajaxSetup({
        async: false
    });

    var colors
    $.ajax({
        url: "/colors",
        success: function (data) {
            data = JSON.parse(data)
            colors = data.colors
            console.log(colors)
        }
    })
    console.log(colors)

    $.ajaxSetup({
    async: true
    });

    $.ajax({
        url: "/toggles",
        success: function (data) {
            data = JSON.parse(data)
            data.devices.forEach(function (item, index) {
                div=document.createElement('div');
                div.id = item.name
                div.classList.add('toggle')
                title = document.createElement('h2')
                title.classList.add('title')
                title.textContent = item.name
                div.appendChild(title);
                if (item.type == "direct"){
                    status = ""
                    if (item.state == 0){
                        status = "OFF"
                    }
                    else {
                        status = "ON"
                    }
                    div.appendChild(create_form(status, 1 - item.state, item.name))
                }
                else{
                    div.appendChild(create_form("ON", 1, item.name))
                    div.appendChild(create_form("OFF", 0, item.name))
                }
                
                div.appendChild(my_form)
                $("#toggles").append(div)
                if (item.name.includes("light")){
                    div.append(create_colors(colors))
                }
            })
        }
    })
})



//Creates a div and adds buttons for controlling colors to it
function create_colors(colors){
    var div1=document.createElement('div');
    colors.forEach(function (color, index) {
        my_form=document.createElement('FORM');
        my_form.method ='POST'
        my_form.action = '/control?device=light1' + '&color=' + color
        my_tb=document.createElement('BUTTON')
        my_tb.classList.add('button')
        my_tb.classList.add('button2')
        my_tb.style.backgroundColor = "#" + color
        my_form.appendChild(my_tb);
        div1.appendChild(my_form)
    })
    return div1
}



function create_form (text, mode, item){
    my_form=document.createElement('FORM');
    my_form.method ='POST'
    my_form.action = '/control?device=' + String(item) + '&power=' + mode
    my_tb=document.createElement('BUTTON')
    my_tb.classList.add('button')
    my_tb.classList.add('button1')
    my_tb.class = "button"
    my_tb.textContent = text
    my_form.appendChild(my_tb);
    return my_form
}