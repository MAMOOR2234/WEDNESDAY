"""
Skills Registry - Dynamic skill loading system for Wednesday
Based on JARVIS modular architecture
"""

import importlib
import inspect
from pathlib import Path
from .logger import setup_logger

logger = setup_logger(__name__)


class SkillsRegistry:
    """Registry for dynamically loading and executing skills."""

    def __init__(self):
        """Initialize skills registry."""
        self.skills = {}
        self._load_skills()

    def _load_skills(self):
        """Dynamically load all skills from skills directory."""
        skills_dir = Path(__file__).parent.parent / "skills"
        skills_dir.mkdir(exist_ok=True)

        # Create __init__.py if it doesn't exist
        init_file = skills_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text("")

        # Load skill modules
        for skill_file in skills_dir.glob("*.py"):
            if skill_file.name.startswith("_"):
                continue

            skill_name = skill_file.stem
            try:
                module = importlib.import_module(f"skills.{skill_name}")

                # Look for Skill class
                if hasattr(module, "Skill"):
                    skill_class = module.Skill
                    self.skills[skill_name] = skill_class()
                    logger.info(f"Loaded skill: {skill_name}")

            except Exception as e:
                logger.warning(f"Failed to load skill {skill_name}: {e}")

    def execute(self, skill_name, args):
        """Execute a skill by name with arguments."""
        if skill_name not in self.skills:
            raise ValueError(f"Skill not found: {skill_name}")

        skill = self.skills[skill_name]
        return skill.execute(args)

    def list_skills(self):
        """List all available skills."""
        return {
            name: {
                "name": skill.name if hasattr(skill, "name") else name,
                "description": skill.description if hasattr(skill, "description") else "No description",
            }
            for name, skill in self.skills.items()
        }

    def get_skill(self, skill_name):
        """Get a skill instance."""
        return self.skills.get(skill_name)
