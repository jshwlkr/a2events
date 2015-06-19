


$(document).ready( function() {

    $.ajaxSetup({ scriptCharset: "utf-8" , contentType: "application/json; charset=utf-8"});
    $.getJSON('data.json', function(json) {

      $('.calendar').clndr({
        events: json,
        template: $('#template').html(),

  clickEvents: {
    click: function(target) {
      console.log(target);
    },
    onMonthChange: function(month) {
      console.log('you just went to ' + month.format('MMMM, YYYY'));
    }
  },
  doneRendering: function() {
    $('body').removeClass('loading').addClass('loaded');
  }
});



    });
});
