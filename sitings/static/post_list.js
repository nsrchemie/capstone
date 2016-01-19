// window.AddEventListener('load', function() {

//     var script = document.createElement('script');
//     script.text = 
//         $(document).ready(function(){
//     var lat = $('#addition_form');
//     lat.hide();

// });
// $('#show_form').click(function(){
//     $("#addition_form").toggle()

//     function addMarker(e){
//     var newMarker = new L.marker(e.latlng).addTo(map);
//         var m = newMarker.getLatLng();
//         $('#id_location').val(m.lat + ',' + m.lng);
//         map.off("click");
// };
// map.on('click', addMarker);
// });

//         var portland = [45.5200, -122.6819];
//         var defaultzoom = 8;
//         var map = L.map('map').setView(portland, defaultzoom);
//         var newMarker;
//         var mapLink = 
//             '<a href="http://openstreetmap.org">OpenStreetMap</a>';
//         L.tileLayer(
//             'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//             attribution: '&copy; ' + mapLink + ' Contributors',
//             maxZoom: 18,
//             }).addTo(map);
// {% for post in posts %}
//             marker = new L.marker([{{post.location}}],
//                 {title : "{{post.title}}"})
//                 .bindPopup("<img src={{post.picture.url}} height='200' width='280'>");
//                 .addTo(map);
// {% endfor %}


// );
//     document.body.appendChild(script)
// });