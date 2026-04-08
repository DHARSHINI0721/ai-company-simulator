from models import Observation, Action, Reward
from tasks import get_task, get_all_tasks
from graders import evaluate
from typing import Tuple, Dict, Any

class CompanyEnv:
    def __init__(self, task_index: int = None):
        self.task = None
        self.task_index = task_index
        self.step_count = 0
        self.history = []

    def reset(self) -> Observation:
        self.task = get_task(self.task_index)
        self.step_count = 0
        self.history = []
        return Observation(
            input_text=self.task["input"],
            task_type=self.task["type"],
            step_number=0,
            context={"difficulty": self.task["difficulty"], "task_id": self.task["id"]}
        )

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        self.step_count += 1
        reward_obj = evaluate(self.task, action.output)
        self.history.append({
            "step": self.step_count,
            "action": action.output,
            "reward": reward_obj.score
        })

        # Penalize if agent takes too many steps (infinite loop prevention)
        if self.step_count > 5:
            reward_obj.score = max(0.0, reward_obj.score - 0.1 * (self.step_count - 5))
            reward_obj.feedback += " | Penalty: too many steps"

        done = self.step_count >= 1
        obs = Observation(
            input_text=self.task["input"],
            task_type=self.task["type"],
            step_number=self.step_count,
            context={"difficulty": self.task["difficulty"], "task_id": self.task["id"]}
        )
        return obs, reward_obj.score, done, {
            "reward_breakdown": reward_obj.breakdown,
            "feedback": reward_obj.feedback,
            "task_id": self.task["id"]
        }

    def state(self) -> Dict[str, Any]:
        return {
            "task": self.task,
            "step_count": self.step_count,
            "history": self.history
        }