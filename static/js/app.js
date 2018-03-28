'use strict';

var myApp = angular.module('myApp', ['ngRoute']);

myApp.config(['$routeProvider',
     function($routeProvider) {
         $routeProvider.
             when('/', {
                 templateUrl: '/static/partials/index.html',
             }).
             when('/report', {
                 templateUrl: '/static/partials/report.html',
             }).
             otherwise({
                 redirectTo: '/'
             });
    }]);

myApp.controller("MyCtrl", function ($scope, $http) {

        $scope.reportData = {}
        $scope.isShow = false;

        $scope.SendData = function () {
        
            var form_data = new FormData($('#upload-file')[0]);

            $http.post('/upload', form_data, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            })
            .success(function(data){
                $scope.isShow = true;
                $scope.reportData = data;
                if (data["isCached"] === 1){
                    $('.modal').modal();
                    $('#modal').modal('open');
                }
            })
            .error(function(){
            });
        };

    });