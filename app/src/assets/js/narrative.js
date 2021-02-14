// Request the data
var charactersMap = {};

function get_data(datafile, parent) {
  d3.json(datafile, function(err, response) {
    var svg, scenes, width, height, sceneWidth;

    // Get the data in the format we need to feed to d3.layout.narrative().scenes
    scenes = wrangle(response);

    // Some defaults
    sceneWidth = 10;
    width = scenes.length * sceneWidth * 4;
    height = 600;
    labelSize = [150, 15];

    // The container element (this is the HTML fragment);
    svg = d3
      .select(parent)
      .append("svg")
      .attr("id", "narrative-chart")
      .attr("width", width)
      .attr("height", height);

    // Calculate the actual width of every character label.
    scenes.forEach(function(scene) {
      scene.characters.forEach(function(character) {
        character.width =
          svg
            .append("text")
            .attr("opacity", 0)
            .attr("class", "temp")
            .text(character.name)
            .node()
            .getComputedTextLength() + 10;
      });
    });

    var tip = d3
      .tip()
      .attr("class", "d3-tip")
      .offset([-10, 0])
      .html(function(d) {
        return "<span style='color:red'>" + d.description + "</span>";
      });

    var tip2 = d3
      .tip()
      .attr("class", "d3-tip")
      .offset([-10, 0])
      .html(function(d) {
        return "<span style='color:blue'>" + d.character.name + "</span>";
      });

    // Remove all the temporary labels.
    svg.selectAll("text.temp").remove();

    // Do the layout
    narrative = d3.layout
      .narrative()
      .scenes(scenes)
      .size([width, height])
      .pathSpace(30)
      .groupMargin(10)
      .labelSize([250, 15])
      .scenePadding([5, sceneWidth / 2, 5, sceneWidth / 2])
      .labelPosition("left")
      .layout();

    // Get the extent so we can re-size the SVG appropriately.
    svg.attr("height", narrative.extent()[1]);

    function strongLinkCharacter(character) {
      svg
        .selectAll(".link ")
        .filter("." + character.id)
        .call(function(l) {
          l.attr("stroke-opacity", 1);
        });
    }
    function transparentAllLinks() {
      svg.selectAll(".link").call(function(l) {
        l.attr("stroke-opacity", 0.1);
      });
    }
    function strongAllLinks() {
      svg.selectAll(".link").call(function(l) {
        l.attr("stroke-opacity", 1);
      });
    }

    svg.on("click", strongAllLinks);

    // Draw the scenes
    svg
      .selectAll(".scene")
      .data(narrative.scenes())
      .enter()
      .append("g")
      .attr("class", "scene")
      .attr("transform", function(d) {
        var x, y;
        x = Math.round(d.x) + 0.5;
        y = Math.round(d.y) + 0.5;
        return "translate(" + [x, y] + ")";
      })
      .append("rect")
      .attr("pointer-events", function() {
        return "visible";
      })
      .attr("width", sceneWidth)
      .attr("height", function(d) {
        return d.height;
      })
      .attr("y", 0)
      .attr("x", 0)
      .attr("rx", 3)
      .attr("ry", 3)
      .on("mouseover", tip.show)
      .on("mouseout", tip.hide)
      .on("click", function(d) {
        if (this.hasAttribute("highlighted")) {
          strongAllLinks();
          this.removeAttribute("highlighted");
        } else {
          transparentAllLinks();
          d.characters.forEach(strongLinkCharacter);
          this.setAttribute("highlighted", true);
        }
      });

    // Draw appearances
    svg
      .selectAll(".scene")
      .selectAll(".appearance")
      .data(function(d) {
        return d.appearances;
      })
      .enter()
      .append("circle")
      .attr("cx", function(d) {
        return d.x;
      })
      .attr("cy", function(d) {
        return d.y;
      })
      .attr("r", function() {
        return 5;
      })
      .attr("class", function(d) {
        return "appearance " + d.character.id;
      });

    // Draw links
    svg
      .selectAll(".link")
      .data(narrative.links())
      .enter()
      .append("path")
      .attr("class", function(d) {
        return "link " + d.character.id;
      })
      .attr("d", narrative.link())
      .on("click", function(d) {
        if (this.hasAttribute("highlighted")) {
          strongAllLinks();
          this.removeAttribute("highlighted");
        } else {
          transparentAllLinks();
          strongLinkCharacter(d.character);
          this.setAttribute("highlighted", true);
        }
      })
      .on("mouseover", tip2.show)
      .on("mouseout", tip2.hide);

    svg.call(tip);
    svg.call(tip2);

    // Draw intro nodes
    svg
      .selectAll(".intro")
      .data(narrative.introductions())
      .enter()
      .call(function(s) {
        var g, text;

        g = s.append("g").attr("class", "intro");

        g.append("rect")
          .attr("y", -4)
          .attr("x", -4)
          .attr("width", 4)
          .attr("height", 8);

        text = g.append("g").attr("class", "text");

        // Apppend two actual 'text' nodes to fake an 'outside' outline.
        text.append("text");
        text.append("text").attr("class", "color");

        g.attr("transform", function(d) {
          var x, y;
          x = Math.round(d.x);
          y = Math.round(d.y);
          return "translate(" + [x, y] + ")";
        });

        g.selectAll("text")
          .attr("text-anchor", "end")
          .attr("y", "4px")
          .attr("x", "-8px")
          .text(function(d) {
            return d.character.name;
          });

        g.select(".color").attr("class", function(d) {
          return "color " + d.character.affiliation;
        });

        g.select("rect").attr("class", function(d) {
          return d.character.affiliation;
        });
      });
  });
}

get_data("data.json", "#all_books");
get_data("book/1/data.json", "#book1");
get_data("book/2/data.json", "#book2");
get_data("book/3/data.json", "#book3");

function wrangle(data) {
  return data.scenes.map(function(scene) {
    return {
      characters: scene.character_ids.map(characterById),
      description: scene.description,
      y: scene.y_pos
    };
  });

  // Helper to get characters by ID from the raw data
  function characterById(id) {
    charactersMap = charactersMap || {};
    charactersMap[id] =
      charactersMap[id] ||
      data.characters.find(function(character) {
        return character.id === id;
      });
    if (charactersMap[id] === undefined) {
      console.log("id  not found " + id);
    }
    return charactersMap[id];
  }
}
