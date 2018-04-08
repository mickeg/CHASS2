/* global $ */

$(document).ready(function () {
    init();

    function init() {
        initSelectors();
        
        //getObservationCoordinates();
    }

    function getObservationCoordinates(selected) {
        $.support.cors = true;
        taxonID = $('#speicesSelector').find(":selected").val();
        console.log("taxonID", taxonID);
        $.ajax({
            url: 'http://127.0.0.1:5000/api/v1/observations?TaxonID='+taxonID,
            dataType: "json",
            crossDomain: true,
            success: function (data) {
                console.log(data)
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log('error ' + textStatus + " " + errorThrown);
            }
        });
    }

    function initSelectors(){
        $("#observations").click(function(){
            var selected = $('#speicesSelector').find(":selected").val();
            console.log("selected", selected);
            getObservationCoordinates(selected)
        });
    }

});

