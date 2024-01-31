
// var ctx = document.getElementById('myChart').getContext('2d');
var graphData = {
    type: 'line',
    data: {
        datasets: [{
            label: '# of votes',
            data: [ ],
            backgroundColor: [
                'rgba(73, 198, 230, 0.5)',
            ],
            borderWidth: 1
        }]
    },
    options: {}
}

// var myChart = new Chart(ctx, graphData);

var socket = new WebSocket('ws://localhost:8000/ws/mac_add/')

socket.onmessage = function(e){
    var djangoData = JSON.parse(e.data);
    console.log(djangoData);
    
    document.querySelector('#app').innerText = djangoData.value;
    var currentTime = new Date(); // Get the current time
    var timeString = currentTime.toLocaleTimeString(); // Format the time as a string

    var newGraphData = graphData.data.datasets[0].data;
    newGraphData.shift();
    newGraphData.push(djangoData.value);

    graphData.data.labels.push(timeString); // Add the current time to the labels array
    graphData.data.datasets[0].data = newGraphData;

    myChart.update();
}   