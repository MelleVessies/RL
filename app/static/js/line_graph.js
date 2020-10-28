function create_line_graph(data, target, graph_id, title = "") {
    // No idea wtf this does
    var R = 6

    let colors = [
        '#035dfd',
        '#c93cff',
        '#36ad02',
        '#8d4903',
        '#fc0404'
    ];

    // set the dimensions and margins of the graph
    var margin = {top: 40, right: 200, bottom: -50, left: 70},
        width = 610 - margin.left - margin.right,
        height = 350 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select(target.get(0))
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom + 100)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("font-color", "white")
        .style("text-decoration", "underline")
        .style("fill", "black")
        .text(title + " Average Returns");

    svg.append("text")
        .attr("transform",
            "translate( " + - (margin.left + 26)/2  +"," +
                           (height/2) + ")")
        .style("text-anchor", "middle")
        .text("Return");

    svg.append("text")
        .attr("transform",
            "translate(" + (width/2) + " ," +
                           (height + margin.top) + ")")
        .style("text-anchor", "middle")
        .text("Number of episodes");


    let all_x = [];
    let all_y = [];
    let line_names = [];

    // Ugliest way possible to later get the max
    for (const [seed_idx, seed_res] of Object.entries(data.data)) {
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
        .exponent(0.3)
        .domain([Math.min(...all_y) - 1, Math.max(...all_y) + 5])
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    var legendMouseover = function(d, i) {
        svg.select('#' + graph_id +"_line_"+i).dispatch('dohighlightLine');
        d3.select(this).style("outline", '2px solid rgba(127,124,124,0.7)');
    }

    var legendMouseleave = function(d,i) {
        svg.select('#' + graph_id +"_line_"+i).dispatch('mouseout');
        d3.select(this).style("outline", "none");
    }


    var svgLegend = svg.append('g')
            .attr('class', 'gLegend')
            .attr("transform", "translate(" + (width + 20) + "," + 0 + ")")

    var legend = svgLegend.selectAll('.legend')
        .data(line_names)
        .enter().append('g')
                .attr("class", "legend")
                .style('margin-top', '3px')
                .style('padding', '5px')
                .attr("transform", function (d, i) {return "translate(0," + i * 20 + ")"})
                .on('mouseover', legendMouseover)
                .on('mouseleave', legendMouseleave)

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

    var highlightLine = function(d, target){
        if(typeof target === 'number'){
            target = this
        }
        d3.select(target).transition().style("opacity", "0.6");
    }

    var showToolTip = function(target){
        tooltip.transition()
            .style("opacity", 1);
        tooltip
            .html(line_names[d3.select(target).attr('data-line-idx')])
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY - 28) + "px")
            .style("z-index", 9999999)
    }

    var mouseover = function(d) {
        highlightLine(d, this)
        showToolTip(this)
    }

    var mouseleave = function(d,i) {
        d3.select(this).transition().style("opacity", "0");
        tooltip.transition().style("opacity", 0)
    }


    $(Object.values(data.data)).each((idx, res) => {


        svg.append("path")
            .datum(res)
            .attr("fill", "none")
            .attr("stroke", colors[idx])
            .attr("stroke-width", 1.5)
            // .attr("id", function(d,i){ return "graph_line_"+i})
            .attr("d", d3.line()
                .x(function (d) {
                    return x(d.x)
                })
                .y(function (d) {
                    return y(d.y)
                })
            );

        if(data.std !== undefined) {
            //Show confidence interval
            svg.append("path")
                .datum(res)
                .attr("fill", colors[idx])
                .attr("stroke", "none")
                .attr('opacity', "0.3")
                .attr("d", d3.area()
                    .x(function (d) {
                        return x(d.x)
                    })
                    .y0(function (d, i) {
                       return y(d.y - (data.std[line_names[idx]][i].y/5));
                    })
                    .y1(function (d, i) {
                        return y(d.y + (data.std[line_names[idx]][i].y)/5);
                    })
            )
        }

        svg.append("path")
            .datum(res)
            .attr("fill", "none")
            .attr("stroke", colors[idx])
            .attr("stroke-width", 7)
            .attr("opacity", 0)
            .attr("data-line-idx", idx)
            .attr("id", graph_id +"_line_"+idx)
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
            .on("dohighlightLine", highlightLine)
    });
}
