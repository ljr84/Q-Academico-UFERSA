


function notify_front(title, message, delay, autohide, class_notification, callback=null){
    var toast = $(document).Toasts('create', {
        title: title,
        body: message,
        delay: delay,
        class: class_notification,
        autohide: autohide
    });

    toast.on('removed.lte.toasts', function () {
        if(callback !== null){
            callback.call(this);
        }
    });
}




function notify_success(message, callback=null, delay=2500, title='Sucesso', autohide=true){
    notify_front(title, message, delay, autohide, 'bg-success', callback);
}

function notify_info(message, callback=null, delay=2500, title='Notifica&ccedil;&atilde;o', autohide=true){
    notify_front(title, message, delay, autohide, 'bg-info', callback);
}

function notify_error(message, callback=null, delay=2500, title='Erro', autohide=true){
    notify_front(title, message, delay, autohide, 'bg-danger', callback);
}



function noty_success_302(message, url, delay=2500){
    notify_success(message, function(e){window.location = url;}, delay)
}

function noty_info_302(message, url, delay=2500){
    notify_info(message, function(e){window.location = url;}, delay)
}

function noty_error_302(message, url, delay=2500){
    notify_error(message, function(e){window.location = url;}, delay)
}




function ajaxMe(method, url, data, successCallback=null, errorCallback=null){
    $.ajax({
        type: method,
        url: url,
        data: data,
        success: function(e){
            console.log(`ajaxMe.success - ${e}`);
            if(successCallback !== null){
                successCallback(e);
            }
        },
        error: function(x, status, error){
            console.log(`ajaxMe.error - ${x} - ${status} - ${error}`);
            let errorMessage = "Erro desconhecido.";
            if (x.responseJSON && x.responseJSON.message) {
                errorMessage = x.responseJSON.message;
            }
            if(errorCallback !== null){
                errorCallback(errorMessage);
            }
        },
        dataType: 'json'
    });
}

function ajaxGet(url, successCallback=null, errorCallback=null){
    ajaxMe('GET', url, {}, successCallback, errorCallback);
}

function ajaxPost(url, data, successCallback=null, errorCallback=null){
    ajaxMe('POST', url, data, successCallback, errorCallback);
}



//https://stackoverflow.com/a/9204568
function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}