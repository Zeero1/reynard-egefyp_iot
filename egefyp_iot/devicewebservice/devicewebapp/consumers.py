import json
import subprocess
import re
import asyncio
import traceback
from channels.generic.websocket import AsyncWebsocketConsumer  
from .views import *

from devicewebapp.models import Device

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        while True:
            
            try:
                signal_info = await self.get_signal_info()
                connected_devices = await self.get_connected_devices(signal_info)
                print(connected_devices)
                print(signal_info)
                message_data = {
                    'signal_list': signal_info,
                    'connected_devices': connected_devices
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
        signal_list = []

        for line in signal_lines:
            line_strip = line.strip()
            if "Station" in line_strip:
                mac_address = line_strip.split("Station ")[-1].split(" (")[0]
            elif "signal" in line_strip:
                signal_strength = line_strip.split("signal:")[-1].strip().split(" ")[0]
                signal_list.append((mac_address, signal_strength))

        return signal_list

    async def get_connected_devices(self, signal_info):
        arp_scan_output = subprocess.run(
            ["arp", "-a"],
            capture_output=True,
            text=True,
            check=True
        )
        # LAPTOP-1KKIANDS.byteacs.com (192.168.23.162) at 3c:9c:0f:61:3b:1d [ether] on wlan1

        connected_devices = []

        pattern = re.compile(r'(\S+)\.byteacs\.com \((\d+\.\d+\.\d+\.\d+)\) at (\S+) \[ether\]')

        for signal in signal_info:
            for line in arp_scan_output.stdout.splitlines():
                matches = pattern.findall(line)

                # Compare mac address
                if matches and matches[0][2] == signal[0]:
                    connected_devices.append(matches[0])
                    

                    # Create and save Device object
                    hostnm = matches[0][0]
                    ipaddr = matches[0][1]
                    macaddr = matches[0][2]
                    signalstr = signal[1]

                    # subprocess.run(Device.objects.create(hostnm=hostnm, ipaddr=ipaddr, macaddr=macaddr, signalstr=signalstr))
                    

                    # print(hostnm, ipaddr, macaddr, signalstr)

                    # d = Device.objects.create(hostnm=hostnm, ipaddr=ipaddr, macaddr=macaddr, signalstr=signalstr)
                    # d.save()
                    
                    # print(list(Device.objects.all().values()) + ["hello"])

        return connected_devices

    async def send_message(self, message_data):
        await self.send(json.dumps(message_data))

    async def send_error(self, error_message):
        await self.send(text_data=json.dumps({'error': error_message}))

    async def disconnect(self):
        pass