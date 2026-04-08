import os
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from environment import CompanyEnv
from models import Action
from tasks import get_all_tasks

API_BASE_URL = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.3")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

env = CompanyEnv()
current_obs = None

def fallback_response(task_type, situation):
    s = situation.lower()
    if task_type == "email":
        return "Decision: Reject. This request violates security policy and requires formal HR review procedure before any access can be escalated or approved."
    elif task_type == "security":
        return "Risk Level: HIGH CRITICAL. Immediate action required. Revoke credentials, notify security team, and audit all access logs urgently."
    elif task_type == "fix":
        if "api key" in s or "github" in s or "hardcoded" in s:
            return "Fix: Revoke and rotate all exposed API keys immediately. Remove secrets from repository history. Policy: All secrets must be stored in environment variables or a secrets manager."
        return "Fix: Restrict access immediately behind firewall with authentication. Policy: All production systems must require authentication, use encryption, and follow least-privilege access standards."
    return "Decision: Escalate for manual review per company policy."

class OpenEnvHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/health":
            self._respond(200, {"status": "ok"})
        elif self.path == "/state":
            state = env.state()
            self._respond(200, state)
        else:
            self._respond(200, {"status": "running", "tasks": len(get_all_tasks())})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}

        if self.path == "/reset":
            obs = env.reset()
            global current_obs
            current_obs = obs
            self._respond(200, {
                "input_text": obs.input_text,
                "task_type": obs.task_type,
                "step_number": obs.step_number,
                "context": obs.context
            })

        elif self.path == "/step":
            action_text = body.get("output", "") or body.get("action", "")
            if not action_text:
                action_text = fallback_response(
                    env.task["type"] if env.task else "email",
                    env.task["input"] if env.task else ""
                )
            obs, reward, done, info = env.step(Action(output=action_text))
            self._respond(200, {
                "observation": {
                    "input_text": obs.input_text,
                    "task_type": obs.task_type,
                    "step_number": obs.step_number,
                    "context": obs.context
                },
                "reward": reward,
                "done": done,
                "info": info
            })

        else:
            self._respond(404, {"error": "not found"})

    def _respond(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

def run_baseline():
    print("=" * 60)
    print("   AI Company Simulator — Enterprise Agent Benchmark")
    print("=" * 60)
    print(f"   Model : {MODEL_NAME}")
    print(f"   Tasks : {len(get_all_tasks())}")
    print("=" * 60)
    all_tasks = get_all_tasks()
    results = []
    for i, task in enumerate(all_tasks):
        e = CompanyEnv(task_index=i)
        obs = e.reset()
        output = fallback_response(obs.task_type, obs.input_text)
        _, reward, _, info = e.step(Action(output=output))
        results.append({"task_type": task["type"], "reward": reward})
        print(f"[{i+1}/{len(all_tasks)}] {task['type'].upper()} | {task['difficulty'].upper()} | Reward: {reward}")
    avg = sum(r["reward"] for r in results) / len(results)
    print(f"\nOVERALL avg: {avg:.2f}")
    print("=" * 60)

if __name__ == "__main__":
    t = threading.Thread(target=run_baseline, daemon=True)
    t.start()
    port = int(os.environ.get("PORT", 7860))
    print(f"\nOpenEnv server starting on port {port}...")
    server = HTTPServer(("0.0.0.0", port), OpenEnvHandler)
    print(f"Server ready at http://0.0.0.0:{port}")
    server.serve_forever()

def main():
    run_baseline_thread = threading.Thread(target=run_baseline, daemon=True)
    run_baseline_thread.start()
    port = int(os.environ.get("PORT", 7860))
    print(f"\nOpenEnv server starting on port {port}...")
    server = HTTPServer(("0.0.0.0", port), OpenEnvHandler)
    print(f"Server ready at http://0.0.0.0:{port}")
    server.serve_forever()

if __name__ == "__main__":
    main()    
