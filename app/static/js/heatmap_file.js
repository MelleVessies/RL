// set the dimensions and margins of the graph
function heatmap_func(){
var margin = {top: 30, right: 30, bottom: 30, left: 30},
  width = 450 - margin.left - margin.right,
  height = 450 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my_dataviz")
.append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
.append("g")
  .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

// Labels of row and columns
var myEpsilons = ["0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"]
var myDiscounts = ["0.8", "0.8", "0.8", "0.8", "0.8", "0.8", "0.8", "0.8", "0.8", "0.8", "0.80"]

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
      .text("Epsilon");

// Build X scales and axis:
var y = d3.scaleBand()
  .range([ height, 0 ])
  .domain(myDiscounts)
  .padding(0.01);
svg.append("g")
  .call(d3.axisLeft(y))
  svg.append("text")
      .attr("transform",
            "translate( -30 ," +
                           (height/2 + margin.top + 0) + ")")
      .style("text-anchor", "middle")
      .text("Date");


// Build color scale
var myColor = d3.scaleLinear()
  .range(["white", "#69b3a2"])
  .domain([1,100])

//Read the data
// d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/heatmap_data.csv", function(data) {
d3.csv("static/csv/grid-no_tricks_settings-CartPole-v1-return.csv", function(data) {

  svg.selectAll()
      .data(data, function(d) {return d.group+':'+d.variable;})
      .enter()
      .append("rect")
      .attr("x", function(d) { return x(d.Epsilon) })
      .attr("y", function(d) { return y(d.Discount) })
      .attr("width", x.bandwidth() )
      .attr("height", y.bandwidth() )
      .style("fill", function(d) { return myColor(d.value)} )

})
}
