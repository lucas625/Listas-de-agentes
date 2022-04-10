# A*

This is an implementation of the A* algorithm for the "Paris subway" problem.
It tries to find the best path from 2 different nodes based on the distance and the direct distance. As such, we consider the direct distance to be an heuristic.

## Table of Contents

- [A*](#a)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Run](#run)

## Requirements

- Ubuntu
- [Python 3.8.10](https://www.python.org/downloads/)

## Run

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Run the code
# The code will be executed with the JSON related to the activity.
# Should you need to change the target or origin node, just update the src/input/sample_input.json file.
python main.py

# It is also possible to specify a different JSON file, for example:
python main.py --json_input_file_path src/input/already_visited.json
```
