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

d3.csv('../../static/data/sample.csv', function(error, data) {
    d3.select('#map')
        .datum(data)
        .call(map.draw, map);
});
