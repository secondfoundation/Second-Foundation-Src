if (Highcharts != null) {
	if (Highcharts.charts == null) {
		Highcharts.charts = {};
	}
	
	if (Highcharts.getChart == null) {
		Highcharts.getChart = function(chartId, containerId) {
			var opts = Highcharts.charts[chartId];
			opts.chart.renderTo = containerId;
			return opts;
		}
	}
	
	Highcharts.charts['basicBarChart'] = {
		chart: {
			renderTo: 'container',
			type: 'bar',
			animation: false
		},
		title: {
			text: 'Top Terms'
		},
		xAxis: {
			categories: [],
			title: {
				text: null
			}
		},
		yAxis: {
			min: 0,
			title: {
				text: 'Occurrences',
				align: 'high'
			}
		},
		tooltip: {
			formatter: function() {
				return ''+
					this.series.name +': '+ this.y +' occurrences';
			}
		},
		plotOptions: {
			bar: {
				dataLabels: {
					enabled: true
				}
			}
		},
		legend: {
			layout: 'vertical',
			align: 'right',
			verticalAlign: 'top',
			x: -100,
			y: 100,
			floating: true,
			borderWidth: 1,
			backgroundColor: '#FFFFFF',
			shadow: true
		},
		credits: {
			enabled: false
		}
	}
}