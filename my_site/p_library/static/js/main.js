function onReady(callback) {
    const intervalId = window.setInterval(function () {
        if (document.getElementsByTagName('body')[0] !== undefined) {
            window.clearInterval(intervalId);
            callback.call(this);
        }
    }, 1000);
}

function setVisible(selector, visible) {
    document.querySelector(selector).style.display = visible ? 'flex' : 'none';
}

onReady(function () {
    setVisible('main', true);
    setVisible('.preloader', false);
});

$(document).ready(function () {
    $('.sidenav').sidenav();
    $('.materialboxed').materialbox();
});