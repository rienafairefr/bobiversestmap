<template>
  <div>
    <h1>Character Co-occurrence</h1>
    <p>
      We count any time two characters talk to each other in a sentence. Blue
      are the Bobs, other characters are grouped by affiliation (e.g. Deltans,
      Poseidonians)
    </p>

    <div>
      <div>
        <div :click="selectTab(0)">All books</div>
        <div :click="selectTab(1)">Book 1</div>
        <div :click="selectTab(2)">Book2</div>
        <div :click="selectTab(3)">Book 3</div>
      </div>
      <svg id="chart"></svg>
    </div>
  </div>
</template>
<style scoped>
.wrapper div div {
  display: inline-block;
}
</style>
<script>
import * as d3 from "d3";
import { url_for } from "../data.js";

export default {
  data() {
    return {
      selectedTab: 0,
      windowWidth: window.innerWidth,
    };
  },
  mounted() {
    this.selectTab(0);
    window.onresize = () => {
      this.windowWidth = window.innerWidth;
      this.draw();
    };
  },
  methods: {
    selectTab(index) {
      this.selectedTab = index;
      this.draw();
    },
    draw() {
      let json =
        this.selectedTab == 0
          ? url_for("cooccurences.json")
          : url_for(`book/${this.selectedTab + 1}/cooccurences.json`);
      var parent = "#chart";
      var margin = {
        top: 120,
        right: 0,
        bottom: 10,
        left: 160,
      };
      var width = 600;
      var height = 600;

      var x = d3.scaleBand().range([0, width]);
      console.log(x);
      var z = d3.scaleLinear().domain([0, 4]).clamp(true);
      var c = d3.scaleOrdinal(d3.schemeCategory10);

      var svg = d3
        .select(parent)
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .style("margin-left", "0px")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      // Based on the user-selected input text above, make the appropriate api call and retrieve the json
      d3.json(json).then((data) => {
        console.log({ data });
        var matrix = [];
        var nodes = data.nodes;
        var n = nodes.length;

        // Compute index per node.
        nodes.forEach(function (node, i) {
          node.index = i;
          node.count = 0;
          matrix[i] = d3.range(n).map((j) => ({
            x: j,
            y: i,
            z: 0,
          }));
        });

        // Convert links to matrix; count character occurrences.
        data.links.forEach(function (link) {
          var source = nodes.filter((obj) => obj.id === link.source).shift();
          var target = nodes.filter((obj) => obj.id === link.target).shift();
          if (source.index == target.index) return;
          matrix[source.index][target.index].z += link.value;
          matrix[target.index][source.index].z += link.value;
          matrix[source.index][source.index].z += link.value;
          matrix[target.index][target.index].z += link.value;
          nodes[source.index].count += link.value;
          nodes[target.index].count += link.value;
        });

        // Precompute the orders.
        var orders = {
          name: d3
            .range(n)
            .sort((a, b) => d3.ascending(nodes[a].name, nodes[b].name)),
          count: d3.range(n).sort((a, b) => nodes[b].count - nodes[a].count),
          group: d3.range(n).sort((a, b) => nodes[b].group - nodes[a].group),
        };

        // The default sort order.
        x.domain(orders.name);

        svg
          .append("rect")
          .attr("class", "background")
          .attr("width", width)
          .attr("height", height)
          .attr("fill", "white");

        var row = svg
          .selectAll(".row")
          .data(matrix)
          .enter()
          .append("g")
          .attr("class", "row")
          .attr("transform", (d, i) => "translate(0," + x(i) + ")")
          .each(row_func);

        row.append("line").attr("x2", width);

        row
          .append("text")
          .attr("x", -6)
          .attr("y", x.bandwidth() / 2)
          .attr("dy", ".32em")
          .attr("text-anchor", "end")
          .text((d, i) => nodes[i].name);

        var column = svg
          .selectAll(".column")
          .data(matrix)
          .enter()
          .append("g")
          .attr("class", "column")
          .attr("transform", (d, i) => "translate(" + x(i) + ")rotate(-90)");

        column.append("line").attr("x1", -width);

        column
          .append("text")
          .attr("x", 6)
          .attr("y", x.bandwidth / 2)
          .attr("dy", ".32em")
          .attr("text-anchor", "start")
          .text((d, i) => nodes[i].name);

        function row_func(row) {
          d3.select(this)
            .selectAll(".cell")
            .data(row.filter((d) => d.z))
            .enter()
            .append("rect")
            .attr("class", "cell")
            .attr("x", (d) => x(d.x))
            .attr("width", x.bandwidth)
            .attr("height", x.bandwidth)
            .style("fill-opacity", (d) => z(d.z))
            .style("fill", (d) =>
              nodes[d.x].group == nodes[d.y].group ? c(nodes[d.x].group) : null
            )
            .on("mouseover", mouseover)
            .on("mouseout", mouseout);
        }

        function mouseover(p) {
          d3.selectAll(".row text").classed("active", (d, i) => i == p.y);
          d3.selectAll(".column text").classed("active", (d, i) => i == p.x);
        }

        function mouseout() {
          d3.selectAll("text").classed("active", false);
        }

        d3.select("#order").on("change", function () {
          clearTimeout(timeout);
          order(this.value);
        });

        function order(value) {
          x.domain(orders[value]);

          var t = svg.transition().duration(2500);

          t.selectAll(".row")
            .delay((d, i) => x(i) * 4)
            .attr("transform", (d, i) => "translate(0," + x(i) + ")")
            .selectAll(".cell")
            .delay((d) => x(d.x) * 4)
            .attr("x", (d) => x(d.x));

          t.selectAll(".column")
            .delay((d, i) => x(i) * 4)
            .attr("transform", (d, i) => "translate(" + x(i) + ")rotate(-90)");
        }

        var timeout = setTimeout(function () {
          order("group");
          d3.select("#order").property("selectedIndex", 2).node().focus();
        }, 5000);
      });
    },
  },
};
</script>
