// Google Map
let map;

// Markers for map
let markers = [];

// Info window
let info = new google.maps.InfoWindow();


// Execute when the DOM is fully loaded
$(document).ready(function() {

    // Styles for map
    // https://developers.google.com/maps/documentation/javascript/styling
    let styles = [

        // Hide Google's labels
        {
            featureType: "all",
            elementType: "labels",
            stylers: [
                {visibility: "off"}
            ]
        },

        // Hide roads
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [
                {visibility: "off"}
            ]
        }

    ];

    // Options for map
    // https://developers.google.com/maps/documentation/javascript/reference#MapOptions
    let options = {
        center: {lat: 42.3770, lng: -71.1256}, // Cambridge, Massachusetts
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        maxZoom: 14,
        panControl: true,
        styles: styles,
        zoom: 13,
        zoomControl: true
    };

    // Get DOM node in which map will be instantiated
    let canvas = $("#map-canvas").get(0);

    // Instantiate map
    map = new google.maps.Map(canvas, options);

    // Configure UI once Google Map is idle (i.e., loaded)
    google.maps.event.addListenerOnce(map, "idle", configure);

});


// Add marker for place to map
function addMarker(place)
{
    // Beautifying, entries admin_code1 may be empty
    let markerTitle = place.admin_code1 == "" ? place.place_name : place.place_name + ", " + place.admin_code1;

    // Simple Google map marker
    let image = {
        url: 'http://maps.google.com/mapfiles/ms/micons/red-dot.png',
        // The origin for this image is (0, 0).
        origin: new google.maps.Point(0, 0),
        // Label origin, arbitrarily defined to be (15, 40), looks neat
        labelOrigin: new google.maps.Point(15, 40)
      };

    // Creates the actual marker
    let marker = new google.maps.Marker({
        position: {lat: place.latitude, lng: place.longitude},
        map: map,
        icon: image,
        label: markerTitle
    });

    // For retrieving articles based on the searched postal code
    let geo = {
        geo: place.postal_code
    };

    marker.addListener('click', function(event) {
        $.getJSON("/articles", geo, function(results, textStatus, jqXHR) {
        // Puts an event listener to make use of showInfo function
        // That will be listening to mouse click then showing up the info window

            // Make an unordered list to store news
            let contents = "<ul>";
            for (let i = 0; i < results.length; i++)
            {
                // `` is template literals
                contents += `<li><a href="${results[i].link}" target="_blank">
                    ${results[i].title}</a></li>`;
            }
            contents += "</ul>";
            showInfo(marker, contents);
        });
    });

    // Add the marker into markers array
    markers.push(marker);
}


// Configure application
function configure()
{
    // Update UI after map has been dragged
    google.maps.event.addListener(map, "dragend", function() {

        // If info window isn't open
        // http://stackoverflow.com/a/12410385
        if (!info.getMap || !info.getMap())
        {
            update();
        }
    });

    // Update UI after zoom level changes
    google.maps.event.addListener(map, "zoom_changed", function() {
        update();
    });

    // Configure typeahead
    // Handlebars using conditional block helpers to evaluate if admin_name1 is null or not
    $("#q").typeahead({
        highlight: false,
        minLength: 1
    },
    {
        display: function(suggestion) { return null; },
        limit: 10,
        source: search,
        templates: {
            suggestion: Handlebars.compile(
                "<div>" +
                "{{#if admin_name1}}" +
                "{{place_name}}, {{admin_name1}}, {{postal_code}}" +
                "{{else}}" +
                "{{place_name}}, {{postal_code}}" +
                "{{/if}}" +
                "</div>"
            )
        }
    });

    // Re-center map after place is selected from drop-down
    $("#q").on("typeahead:selected", function(eventObject, suggestion, name) {

        // Set map's center
        map.setCenter({lat: parseFloat(suggestion.latitude), lng: parseFloat(suggestion.longitude)});

        // Update UI
        update();
    });

    // Hide info window when map is clicked
    google.maps.event.addListener(map, "click", function() {
        info.close();
    });

    // Hide info window when text box has focus
    $("#q").focus(function(eventData) {
        info.close();
        $("#q").typeahead('close');
    });

    // Re-enable ctrl- and right-clicking (and thus Inspect Element) on Google Map
    // https://chrome.google.com/webstore/detail/allow-right-click/hompjdfbfmmmgflfjdlnkohcplmboaeo?hl=en
    document.addEventListener("contextmenu", function(event) {
        event.returnValue = true;
        event.stopPropagation && event.stopPropagation();
        event.cancelBubble && event.cancelBubble();
    }, true);

    // Update UI
    update();

    // Give focus to text box
    $("#q").focus();
}


// Remove markers from map
function removeMarkers()
{
    for(let i = 0; i < markers.length; i++)
    {
        markers[i].setMap(null);
    }

    // Removes the reference
    markers = [];
}


// Search database for typeahead's suggestions
function search(query, syncResults, asyncResults)
{
    // Get places matching query (asynchronously)
    let parameters = {
        q: query
    };
    $.getJSON("/search", parameters, function(data, textStatus, jqXHR) {

        // Call typeahead's callback with search results (i.e., places)
        asyncResults(data);
    });
}


// Show info window at marker with content
function showInfo(marker, content)
{
    // Start div
    let div = "<div id='info'>";
    if (typeof(content) == "undefined")
    {
        // http://www.ajaxload.info/
        div += "<img alt='loading' src='/static/ajax-loader.gif'/>";
    }
    else
    {
        div += content;
    }

    // End div
    div += "</div>";

    // Set info window's content
    info.setContent(div);

    // Open info window (if not already open)
    info.open(map, marker);
}


// Update UI's markers
function update()
{
    // Get map's bounds
    let bounds = map.getBounds();
    let ne = bounds.getNorthEast();
    let sw = bounds.getSouthWest();

    // Get places within bounds (asynchronously)
    let parameters = {
        ne: `${ne.lat()},${ne.lng()}`,
        q: $("#q").val(),
        sw: `${sw.lat()},${sw.lng()}`
    };
    $.getJSON("/update", parameters, function(data, textStatus, jqXHR) {

       // Remove old markers from map
       removeMarkers();

       // Add new markers to map
       // The data is from rows being jsonified in application.py
       for (let i = 0; i < data.length; i++)
       {
           addMarker(data[i]);
       }
    })
};
