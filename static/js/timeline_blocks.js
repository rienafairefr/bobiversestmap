var margin = {top: 50, right: 0, bottom: 100, left: 30},
    width = 960 - margin.left - margin.right,
    height = 430 - margin.top - margin.bottom,
    gridSize = Math.floor(width / 100),
    legendWidth = (gridSize / 2 + 4),
    buckets = 10;
    mu = 10,
    sigma = 5,
    lambda = 0.1;

var svg = d3.select("svg")
    .append("g");

d3.json("timeline_blocks.json",

    function (error, data) {

        var maxNum = Math.round(d3.max(data.matrix, function (d) {
            return d.value;
        }));

        var colors = colorbrewer.RdYlGn[buckets];

        var colorScale = d3.scale.quantile()
            .domain([0, buckets - 1, maxNum])
            .range(colors);

        var tip = d3.tip()
            .attr('class', 'd3-tip')
            .style("visibility", "visible")
            .offset([-20, 0])
            .html(function (d) {
                return "Value:  <span style='color:red'>" + Math.round(d.value);
            });

        tip(svg.append("g"));

        var dim1Labels = svg.selectAll(".dim1Label")
            .data(data.dim1)
            .enter().append("text")
            .text(function (d) {
                return d.label;
            })
            .attr("x", 0)
            .attr("y", function (d, i) {
                return i * gridSize;
            })
            .style("text-anchor", "end")
            .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
            .attr("class", "mono");

        var dim2Labels = svg.selectAll(".dim2Label")
            .data(data.dim2)
            .enter().append("text")
            .text(function (d) {
                return d.label;
            })
            .attr("x", function (d, i) {
                return i * gridSize;
            })
            .attr("y", 0)
            .style("text-anchor", "middle")
            .attr("transform", "translate(" + gridSize / 2 + ", -6)")
            .attr("class", "mono");

        var heatMap = svg.selectAll(".dim2")
            .data(data.matrix)
            .enter().append("rect")
            .attr("x", function (d) {
                return (d.dim2 - 1) * gridSize;
            })
            .attr("y", function (d) {
                return (d.dim1 - 1) * gridSize;
            })
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("class", "dim2 bordered")
            .attr("width", gridSize - 2)
            .attr("height", gridSize - 2)
            .style("fill", colors[0])
            .attr("class", "square")
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide);

        heatMap.transition()
            .style("fill", function (d) {
                return colorScale(d.value);
            });

        heatMap.append("title").text(function (d) {
            return d.value;
        });

        var legend = svg.selectAll(".legend")
            .data([0].concat(colorScale.quantiles()), function (d) {
                return d;
            })
            .enter().append("g")
            .attr("class", "legend");

        legend.append("rect")
            .attr("x", function (d, i) {
                return gridSize * 11;
            })
            .attr("y", function (d, i) {
                return (i * legendWidth + 7);
            })
            .attr("width", gridSize / 2)
            .attr("height", gridSize / 2)
            .style("fill", function (d, i) {
                return colors[i];
            })
            .attr("class", "square");

        legend.append("text")
            .attr("class", "mono")
            .text(function (d) {
                return "≥ " + Math.round(d);
            })
            .attr("x", function (d, i) {
                return gridSize * 11 + 25;
            })
            .attr("y", function (d, i) {
                return (i * legendWidth + 20);
            });

        var title = svg.append("text")
            .attr("class", "mono")
            .attr("x", gridSize * 11)
            .attr("y", -6)
            .style("font-size", "14px")
            .text("Legend");
    }
);