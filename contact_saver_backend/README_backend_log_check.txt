Backend Flask Log Check Instructions:

DEBUGGING STEPS – Flask Server Status & Connectivity
---------------------------------------------------
To quickly check key troubleshooting details:

A. Confirm the Flask server is running:
   - Use `ps aux | grep python` or `lsof -i :3001` (default port from run.py).
   - Look for a process similar to: `python run.py` or similar.

B. List all running processes related to python/flask:
   - `ps aux | grep python`
   - Result should show the Flask server (`run.py`). Note the PID.

C. Check port usage and listening sockets:
   - `lsof -i :3001`  — Confirms that Flask is listening on port 3001.
   - Should show a line like: `Python ... TCP *:3001 (LISTEN)`

D. Send a direct test request from the backend terminal:
   - `curl -i http://localhost:3001/contacts/`
   - You should see either a list of contacts (`200 OK`) or an empty list, not a 404/500.

E. To check endpoint registration and Swagger docs:
   - Visit: http://localhost:3001/docs or (external) the /openapi.json URL.
   - The /contacts endpoints should be present and described.

F. Check for incoming frontend requests and CORS/errors:
   - Tail logs where Flask is started: look for `[DEBUG] [REQ] ...` and `[DEBUG] [RESP] ...`.
   - If no logs, frontend isn't reaching backend or port is wrong.

-----------------

1. When the frontend attempts to GET or POST /contacts, observe the console/log output produced by the Flask server (python run.py).
2. Look for "[DEBUG] [REQ] ..." and "[DEBUG] [RESP] ..." lines in the logs (these appear due to the log_every_request and debug_after_request functions in app/__init__.py).
3. On a GET or POST to /contacts, you should see:
   - For GET: '[DEBUG] [REQ] GET /contacts/' and later '[DEBUG] [RESP] GET /contacts/' and debug prints from contacts.py.
   - For POST: '[DEBUG] [REQ] POST /contacts/' and later '[DEBUG] [RESP] POST /contacts/' plus details of the posted data.
4. If there is a CORS issue, look for errors such as 'CORS rejection', missing 'Access-Control-Allow-Origin', or preflight (OPTIONS) errors.
5. If requests do not show in the logs at all, double-check network settings, container interconnectivity, and that the frontend is targeting the correct backend URL (should be http://localhost:3001/contacts or the correct host:port).

Use 'tail -n 60' or 'less' on the running terminal's stdout from the Flask server. The relevant log statements should make debugging straightforward.
