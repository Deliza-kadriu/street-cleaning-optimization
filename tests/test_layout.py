"""Check the relocated data paths without rerunning the large instance."""

from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LayoutTests(unittest.TestCase):
    def test_default_and_explicit_input_paths(self):
        with TemporaryDirectory() as folder:
            cwd = Path(folder)
            inputs = cwd / "data/input"
            inputs.mkdir(parents=True)
            text = "2 1 4 1 0 1.0\n0 1 2 2 1000 M 10\nS\n"
            for name, args in [("instance_E", []), ("tiny", ["data/input/tiny.txt"])]:
                (inputs / f"{name}.txt").write_text(text)
                result = subprocess.run(
                    [sys.executable, "-B", str(ROOT / "main.py"), *args],
                    cwd=cwd, capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("Solution generated: VALID", result.stdout)
                self.assertIn("Score: 1.0", result.stdout)
                output = cwd / f"data/output/{name}_solution.txt"
                self.assertEqual(output.read_text(), "1\n2\n0 1 0\n0\n")


if __name__ == "__main__":
    unittest.main()
