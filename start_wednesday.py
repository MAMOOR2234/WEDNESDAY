#!/usr/bin/env python3
"""
Wednesday AI Assistant - Easy Launcher
Starts in CLI mode (works everywhere)
"""

import sys
import os

# Add assistant module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assistant.core import WednesdayCore
from assistant.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Launch Wednesday CLI."""
    print("\n" + "=" * 60)
    print("  WEDNESDAY - AI Assistant")
    print("=" * 60)
    print()

    try:
        print("[*] Initializing Wednesday...\n")
        core = WednesdayCore()

        print("[Wednesday is ONLINE]")
        print("-" * 60)
        print("Commands:")
        print("  - Type anything to chat")
        print("  - 'help' for more commands")
        print("  - 'exit' to quit")
        print("-" * 60 + "\n")

        logger.info("Wednesday session started")

        # Main loop
        while True:
            try:
                # Get input
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Handle exit
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\n[Wednesday] Aight, catch you later! Stay awesome! 💯\n")
                    logger.info("Wednesday session ended - user exit")
                    break

                # Handle help
                if user_input.lower() == 'help':
                    print("""
WEDNESDAY - Commands:
  Type anything to chat with Wednesday

Examples:
  - "What time is it?"
  - "Open Chrome"
  - "Tell me a joke"
  - "Search for Python"
  - "Take a screenshot"
  - "What's the weather?"
  - "Create a reminder"

Special:
  - 'help' - Show this
  - 'exit' - Quit
                    """)
                    continue

                # Process with AI
                print("\n[*] Wednesday thinking...\n")
                logger.info(f"Processing: {user_input[:50]}")

                response, skills = core.process_input(user_input)

                print(f"Wednesday: {response}\n")
                logger.info(f"Response: {response[:100]}")

                # Show skill execution
                if skills:
                    for skill in skills:
                        status = skill.get('status', 'unknown')
                        skill_name = skill.get('skill', 'unknown')
                        if status == 'success':
                            result = skill.get('result', 'Done')
                            print(f"  [✓ Executed] {skill_name}: {result}\n")
                        else:
                            error = skill.get('error', 'Unknown error')
                            print(f"  [✗ Error] {skill_name}: {error}\n")

            except KeyboardInterrupt:
                print("\n\n[Wednesday] Interrupted. Goodbye!\n")
                logger.info("Session interrupted")
                break

            except Exception as e:
                print(f"\n[ERROR] {str(e)[:100]}\n")
                logger.error(f"Error in loop: {e}")
                continue

        return 0

    except Exception as e:
        print(f"\n[FATAL ERROR] {e}\n")
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
