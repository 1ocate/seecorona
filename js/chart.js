<script src="https://d3js.org/d3.v5.min.js"></script>

<!-- Load billboard.js with base(or theme) style -->
<link rel="stylesheet" href="css/billboard.css">
<script src="js/billboard.js"></script>

var chart = bb.generate({
  data: {
    columns: [
	["data1", 300, 350, 300, 0, 0, 0],
	["data2", 130, 100, 140, 200, 150, 50]
    ],
    types: {
      data1: "area",
      data2: "area-spline"
    }
  },
  bindto: "#areaChart"
});
