"""
Pre Quantum - Chapter 21: The Quantum Classical Stack
Code Example: Beat 3: The Concept Build > 3.8 QuantumGridOS Architecture: A Case Study
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-21/example_09_quantumgridos_architecture_a_case_study.py
"""

# Simplified from qgo's TCP interface pattern
import asyncio
import json

class QuantumPowerInterface:
    """TCP server for SCADA integration."""

    def __init__(self, port: int = 5555):
        self.port = port
        self.protocol = "IEEE_CIM_v3"
        self._schedule = None
        self._server = None

    def publish_schedule(self, schedule):
        """Store schedule and start serving it over TCP."""
        self._schedule = schedule
        asyncio.get_event_loop().run_until_complete(
            self._start_server()
        )

    async def _start_server(self):
        self._server = await asyncio.start_server(
            self._handle_client, '0.0.0.0', self.port
        )

    async def _handle_client(self, reader, writer):
        """Handle incoming SCADA connection."""
        request = await reader.read(1024)
        command = request.decode().strip()

        if command == "GET_SCHEDULE":
            payload = self._format_cim(self._schedule)
            writer.write(payload.encode())
        elif command == "GET_STATUS":
            writer.write(b"READY")
        elif command.startswith("GET_PERIOD"):
            period = int(command.split()[1])
            payload = self._format_cim(self._schedule[:, period])
            writer.write(payload.encode())

        await writer.drain()
        writer.close()

    def _format_cim(self, data):
        """Convert numpy schedule to IEEE CIM XML."""
        # Production qgo has full CIM serialization
        return json.dumps({"format": self.protocol, "data": data.tolist()})
