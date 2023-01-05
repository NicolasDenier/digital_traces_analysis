var canvas = document.getElementById("distributionChart");
var labels = [
    {% for item in labels %}
        {{ item }},
    {% endfor %}]
var values0 = [
        {% for item in values0 %}
            {{ item }},
        {% endfor %}]
var values1 = [
            {% for item in values1 %}
                {{ item }},
            {% endfor %}]

var option = {
  tooltips: {
    enabled: false
  },
  legend: {
    display: true
  },
  scales: {
    yAxes: [
      {
        display: false,
      }
    ],
    xAxes: [{
        id: "bar-x-axis2",
        display: false,
        barThickness: 30,
        stacked: true,
        categoryPercentage: 0,
        barPercentage: 0.5,
    },
    {
        display: true,
        stacked: true,
        id: "bar-x-axis1",
        barThickness: 30,
        type: 'category',
        categoryPercentage: 0,
        barPercentage: 1,
        gridLines: {
            offsetGridLines: true,
            display: false
        },
        offset: true
    }
    ]
  }
};

var myBarChart = Chart.Bar(canvas, {
  data: {
    labels: labels,
    datasets: [{
    data: values0,
    backgroundColor: "rgba(93, 42, 66,0.5)", //"#5D2A4290"
    label: "dictionary",
    stack: 1,
    xAxisID: "bar-x-axis1"
    },{
    data: values1,
    backgroundColor: "rgba(251, 99, 118,0.5)",//"#FB637690",
    label: "counter",
    stack: 2,
    xAxisID: "bar-x-axis2"
    }]},
  options: option
});

