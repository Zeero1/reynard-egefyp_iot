

//Initialize all variables at the top
registeredDevices = [];
console.log("Starting Webservice");
let rowIdCounter = 0;
var canvas = document.getElementById('myChart'),
    ctx = canvas.getContext('2d'),
    startingData = {
        labels: [10,9,8,7,6,5,4,3,2,1,0],
        datasets: [
        {   
            label: 'Device #1',
            backgroundColor: [
                'rgba(73, 198, 230, 0.5)',
            ],
            borderWidth: 1,
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]
        },
        {
            label: 'Device #2', 
            backgroundColor: [
                'rgba(255, 99, 71, 0.5)',
            ],
            borderWidth: 1,
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]
        }
    ]
};

const socket = new WebSocket(
'ws://'
+ window.location.host
+ '/ws/devicewebapp/mac_add/'
);

socket.onmessage = function(e){
    var data = JSON.parse(e.data);
    console.log("Received data from WebSocket:", data);

    // Access the data properties (connected_devices and signal_list)
    
    var connectedDevices = data.connected_devices;
    var signalList = data.signal_list;
    var signalstrDevices = data.signalstr_devices;
    
    buildTable(connectedDevices)
    // updateTable(signalstrDevices)
    signalGraph(signalstrDevices)
    function signalGraph(data){
        let i = 0;
        for (let x of data){
            newGraphData = myLiveChart.data.datasets[i].data;
            newGraphData.shift();
            dBm = -x[3];
            newGraphData.push(dBm);
            var currentTime = new Date(); // Get the current time
            var timeString = currentTime.toLocaleTimeString(); // Format the time as a string
            newGraphxLabel = myLiveChart.data.labels;
            newGraphxLabel.shift(); // Remove the oldest entry in the x-axis (time)
            newGraphxLabel.push(timeString);
            myLiveChart.update();
            i++;
        }
    }
    

    function buildTable(data) {
        var table = document.getElementById('myTable');

        for (var i = 0; i < data.length; i++) {
            hostname = data[i][0];
            ip_address = data[i][1];
            mac_address = data[i][2];
            
            // Generate a unique ID for the row
            let rowId = `row_${hostname}`;

            // Check if a row with the same ID already exists
            if (!document.getElementById(rowId)) {
                // If the row doesn't exist, create and append it
                var row = `<tr id="${rowId}">
                                <td id="hostname_${hostname}">${data[i][0]}</td>
                                <td id="ip_${hostname}">${data[i][1]}</td>
                                <td id="mac_${hostname}">${data[i][2]}</td>
                                <td id="signal_${hostname}"></td>
                        </tr>`;
                table.innerHTML += row;
            }
            else{
                console.log("Hello")
                let signalId = 'signal_${hostname}';
                document.getElementById(signalId).innerText = 'hello';
            }
        }
    }

    // function buildTable(data){
	// 	var table = document.getElementById('myTable')

	// 	for (var i = 0; i < data.length; i++){
	// 		hostname = data[i][0];
    //         ip_address = data[i][1];
    //         mac_address = data[i][2];
            
    //         var row = `<tr>
	// 						<td>${data[i][0]}</td>
	// 						<td>${data[i][1]}</td>
	// 						<td>${data[i][2]}</td>
	// 				  </tr>`
    //         table.innerHTML += row;
            
	// 	}
        
	// }

socket.onclose = function(event) {
    console.error("WebSocket closed with code: " + event.code);
};
    


    /*for (let i in registeredDevices) {
        if (!registeredDevices.includes(connectedDevices[i])){
            console.log(connectedDevices[i]);
            registeredDevices.push(connectedDevices[i]);
            console.log(registeredDevices.length);
            console.log(registeredDevices);
        }
        else{
            // Set the flag to true if IP exists
            ipExists = true;       
        }
    }

    if (ipExists) {
        console.log("All IPs are unique, create table");
        if (tableContainer.childNodes.length === 0) { 
//ensures that the table is created only once, even if multiple messages are received with the same connected devices.
            tableContainer.appendChild(createTable());
            ipExists = false;
        }
    }*/
    
    

    


    // Use the data as needed
    //console.log('Connected Devices:', connectedDevices);
    //console.log('Signal List:', signalList);

    
    

    // var currentTime = new Date(); // Get the current time
    // var timeString = currentTime.toLocaleTimeString(); // Format the time as a string
    // newGraphxLabel = myLiveChart.data.labels;
    // newGraphxLabel.shift(); // Remove the oldest entry in the x-axis (time)
    // newGraphxLabel.push(timeString);
    
    // Change the value of the text to randint
    //document.querySelector('#app').innerText = signal_list;
}
var myLiveChart = new Chart(ctx, {type: 'line', data: startingData, options: {
    animation: {duration: 15},
    scales: {
        xAxes: [{
            scaleLabel:{
                display: true, 
                labelString: 'Time(s)'
            }
        }],
        yAxes: [{
            ticks: {min:-0, max:100},
            scaleLabel: {
                display: true,
                labelString: 'Signal Strength (-dBm)'
            }
        }],
    }
}});
