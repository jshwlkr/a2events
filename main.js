(function(){

  var app = angular.module('a2events', ['mgcrea.ngStrap', 'angular-inview']);

  app.controller('CalendarController', function($scope, $http) {
    $http.get('data.json')
         .success(function(data, status, headers, config) {
          angular.forEach(data, function(value, key) {
            date = new Date(value['date']);
            if (value['date'].length < 11) {
              value['full_day'] = true;
            } else {
              value['full_day'] = false;
            }
            value['date'] = date;
            value['year'] = date.getFullYear();
            value['month'] = date.getMonth();
            value['day'] = date.getDate();
          });
      $scope.events = data;
      $scope.stickyYear = "";
      $scope.stickyDay = "";

      $scope.headingScroll = function(date){
        //angular.element('.stick.heading div').textContent = year;
        $scope.stickyYear = date;
      }

      $scope.dayScroll = function(){
        $scope.stickyDay = ""
      }

    })
    .error(function(data, status, headers, config) {
      console.log(status);
    });
  });




})();


