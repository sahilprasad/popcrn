function mapcreate(data){
    var format = function(d) {

            return d3.format('1f')(d);
        }

        var map = d3.geomap.choropleth()
            .geofile('../../static/topojson/world/countries.json')
            .colors(colorbrewer.RdPu[9])
            .column('sentiment')
            .format(format)
            .legend(true)
            .unitId('Country Code');

        d3.csv(data, function(error, d) {
            d3.select('#map')
                .datum(d)
                .call(map.draw, map);
        });
}
