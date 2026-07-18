# NII control panel

Use the private Gradio Space `imo2026-challenge/control-panel-nguyen` to run
commands on NII nodes when direct SSH is unavailable. The relay acknowledges a
command immediately; read its output from command history afterward.

## Node ownership

UI node numbers and relay client ranks are both zero-based:

| Member | Human nodes | Relay clients |
|---|---:|---|
| `vu` | 0 | `node0` |
| `bogo` | 1 | `node1` |
| `yi` | 2 | `node2` |
| `nguyen` | 3 | `node3` |
| `all` | 0-3 | `node0` through `node3` |

Choose `all` when cluster administration requires access to every node. It
lists all registered containers and makes **Run on member node** an all-online
broadcast. Continue to run shared-file mutations on one selected node only.

The nodes share the main filesystem. Run package installs, downloads,
repository updates, and other shared-file mutations on exactly one node. Run a
member-routed command only for node-local work, such as checking GPUs or
starting one rank-specific server.

## Use the web UI

1. Open the private `control-panel-nguyen` Space and hard-refresh after a Space
   rebuild.
2. Select your team member. The container dropdown is automatically limited to
   that member's assigned node.
3. Give the command a session name. Reusing a session preserves its shell
   working directory and exported variables.
4. Choose the correct scope:
   - **Run on selected node**: installs, downloads, shared-file changes, or a
     command intended for one node.
   - **Run on member node**: the member's assigned node, or every online node
     when `all` is selected.
   - **Broadcast to all online**: cluster-wide diagnostics only.
5. Read output in **Selected node history** or **Member history**.

Do not leave a long command in the foreground. A foreground command occupies
that relay session and prevents later commands in the same session from
running. Start long jobs with `nohup`, save their PID and log, and let the relay
command return.

## Connect from Python

Authenticate locally once with `hf auth login`. Do not put a token in source
code or a relay command.

```python
from gradio_client import Client
from huggingface_hub import get_token

SPACE = "imo2026-challenge/control-panel-nguyen"
client = Client(SPACE, token=get_token())
```

Inspect the client assigned to a member:

```python
assignment = client.predict(member="nguyen", api_name="/ui_team_clients")
print(assignment)

online = [item["client_id"] for item in assignment["clients"] if item["online"]]
if not online:
    raise RuntimeError("No Nguyen node is online")
one_node = online[0]
```

Use the returned full client ID when possible. A unique short label such as
`node3` also works, but the full ID makes logs and handoffs unambiguous.

## Run on one node

This is the correct path for installing packages or changing shared files:

```python
import time

session = f"nguyen-install-{time.time_ns()}"
reply = client.predict(
    client_label=one_node,
    session=session,
    command="python -m pip install --user example-package",
    timeout=120,
    api_name="/ui_send",
)
print(reply)
```

`/ui_send` returns an acknowledgement, not the final command output.

## Run on the member node

Use member routing to execute a command on the selected member's assigned node:

```python
import time

session = f"nguyen-gpu-check-{time.time_ns()}"
reply = client.predict(
    member="nguyen",
    session=session,
    command="hostname && nvidia-smi",
    timeout=120,
    api_name="/ui_team_broadcast",
)
print(reply)
```

The acknowledgement lists the exact clients that received the command.

## Read command history

Read one node's history with `/ui_history`:

```python
history = client.predict(client_label=one_node, api_name="/ui_history")
marker = f"[{session}]"
start = history.rfind(marker)
print(history[start:] if start >= 0 else history)
```

Read the member node's combined view with `/ui_team_history`:

```python
history = client.predict(member="nguyen", api_name="/ui_team_history")
marker = f"[{session}]"
start = history.rfind(marker)
print(history[start:] if start >= 0 else history)
```

For automation, poll until the session appears with an exit status:

```python
import time

deadline = time.monotonic() + 300
while time.monotonic() < deadline:
    history = client.predict(client_label=one_node, api_name="/ui_history")
    start = history.rfind(f"[{session}]")
    current = history[start:] if start >= 0 else ""
    if "-> exit " in current or "→ exit " in current:
        print(current)
        break
    time.sleep(3)
else:
    raise TimeoutError(f"No completed history entry for {session}")
```

History is a bounded relay view, not permanent job storage. Long jobs must
write logs and status files to the shared filesystem.

## Start and monitor a long job

Submit the launcher on one selected node and return immediately:

```python
run_id = "my-inference-run"
log = f"/tmp/{run_id}.log"
pidfile = f"/tmp/{run_id}.pid"
status = f"/tmp/{run_id}.status"

command = f'''set -eu
rm -f "{status}"
nohup bash -lc 'set +e; your-command; rc=$?; printf "%s\\n" "$rc" > "{status}"' \
  > "{log}" 2>&1 < /dev/null &
echo $! > "{pidfile}"
echo "started pid=$(cat '{pidfile}') log={log} status={status}"'''

print(
    client.predict(
        client_label=one_node,
        session=f"launch-{run_id}",
        command=command,
        timeout=120,
        api_name="/ui_send",
    )
)
```

Poll it through a separate short relay session:

```python
poll = f'''PID=$(cat "{pidfile}" 2>/dev/null || true)
if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
  echo RUNNING
else
  echo STOPPED
fi
printf "status="
cat "{status}" 2>/dev/null || echo pending
tail -n 80 "{log}" 2>/dev/null || true'''

print(
    client.predict(
        client_label=one_node,
        session=f"poll-{run_id}",
        command=poll,
        timeout=120,
        api_name="/ui_send",
    )
)
```

Then call `/ui_history` for the `poll-<run_id>` session to read the result.

## Safety rules

- Never include Hugging Face, GitHub, W&B, or other secrets in relay commands;
  users with Space access can read command history.
- Do not broadcast package installs or shared-file mutations.
- Do not use broad `pkill` patterns.
- Preserve `/app/entrypoint.sh`, `endpoint.sh`, the daemon connected to
  `imo2026-challenge/control-panel`, and unrelated training or inference jobs.
- Stop a job through its saved PID file and verify the command line before
  sending a signal.

For the vLLM-specific NII bootstrap and smoke procedure, continue with
[NII_VLLM_SETUP.md](NII_VLLM_SETUP.md).
