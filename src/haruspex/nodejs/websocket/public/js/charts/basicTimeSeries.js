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
	
	Highcharts.charts['basicTimeSeries'] = {
		chart: {
			renderTo: 'container',
			type: 'spline',
			animation: false
		},
		title: {
			text: 'Sentiment'
		},
		xAxis: {
			type: 'datetime'
		},
		yAxis: {
			title: {
				text: 'Coefficient (m)'
			}
		},
		tooltip: {
			shared: true
		},
		legend: {
			enabled: false
		}					
	}
}