$(document).ready(function () {
    $.ajax({
        url: "/toggles",
        success: function (data) {
            data = JSON.parse(data)
            data.devices.forEach(function (item, index) {
                div=document.createElement('div');
                div.classList.add('toggle')
                my_form=document.createElement('FORM');
                my_form.name='myForm'
                my_form.method='POST'
                my_form.action='http://www.another_page.com/index.htm';
                title = document.createElement('h2')
                title.classList.add('title')
                title.textContent = item
                my_form.appendChild(title);
                my_form.appendChild(create_button("ON"));
                my_form.appendChild(create_button("OFF"));
                div.appendChild(my_form)
                $("#toggles").append(div)
            });
        }
    })
})


function create_button (text){
    my_tb=document.createElement('BUTTON')
    my_tb.classList.add('button')
    my_tb.name='myInput'
    my_tb.class = "button"
    my_tb.textContent = text
    return my_tb
}