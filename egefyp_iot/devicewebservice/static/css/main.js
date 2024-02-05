

//Initialize all variables at the top
registeredDevices = [];
let ipExists = false;
console.log("Starting Webservice");



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

    // Access the data properties (connected_devices and signal_list)
    var connectedDevices = data.connected_devices;
    var signalList = data.signal_list;

    for (let i in connectedDevices) {
        if (!registeredDevices.includes(connectedDevices[i])){
            registeredDevices.push(connectedDevices[i]);
            console.log(registeredDevices)
        }
    }

    buildTable(registeredDevices)
    
    function buildTable(data){
		var table = document.getElementById('myTable')

		for (var i = 0; i < data.length; i++){
			var row = `<tr>
							<td>${data[i][0]}</td>
							<td>${data[i][1]}</td>
							<td>${data[i][2]}</td>
					  </tr>`
			table.innerHTML += row


		}
	}
    //console.log(registeredDevices)

    /*function createTable(){
        
        var table = document.createElement("table"); //makes a table element for the page
        table.style.border = "1px solid black"; //adds a border to the table
        table.style.borderCollapse = "collapse"; //makes the borders between cells collapse
        table.style.margin = "15px";
        for (var i = 0; i < connectedDevices.length; i++) {

            hostname = connectedDevices[i][0];
            ip_address = connectedDevices[i][1];
            mac_address = connectedDevices[i][2];

            var row1 = table.insertRow(0);
            row1.insertCell(0).innerHTML = '<strong>Host:</strong> ' +  hostname; // Host: LAPTOP-1KKIANDS

            var row2 = table.insertRow(1);
            row2.insertCell(0).innerHTML = '<strong>IP Address:</strong> ' + ip_address; // IP Address: 192.168.23.162

            var row3 = table.insertRow(2);
            row3.insertCell(0).innerHTML = '<strong>MAC Address:</strong> ' + mac_address.toUpperCase(); // MAC Address:  5C:CF:7F:3E:9A:84
            registeredDevices.push(connectedDevices[i]);
            return table;
            for (var x = 0; x < signalList.length; x++){
                if (signalList[x][0] == mac_address){
                    // Signal Strength: 
                    document.querySelector('#signalstrength').innerText = signalList[x][1];
                };
        };
    }

    
    
    

    var tableContainer = document.getElementById("table_devices");
    //for (var y = 0; y < connectedDevices.length; y++){ // Number of table created
        
    //}

    


    for (let i in registeredDevices) {
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

    //Shows the signal strength
    document.querySelector('#app').innerText = signalList[0][2];
    
    //Displaying the signal strength onto the Chart
    var newGraphData = myLiveChart.data.datasets[0].data; // make the dataset[0] become newGraphData
    newGraphData.shift(); // remove the first item from array

    dBm = signalList[0][2];
    let quality = 2 * (dBm + 100);

    newGraphData.push(quality); // add the new value to the end
    myLiveChart.update();


    //var djangoData = JSON.parse(e.data);
    //console.log(djangoData);
    

    /*var currentTime = new Date(); // Get the current time
    var timeString = currentTime.toLocaleTimeString(); // Format the time as a string
    newGraphxLabel = myLiveChart.data.labels;
    newGraphxLabel.shift(); // Remove the oldest entry in the x-axis (time)
    newGraphxLabel.push(timeString);*/
    
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
            ticks: {min:0, max:100},
            scaleLabel: {
                display: true,
                labelString: 'Signal Strength (%)'
            }
        }],
    }
}});
