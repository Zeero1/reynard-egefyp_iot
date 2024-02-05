import json
import re
import subprocess
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_signal_strength = {}

        await self.accept()
        await self.get_device_signal_strength()

    async def disconnect(self, close_code):
        pass

    async def get_device_signal_strength(self):
        try:
            # Command to get signal strength
            output_signal_cmd = subprocess.run(["iw", "dev", "wlan1", "station", "dump"], capture_output=True, text=True, check=True)
            output_signal = output_signal_cmd.stdout

            # Split the lines into a list
            signal_lines = output_signal.splitlines()

            device_signal = {}
            for line in signal_lines:
                if "Station" in line:
                    mac_address = line.split(" ")[1].strip(":")
                    signal_info = line.split("signal:")[1].strip()
                    signal_value = int(signal_info.split("dBm")[0])

                    device_signal[mac_address] = signal_value

            self.device_signal_strength = device_signal

            arp_scan = subprocess.run(["arp", "-a"], capture_output=True, text=True, check=True)
            arp_scan_output = arp_scan.stdout

            connected_devices = []
            for line in arp_scan_output.splitlines():
                if "byteacs.com" in line:
                    match = re.search(r"(\w+)\.byteacs\.com\s+\(([\d\.]+)\)\s+at\s+(\w+)", line)
                    if match:
                        mac_address = match.group(3)
                        if mac_address in self.device_signal_strength:
                            connected_devices.append({
                                "name": match.group(1),
                                "ip": match.group(2),
                                "mac": mac_address,
                                "signal": self.device_signal_strength[mac_address]
                            })

            data_to_send = {'connected_devices': connected_devices}
            await self.send(json.dumps(data_to_send))

        except Exception as e:
            context = {
                'error_message': f"Error executing command: {str(e)}",
            }
            await self.send(json.dumps({'error': str(e)}))

        finally:
            await asyncio.sleep(1)
            await self.get_device_signal_strength()