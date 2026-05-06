"""Base Skill class for all Wednesday skills."""


class BaseSkill:
    """Base class for all skills."""

    name = "Base Skill"
    description = "Base skill class"

    def execute(self, args):
        """Execute the skill. Must be overridden."""
        raise NotImplementedError()

    def validate_args(self, args, required):
        """Validate required arguments."""
        for arg in required:
            if arg not in args:
                raise ValueError(f"Missing required argument: {arg}")
