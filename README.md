# Jelka FMF

View the website at [jelka.4a.si](https://jelka.4a.si/).

## Directory Structure

* `patterns` - Contains patterns
* `library` - API that patterns should use
* `simulation` - Code for simulating tree in Pygame
* `hardware` - Code for running patterns on the real tree and server
* `development` - Development stuff

## Contributing Patterns

1. Install [required dependencies](requirements.txt). Currently, only [`pygame`](https://pypi.org/project/pygame/) is required for running the simulation.
2. Write and save your pattern inside the [`patterns`](patterns) directory. For inspiration, examples and help, you can check the existing patterns.
3. The pattern filename should describe the pattern or be your name. Each pattern also needs to contain a `# NAME: Your Pattern Name` comment with the pattern display name. The display name should be similar to the filename. Patterns with the display name `DEBUG` (case-sensitive) will be disabled and hidden.
4. It is recommended to use our simulation while testing your pattern. You can see the instructions for running the simulation below.
5. Once your pattern is ready, create a PR to this repository on GitHub.

## Running Patterns On Simulation

* Optional: Run `python simulation/simulation.py` to create a randomized tree file.
* Run `python -m patterns.one_color_change` from the repository root to run your pattern.

## Running Patterns On Raspberry Pi

Good luck...
