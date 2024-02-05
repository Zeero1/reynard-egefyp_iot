import json
from channels.generic.websocket import WebsocketConsumer
import subprocess
import re
import asyncio
import traceback

from .views import *

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        while True:
            try:
                signal_info = await self.get_signal_info()
                connected_devices = await self.get_connected_devices(signal_info)

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

        connected_devices = []

        pattern = re.compile(r'(\S+)\.byteacs\.com \((\d+\.\d+\.\d+\.\d+)\) at (\S+) \[ether\]')

        for signal in signal_info:
            for line in arp_scan_output.stdout.splitlines():
                matches = pattern.findall(line)
                if matches and matches[0][2] == signal[0]:
                    connected_devices.append(matches[0])

        return connected_devices

    async def send_message(self, message_data):
        await self.send(json.dumps(message_data))

    async def send_error(self, error_message):
        await self.send(text_data=json.dumps({'error': error_message}))

    async def disconnect(self):
        pass