# NII control panel

Use the private Gradio Space `imo2026-challenge/control-panel-nguyen` to run
commands on NII nodes when direct SSH is unavailable. The relay acknowledges a
command immediately; read its output from command history afterward.

## Node ownership

Human-facing node numbers are one-based, while relay client ranks are
zero-based:

| Member | Human nodes | Relay clients |
|---|---:|---|
| `vu` | 1-2 | `node0`, `node1` |
| `bogo` | 3-4 | `node2`, `node3` |
| `yi` | 5-6 | `node4`, `node5` |
| `nguyen` | 7-8 | `node6`, `node7` |

The nodes share the main filesystem. Run package installs, downloads,
repository updates, and other shared-file mutations on exactly one node. Run a
command on both member nodes only when each node must perform local work, such
as checking GPUs or starting one rank-specific server per node.

## Use the web UI

1. Open the private `control-panel-nguyen` Space and hard-refresh after a Space
   rebuild.
2. Select your team member and one of its two containers.
3. Give the command a session name. Reusing a session preserves its shell
   working directory and exported variables.
4. Choose the correct scope:
   - **Run on selected node**: installs, downloads, shared-file changes, or a
     command intended for one node.
   - **Run on member nodes**: node-local work on the member's assigned pair.
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

Inspect the two clients assigned to a member:

```python
pair = client.predict(member="nguyen", api_name="/ui_team_clients")
print(pair)

online = [item["client_id"] for item in pair["clients"] if item["online"]]
if not online:
    raise RuntimeError("No Nguyen node is online")
one_node = online[0]
```

Use the returned full client ID when possible. A unique short label such as
`node6` also works, but the full ID makes logs and handoffs unambiguous.

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

## Run on both member nodes

Use member routing only when both nodes must execute the command independently:

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

Read combined history for both member nodes with `/ui_team_history`:

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
