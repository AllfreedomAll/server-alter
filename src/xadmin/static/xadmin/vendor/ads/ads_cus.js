;(function ($) {

        var cus_modal = $("#export-modal-xml").clone();
        var dom = cus_modal.find('.modal-dialog');
        dom.addClass('modal-lg');
        cus_modal.find('button[type="submit"]').addClass('hidden');
        cus_modal.attr("id","cus_modal");
        cus_modal.find('.modal-body').html($('<textarea class="ad_json_body" style="margin: 0px; width: 541px; height: 603px;"></textarea>'));
        $('.export').append(cus_modal);
        $(".ads_copy_btn").click(function () {

            var ads_id = this.getAttribute("ads");

            $.ajax({
                url: '/ads/add/',
                contentType: "application/json;charset=utf-8",
                type: "post",
                dataType: "json",
                data: JSON.stringify({"ads_id":ads_id, "op":"dup_add"}),
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $.getCookie('csrftoken'))
                },
                // complete: function () {
                //     $('#submit-form').removeClass('disabled');
                //     $('#submit-form').text('Submit');
                // },
                success: function (data, this_obj) {
                    if  (data.code>=0){
                    location.reload();
                    }
                    else {
                        alert("Error");
                    }
                }
            });

        });




        // 展示json

        $("body").on("click",".ad_l_show_json",function () {
            var edit_id = $(this).attr("ads");
            $.ajax({
                url: '/ads/edit/',
                contentType: "application/json;charset=utf-8",
                type: "post",
                dataType: "json",
                data: JSON.stringify({"edit_id":edit_id,"op":"get_content"}),
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $.getCookie('csrftoken'));
                },
                complete: function () {

                },
                success: function (data, this_obj) {
                    console.log(data);
                    if (data.code>=0){
                        var t = JSON.stringify(data.data,null,2);
                        $('#cus_modal').find('h4').text("Json");
                        $('#cus_modal').find('.ad_json_body').text(t);
                        $('#cus_modal').modal("show");

                    }
                    else {
                        alert("Error!");
                    }


                }
            });
            $('#cus_modal').modal("show");

        });




    }
)(jQuery);