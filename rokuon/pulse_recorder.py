import re
import subprocess
import os

from rokuon.constants import tmp_directory


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

    def record_start(self, index, ext):
        sinks, _ = self.load_sink_inputs()

        if len(sinks) == 0:
            raise RuntimeError("no sink inputs found")
        if index < 0:
            raise RuntimeError("invalid index")

        self.sink = sinks[index]
        self.load_record_module(self.sink)

        if not self.record_module_id:
            raise RuntimeError("module not available")

        os.system(f"pactl move-sink-input {index} record-audio")

        tmp_file = os.path.join(tmp_directory, f"temp.{ext}")

        self.subp = subprocess.Popen(
            f"ffmpeg -f pulse -i record-audio.monitor -ac 2 {tmp_file}",
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def record_stop(self):
        # Send "q" to stop the recording
        if self.subp:
            self.subp.communicate(b"q")
            self.subp.terminate()
            self.subp = None

        # Restore old sink input
        if self.index and self.sink:
            os.system(f"pactl move-sink-input {self.index} {self.sink}")
            self.index = None
            self.sink = None

        # Unload record module
        self.unload_record_module()
