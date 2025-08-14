$(function () {

    /**
     * Some examples of how to use features.
     *
     **/


    var ChatosExamle = {
        Message: {
            add: function (message, type, dt) {
                var chat_body = $('.layout .content .chat .chat-body');
                if (chat_body.length > 0) {

                    type = type ? type : '';
                    message = message ? message : '';
                    dt = dt ? dt : '';
                    if (message.length > 0) {
                        var startwith = message.substr(0,3);
                        var f_name='';
                        if (startwith==="il@"){
                            f_name =message.substr(4,);
                            $('.layout .content .chat .chat-body .messages').append('<div class="message-item ' + type + ' "><div class="message-content"><div style="width: 300px"><img src="/media/@' +user_id+'-'+ f_name + '" class="img-responsive center-block"><ul class="list-inline"><li class="list-inline-item"><a href="' + downloadUrl+f_name + '">Download</a></li></ul></div></div><div class="message-action">' + dt + '</div></div>');
                        }
                        else if(startwith==="fl@"){
                            f_name = message.substr(4,);
                            $('.layout .content .chat .chat-body .messages').append('<div class="message-item ' + type + ' "><div class="message-content message-file"><div class="file-icon"><i class="fa fa-file"></i></div><div><div>'+f_name+'</div><li class="list-inline-item"><a href="' + downloadUrl+f_name + '">Download</a></li></div></div><div class="message-action">' + dt + '</div></div>');

                        }else{
                            $('.layout .content .chat .chat-body .messages').append('<div class="message-item ' + type + '"><div class="message-content">' + message + '</div><div class="message-action">' + dt + (type ? '<i class="ti-check"></i>' : '') + '</div></div>');

                        }
                    }
                    chat_body.scrollTop(chat_body.get(0).scrollHeight, -1);
                }
            }
        }
    };

    setInterval(function () {
        $.ajax({
            url: '/ccc/sl/?i=' + user_id + "&p=" + lastdt,// 需要修改
            contentType: "application/json;charset=utf-8",
            type: "get",
            // data: JSON.stringify({"i":user_id,"g":message,"si":si,"m":u_name}),
            dataType: "json",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $.getCookie('csrftoken'));
                xhr.setRequestHeader("P", u_pkg);
            },
            complete: function (data) {

            },
            success: function (data, status, xhr) {
                if (status === 'success' && data) {
                    lastdt = data[data.length - 1].timestamp;
                    var obj = $('.layout .content .chat .chat-body .messages');
                    $.each(data, function (idx, clm) {
                        var dt = dateFormat(Number(clm.timestamp), "Y/m/d H:i:s");
                        var startwith = clm.msg.substr(0,3);
                        var f_name='';
                        if (startwith==="il@"){
                            f_name = clm.msg.substr(4,);
                            obj.append('<div class="message-item "><div class="message-content"><div style="width: 300px"><img src="/media/@' +user_id+'-'+ f_name + '" class="img-responsive center-block"><ul class="list-inline"><li class="list-inline-item"><a href="' + downloadUrl+f_name + '">Download</a></li></ul></div></div><div class="message-action">' + dt + '</div></div>'	);
                        }
                        else if(startwith==="fl@"){
                            f_name = clm.msg.substr(4,);
                            obj.append('<div class="message-item "><div class="message-content message-file"><div class="file-icon"><i class="fa fa-file"></i></div><div><div>'+f_name+'</div><li class="list-inline-item"><a href="' + downloadUrl+f_name + '">Download</a></li></div></div><div class="message-action">' + dt + '</div></div>');

                        }else{
                            obj.append('<div class="message-item"><div class="message-content">' + clm.msg + '</div><div class="message-action">' + dt + ' ' + ('' ? '<i class="ti-check"></i>' : '') + '</div></div>');


                        }
                    });
                    var chat_body = $('.layout .content .chat .chat-body');
                    if (chat_body.length > 0) {
                        chat_body.scrollTop(chat_body.get(0).scrollHeight, -1);
                    }


                }
            }
        });
        // ChatosExamle.Message.add();
    }, 3000);

    // setTimeout(function () {
    //     // $('#disconnected').modal('show');
    //     $('#call').modal('show');
    // }, 2000);

    $(document).on('submit', '.layout .content .chat .chat-footer form', function (e) {
        e.preventDefault();

        var input = $(this).find('input[type=text]');
        var message = input.val();

        message = $.trim(message);

        if (message) {
            $.ajax({
                url: '/ccc/sh/',// 需要修改
                contentType: "application/json;charset=utf-8",
                type: "post",
                data: JSON.stringify({"i": user_id, "g": message, "si": si, "m": u_name}),
                dataType: "json",
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $.getCookie('csrftoken'))
                    xhr.setRequestHeader("P", u_pkg);
                },
                complete: function (data) {

                },
                success: function (data, status, xhr) {
                    if (status === 'success') {
                        lastdt = data.t;
                        var dt = dateFormat(data.t,"Y/m/d H:i:s");
                        ChatosExamle.Message.add(message, 'outgoing-message', dt);
                        input.val('');

                    }
                }
            });
        } else {
            input.focus();
        }
    });

    $(document).on('click', '.layout .content .sidebar-group .sidebar .list-group-item', function () {
        if (jQuery.browser.mobile) {
            $(this).closest('.sidebar-group').removeClass('mobile-open');
        }
    });

});