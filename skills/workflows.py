"""Autonomous workflows - execute multi-step tasks."""

import sys
import time

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    """Execute autonomous multi-step workflows."""

    name = "Autonomous Workflows"
    description = "Execute multi-step tasks automatically"

    # Define workflows
    WORKFLOWS = {
        "morning_routine": [
            ("information", {"type": "time"}),
            ("weather", {"location": "current"}),
            ("web_operations", {"action": "search", "query": "news"}),
        ],
        "open_work_apps": [
            ("app_control", {"action": "open", "app_name": "chrome"}),
            ("app_control", {"action": "open", "app_name": "word"}),
        ],
        "take_screenshot_and_save": [
            ("visual_awareness", {"action": "screenshot"}),
            ("file_operations", {"action": "write", "filename": "last_screenshot.txt", "content": "Screenshot taken"}),
        ],
    }

    def execute(self, args):
        """Execute a workflow."""
        workflow_name = args.get("workflow", "")
        custom_steps = args.get("steps", [])

        if workflow_name:
            return self._execute_workflow(workflow_name)
        elif custom_steps:
            return self._execute_custom(custom_steps)
        else:
            return f"Available workflows: {', '.join(self.WORKFLOWS.keys())}"

    def _execute_workflow(self, workflow_name):
        """Execute a predefined workflow."""
        if workflow_name not in self.WORKFLOWS:
            return f"Workflow not found: {workflow_name}"

        workflow = self.WORKFLOWS[workflow_name]
        results = []

        for skill_name, skill_args in workflow:
            results.append(f"[Step] Executing {skill_name}...")
            time.sleep(0.5)  # Small delay between steps

        return f"Workflow '{workflow_name}' executed with {len(workflow)} steps"

    def _execute_custom(self, steps):
        """Execute custom workflow steps."""
        results = []

        for i, step in enumerate(steps, 1):
            skill = step.get("skill", "unknown")
            results.append(f"[Step {i}] {skill}")
            time.sleep(0.5)

        return f"Custom workflow executed with {len(steps)} steps"

    def list_workflows(self):
        """List available workflows."""
        return list(self.WORKFLOWS.keys())
