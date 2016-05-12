# interactive web pages with javascript/d3

## Three points about javascript:

- Everything in javascript is an object
```
var foo = 'a string'
var bar = foo.length
console.log("foo = "+foo)
console.log("bar = "+bar)
```

- Including html documents
```
<html>
  <head>
    <title>example html document</title>
  </head>
  <body>
    <script src="http://d3js.org/d3.min.js"/>
    <div>
      <p>Hello world</p>
    </div
  </body>
</html>
```

- Giving rise to the Document Object Model (DOM)
```
var title = document.getElementsByTagName('title')
console.log(title)
```

## Data Driven Documents

- d3 provides a way to bind data to DOM elements...
```
var data = [1,2,4,8,16]
d3.select('body').selectAll('p').data(data)
```

- ...and a pattern to use those data to manipulate the DOM
```
var data = [1,2,4,8,16]
// Select/Bind
var selection = d3.select('body').selectAll('p').data(data)
// Enter
selection.enter().append('p')
// Update
selection.html(function(d){return d})
// Exit
selection.exit().remove()
```

## Scalable Vector Graphics (SVG)
```
<svg>
  <g>
    <circle></circle>
  </g>
</svg>
```

- SVG can be included in an html document and is treated as part of the DOM
```
var svg = d3.select('body').append('svg');
svg.attr('width',300).attr('height',300);
var data = [{x:20,y:100,z:2},{x:120,y:150,z:4},{x:220,y:200,z:8}]
// Select/Bind
var selection = svg.selectAll('circle').data(data)
// Enter
selection.enter().append('circle')
// Update
selection.attr('cx',function(d){return d.x})
         .attr('cy',function(d){return d.y})
         .attr('r',function(d){return d.z})
// Exit
selection.exit().remove()
```

- Scales and transitions make things even more exciting
```
var xScale = d3.scale.sqrt()
                     .domain([0,300])
                     .range([300,0])
// Update
selection.transition()
         .delay(function(d){return 200 * d.z})
         .duration(1500)
         .attr('cx',function(d){return xScale(d.x)})
```

- Three little circles

Even more fun with circles at [bost.ocks.org](https://bost.ocks.org/mike/circles/)

## Phylo-plot
[github.com/rjchallis/phylo-plot](https://github.com/rjchallis/phylo-plot)
