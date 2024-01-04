/* globals Chart:false */

(() => {
    'use strict'

    const all_charts = document.querySelectorAll('canvas.chart')
    all_charts.forEach((element) => {
        const fileName = element.dataset.fileName
        fetch(fileName)
            .then(response => response.json())
            .then(data => makeChart(element, data["data_points"]))
            .catch(error => console.error('Error:', error))
    })

    function makeChart(element, data) {
        new Chart(element, {
            type: 'line',
            data: {
                labels: data.map((each) => each.x),
                datasets: [{
                    data: data.map((each) => each.y),
                    lineTension: 0,
                    backgroundColor: 'transparent',
                    borderColor: '#007bff',
                    borderWidth: 4,
                    pointBackgroundColor: '#007bff',
                }],
            },
            options: {
                plugins: {
                    legend: {
                        display: false,
                    },
                    tooltip: {
                        boxPadding: 3,
                    },
                },
            },
        })
    }
})()
