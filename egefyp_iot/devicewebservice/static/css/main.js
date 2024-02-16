

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

    // Access the data properties (connected_devices and sign   booll_list)
    
    var connectedDevices = data.connected_devices;
    var signalList = data.signal_list;
    var signalstrDevices = data.signalstr_devices;
    
    add_registeredDevices(connectedDevices)
    buildTable(connectedDevices)
    updateTable(signalstrDevices)
    signalGraph(signalstrDevices)
    numofdevicesconn(signalstrDevices)

    console.log(registeredDevices)
    

    function add_registeredDevices(data) {
        for (let device of data) {
            let isAlreadyRegistered = false;
            for (let x of registeredDevices) {
                if (x[0] === device[0]) { // If the device matches any element in registeredDevices 
                    isAlreadyRegistered = true;
                    x[1] = "Online"; // Mark the device as online
                }
            }
            if (!isAlreadyRegistered) {
                registeredDevices.push([device[0], "Online"]); // Add the device along with its status
            }
        }
        // Mark devices as offline if they are not connected
        for (let device of registeredDevices) {
            let found = false;
            for (let connectedDevice of data) {
                if (device[0] === connectedDevice[0]) {
                    found = true;
                    break;
                }
            }
            if (!found) {
                device[1] = "Offline"; // Mark the device as offline if not found in connected devices
            }
        }
    }
    


    function numofdevicesconn(data){
        document.querySelector('#no_of_devices').innerText = data.length;
    }

    function signalGraph(data){
        let i = 0;
        for (let x of data){
            graphname = myLiveChart.data.datasets[i].label;
            graphname = x;
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
    
    function updateTable(data){
        for (let device of data) {
            hostname = device[0];
            signalstrength = device[3];
            let rowId = `row_${hostname}`;

            // Check if a row with the same ID already exists
            if (document.getElementById(rowId)) {
                var trElement = document.getElementById(rowId);
                var tdElements = trElement.getElementsByTagName("td");

                // Access the first td element (index 0)
                var firstTdElement = tdElements[0];
            
                // Set inner HTML of the first td element to the online image 
                firstTdElement.innerHTML = '<img src="/static/green-dot-icon.png" alt="Online" width="20px" height="20px">';

                // Access the fourth td element (index 3)
                var fifthTdElement = tdElements[4];
                fifthTdElement.innerText = signalstrength;
            }
            for (let x of registeredDevices){
                if (x[1] == "Offline"){
                    let rowId = `row_${x[0]}`;
                    var trElement = document.getElementById(rowId);
                    var tdElements = trElement.getElementsByTagName("td");
                    // Access the first td element (index 0)
                    var firstTdElement = tdElements[0];
        
                    // Set inner HTML of the first td element to the offline image 
                    firstTdElement.innerHTML = '<img src="/static/red-dot-icon.png" alt="Offline" width="20px" height="20px">';
                }
            }
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
                                <td id="status"><img src="/static/green-dot-icon.png" alt="Online" width="20px" height="20px"></td>
                                <td id="hostname">${hostname}</td>
                                <td id="ip">${ip_address}</td>
                                <td id="mac">${mac_address}</td>
                                <td id="signal">0</td>
                        </tr>`;
                table.innerHTML += row;
            }
        }
    }


socket.onclose = function(event) {
    console.error("WebSocket closed with code: " + event.code);
};
    
    // Use the data as needed
    //console.log('Connected Devices:', connectedDevices);
    //console.log('Signal List:', signalList);

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
                labelString: 'Signal Strength (-dBm)'
            }
        }],
    }
}});
