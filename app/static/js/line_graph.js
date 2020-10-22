function create_line_graph(data, target) {
    // console.log(data);

    // No idea wtf this does
    var R = 6

    let colors = [
        '#035dfd',
        '#f8d804',
        '#36ad02',
        '#af5b03',
        '#fc0404'
    ];

    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 200, bottom: 30, left: 60},
        width = 600 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select(target.get(0))
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    let all_x = [];
    let all_y = [];
    let line_names = [];

    // Ugliest way possible to later get the max
    for (const [seed_idx, seed_res] of Object.entries(data)) {
        line_names.push(seed_idx);
        for (const [bla, res_entry] of Object.entries(seed_res)) {
            all_x.push(res_entry.x)
            all_y.push(res_entry.y)
        }
    }

    var x = d3.scaleLinear()
        .domain([-1, Math.max(...all_x) + 5])
        .range([0, width]);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    var y = d3.scalePow()
        .exponent(0.2)
        .domain([Math.min(...all_y) - 1, Math.max(...all_y) + 5])
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));


    var svgLegend = svg.append('g')
            .attr('class', 'gLegend')
            .attr("transform", "translate(" + (width + 20) + "," + 0 + ")")

    var legend = svgLegend.selectAll('.legend')
        .data(line_names)
        .enter().append('g')
                .attr("class", "legend")
                .attr("transform", function (d, i) {console.log(d); return "translate(0," + i * 20 + ")"})

    legend.append("circle")
        .attr("class", "legend-node")
        .attr("cx", 0)
        .attr("cy", 0)
        .attr("r", R)
        .style("fill", (d, i)=> { return colors[i] })

    legend.append("text")
        .attr("class", "legend-text")
        .attr("x", R*2)
        .attr("y", R/2)
        .style("fill", "#A9A9A9")
        .style("font-size", 12)
        .text((d) => {return d})


    // Show confidence interval
    // svg.append("path")
    //     .datum(data)
    //     .attr("fill", "#cce5df")
    //     .attr("stroke", "none")
    //     .attr("d", d3.area()
    //         .x(function (d) {
    //             return x(d.x)
    //         })
    //         .y0(function (d) {
    //             return y(d.CI_right)
    //         })
    //         .y1(function (d) {
    //             return y(d.CI_left)
    //         })
    //     )



    // create a tooltip
    var tooltip = d3.select(target.get(0))
      .append("div")
      .style("opacity", 0)
      .attr("class", "tooltip")
      .style("background-color", "white")
      .style("border", "solid")
      .style("border-width", "2px")
      .style("border-radius", "5px")
      .style("padding", "5px")

    // Three function that change the tooltip when user hover / move / leave a cell
    var mouseover = function(d,i) {
        d3.select("#graph_line_"+i).transition().style("fill", "#007DBC");

        tooltip.transition()
            .style("opacity", 1);
        tooltip
            .html(line_names[i])
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY - 28) + "px")
            .style("z-index", 9999999)

    }

    var mouseleave = function(d,i) {
        d3.select("#graph_line_"+i).transition().style("fill", colors[i]);

        tooltip.transition().style("opacity", 0)
    }


    $(Object.values(data)).each((idx, res) => {

        svg.append("path")
            .datum(res)
            .attr("fill", "none")
            .attr("stroke", colors[idx])
            .attr("stroke-width", 1.5)
            .attr("id", function(d,i){ return "graph_line_"+i})
            .attr("d", d3.line()
                .x(function (d) {
                    return x(d.x)
                })
                .y(function (d) {
                    return y(d.y)
                })
            )
            .on("mouseover", mouseover)
            .on("mouseout", mouseleave)
    });
}
