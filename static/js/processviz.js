var chart;
$(document).ready(function () {
    $("#datepicker1").datepicker({
        showOn: 'button',
        buttonImage: 'css/base/images   /calendar.gif',
        buttonImageOnly: true,
        dateFormat: "yy-mm-dd"
    });
});

function draw_chart() {
    var url = "/main/api/process/data";
    chart = new Highcharts.Chart({}); //PROBLEM ONE - empty initialisation

    $.getJSON(url, function (data1) {
        var options = {
            chart: {
                renderTo: 'container',
                type: 'line'
            },

            xAxis: {
                type: 'datetime'

            },
            yAxis: {
                title: {
                    text: 'test'
                }

            },
            series: [{
                data: eval(data1.result[0].dayactivity),
                name: "name"
            }]

        };
        //var chart = new Highcharts.Chart(options); // removed var here, as it looks you want it to be global
        chart = new Highcharts.Chart(options);
    });
}
draw_chart();