var charactersMap = {}, datesMap = {}, locationsMap = {};


var svg = d3.select("#all_books"),
    margin = {top: 20, right: 80, bottom: 30, left: 50},
    width = svg.attr("width") - margin.left - margin.right,
    height = svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var parseTime = d3.timeParse("%Y%m%d");

var x = d3.scaleTime().range([0, width]),
    y = d3.scaleLinear().range([height, 0]);

var line = d3.line()
    .curve(d3.curveBasis)
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.location); });


d3.csv('travels.csv', function(error, data){
  if (error) throw error;

  var characters = data.columns.slice(1).map(function(id) {
    return {
      id: id,
      values: data.map(function(d) {
        return {date: d.date, location: d[id]};
      })
    };
  });

  x.domain(d3.extent(data, function(d) { return d.date; }));

  y.domain([
    d3.min(characters, function(c) { return d3.min(c.values, function(d) { return d.location; }); }),
    d3.max(characters, function(c) { return d3.max(c.values, function(d) { return d.location; }); })
  ]);

  //z.domain(characters.map(function(c) { return c.id; }));

  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y))
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.71em")
      .attr("fill", "#000")
      .text("Temperature, ºF");

  var character = g.selectAll(".character")
    .data(characters)
    .enter().append("g")
      .attr("class", "character");

  character.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); });
      //.style("stroke", function(d) { return z(d.id); });

  character.append("text")
      .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.location) + ")"; })
      .attr("x", 3)
      .attr("dy", "0.35em")
      .style("font", "10px sans-serif")
      .text(function(d) { return d.id; });
});

function type(d, _, columns) {
  d.date = parseTime(d.date);
  for (var i = 1, n = columns.length, c; i < n; ++i) d[c = columns[i]] = +d[c];
  return d;
}


function wrangle(data) {
    return data.travels.map(function (travel_one_character) {
        return {
            character: characterById(travel_one_character.character_id),
            travels: travel_one_character.travels.map(function (travel) {
                var loc = locationById(travel.location_id);
                return loc !== null ? {date: dateById(travel.date_id), location: loc} : null;
            })
        };
    });

    // Helper to get characters by ID from the raw data
    function characterById(id) {
        charactersMap = charactersMap || {};
        charactersMap[id] = charactersMap[id] || data.characters.find(function (character) {
            return character.id === id;
        });
        if (charactersMap[id] === undefined) {
            console.log("id  not found " + id);
        }
        return charactersMap[id];
    }

    // Helper to get date by ID from the raw data
    function dateById(id) {
        datesMap = datesMap || {};
        datesMap[id] = datesMap[id] || data.dates.find(function (date) {
            return date.id === id;
        });
        if (datesMap[id] === undefined) {
            console.log("id  not found " + id);
        }
        return datesMap[id];
    }

    // Helper to get location by ID from the raw data
    function locationById(id) {
        locationsMap = locationsMap || {};
        if (id === null) return null;
        if (id instanceof Array) {
            return [locationById(id[0]), locationById(id[1])]
        } else {
            locationsMap[id] = locationsMap[id] || data.locations.find(function (location) {
                return location.id === id;
            });
            if (locationsMap[id] === undefined) {
                console.log("id  not found " + id);
            }
            return locationsMap[id];
        }
    }

}
