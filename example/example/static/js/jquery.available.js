(function($){
    //è¦ç´ ã®ä½¿ç”¨å¯å¦ã‚’åˆ‡ã‚Šæ›¿ãˆã‚‹
    function toggle_condition(condition,clear){
        if(condition){
            if($(this).data('disabled') && clear == true){
                $(this).val($(this).data('_cur_value'));
                if($(this).data('_cur_checked')){
                    $(this).attr('checked','checked');
                }
            }
            $(this).removeAttr('disabled');
            $(this).removeClass('disabled');
        }else{
            if(!$(this).data('disabled') && clear == true){
                $(this).data('_cur_value',$(this).val());
                $(this).data('_cur_checked',$(this).attr("checked"));
                $(this).val('');
            }
            $(this).removeAttr('checked');
            $(this).attr('disabled','disabled');
            $(this).addClass('disabled');
        }
        $(this).data('disabled',!condition);
    }

    $.fn.enable_if = function(options){
        var settings = {
                clear : true
        }
        $.extend(settings, options);
        var target = this;
        $(settings.trigger).change(function(){
            $(target).each(function(){
                toggle_condition.call(this, settings.condition.call(settings.trigger, this), settings.clear);
            });
        }).change();
        return $(this);
    }
    $.fn.disable_if = function(options){
        var settings = {
                clear : true
        }
        $.extend(settings, options);
        var target = this;
        $(settings.trigger).change(function(){
            $(target).each(function(){
                toggle_condition.call(this, !settings.condition.call(settings.trigger, this),settings.clear);
            });
        }).change();
        return $(this);
    }
    //é€ä¿¡å‰ã«å…¨ã¦ã® disabled ã‚’è§£é™¤
    $(function(){
        $("form").submit(function(){
            $(this).find("[disabled]")
            .each(function(){
                $(this).removeAttr('disabled');
            });
            return true;
        });
    });
})(jQuery);

