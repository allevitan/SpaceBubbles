(function ($) {

/**
* @function
* @property {object} jQuery plugin which runs handler function once specified element is inserted into the DOM
* @param {function} handler A function to execute at the time when the element is inserted
* @param {bool} shouldRunHandlerOnce Optional: if true, handler is unbound after its first invocation
* @example $(selector).waitUntilExists(function);
*/

$.fn.waitUntilExists    = function (handler, shouldRunHandlerOnce, isChild) {
    var found       = 'found';
    var $this       = $(this.selector);
    var $elements   = $this.not(function () { return $(this).data(found); }).each(handler).data(found, true);

    if (!isChild)
    {
        (window.waitUntilExists_Intervals = window.waitUntilExists_Intervals || {})[this.selector] =
            window.setInterval(function () { $this.waitUntilExists(handler, shouldRunHandlerOnce, true); }, 500)
        ;
    }
    else if (shouldRunHandlerOnce && $elements.length)
    {
        window.clearInterval(window.waitUntilExists_Intervals[this.selector]);
    }

    return $this;
};

}(jQuery));

var width = 0.8*$(window).width(),
    height = 0.8*$(window).height();

var svg = d3.select('#viz')
    .append('svg')
    .attr('width', width)
    .attr('height', height);

var node, link;

var force = d3.layout.force()
    .gravity(0.05)
    .charge(-100)
    .friction(0.3)
    .linkDistance(66)
    .size([width, height]);

force.on('tick', function() {
    node.attr('transform', function(d) { return 'translate('+d.x+','+d.y+')'; })
        .attr('clip-path', function(d) { return 'url(#clip-'+d.index+')'; });

    link.attr('x1', function(d) { return d.source.x; })
        .attr('y1', function(d) { return d.source.y; })
        .attr('x2', function(d) { return d.target.x; })
        .attr('y2', function(d) { return d.target.y; });
});

d3.json('/api/get/graph', function(err, data) {

    var max = 0;
    var min = 100;
    data.nodes.forEach(function(d, i) {
        d.id = i;
        if (d.score > max){
            max = d.score;
        }
        if (d.score < min){
            min = d.score;
        }
    });

    link = svg.selectAll('.link')
        .data( data.links )
        .enter().append('line')
        .attr('class', 'link')
        .style("stroke-width", function(d) { return Math.log(d.value)+1; })
        .style("stroke", "black")
        .style("stroke-opacity", function(d){ return Math.log(d.value)+0.66});

    node = svg.selectAll('.node')
        .data( data.nodes )
        .enter().append('g')
        .attr('title', name)
        .attr('class', 'node');

    node.append('circle')
        .attr('r', function(d){
            var value = 3.5*(((d.score - min)/(max-min))-0.5);
            return 30*(1/(1+Math.exp(-value)));
        })
        .attr('title', function(d) {return d.name;})
        .attr('label', function(d) {return d.title;})
        .style('fill', function(d) {
            var value = d.score;
            var red = Math.floor(255*(Math.pow((value - min)/(max/15-min), 0.666)));
            var blue = 255-red;
            var value = "rgb(" + red + ",150," + blue + ')';
            return value;
        });

    force
        .nodes( data.nodes )
        .links( data.links )
        .start();
    svg.append("p").attr('id', 'svg-finished');
});

var change = function(){
    d3.selectAll(".node").style('visibility', 'hidden');
    d3.selectAll(".link").style('visibility', 'hidden');
    d3.select(this.firstChild)
        .transition()
        .style('visibility', 'visible')
        .duration(1000)
        .attr('r', '30%')
        .attr('fill','red');
    };

$('#svg-finished').waitUntilExists(function(){
    $("#viz").on("click", function(event){
        console.log(event.target.getAttribute('title'));
    });

    $("#viz").on("mouseover", function(event){
        $("#disWhereYouNeedToPutIt").text(event.target.getAttribute('title'));
    });
});
