#!/usr/bin/env python3
import re
import subprocess
import os
import signal


class Recorder:
    def __init__(self):
        self.subp = None
        self.index = None
        self.sink = None
        self.record_module_id = None

    def load_record_module(self, sink):
        cmd = [
            "pactl",
            "load-module",
            "module-combine-sink",
            "sink_name=record-audio",
            f"slaves={sink}",
            "sink_properties=device.description=record-audio",
        ]
        output = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
        self.record_module_id = int(output.stdout.strip())

    def unload_record_module(self):
        if self.record_module_id:
            os.system(f"pactl unload-module {self.record_module_id}")
            self.record_module_id = None

    def load_sink_inputs(self):
        output = subprocess.run(
            ["pacmd", "list-sink-inputs"], stdout=subprocess.PIPE, check=True
        )
        output = output.stdout.decode("utf-8")

        regex = re.compile(
            r"""index:\s+(\d+).*?
                sink:\s+(\d+)\s+<.*?>.*?
                client:\s+\d+\s+<(.*?)>.*?""",
            re.DOTALL | re.MULTILINE | re.VERBOSE,
        )

        sinks = {}
        clients = {}

        for match in regex.findall(output):
            index = match[0]
            sinks[index] = match[1]
            clients[index] = match[2]

        return sinks, clients

    def record_start(self, index):
        sinks, _ = self.load_sink_inputs()
        self.sink = sinks[index]
        self.load_record_module(self.sink)
        os.system(f"pactl move-sink-input {index} record-audio")

        self.subp = subprocess.Popen(
            """parec --format=s16le -d record-audio.monitor |  \
            lame -r -q 3 --lowpass 17 --abr 192 - 'temp.mp3' > \
            /dev/null &1>/dev/null""",
            shell=True,
        )

    def record_stop(self):
        # Send CTRL+C to stop the recording
        if self.subp:
            self.subp.send_signal(signal.SIGINT)
            self.subp = None

        # Restore old sink input
        if self.index and self.sink:
            os.system(f"pactl move-sink-input {self.index} {self.sink}")
            self.index = None
            self.sink = None

        # Unload record module
        self.unload_record_module()
