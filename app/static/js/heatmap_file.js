// set the dimensions and margins of the graph
function init_heatmap(data, target, plot_type, upper, lower){
    var margin = {top: 40, right: 250, bottom: 40, left: 40},
      width = 700 - margin.left - margin.right,
      height = 450 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select(target.get(0))
    .append("svg")
      .attr("width", width + margin.left + margin.right )
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // Labels of row and columns
    var myEpsilons = [];
    var myDiscounts = [];
    var myValues = [];

    $(data).each((idx, val) => {
        myEpsilons.push(val.epsilon);
        myDiscounts.push(val.discount_factor);
        myValues.push(val[plot_type]);
    });

    myEpsilons.sort(function(a, b) {
        return a - b;
    });

    myDiscounts.sort(function(a, b) {
        return a - b;
    });

    // Build X scales and axis:
    var x = d3.scaleBand()
      .range([ 0, width ])
      .domain(myEpsilons)
      .padding(0.01);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
    svg.append("text")
        .attr("transform",
            "translate(" + (width/2) + " ," +
                           (height + margin.top + 0) + ")")
        .style("text-anchor", "middle")
        .text("\u03B5"); // unicode for epsilon

    // Build X scales and axis:
    var y = d3.scaleBand()
        .range([ height, 0 ])
        .domain(myDiscounts)
        .padding(0.01);

    svg.append("g")
        .attr("transform", "translate(-1, 0)")
        .call(d3.axisLeft(y))
    svg.append("text")
        .attr("transform",
            "translate( " + - (margin.left + 26)/2  +"," +
                           (height/2 + 0) + ")")
        .style("text-anchor", "middle")
        .text("\u03B3"); // unicode for gamma

    // function range(start, stop, step) {
    //     var a = [start], b = start;
    //
    //     while (b < stop) {
    //         a.push(b += step);
    //     }
    //     return a;
    // }


    // Build color scale
    var myColor = d3.scaleQuantize()
        .range(colorbrewer.Blues[9])
        .domain([lower,upper])

    // Color legend.
    var colorScale = d3.scaleQuantize()
        .range(colorbrewer.Blues[9])
        .domain([lower, upper])

    var colorLegend = d3.legendColor()
        .labelFormat(d3.format(".0f"))
        .scale(colorScale)
        .shapePadding(35)
        .shapeWidth(50)
        .shapeHeight(40)
        .labelAlign("middle");

    $('text.label').attr('transform', 'translate(55, 25)');

    svg.append("g")
        .attr("height", height - 30)
        .attr("transform", "translate(" + (width + 20) + "," + 20 + ")")
        .call(colorLegend);

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
    var mouseover = function(d) {
      tooltip.transition()
          .duration(200)
          .style("opacity", 1);
      tooltip
            .html("<b>Value: </b>" + d[plot_type] + "<br/><b>Epsilon: </b>" + d.epsilon + "<br/><b>Discount factor: </b>" + d.discount_factor)
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY - 28) + "px")
            .style("z-index", 9999999)

    }

    var mouseleave = function(d) {
      tooltip.transition()
          .duration(200)
          .style("opacity", 0)
    }

    svg.selectAll()
        .data(data, function(d) {return d;})
        .enter()
        .append("rect")
        .attr("x", function(d) { return x(d.epsilon) })
        .attr("y", function(d) { return y(d.discount_factor) })
        .attr("width", x.bandwidth() )
        .attr("height", y.bandwidth() )
        .style("fill", function(d) {return myColor(d[plot_type]);} )
        .on("mouseover", mouseover)
        .on("mouseout", mouseleave)
}
