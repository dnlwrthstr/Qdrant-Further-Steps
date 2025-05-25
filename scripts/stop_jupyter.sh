#!/bin/bash

# Script to stop the Jupyter notebook server

# Find Jupyter notebook processes
JUPYTER_PIDS=$(pgrep -f "jupyter-notebook")

if [ -z "$JUPYTER_PIDS" ]; then
    echo "No Jupyter notebook server is running."
else
    echo "Stopping Jupyter notebook server..."
    for PID in $JUPYTER_PIDS; do
        kill $PID
        echo "Sent termination signal to process $PID"
    done
    echo "Jupyter notebook server has been stopped."
fi

echo "To start the Jupyter server again, run: ./scripts/start_jupyter.sh"