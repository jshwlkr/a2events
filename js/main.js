(function(){

  var app = angular.module('a2Events', []);

  app.controller('CalendarController', function($scope, $http) {
    $http.get('../data.json')
         .success(function(data, status, headers, config) {
      $scope.events = data;
      console.log('sucess');
    })
         .error(function(data, status, headers, config) {
      console.log('error');
      console.log(status);
    });
  });

})();