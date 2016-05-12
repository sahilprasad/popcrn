/**
 * @author Trushitha
 * based on particlefield from @mrjnicol
 *
 */

$(document).ready(function() {
  $('#starfield').particleground({
    dotColor: '#DDDDDD',
    lineColor: 'rgba(255, 255, 255, .2)',
    particleRadius: 3,
    proximity: 80,
    minRadiusPct: .4,
    maxRadiusPct: 1.8,
    minOpacity: .4,
    maxOpacity: .8,
    parallax: true
  });
});
