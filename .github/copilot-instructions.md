# Copilot Instructions for *algorithm-learn* repository

This repository is a small personal "algorithm learning" workspace. It contains a handful of self‑contained Python scripts that implement classic data structures and problems along with simple test harnesses. The goal of `copilot-instructions.md` is to give an AI agent the minimal context needed to be productive here.

---

## 📁 Structure overview

- `b_plus_tree.py` – full implementation of a B+‑tree in pure Python.  All logic lives in this file; the tree supports insert/search/delete/range and a stub for underflow handling.  Classes: `BPlusTree`, `BPlusTreeNode` and subclasses.
- `knapsack_01.py` – several variants of the 0‑1 knapsack problem (DP, optimized DP, brute force, branch‑and‑bound) plus a `test_knapsack()` and a simple CLI.  The file is designed to be run directly (`python knapsack_01.py`), with `--test` flag invoking the tests.
- `test_b_plus_tree.py` – a standalone test module that exercises almost every tree operation and prints results.  Tests use plain `assert` statements and exit with status `1` on failure.

There are no packages or dependencies; everything runs on stock Python 3.10+.

---

## 🛠 Developer workflows

- **Running tests**
  ```bash
  python3 test_b_plus_tree.py            # executes the B+ tree suite
  python3 knapsack_01.py --test          # runs knapsack algorithms
  ```
  Tests are not managed by `pytest` or `unittest`; they are invoked directly from the script.

- **Interactive demo**
  Launch `python3 knapsack_01.py` and follow the console prompts to exercise different algorithms with hard‑coded sample data.

- **Editing/adding algorithms**
  - New algorithms live alongside existing ones in a new `.py` file or appended to `knapsack_01.py`.
  - Provide a `main()` or `test_...()` function matching the style above.  Copy the structure of `test_b_plus_tree.py` if you need a more elaborate harness.

- **Conventions**
  - Use snake_case for functions and variables.
  - Docstrings are present for every algorithm and explain time/space complexity.
  - Tests and examples include helpful Chinese comments, but code logic is entirely English; stick to this mix if you add new comments or tests.
  - `if __name__ == "__main__"` is used for quick manual experimentation; tests are safe to run on import.

---

## ⚠️ Project‑specific notes

- **Incomplete features**: `BPlusTree._handle_underflow` is a TODO.  Current tests do not exercise merge/redistribution, so any new code should either implement or guard around this.
- **No external dependencies** beyond the standard library.  Avoid introducing third‑party packages unless absolutely necessary; the learning goal is implementing algorithms by hand.
- **Data flow** is simple: functions accept lists/primitive values and return tuples (e.g. `(max_value, selected_items)`) or booleans for tree operations.

- **Edge case handling**: most functions validate inputs (matching list lengths, positive weights/values). Follow this pattern when adding new utilities.

---

## ✅ Guidance for Copilot/AI agents

- Focus on algorithmic correctness and clarity rather than engineering infrastructure.
- When generating tests, mimic the style in `test_b_plus_tree.py`: print sections, use `assert`, handle expected failures gracefully, and include a `main()` driving function.
- Keep output localized to the script; nothing writes to files or external services.
- There is no build system; code is run directly with the Python interpreter.

---

Feel free to ask for clarification if any aspect of this small codebase is unclear.  The next step for an agent after reading this file is usually to open one of the `.py` files and start editing or extending algorithms.