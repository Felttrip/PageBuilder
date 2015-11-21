function getPages(){
    $.ajax({
        type: "GET",
        url: "/api/pages",
        beforeSend: function() {
            $(placeholder).addClass('loading');
            i++;
        },
        success: function(data, textStatus) {
            $(".result").html(data);
        },
        error: function() {
            alert('Not OKay');
        }
    });
}