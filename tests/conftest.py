import sys
from pathlib import Path

# Ensure project root and tools are importable during tests.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
