/*global m document*/
'use strict'(function() {
  var app = {};

  function AMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0' + minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
  }

  app.controller = function() {
    // changed from this. to var so it's accessible inside the then function
    var eventlist = m.prop([]);

    // load initial data
    var init = function() {
      m.request({
      method: 'GET',
      url: 'event-segment-1.json'
      }).
        // assign the result to the getter/setter
        then(eventlist).
        // send the request for the rest of the data
        then(rest)
      ;
    };

    // load the rest of the data
    var rest = function() {
      m.request({
      method: 'GET',
      url: 'event-segment-2.json'
      }).
        // concat the resulting array with the current one
        then(function(result) {
          eventlist(
            eventlist().concat(result)
          );
        })
      ;
    };

    init();

    // return the eventlist so the view can access it
    return {
      eventlist: eventlist
    }
  };

  app.view = function(controller) {
    var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    return m('div', [
    controller.eventlist().map(function(item) {
      var current = new Date(item.date);
      var display_date = current.getDate() + ', ' + months[current.getMonth()] + ' — ' + days[current.getDay()];
      var display_time = AMPM(current);
      if (typeof controller.check === 'undefined' || controller.check.getMonth() != current.getMonth()) {
        controller.check = new Date(current);
        return [m('div', {
          class: 'month'
          }, [m('h2', months[current.getMonth()])]),
          m('div', {
          class: 'h-event'
          }, [
          m('div', {
          class: 'dt-start'
          }, display_date),
          m('a', {
          class: 'p-name',
          href: item.url
          }, item.name),
          m('div', {
          class: 'time'
          }, display_time),
          m('div', {
          class: 'p-description'
          }, item.description)
          ])];
      } else {
        controller.check = new Date(current);
        return m('div', {
        class: 'h-event'
        }, [
        m('div', {
        class: 'dt-start'
        }, display_date),
        m('a', {
        class: 'p-name',
        href: item.url
        }, item.name),
        m('div', {
        class: 'time'
        }, display_time),
        m('div', {
        class: 'p-description'
        }, item.description)
        ]);
      }
    })
    ]);
  };

  m.module(document.body, app);
})();
