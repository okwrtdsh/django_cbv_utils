(function($){
  $(function(){
    $('.btn-file :file').change(function(){
      var input = $(this);
      var numFiles = input.get(0).files ? input.get(0).files.length : 1;
      var label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
      var display = input.parents('.input-group').find(':text');
      var log = numFiles > 1 ? numFiles + ' files selected' : label;
      if(display.length){
        display.val(log);
      }
      else{
        if(log) alert(log);
      }
    });
  });
})(jQuery);

