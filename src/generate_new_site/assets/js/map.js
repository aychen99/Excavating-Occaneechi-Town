export default function define(runtime, observer) {
    const main = runtime.module();
    const fileAttachments = new Map([["excavations@1.json","https://comp523eot.netlify.app/assets/json/excavations@1_minify.json"]]);
    main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
    main.variable(observer("chart")).define("chart", ["d3","excavation","path"], function(d3,excavation,path)
  {
    const width = 520;
    const height = 600;
  
    const zoom = d3.zoom()
        .scaleExtent([1, 8])
        .on("zoom", zoomed);
  
    const svg = d3.create("svg")
        .attr("viewBox", [0, 0, width, height])
        .on("click", reset);
  
    const g = svg.append("g");
  
    const gr = g.append("g")
        .attr("stroke", "blue")
        .attr("fill", "#FFF")
        .attr("cursor", "pointer")
      .selectAll("path")
      .data(excavation.grid.features)
      .join("path")
        .on("click", clicked)
        .attr("d", path);
    
    const ph = g.append("g")
        .attr("stroke", "black")
        .attr("fill-opacity", "0")
        .attr("cursor", "pointer")
      .selectAll("path")
      .data(excavation.postholes.features)
      .join("path")
        .attr("d", path);
    
    const stru_i = g.append("g")
        .attr("stroke", "orange")
        .attr("fill-opacity", "0")
        .attr("cursor", "pointer")
      .selectAll("path")
      .data(excavation.structures_internal.features)
      .join("path")
        .attr("d", path);
    
    const stru_o = g.append("g")
        .attr("stroke", "orange")
        .attr("stroke-dasharray", "5,5")
        .attr("fill-opacity", "0")
        .attr("cursor", "pointer")
      .selectAll("path")
      .data(excavation.structures_external.features)
      .join("path")
        .on("click", clicked)
        .attr("d", path);
    
    const feat = g.append("g")
        .attr("stroke", "red")
        .attr("fill-opacity", "0")
        .attr("cursor", "pointer")
      .selectAll("path")
      .data(excavation.features.features)
      .join("path")
        .on("click", clicked)
        .attr("d", path);
  
    svg.call(zoom);
  
    function reset() {
      svg.transition().duration(750).call(
        zoom.transform,
        d3.zoomIdentity,
        d3.zoomTransform(svg.node()).invert([width / 2, height / 2])
      );
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
    }
  
    function zoomed(event) {
      const {transform} = event;
      g.attr("transform", transform);
      g.attr("stroke-width", 1 / transform.k);
    }
  
    return svg.node();
  }
  );
    main.variable(observer()).define(["md"], function(md){return(
  md`# Annex`
  )});
    main.variable(observer("path")).define("path", ["d3"], function(d3){return(
  d3.geoPath()
  )});
    main.variable(observer("d3")).define("d3", ["require"], function(require){return(
  require("d3@6")
  )});
    main.variable(observer("excavation")).define("excavation", ["FileAttachment"], function(FileAttachment){return(
  FileAttachment("excavations@1.json").json()
  )});
    return main;
  }