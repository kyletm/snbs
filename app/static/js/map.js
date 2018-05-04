<script>
    function myMap() {
    var myCenter = new google.maps.LatLng(40.3495, -74.6527);
    var mapProp = {center:myCenter, zoom:18, scrollwheel:false, draggable:false, mapTypeId:google.maps.MapTypeId.ROADMAP};
    var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
    var marker = new google.maps.Marker({position:myCenter});
    marker.setMap(map);
    }
</script>