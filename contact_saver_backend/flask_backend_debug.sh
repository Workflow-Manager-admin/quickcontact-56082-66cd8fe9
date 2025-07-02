#!/bin/bash
# Quick diagnostic script for Flask backend status & logs

echo "==== Step 1: PS check for python/flask server ===="
ps aux | grep python | grep -v grep

echo
echo "==== Step 2: Port 3001 listening check ===="
lsof -i :3001

echo
echo "==== Step 3: Test GET /contacts endpoint directly ===="
curl -i http://localhost:3001/contacts/

echo
echo "==== Step 4: Show last 60 backend log lines (adjust if needed) ===="
# Assumes run.py is started from a terminal and logs are visible in terminal.
echo "(If Flask runs in foreground, review terminal log; otherwise adjust for file logs)"

echo
echo "==== Step 5: Confirm API docs are reachable ===="
curl -i http://localhost:3001/docs/
