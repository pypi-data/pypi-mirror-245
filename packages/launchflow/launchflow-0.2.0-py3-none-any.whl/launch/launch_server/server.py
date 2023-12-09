import asyncio
import dataclasses
import json
import random
import signal
import socket
import subprocess
import time
from typing import Any, Dict, List

import requests
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

exclude_keys = {
    "status",
    "timestamp_millis",
    "processor_id",
    "processor_type",
    "group_id",
    "group_type",
    "processor_snapshots",
}


def flatten_snapshots(processor_snapshots: Dict[str, Any]) -> List[Dict[str, Any]]:
    flattened_snapshots = []
    for snapshot_id, snapshot in processor_snapshots.items():
        for metric_name, metric_value in snapshot.items():
            if metric_name not in exclude_keys:
                flattened_snapshots.append(
                    {
                        "processorId": snapshot_id,
                        "metricName": metric_name,
                        "metricValue": metric_value,
                    }
                )
    return flattened_snapshots


def parse_metrics(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Flatten processor_snapshots
    return [
        metric
        for group in data["processor_groups"]
        for metric in flatten_snapshots(group["processor_snapshots"])
    ]


def generate_run_id() -> str:
    chars: str = "abcdefghijklmnopqrstuvwxyz0123456789"
    result: str = "run_"
    for _ in range(4):
        result += random.choice(chars)
    return result


def get_open_server_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Bind the socket to any address with port 0.
        # The operating system will assign a random available port.
        sock.bind(("", 0))
        # Retrieve the assigned port number.
        _, port = sock.getsockname()
        return port


@dataclasses.dataclass
class Launch:
    id: str
    runtime: str
    url: str
    createdAt: str
    metrics: dict
    status: str
    statusMessage: str
    startTime: str
    endTime: str
    flowstate: dict


@dataclasses.dataclass
class Run(Launch):
    appPath: str
    appName: str
    runtimeServerPort: int
    exitCode: int


@dataclasses.dataclass
class Deployment(Launch):
    projectId: str
    environment: str
    environmentVariables: dict
    usage: dict


@dataclasses.dataclass
class BuildFlowApp:
    name: str
    app_dir: str


class LaunchManager:
    def __init__(self, buildflow_app: BuildFlowApp):
        # Launch configuration
        self.buildflow_app = buildflow_app
        self.runtime_server_port = get_open_server_port()
        self.relay_server_port = get_open_server_port()
        self.run_id = generate_run_id()
        self.url = "http://localhost:8000"

        # FastAPI server setup
        self.fastapi_app = FastAPI()
        self.configure_routes()
        self.fastapi_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        # NOTE: the mount() call needs to happen after we define the routes or else the
        # routes will not work.
        self.fastapi_app.mount(
            "/",
            StaticFiles(packages=[("launch", "launch_server/static")], html=True),
            name="static",
        )

        # Launch state
        self.buildflow_run_subprocess = None
        self.uvicorn_server = None
        self.draining = False
        self.stopping = False
        self.disconnected = False

        # Signal handling
        signal.signal(signal.SIGINT, self.signal_handler)
        # signal.signal(signal.SIGTERM, self.signal_handler)

    def configure_routes(self):
        @self.fastapi_app.post("/api/drain")
        async def drain():
            self.draining = True
            result = requests.post(
                f"http://localhost:{self.runtime_server_port}/runtime/drain"
            )
            print("drain result", result.json())
            return result.json()

        @self.fastapi_app.post("/api/stop")
        async def stop():
            self.stopping = True
            result = requests.post(
                f"http://localhost:{self.runtime_server_port}/runtime/stop"
            )
            print("stop result", result.json())
            return result.json()

        @self.fastapi_app.get("/api/events")
        async def get_events():
            async def event_generator():
                flowstate = None
                runtime_state = {
                    "status": "PENDING",
                    "timestamp_millis": int(time.time() * 1000),
                    "processor_groups": [],
                    "appPath": self.buildflow_app.app_dir,
                    "appName": self.buildflow_app.name,
                    "runtimeServerPort": self.runtime_server_port,
                    "id": self.run_id,
                    "url": self.url,
                    "createdAt": int(time.time() * 1000),
                }
                yield f"event: runtime\ndata: {json.dumps(runtime_state)}\n\n"

                while True:
                    if self.uvicorn_server.should_exit:
                        print("relay server was shut down, closing event stream")
                        break
                    try:
                        # TODO: This should use httpx so this request can run async
                        runtime_state_json = requests.get(
                            f"http://localhost:{self.runtime_server_port}/runtime/snapshot"  # noqa
                        ).json()
                        runtime_state.update(runtime_state_json)
                        if runtime_state.get("startTime", None) is None:
                            runtime_state["startTime"] = int(time.time() * 1000)

                        # update the metrics
                        # for metric in parse_metrics(runtime_state):
                        #     processor_id = metric["processorId"]
                        #     metric_name = metric["metricName"]
                        #     metric_value = metric["metricValue"]
                        #     key = f"{processor_id}::{metric_name}"
                        #     if key not in self.metrics:
                        #         self.metrics[key] = deque(maxlen=10)
                        #     self.metrics[key].append(
                        #         {
                        #             "timestamp": int(time.time() * 1000),
                        #             "value": metric_value,
                        #         }
                        #     )

                        # update the runtime state with the metrics
                        # runtime_state["running_metrics"] = {
                        #     key: list(metric_values)
                        #     for key, metric_values in self.metrics.items()
                        # }

                        yield f"event: runtime\ndata: {json.dumps(runtime_state)}\n\n"

                    except Exception as e:
                        if self.stopping or runtime_state["status"] == "STOPPING":
                            print("IN STOPPING BLOCK")
                            runtime_state["status"] = "STOPPED"
                            runtime_state["endTime"] = int(time.time() * 1000)
                            yield f"event: runtime\ndata: {json.dumps(runtime_state)}\n\n"  # noqa
                            self.shutdown()
                            return
                        elif self.draining or runtime_state["status"] == "DRAINING":
                            print("IN DRAINING BLOCK")
                            runtime_state["status"] = "DRAINED"
                            runtime_state["endTime"] = int(time.time() * 1000)
                            yield f"event: runtime\ndata: {json.dumps(runtime_state)}\n\n"  # noqa
                            self.shutdown()
                            return
                        elif self.disconnected:
                            print("IN DISCONNECTED BLOCK")
                            runtime_state["status"] = "DISCONNECTED"
                            runtime_state["endTime"] = int(time.time() * 1000)
                            yield f"event: runtime\ndata: {json.dumps(runtime_state)}\n\n"  # noqa
                            self.shutdown()
                            return
                        else:
                            print("runtime error: ", e)
                            pass

                    # only pull flowstate if it hasn't been pulled yet for this request
                    # / connection
                    if flowstate is None:
                        try:
                            flowstate = requests.get(
                                f"http://localhost:{self.runtime_server_port}/flowstate"
                            ).json()
                            yield f"event: flowstate\ndata: {json.dumps(flowstate)}\n\n"
                            # print("flowstate", flowstate)
                        except Exception:
                            print("flowstate error")
                            pass

                    await asyncio.sleep(5)

            return StreamingResponse(event_generator(), media_type="text/event-stream")

    def run(self):
        self.buildflow_run_subprocess = subprocess.Popen(
            [
                "buildflow",
                "run",
                "--start-runtime-server",
                f"--runtime-server-port={self.runtime_server_port}",
            ],
            cwd=self.buildflow_app.app_dir,
        )

        config = uvicorn.Config(self.fastapi_app, port=self.relay_server_port)
        self.uvicorn_server = uvicorn.Server(config)
        loop = asyncio.get_event_loop()
        relay_server_task = loop.create_task(self.uvicorn_server.serve())

        # Start the monitoring coroutine as a task
        monitor_task = loop.create_task(self.monitor_buildflow_run_subprocess())

        try:
            loop.run_until_complete(monitor_task)
        finally:
            print("made it to cleanup block")
            # Ensure proper cleanup
            relay_server_task.cancel()
            loop.stop()
            print("relay server task done")

    async def monitor_buildflow_run_subprocess(self):
        # Checks if the buildlfow run subprocess has terminated every 2 seconds
        while True:
            if self.buildflow_run_subprocess.poll() is not None:
                print("BuildFlow subprocess has terminated unexpectedly.")
                self.disconnected = True
                return
            await asyncio.sleep(2)

    def signal_handler(self, signum, frame):
        print("Signal received, shutting down...")
        self.shutdown()

    def shutdown(self):
        print("in shutdown")
        # Shut down the buildflow subprocess
        if self.buildflow_run_subprocess is not None:
            print("terminating buildflow subprocess")
            self.buildflow_run_subprocess.terminate()
            print("buildflow subprocess terminated")
        # Shut down the uvicorn server
        if self.uvicorn_server is not None:
            print("shutting down uvicorn server")
            loop = asyncio.get_event_loop()
            loop.create_task(self.uvicorn_server.shutdown())
            print("uvicorn server shut down")
