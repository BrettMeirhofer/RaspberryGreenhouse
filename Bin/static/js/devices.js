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
                div.id = item
                div.classList.add('toggle')
                title = document.createElement('h2')
                title.classList.add('title')
                title.textContent = item
                div.appendChild(title);
                div.appendChild(create_form("ON", 1, item))
                div.appendChild(create_form("OFF", 0, item))
                div.appendChild(my_form)
                $("#toggles").append(div)
                if (item.includes("light")){
                    var div1=document.createElement('div');
                    div.append(div1)
                    colors.forEach(function (item, index) {
                        my_form=document.createElement('FORM');
                        my_form.method ='POST'
                        my_form.action = '/control?device=light1' + '&color=' + item
                        my_tb=document.createElement('BUTTON')
                        my_tb.classList.add('button')
                         my_tb.classList.add('button2')
                         console.log("#" + item)
                         my_tb.style.backgroundColor = "#" + item
                         my_form.appendChild(my_tb);
                         div1.appendChild(my_form)
                         console.log(div1)
                    })
                }
            })
        }
    })
})


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