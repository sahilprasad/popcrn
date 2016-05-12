var format = function(d) {
    d = d / 1000000;
    return d3.format(',.02f')(d) + 'M';
}

var map = d3.geomap.choropleth()
    .geofile('../../static/topojson/world/countries.json')
    .colors(colorbrewer.RdPu[9])
    .column('YR2010')
    .format(format)
    .legend(true)
    .unitId('Country Code');

d3.csv('../../static/data/sample.csv', function(error, data) {
    d3.select('#map')
        .datum(data)
        .call(map.draw, map);
});
