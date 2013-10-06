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

var width = 960,
    height = 500;

var svg = d3.select('#viz')
    .append('svg')
    .attr('width', width)
    .attr('height', height);

var node, link;

var force = d3.layout.force()
    .gravity(0.05)
    .charge(-100)
    .friction(0.3)
    .linkDistance(50)
    .size([width, height]);

force.on('tick', function() {
    node.attr('transform', function(d) { return 'translate('+d.x+','+d.y+')'; })
        .attr('clip-path', function(d) { return 'url(#clip-'+d.index+')'; });

    link.attr('x1', function(d) { return d.source.x; })
        .attr('y1', function(d) { return d.source.y; })
        .attr('x2', function(d) { return d.target.x; })
        .attr('y2', function(d) { return d.target.y; });
});

d3.json('static/json/data.json', function(err, data) {

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
        .style("stroke-width", function(d) { return Math.log(d.value); })
        .style("stroke", "black");

    node = svg.selectAll('.node')
        .data( data.nodes )
        .enter().append('g')
        .attr('title', name)
        .attr('class', 'node')
        .call( force.drag );

    node.append('circle')
        .attr('r', function(d){
            var value = 3.5*(((d.score - min)/(max-min))-0.5);
            return 30*(1/(1+Math.exp(-value)));
        })
        .attr('fill', '#231198')
        .attr('title', function(d) {return d.name;});

    force
        .nodes( data.nodes )
        .links( data.links )
        .start();
    svg.append("p").attr('id', 'svg-finished');
});

var change = function(){
    d3.select(this).attr('r', 25)
        .attr("fill", "red")
        .style("stroke","yellow");
    };

$('#svg-finished').waitUntilExists(function(){
    d3.selectAll(".node").on('click', change);
});
