var charactersMap = {}, datesMap = {}, locationsMap = {};

// Set the dimensions of the canvas / graph
var margin = {top: 30, right: 20, bottom: 30, left: 50},
    width = 600 - margin.left - margin.right,
    height = 270 - margin.top - margin.bottom;


// Get the data
d3.json("travels.json", function (error, all_data) {

    // Set the ranges
    var x = d3.time.scale().range([0, width]);
    var y = d3.scale.linear().range([0, height]);

    // Define the axes
    var xAxis = d3.svg.axis().scale(x)
        .orient("bottom").ticks(5);

    var yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(5);

    // Define the line
    var valueline = d3.svg.line()
        .x(function (d) {
            return x(d.date.start);
        })
        .y(function (d) {
            return y(d.location);
        });

    // Adds the svg canvas
    var svg = d3.select("#all_books")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    all_data = wrangle(all_data);

    all_data.forEach(function (line_data) {
        var data = line_data.travels;
        // Scale the range of the data
        x.domain([0, d3.max(data, function (d) {
            return d.date.start;
        })]);
        y.domain([0, d3.max(data, function (d) {
            return d.location.distance;
        })]);

        // Add the valueline path.
        svg.append("path")
            .attr("class", "line")
            .attr("d", valueline(data));

        // Add the scatterplot
        svg.selectAll("dot")
            .data(data)
            .enter().append("circle")
            .attr("r", 3.5)
            .attr("cx", function (d) {
                return x(d.date.start);
            })
            .attr("cy", function (d) {
                return y(d.location);
            });
    });
    // Add the X Axis
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    // Add the Y Axis
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);
});

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
