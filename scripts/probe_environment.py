"""Read-only feasibility probe; run with uv run --no-project scripts/probe_environment.py."""
import importlib.util
import json
import platform
import shutil
import subprocess
from datetime import datetime, timezone


def command(args):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=20)
        return {"command": args, "returncode": p.returncode,
                "stdout": p.stdout, "stderr": p.stderr}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"command": args, "error": str(e)}


result = {"observed_at": datetime.now(timezone.utc).isoformat(),
          "architecture": platform.machine(), "python": platform.python_version(),
          "tools": {x: shutil.which(x) for x in
                    ["uv", "docker", "codex", "agent", "tectonic", "pdflatex", "latexmk"]},
          "modules_in_probe_interpreter": {x: importlib.util.find_spec(x) is not None
                    for x in ["torch", "mlx", "mlx_lm", "transformers", "peft"]}}
hardware = command(["system_profiler", "SPHardwareDataType", "SPDisplaysDataType"])
# Keep hardware facts, never machine serial numbers or device identifiers.
hardware["stdout"] = "\n".join(line for line in hardware.get("stdout", "").splitlines()
    if any(key in line for key in ["Model Name:", "Chip:", "Memory:",
                                   "Total Number of Cores:", "Metal:"]))
result["hardware"] = hardware
result["checks"] = [command(args) for args in [
    ["sw_vers"], ["df", "-h", "."], ["uv", "--version"],
    ["docker", "model", "version"], ["docker", "model", "list"],
    ["docker", "model", "--help"], ["docker", "context", "ls"],
    ["git", "status", "--short"],
]]
print(json.dumps(result, indent=2))
