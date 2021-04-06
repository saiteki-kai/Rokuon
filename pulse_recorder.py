#!/usr/bin/env python3
import re
import subprocess
import os
import signal


def load_record_module(sink):
    cmd = [
        "pactl",
        "load-module",
        "module-combine-sink",
        "sink_name=record-audio",
        f"slaves={sink}",
        "sink_properties=device.description=record-audio",
    ]
    output = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
    return int(output.stdout.strip())


def load_sink_inputs():
    output = subprocess.run(
        ["pacmd", "list-sink-inputs"], stdout=subprocess.PIPE, check=True
    )
    output = output.stdout.decode("utf-8")

    regex = re.compile(
        r"index:\s+(\d+).*?sink:\s+(\d+)\s+<.*?>.*?client:\s+\d+\s+<(.*?)>.*?",
        re.DOTALL | re.MULTILINE,
    )

    sinks = {}
    clients = {}

    for match in regex.findall(output):
        index = match[0]
        sinks[index] = match[1]
        clients[index] = match[2]

    return sinks, clients


def record_start(index):
    sinks, clients = load_sink_inputs()
    sink = sinks[index]
    record_module_id = load_record_module(sink)
    os.system(f"pactl move-sink-input {index} record-audio")

    subp = subprocess.Popen(
        """parec --format=s16le -d record-audio.monitor |  \
        lame -r -q 3 --lowpass 17 --abr 192 - 'temp.mp3' > \
        /dev/null &1>/dev/null""",
        shell=True,
    )

    return {
        "pid": os.getpgid(subp.pid),
        "index": index,
        "sink": sink,
        "record_module_id": record_module_id,
    }


def record_stop(data):
    # Restore old sink input
    os.system(f"pactl move-sink-input {data['index']} {data['sink']}")
    os.system(f"pactl unload-module {data['record_module_id']}")

    # Kill parec and lame to stop the recording
    os.killpg(data["pid"], signal.SIGKILL)
