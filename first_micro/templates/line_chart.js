Chart.defaults.global.animationSteps = 50;
Chart.defaults.global.tooltipYPadding = 16;
Chart.defaults.global.tooltipCornerRadius = 0;
Chart.defaults.global.tooltipTitleFontStyle = "normal";
Chart.defaults.global.tooltipFillColor = "rgba(0,0,0,0.8)";
Chart.defaults.global.animationEasing = "easeOutBounce";
Chart.defaults.global.responsive = false;
Chart.defaults.global.scaleLineColor = "black";
Chart.defaults.global.scaleFontSize = 16;

var labels=[
    {% for item in labels %}
      "{{ item }}",
    {% endfor %}
  ]
var data1 = [
    {% for item in values1 %}
        {{ item }},
    {% endfor %}]
var data2 = [
    {% for item in values2 %}
        {{ item }},
    {% endfor %}]
    new Chart("chart", {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
        data: data1,
        label: "Cookie food",
        borderColor: "#5D2A42",
        fill: false
        },{
        data: data2,
        label: "Cookie web",
        borderColor: "#FB6376",
        fill: false
        }]
    },
    options: {
        hover: {
        mode: 'index',
        intersect: true
        },
    }
});