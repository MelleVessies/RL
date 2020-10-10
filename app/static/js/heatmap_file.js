// set the dimensions and margins of the graph
function heatmap_func(){
var margin = {top: 40, right: 40, bottom: 40, left: 40},
  width = 450 - margin.left - margin.right,
  height = 450 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my_dataviz")
.append("svg")
  .attr("width", width + margin.left + margin.right )
  .attr("height", height + margin.top + margin.bottom)
.append("g")
  .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

// Labels of row and columns
var myEpsilons = ["0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]
var myDiscounts = ["0.8", "0.82", "0.84", "0.86", "0.88", "0.9", "0.92", "0.94", "0.96", "0.98", "1.0"]

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
  // .domain([0.1,0.2,0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
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


// Build color scale
var myColor = d3.scaleLinear()
  .range(["white", "#69b3a2"])
  .domain([1,100])

//Read the data
// d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/heatmap_data.csv", function(data) {
d3.csv("static/csv/grid-no_tricks_settings-CartPole-v1-return.csv", function(data) {

    // create a tooltip
    var tooltip = d3.select("#my_dataviz")
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
      tooltip.style("opacity", 1)
    }
    var mousemove = function(d) {
      tooltip
        .html("The exact value of<br>this cell is: " + d.value)
        .style("left", (d3.mouse(this)[0]+70) + "px")
        .style("top", (d3.mouse(this)[1] +600) + "px")
    }
    var mouseleave = function(d) {
      tooltip.style("opacity", 0)
    }

  svg.selectAll()
      .data(data, function(d) {return d.group+':'+d.variable;})
      .enter()
      .append("rect")
      .attr("x", function(d) { return x(d.Epsilon) })
      .attr("y", function(d) { return y(d.Discount) })
      .attr("width", x.bandwidth() )
      .attr("height", y.bandwidth() )
      .style("fill", function(d) { return myColor(d.value)} )
      .on("mouseover", mouseover)
      .on("mousemove", mousemove)
      .on("mouseleave", mouseleave)
})
}
