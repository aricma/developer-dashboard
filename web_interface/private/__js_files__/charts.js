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

    function getChartYMaxForVelocityData(data) {
        const allYData = [...data['team_velocity'], ...data['developer_velocity']].map(each => each.y)
        const averageValue = allYData.reduce((sum, each) => sum + each, 0) / (allYData.length || 1)
        const maxInData = Math.ceil(Math.max(...allYData))
        const newMaxBasedOnAverage = Math.ceil(averageValue * 3)
        return (newMaxBasedOnAverage > maxInData) ? newMaxBasedOnAverage : maxInData
    }

    function makeVelocityChart(element, data) {
        new Chart(element, {
            type: 'line',
            data: {
                datasets: [
                    {
                        label: 'Team Velocity',
                        data: data['team_velocity'],
                        borderColor: CHART_COLORS.blue,
                        borderWidth: 4,
                        pointBackgroundColor: CHART_COLORS.blue,
                    },
                    {
                        label: 'Developer Velocity',
                        data: data['developer_velocity'],
                        borderColor: CHART_COLORS.purple,
                        borderWidth: 4,
                        pointBackgroundColor: CHART_COLORS.purple,
                    },
                ],
            },
            options: {
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            usePointStyle: true,
                        },
                    },
                    tooltip: {
                        boxPadding: 3,
                    },
                },
                scales: {
                    y: {
                        min: 0,
                        max: getChartYMaxForVelocityData(data),
                        grid:
                            {
                                color: 'rgb(100,100,100)',
                            },
                    },
                    x: {
                        grid: {
                            color: 'rgb(100,100,100)',
                        },
                    },
                },
            },
        })
    }

    function makeBurnDownChart(element, data) {
        const yData = data.map(each => each.y);
        const realBurnDownData = data.filter((each) => !(each?.meta?.estimated))
        const lastDataPointOfRealDataToConnectTheGraphs = realBurnDownData[realBurnDownData.length - 1]
        const estimatedBurnDownData = [
            lastDataPointOfRealDataToConnectTheGraphs,
            ...data.filter((each) => each?.meta?.estimated),
        ]
        new Chart(element, {
            type: 'line',
            data: {
                datasets: [
                    {
                        label: "Finished Tasks",
                        data: realBurnDownData,
                        borderColor: CHART_COLORS.blue,
                        borderWidth: 4,
                        pointBackgroundColor: CHART_COLORS.blue,
                        backgroundColor: 'rgb(255, 205, 86, .75)',
                        fill: true,
                    },
                    {
                        label: "Estimated Task Burn Down",
                        data: estimatedBurnDownData,
                        borderColor: CHART_COLORS.grey,
                        borderWidth: 4,
                        pointBackgroundColor: CHART_COLORS.grey,
                        borderDash: [6, 6],
                        fill: false,
                    },
                ],
            },
            options: {
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            usePointStyle: true,
                        },
                    },
                    tooltip: {
                        boxPadding: 3,
                    },
                },
                scales: {
                    y: {
                        min: 0,
                        max: Math.ceil(Math.max(...yData) * 1.2),
                        grid: {
                            color: 'rgb(100,100,100)',
                        },
                    },
                    x: {
                        grid: {
                            color: 'rgb(100,100,100)',
                        },
                    },
                },
            },
        })
    }
})()
