import json
import subprocess
import re
import asyncio
import traceback
from channels.generic.websocket import AsyncWebsocketConsumer  
from .views import *

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        while True:
            try:
                signal_info = await self.get_signal_info()
                connected_devices = await self.get_connected_devices()
                # try:
                #     for hostname, ip, mac in connected_devices:
                #         #adding device to Django ORD
                #         await sync_to_async(Device.objects.create(hostnm = hostname, ipaddr = ip, macaddr = mac))
                        
                # except Exception as error:
                #     print("An error occurred:", type(error).__name__, "–", error)

                
                
                signalstr_devices = []

                for x in connected_devices: # looping over all elements in a list and check if the mac is the same
                    mac = x[2]
                    for y in signal_info:
                        if mac == y[0]:
                            # This will add all the elements in the sublist and the last element of signal_info
                            signalstr_devices.append(x + y[1:]) 
                print(signalstr_devices)
                print(connected_devices)
                print(signal_info)

                message_data = {
                    'connected_devices': connected_devices,
                    'signalstr_devices': signalstr_devices
                }

                await self.send_message(message_data)

            except Exception as e:
                error_message = f"Error executing command: {str(e)}\n{traceback.format_exc()}"
                await self.send_error(error_message)

            await asyncio.sleep(1)

    async def get_signal_info(self):
        output_signal_cmd = subprocess.run(
            ["iw", "dev", "wlan1", "station", "dump"],
            capture_output=True,
            text=True,
            check=True
        )
        # Station 3c:9c:0f:61:3b:1d (on wlan1)
        # signal:         -24 dBm


        signal_lines = output_signal_cmd.stdout.splitlines()
        signal_info = []
        
        for line in signal_lines:
            line_strip = line.strip()
            if "Station" in line_strip:
                mac_address = line_strip.split("Station ")[-1].split(" (")[0]
            elif "signal" in line_strip:
                signal_strength = line_strip.split("signal:")[-1].strip().split(" ")[0]
                signal_info.append((mac_address, signal_strength))

        return signal_info

    async def get_connected_devices(self):
        arp_scan_output = subprocess.run(
            ["arp", "-a"],
            capture_output=True,
            text=True,
            check=True
        )
        # LAPTOP-1KKIANDS.byteacs.com (192.168.23.162) at 3c:9c:0f:61:3b:1d [ether] on wlan1

        connected_devices = []
        pattern = re.compile(r'(\S+)\.byteacs\.com \((\d+\.\d+\.\d+\.\d+)\) at (\S+) \[ether\]')


        for line in arp_scan_output.stdout.splitlines():
            matches = pattern.findall(line)
            if matches:
                connected_devices.append(matches[0])                    
        return connected_devices


        
        # [('LAPTOP-1KKIANDS', '192.168.23.162', '3c:9c:0f:61:3b:1d')]
        # Desired output [('LAPTOP-1KKIANDS', '192.168.23.162', '3c:9c:0f:61:3b:1d', signalstr)]
        
    async def send_message(self, message_data):
        await self.send(json.dumps(message_data))

    async def send_error(self, error_message):
        await self.send(text_data=json.dumps({'error': error_message}))

    async def disconnect(self):
        pass