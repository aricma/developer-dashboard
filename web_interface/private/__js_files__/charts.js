/* globals Chart:false */

(() => {
    'use strict'

    const CHART_COLORS = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)',
    }

    const all_charts = document.querySelectorAll('canvas.chart')
    all_charts.forEach((element) => {
        const fileName = element.dataset.fileName
        const chartType = element.dataset.chartType
        fetch(fileName)
            .then(response => response.json())
            .then(data => makeChart(element, data['data_points'], chartType))
            .catch(error => console.error('Error:', error))
    })

    function makeChart(element, data, chartType) {
        switch (chartType) {
            case 'velocity':
                return makeVelocityChart(element, data)
            case 'burn-down':
                return makeBurnDownChart(element, data)
        }
    }

    function makeVelocityChart(element, data) {
        const yData = data.map((each) => each.y)
        const averageValue = yData.reduce((sum, each) => sum + each, 0) / (yData.length || 1)
        const maxInData = Math.ceil(Math.max(...yData))
        const newMaxBasedOnAverage = Math.ceil(averageValue * 3)
        const max = (newMaxBasedOnAverage > maxInData) ? newMaxBasedOnAverage : maxInData
        new Chart(element, {
            type: 'line',
            data: {
                labels: data.map((each) => each.x),
                datasets: [{
                    data: yData,
                    lineTension: 0,
                    borderColor: '#007bff',
                    borderWidth: 4,
                    pointBackgroundColor: '#007bff',
                    backgroundColor: 'transparent',
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
                scales: {
                    y: {
                        min: 0,
                        max: max,
                    },
                },
            },
        })
    }

    function makeBurnDownChart(element, data) {
        const yData = data.map((each) => each.y)
        new Chart(element, {
            type: 'line',
            data: {
                labels: data.map((each) => each.x),
                datasets: [{
                    data: yData,
                    lineTension: 0,
                    borderColor: '#007bff',
                    borderWidth: 4,
                    pointBackgroundColor: '#007bff',
                    backgroundColor: CHART_COLORS.yellow,
                    fill: true,
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
                scales: {
                    y: {
                        min: 0,
                        max: Math.ceil(Math.max(...yData) * 1.2),
                    },
                },
            },
        })
    }
})()
