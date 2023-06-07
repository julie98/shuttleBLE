function initMap() {
  // The location of Uluru
  const center = { lat: 36.999980, lng: -122.062050 };
  // The map, centered at Uluru
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 8,
    center: center,
  });

  const infoWindow = new google.maps.InfoWindow({
    content: "",
    disableAutoPan: true,
  });
  // Create an array of alphabetical characters used to label the markers.
  const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  // Add some markers to the map.
  const markers = locations.map((val, i) => {
    const label = labels[i % labels.length];
    var position = val[0]
    console.log(position)
    console.log(val)
    const marker = new google.maps.Marker({
      position,
      label,
    })
    console.log(position)
    if (val[1] === "stage 1") {
        marker.setIcon("http://maps.google.com/mapfiles/ms/icons/red-dot.png");
    } else {
        marker.setIcon("http://maps.google.com/mapfiles/ms/icons/green-dot.png");
    }

    // markers can only be keyboard focusable when they have click listeners
    // open info window when marker is clicked
    marker.addListener("click", () => {
      infoWindow.setContent(label);
      infoWindow.open(map, marker);
    });
    return marker;
  });

  // Add a marker clusterer to manage the markers.
  console.log(markers)
  new markerClusterer.MarkerClusterer({ markers, map });
}

const locations = [
  [{ lat: 36.999980, lng: -122.062050 }, "stage 1"] ,
  [{ lat: 36.999950, lng: -122.062113 }, "stage 1"] ,
  [{ lat: 36.999920, lng: -122.062170 }, "stage 1"] ,
  [{ lat: 36.999900, lng: -122.062200 }, "stage 1"] ,
  [{ lat: 36.999880, lng: -122.062250 }, "stage 2"] ,
  [{ lat: 36.999860, lng: -122.062270 }, "stage 2"] ,
  [{ lat: 36.999800, lng: -122.062300 }, "stage 2"] ,
  [{ lat: 36.999790, lng: -122.062330 }, "stage 2"] ,
  [{ lat: 36.999770, lng: -122.062360 }, "stage 2"] ,
  [{ lat: 36.999740, lng: -122.062400 }, "stage 2"] ,
];

window.initMap = initMap;
