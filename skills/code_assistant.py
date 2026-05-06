"""Code Assistant - load a VS Code project so Wednesday can see and help with your code."""

import json
import os
from pathlib import Path
import sys

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill

IGNORED_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    "dist", "build", ".next", ".nuxt", "out", "target", ".cache",
    ".pytest_cache", ".mypy_cache", "coverage", "htmlcov", ".tox",
    "vendor", "bower_components", ".idea", ".vs", ".vscode",
}

CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".scss",
    ".json", ".yaml", ".yml", ".md", ".txt", ".env.example",
    ".java", ".c", ".cpp", ".h", ".hpp", ".cs", ".go", ".rs", ".rb",
    ".php", ".vue", ".svelte", ".sh", ".bat", ".ps1", ".sql",
    ".toml", ".cfg", ".ini", ".xml", ".graphql", ".prisma",
    ".gitignore", ".dockerignore", "Dockerfile", ".tf",
}

MAX_FILE_CHARS = 8000    # chars per file in context
MAX_FILES = 60
MAX_CONTEXT_CHARS = 60000  # total context chars sent to Claude


class Skill(BaseSkill):
    """Load a VS Code project so Wednesday can see your code and help."""

    name = "Code Assistant"
    description = "Load a project folder so Wednesday can read your code and assist"

    def __init__(self):
        workspace = Path(__file__).parent.parent / "assistant_workspace"
        workspace.mkdir(exist_ok=True)
        self.project_file = workspace / "loaded_project.json"

    def execute(self, args):
        action = args.get("action", "status")

        if action == "load_project":
            return self.load_project(args.get("path", ""))
        elif action == "list_files":
            return self.list_files()
        elif action == "read_file":
            return self.read_file(args.get("file", ""))
        elif action == "search":
            return self.search_code(args.get("query", ""))
        elif action == "status":
            return self.get_status()
        elif action == "unload":
            return self.unload_project()
        elif action == "get_context":
            return self.get_project_context()
        else:
            return f"Unknown action: {action}"

    def load_project(self, path):
        if not path:
            return "What's the path to your project folder?"
        path = path.strip('"').strip("'").strip()
        proj_path = Path(path)
        if not proj_path.exists():
            return f"Can't find that folder: {path}"
        if not proj_path.is_dir():
            return f"That's a file, not a folder: {path}"

        files = {}
        skipped = []
        total_chars = 0

        for fp in self._iter_code_files(proj_path):
            if len(files) >= MAX_FILES:
                skipped.append("(file limit)")
                break
            try:
                content = fp.read_text(encoding="utf-8", errors="replace")
                rel = str(fp.relative_to(proj_path)).replace("\\", "/")
                if len(content) > MAX_FILE_CHARS:
                    content = content[:MAX_FILE_CHARS] + "\n... (truncated)"
                    skipped.append(f"{rel} (truncated)")
                files[rel] = content
                total_chars += len(content)
                if total_chars > MAX_CONTEXT_CHARS:
                    skipped.append("(context limit reached)")
                    break
            except Exception:
                continue

        data = {
            "path": str(proj_path),
            "name": proj_path.name,
            "files": files,
            "file_count": len(files),
            "total_chars": total_chars,
            "skipped": skipped[:8],
        }
        self.project_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))

        summary = f"Loaded '{proj_path.name}' — {len(files)} files, {total_chars // 1024}KB read into memory."
        if skipped:
            summary += f" Skipped: {', '.join(skipped[:4])}"
        return summary

    def _iter_code_files(self, root):
        for item in sorted(root.rglob("*")):
            if any(p in IGNORED_DIRS for p in item.parts):
                continue
            if item.is_file():
                if item.suffix.lower() in CODE_EXTENSIONS or item.name in CODE_EXTENSIONS:
                    yield item

    def list_files(self):
        data = self._load_data()
        if not data:
            return "No project loaded. Say 'load my project at [path]'"
        files = sorted(data.get("files", {}).keys())
        result = f"Project: {data['name']}  ({len(files)} files)\n"
        result += "\n".join(f"  {f}" for f in files)
        return result

    def read_file(self, filename):
        data = self._load_data()
        if not data:
            return "No project loaded."
        files = data.get("files", {})
        match = None
        for k in files:
            if filename.replace("\\", "/").lower() in k.lower() or k.lower().endswith(filename.lower()):
                match = k
                break
        if not match:
            avail = ", ".join(list(files.keys())[:8])
            return f"File '{filename}' not found. Available: {avail}..."
        return f"=== {match} ===\n{files[match]}"

    def search_code(self, query):
        data = self._load_data()
        if not data:
            return "No project loaded."
        if not query:
            return "What should I search for?"
        results = []
        for filename, content in data.get("files", {}).items():
            for i, line in enumerate(content.splitlines()):
                if query.lower() in line.lower():
                    results.append(f"{filename}:{i + 1}:  {line.strip()}")
                if len(results) >= 25:
                    break
            if len(results) >= 25:
                break
        if not results:
            return f"No matches for '{query}'"
        return f"{len(results)} match(es) for '{query}':\n" + "\n".join(results)

    def get_status(self):
        data = self._load_data()
        if not data:
            return "No project loaded. Say 'load my project at [path]'"
        return f"Project loaded: {data['name']}  ({data['file_count']} files, {data['total_chars'] // 1024}KB)"

    def unload_project(self):
        if self.project_file.exists():
            self.project_file.unlink()
        return "Project unloaded from memory."

    def get_project_context(self):
        """Build the context string to inject into Claude's prompt."""
        data = self._load_data()
        if not data:
            return ""
        lines = [
            f"=== LOADED PROJECT: {data['name']} ({data['path']}) ===",
            f"Files ({data['file_count']}): " + ", ".join(sorted(data.get("files", {}).keys())[:30]),
            "",
        ]
        for filename, content in data.get("files", {}).items():
            lines.append(f"--- {filename} ---")
            lines.append(content)
            lines.append("")
        return "\n".join(lines)

    def _load_data(self):
        if not self.project_file.exists():
            return None
        try:
            return json.loads(self.project_file.read_text(encoding="utf-8"))
        except Exception:
            return None
