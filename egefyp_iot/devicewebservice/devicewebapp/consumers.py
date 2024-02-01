import json
# from channels.generic.websocket import WebsocketConsumer  
from channels.generic.websocket import AsyncWebsocketConsumer  
from random import randint

# from time import sleep  
from asyncio import sleep
from .views  import * 

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        # for i in range(1000):
            # value = randint(0,100)
            # await self.send(json.dumps(value))
            # print(value)
        #     # await self.send(json.dumps({'value': randint(0, 100)}))
        #     # await self.send(json.dumps(signal_list))
        #     await sleep(1)

    async def disconnect(self):
        pass

    async def receive(self, text_data):
        # Run the subprocess command
        output_signal_cmd = subprocess.run(["iw", "dev", "wlan1", "station", "dump"], capture_output=True, text=True, check=True)
        output_signal = output_signal_cmd.stdout

        # Print the output to the console
        print(output_signal)
        # Send the output to the connected client
        await self.send(text_data=json.dumps({
            'output_signal': output_signal
        }))




# class GraphConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # self.group_name = "notification"
#         # Join to group
#         # await self.channel_layer.group_add(self.group_name, self.channel_name)
#         # Called on connection.
#         # To accept the connection call:
#         await self.accept()

    # async def disconnect(self):
    #     pass
#         # Leave group 
#         # await self.channel_layer.group_discard(self.group_name,
#         #                                        self.channel_name)
        
    # Receive message from websocket 
    # async def receive(self, text_data):
        # try:
        #     # Command to get signal strength
            # output_signal_cmd = subprocess.run(["iw", "dev", "wlan1", "station", "dump"], capture_output=True, text=True, check=True)
            # output_signal = output_signal_cmd.stdout
        #     # Sample Output from "iw dev wlan1 station dump"
        #     # output_signal = """Station 3c:9c:0f:61:3b:1d (on wlan1)
        #     # signal:         -37 dBm
        #     # Station 9c:9c:0d:11:3b:1d (on wlan1)
        #     # signal:         -40 dBm"""

        #     # Split the lines into a list
        #     signal_lines = output_signal.splitlines()

        #     nospc_lines_signal = []

        #     # Remove all whitespaces and add into a list
        #     for x in signal_lines:
        #         y = "".join(x.split())
        #         nospc_lines_signal.append(y)

        #     global signal_list
            
        #     for i in range(len(nospc_lines_signal)):
        #         if "Station" in nospc_lines_signal[i]:
        #             x1 = nospc_lines_signal[i].replace("Station", '')  # Removing the "Station" chars
        #             mac_address = x1[0:17]  # mac address
        #             # print(mac_address)
        #         elif "signal" in nospc_lines_signal[i]:
        #             signal = nospc_lines_signal[i].replace("signal:", '')
        #             signal_cut = int(signal.replace("dBm", ''))
        #             signal_list.append((mac_address , signal , signal_cut))
                    

        #     print(signal_list)
        #     # [('3c:9c:0f:61:3b:1d', '-37dBm'), ('9c:9c:0d:11:3b:1d', '-40dBm')]

        #     # Sample output from "arp -a"
        #     # ? (192.168.1.111) at <incomplete> on wlan1
        #     # ? (192.168.1.1) at 00:31:92:33:1c:30 [ether] on wlan0
        #     # ? (192.168.1.1) at <incomplete> on wlan1
        #     # ? (192.168.1.190) at <incomplete> on wlan0
        #     # ? (192.168.188.1) at <incomplete> on wlan1
        #     # LAPTOP-1KKIANDS.byteacs.com (192.168.23.162) at 3c:9c:0f:61:3b:1d [ether] on wlan1
        #     # one.one.one.one (1.1.1.1) at <incomplete> on wlan1
        #     # ? (10.100.2.1) at <incomplete> on wlan1
        #     # ? (192.168.1.112) at <incomplete> on wlan0
        #     # esp32-8CB604.byteacs.com (192.168.23.141) at 94:b9:7e:8c:b6:04 [ether] on wlan1

        #     arp_scan = subprocess.run(["arp", "-a"], capture_output=True, text=True, check=True)
        #     arp_scan_signal = arp_scan.stdout

        #     arp_lines = arp_scan_signal.splitlines()

        #     connected_devices = []
        #     for signal in signal_list:
        #         for arp_line in arp_lines:
        #             if signal[0] in arp_line:
        #                 pattern = re.compile(r'(\S+)\.byteacs\.com \((\d+\.\d+\.\d+\.\d+)\) at (\S+) \[ether\]')
        #                 matches = pattern.findall(arp_line)
        #                 connected_devices.extend(matches)
        #                 print(connected_devices)

        #     # Send the result back to the WebSocket client
        #     await self.send(text_data=json.dumps({'connected_devices': connected_devices, 'signal_list': signal_list}))
            
        # except Exception as e:
        #     context = {
        #         'error_message': f"Error executing command: {str(e)}",
        #     }
            # Handle the error or send an error message back to the WebSocket client
            # await self.send(text_data=json.dumps({'error': str(e)}))
        
    # async def disconnect(self, close_code):
        # Called when the socket closes


        # for i in range(1000):
        #     # await self.send(json.dumps({'value': randint(0, 100)}))
        #     await self.send(json.dumps(signal_list))
        #     print(str(signal_list))
        #     await sleep(1)