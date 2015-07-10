(function(){

  var app = angular.module('a2events', []);

  app.controller('CalendarController', function($scope, $http) {
    $http.get('../data.json')
         .success(function(data, status, headers, config) {
          angular.forEach(data, function(value, key) {
            date = new Date(value['date']);
            value['date'] = date;
            value['year'] = date.getFullYear();
            value['month'] = date.getMonth();
            value['day'] = date.getDate();
          });
      $scope.events = data;
    })
    .error(function(data, status, headers, config) {
      console.log(status);
    });
  });

})();