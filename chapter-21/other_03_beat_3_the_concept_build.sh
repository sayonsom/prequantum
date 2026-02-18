docker build -t quantum-service .
docker run -p 8000:8000 -e IBM_QUANTUM_TOKEN=your_token quantum-service

# Test it:
curl -X POST "http://localhost:8000/jobs/ghz?n_qubits=5"
# {"job_id": "a1b2c3d4", "status": "queued"}
