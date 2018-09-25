  var itemSize = 22,
      cellSize = itemSize - 1,
      margin = {top: 120, right: 20, bottom: 20, left: 110};

  var width = 960 - margin.right - margin.left,
      height = 960 - margin.top - margin.bottom;

  var formatDate = d3.time.format("%Y-%m-%d");

  d3.json('timeline_blocks.json', function ( error, data) {

    var x_elements = d3.set(data.map(function( item ) { return item.x; } )).values(),
        y_elements = d3.set(data.map(function( item ) { return item.y; } )).values();

    var xScale = d3.scale.ordinal()
        .domain(x_elements)
        .rangeBands([0, x_elements.length * itemSize]);

    var xAxis = d3.svg.axis()
        .scale(xScale)
        .tickFormat(function (d) {
            return d;
        })
        .orient("top");

    var yScale = d3.scale.ordinal()
        .domain(y_elements)
        .rangeBands([0, y_elements.length * itemSize]);

    var yAxis = d3.svg.axis()
        .scale(yScale)
        .tickFormat(function (d) {
            return d;
        })
        .orient("left");

    var colorScale = d3.scale.threshold()
        .domain([0.85, 1])
        .range(["#2980B9", "#E67E22", "#27AE60", "#27AE60"]);

    var svg = d3.select('svg')
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var cells = svg.selectAll('rect')
        .data(data)
        .enter().append('g').append('rect')
        .attr('class', 'cell')
        .attr('width', cellSize)
        .attr('height', cellSize)
        .attr('y', function(d) { return yScale(d.y); })
        .attr('x', function(d) { return xScale(d.x); })
        .attr('fill', function(d) { return colorScale(d.value); });

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .selectAll('text')
        .attr('font-weight', 'normal');

    svg.append("g")
        .attr("class", "x axis")
        .call(xAxis)
        .selectAll('text')
        .attr('font-weight', 'normal')
        .style("text-anchor", "start")
        .attr("dx", ".8em")
        .attr("dy", ".5em")
        .attr("transform", function (d) {
            return "rotate(-65)";
        });
  });