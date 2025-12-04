# Python Network Automation Tool 
## Overview
A custom TCP/IP networK management tool built to automate file distrbition and configuration updates across multiple client nodes.

## Architecture
Controller: Multi-threaded server that handles concurrent connections.
Agent: Lightweight client that receives config files and executes commands.
Security: Verifies file integrity upon receipt.

## Usage
1. Start the controller: 'network_controller.py'
2. Connect agent: 'node_agent.py'
3. Use CLI menu to update

## Tech Stack
- Python 3
- Socket API (TCP/IPv4)
- Threading & File I/O
