$('#submit').addClass('form_button')
$('#remember_me').addClass('custom-checkbox')
$('label[for=email]').addClass('form_label')
$('label[for=password]').addClass('form_label')
$('#email').addClass('form_input')
$('#email').focus(function () {
    foc(this, $('label[for=email]'))
}).blur(function () {
    blu(this, $('label[for=email]'))
})

$('#password').addClass('form_input')
$('#password').focus(function () {
    foc(this, $('label[for=password]'))
}).blur(function () {
    blu(this, $('label[for=password]'))
})

if (getParameterValue('mail')) {
    $('label[for=email]').css({
        top: '-18px',
        'font-size': '12px',
        'color': '#999999'
    })
    $('#email').val(getParameterValue('mail') || '')
}

function getParameterValue(name)
{
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    let regexS = "[\\?&]"+name+"=([^&#]*)";
    let regex = new RegExp( regexS );
    let results = regex.exec( window.location.href );
    if( results == null ) return "";
    else return results[1];
}

function foc(el, label) {
    $(el).css({
        'border-bottom': '1px solid #1a73a8'
    })
    label.css({
        top: '-18px',
        'font-size': '12px',
        'color': '#999999'
    })
}

function blu(el, label) {
    $(el).css({
        'border-bottom': '1px solid #cccccc'
    })
    if ($(el).val() === '')
        label.css({
            top: 0,
            color: '#9e9e9e',
            'font-size': '16px'
        })
}