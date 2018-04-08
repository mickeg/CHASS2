var map;
var MAP_RADIUS = 1000;

var mapOptions = {
    zoom: 14,
    //center: {lat: 68.357856, lng: 18.778076},
    //center: { lat: 59.980721, lng: 17.250436 },
    //mapTypeId: 'hybrid'
}
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), mapOptions);

    infoWindow = new google.maps.InfoWindow;

    console.log(navigator.geolocation.getCurrentPosition);

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            //mapOptions.center = pos;

            console.log("lat", pos.lat);
            console.log("long", pos.lng);

            var myPosition = new google.maps.LatLng(pos.lat, pos.lng);
            var myMarker = new google.maps.Marker({
                position: myPosition
            });

            console.log(myMarker);

            var circle = new google.maps.Circle({
                map: map,
                radius: MAP_RADIUS,
                fillColor: '#AA0000'
            });
            circle.bindTo('center', myMarker, 'position');

            infoWindow.setPosition(myPosition);
            infoWindow.setContent('You');
            infoWindow.open(map);
            map.setCenter(myPosition);


            $.support.cors = true;
            $.ajax({
                url: 'http://127.0.0.1:8080/parsetxt',
                dataType: "json",
                crossDomain: true,
                success: function (data) {
                    console.log("success", data);
                    $.each(data.Data, function (k, v) {
                        //console.log(v);

                        lat = v.Coordinates.lat;
                        long = v.Coordinates.long;



                        var position = new google.maps.LatLng(lat, long);

                        //console.log(google.maps.geometry.spherical.computeDistanceBetween(myPosition, position));
                        var distance = google.maps.geometry.spherical.computeDistanceBetween(myPosition, position);
                        if (distance < MAP_RADIUS) {
                            console.log("INSIDE RADIUS: " + v.NAMN);
                            $("#console").append("<p><b>" + v.NAMN + "</b></p><p>" + v.Kännetecken.Artfakta + "</p>");
                        }

                        var marker = new google.maps.Marker({
                            position: position
                        });

                        var infowindowPoint = new google.maps.InfoWindow();

                        google.maps.event.addListener(marker, 'click', function () {
                            infowindowPoint.setContent('<div><strong>' + v.NAMN + '</strong><br>' +
                                'Taxon ID: ' + v.TaxonID + '<br>' +
                                v.Kännetecken.Artfakta + '</div>');
                            infowindowPoint.open(map, this);
                        });

                        marker.setMap(map)

                    });


                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.log('error ' + textStatus + " " + errorThrown);
                }
            });
        }, function () {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }
}