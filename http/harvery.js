
  $(document).ready(function(){
    $.ajax({
        //the api to get each indivual twicher
        url: "https://api.harveyneeds.org/api/v1/shelters",
        data: {
          //to get it in json format
          accept: 'application/json',
          format: 'json'
        },
        //if something goes wrong user will get notified with message
        error: function(err){
          //$('#info').html("An error has occurred");
          console.log(err)
          console.log(err.promise);
          console.log("no");
        },
        dataType: 'json',
        //if the api call is success full the success function kicks in
        success: function(data){
        
         var therealstuff ={
          features:[],
          type:"FeatureCollection"
        }
         for(var i = 0; i < data.shelters.length; i++){
         
           
           var thestuff = {
             type:"",
             properties:{},
             geometry:{}
           }
           var typ="";
           var properties = {
             name:"",
             address:"",
             phone:0,
             taking: "Not Accepting"
           }
           var thelat;
           var thelon;
           var lonlat =[];
           var geometry = {
             coordinates: [],
             type: ""
             
           }
           typ = "Feature";
           properties.name = data.shelters[i].shelter;
           properties.address = data.shelters[i].address;
           properties.phone = data.shelters[i].phone;
           if(data.shelters[i].accepting == true){
             properties.taking = "Accepting"
           }
           thelat = data.shelters[i].latitude;
           thelon = data.shelters[i].longitude;
           //lonlat.push(thelon);
           //lonlat.push(thelat);
           geometry.coordinates.push(thelon);
           geometry.coordinates.push(thelat);
           geometry.type = "Point";

           thestuff.type = typ;
           thestuff.properties = properties;
           thestuff.geometry = geometry;
           therealstuff.features.push(thestuff);
           
        }
        console.log(therealstuff);
        geojson = therealstuff;

        mapboxgl.accessToken = 'pk.eyJ1IjoiYW5keWVscDM2NDgiLCJhIjoiY2o3eHp4b3VrM3lpbjJ3bnF0MndkZXpoYiJ9.db-ayR6Byqk3KyJnO1jVXA';
        
        var map = new mapboxgl.Map({
          container: 'map',
          style: 'mapbox://styles/mapbox/streets-v9',
          center: [-95.3667, 29.7583],
          zoom: 11
        });
        map.on('load',function(){
          map.addLayer({
            "id": "places",
            "type": "symbol",
            "source":{
              "type": "geojson",
              "data": geojson
            }
          })
        })
        

        
        console.log(geojson);
        map.addControl(new MapboxGeocoder({
          accessToken: mapboxgl.accessToken
         }))

        geojson.features.forEach(function(marker) {
          
            // create a HTML element for each feature
            var el = document.createElement('div');
            el.className = 'marker';
          
            // make a marker for each feature and add to the map
            new mapboxgl.Marker(el, { offset: [-50 / 2, -50 / 2] })
            .setLngLat(marker.geometry.coordinates)
          
            //make a dialog box for each marker
            new mapboxgl.Marker(el, { offset: [-50 / 2, -50 / 2] })
            .setLngLat(marker.geometry.coordinates)
            .setPopup(new mapboxgl.Popup({ offset: 25 }) // add popups
            .setHTML('<h4>' + marker.properties.name + '</h4><p>' + marker.properties.address + '</p><p>' + marker.properties.phone +'</p><p>'+ marker.properties.taking+'</p>'))
            
            //add the everything to the map
            
            .addTo(map);
            //console.log(marker.properties.name);
          });
          // map.on('click', function (e) {
          //   console.log(e);
          //   //console.log(geojson);
          //   for(var j = 0; j < geojson.features.length;++j){
          //     if(Math.abs(e.lngLat.lng - geojson.features[j].geometry.coordinates[0]) < .0100 
          //     && Math.abs(e.lngLat.lat - geojson.features[j].geometry.coordinates[1]) < .0100){
          //       console.log(geojson.features[j].properties.name);
          //     }
          //   }
            
          //   new mapboxgl.Popup()
          //       .setLngLat(e.features[0].geometry.coordinates)
          //       .setHTML(e.features[0].properties.description)
          //       .addTo(map);
          // });

        },
        //GET request
        type: 'GET'
      });
});

  

