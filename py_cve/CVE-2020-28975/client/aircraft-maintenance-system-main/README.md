# Aircraft Maintenance System

This project simulates real-time aircraft engine monitoring, diagnostics, and auto-fixing.

## Requirements
- Python 3.8 or later
- FastAPI for backend API
- Scikit-learn for diagnosis module

## Installation
Run the following commands to set up the environment:

```bash
# Clone the repository
git clone https://github.com/AllyElvis/aircraft-maintenance-system.git
cd aircraft-maintenance-system

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn backend.backend:app --reload