function runmap() {
    const path = d3.geoPath();

    const width = 520;
    const height = 600;

    const context_name = d3.select("#context_name");

    const context_href = d3.select("#context_href");

    const zoom = d3.zoom()
        .scaleExtent([1, 8])
        .on("zoom", zoomed);

    const svg = d3.select("#map")
        .on("click", reset);

    const g = svg.append("g");

    var postholes = g.append("g")
        .attr("id", "postholes")
        .attr("stroke", "black")
        .attr("fill-opacity", "0")
        .attr("cursor", "pointer")
      .selectAll("path")
      .data(excavation.postholes.features)
      .join("path")
        .attr("d", path);

    const palisade = g.append("g")
        .attr("id", "palisade")
        .attr("stroke", "black")
        .attr("fill-opacity", "0")
        .attr("cursor", "pointer")
      .selectAll("path")
      .data(excavation.palisade.features)
      .join("path")
        .attr("d", path);

    var postholesVisible = true;

    const grid = g.append("g")
        .attr("id", "grid")
        .attr("stroke", "#0000FF")
        .attr("fill-opacity", "0")
        .attr("cursor", "pointer")
      .selectAll("path")
      .data(excavation.grid.features)
      .join("path")
        .on("click", clicked)
        .attr("id", function(d){return d.id;})
        .attr("d", path);

    const structures_internal = g.append("g")
        .attr("id", "structures-internal")
        .attr("stroke", "#FFA500")
        .attr("fill-opacity", "0")
        .attr("cursor", "pointer")
      .selectAll("path")
      .data(excavation.structures_internal.features)
      .join("path")
        .attr("d", path);

    const structures_external = g.append("g")
        .attr("id", "structures-external")
        .attr("stroke", "#FFA500")
        .attr("stroke-dasharray", "5,5")
        .attr("fill-opacity", "0")
        .attr("cursor", "pointer")
      .selectAll("path")
      .data(excavation.structures_external.features)
      .join("path")
        .on("click", clicked)
        .attr("id", function(d){return d.id;})
        .attr("d", path);

    const features = g.append("g")
        .attr("id", "features")
        .attr("stroke", "#FF0000")
        .attr("fill-opacity", "0")
        .attr("cursor", "pointer")
      .selectAll("path")
      .data(excavation.features.features)
      .join("path")
        .on("click", clicked)
        .attr("id", function(d){return d.id;})
        .attr("d", path);

    //Handle special element styles
    g.select("#feature_34").attr("stroke-dasharray", "1,1");
    g.select("#structure_4").attr("stroke-dasharray", "none");

    const postholesbutton = d3.select("#ph-toggle")
        .on("click", togglePostholes)

    const nofocusbutton = d3.select("#focus-none")
        .on("click", focusNone)

    const featuresbutton = d3.select("#focus-features")
        .on("click", focusFeatures)

    const structuresbutton = d3.select("#focus-structures")
        .on("click", focusStructures)

    const gridbutton = d3.select("#focus-grid")
        .on("click", focusGrid)

    svg.call(zoom);

    function togglePostholes() {
      if(postholesVisible) {
        postholesVisible = false;
        g.select("#postholes").remove();
      } else {
        postholesVisible = true;
        postholes = g.insert("g", ":first-child")
        .attr("id", "postholes")
        .attr("stroke", "black")
        .attr("fill-opacity", "0")
        .attr("cursor", "pointer")
      .selectAll("path")
      .data(excavation.postholes.features)
      .join("path")
        .attr("d", path);
      }
    }

    function reset() {
      svg.transition().duration(750).call(
        zoom.transform,
        d3.zoomIdentity,
        d3.zoomTransform(svg.node()).invert([width / 2, height / 2])
      );
      context_href.attr("href", "#");
      context_name.text("None").style("color", "");
    }

    function clicked(event, d) {
      const [[x0, y0], [x1, y1]] = path.bounds(d);
      event.stopPropagation();
      svg.transition().duration(750).call(
        zoom.transform,
        d3.zoomIdentity
          .translate(width / 2, height / 2)
          .scale(Math.min(8, 0.9 / Math.max((x1 - x0) / width, (y1 - y0) / height)))
          .translate(-(x0 + x1) / 2, -(y0 + y1) / 2),
        d3.pointer(event, svg.node())
      );
      context_href.attr("href", hrefs[d.id]["href"]);

      // Change text and font color of text after "Selected Context:"
      let name = hrefs[d.id]["name"];
      let lowercaseName = name.toLowerCase();
      let textColor = "";
      if (lowercaseName.includes("feature") || lowercaseName.includes("burial")) {
        textColor = "crimson";
      } else if (lowercaseName.includes("structure")) {
        textColor = "#FF4500";
      } else if (lowercaseName.includes("sq")) {
        textColor = "blue";
      } else {
        // Reset to default color when clicking on "None"
      }
      context_name.text(name).style("color", textColor);
    }

    function zoomed(event) {
      const {transform} = event;
      g.attr("transform", transform);
      g.attr("stroke-width", 1 / transform.k);
    }

    // Set up tooltip on hovering over a context
    var tooltipDiv = d3.select("body").append("div")
      .attr("class", "tooltip")
      .attr("id", "d3tooltip")
      .style("position", "absolute")
      .style("display", "none")
      .style("opacity", 0.93)
      .style("background-color", "white")
      .style("font-size", "1.2em")
      .style("border", "2px solid gray")
      .style("padding", "2px");

    /* Handler functions for the tooltip when hovering over the map */
    let mouseoverHandler = function(e) {
      // Prevent tooltip from displaying on touchscreens
      if (matchMedia("(hover: none) and (pointer: coarse)").matches) {
        return;
      }
      let name = hrefs[e.target.id]["name"];
      let lowercaseName = name.toLowerCase();
      let textColor = "";
      if (lowercaseName.includes("feature") || lowercaseName.includes("burial")) {
        textColor = "crimson";
      } else if (lowercaseName.includes("structure")) {
        textColor = "#FF4500";
      } else if (lowercaseName.includes("sq")) {
        textColor = "blue";
      } else {
        // Do nothing
      }
      d3.select("#d3tooltip")
        .style("display", "")
        .style("color", textColor)
        .text(hrefs[e.target.id]["name"]);
    };

    let mouseoutHandler = function(e) {
      d3.select("#d3tooltip").style("display", "none");
    };

    let mousemoveHandler = function(e) {
      if (matchMedia("(min-width: 768px").matches) {
        d3.select("#d3tooltip")
          .style("left", (e.pageX + 10) + "px")
          .style("right", "")
          .style("top", (e.pageY + 10) + "px");
      } else {
        // Determine whether the tooltip should be to the left or right of the
        // cursor based on location in the page, i.e. Make tooltip direction
        // change depending on where in the map it is, to avoid scrollbars from
        // appearing on mobile or narrower screens
        const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
        const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
        if (e.pageX > vw * 2 / 3) {
          d3.select("#d3tooltip")
            .style("left", "")
            .style("right", (vw - (e.pageX) - 10) + "px")
            .style("top", (e.pageY + 10) + "px");
        } else {
          d3.select("#d3tooltip")
            .style("left", (e.pageX + 10) + "px")
            .style("right", "")
            .style("top", (e.pageY + 10) + "px");
        }
      }
    };

    /* 
     * Adjust clickable areas and tooltip display depending on the pressed
     * context button
     */
    function addTooltipHandlers(objectToAddTo) {
      objectToAddTo.on("mouseover", mouseoverHandler)
        .on("mouseout", mouseoutHandler)
        .on("mousemove", mousemoveHandler);
    }

    function removeTooltipHandlers(objectToRemoveFrom) {
      objectToRemoveFrom.on("mouseover", null)
        .on("mouseout", null)
        .on("mousemove", null);
    }

    function focusNone() {
      structures_external.on("click", clicked);
      features.on("click", clicked);
      grid.on("click", clicked);
      g.select("#grid").raise();
      g.select("#structures-internal").raise();
      g.select("#structures-external").raise();
      g.select("#features").raise();
      removeTooltipHandlers(structures_external);
      removeTooltipHandlers(features);
      removeTooltipHandlers(grid);
      addTooltipHandlers(structures_external);
      addTooltipHandlers(features);
      addTooltipHandlers(grid);
    }

    function focusGrid() {
      structures_external.on("click", null);
      features.on("click", null);
      grid.on("click", clicked);
      g.select("#structures-internal").raise();
      g.select("#structures-external").raise();
      g.select("#features").raise();
      g.select("#grid").raise();
      removeTooltipHandlers(d3.select("svg").selectAll("path"));
      removeTooltipHandlers(structures_external);
      removeTooltipHandlers(features);
      addTooltipHandlers(grid);
    }

    function focusFeatures() {
      structures_external.on("click", null);
      grid.on("click", null);
      features.on("click", clicked);
      g.select("#grid").raise();
      g.select("#structures-internal").raise();
      g.select("#structures-external").raise();
      g.select("#features").raise();
      removeTooltipHandlers(d3.select("svg").selectAll("path"));
      removeTooltipHandlers(structures_external);
      removeTooltipHandlers(grid);
      addTooltipHandlers(features);
    }

    function focusStructures() {
      features.on("click", null);
      grid.on("click", null);
      structures_external.on("click", clicked);
      g.select("#features").raise();
      g.select("#grid").raise();
      g.select("#structures-internal").raise();
      g.select("#structures-external").raise();
      removeTooltipHandlers(d3.select("svg").selectAll("path"));
      removeTooltipHandlers(features);
      removeTooltipHandlers(grid);
      addTooltipHandlers(structures_external);
    }

    // Run focusNone to start
    focusNone();

    return;
}
