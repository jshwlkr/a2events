(function(){

  var app = angular.module('a2Events', []);

  app.controller('CalendarController', function($scope, $http) {
    $http.get('../data.json')
         .success(function(data, status, headers, config) {
          angular.forEach(data, function(value, key) {
            value['date'] = Date.parse(value['date']);
          });
      $scope.events = data;

      console.log('sucess');
    })
    .error(function(data, status, headers, config) {
      console.log('error');
      console.log(status);
    });
  });



})();