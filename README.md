# Sudoku CSP Solver (AI Constraint Satisfaction Problem)

This project implements an intelligent Sudoku solver using constraint satisfaction techniques, arc consistency, and recursive backtracking with heuristics.

---

## Features

* Constraint Satisfaction Problem (CSP) formulation
* Arc consistency propagation
* Forward-looking constraint pruning
* Backtracking search with heuristics
* Minimum Remaining Values (MRV) variable selection
* Performance tracking (nodes visited, dead ends)
* Supports multiple puzzle difficulty levels

---

## How It Works

The solver treats Sudoku as a constraint satisfaction problem:

* Each cell is a variable with a domain of possible values (1–9)
* Constraints ensure no repeated values in:

  * Rows
  * Columns
  * 3×3 subgrids

The algorithm uses:

* Constraint propagation to reduce domains early
* Heuristic selection to choose the most constrained cell
* Backtracking search when necessary
* Forward checking to avoid invalid states

---

## Input Format

Puzzles are loaded from text files:

* Each line represents a row
* Digits represent values (0 = empty cell)

Example:

```
530070000
600195000
098000060
...
```

---

## Output

* Solved Sudoku grid
* Number of nodes expanded
* Number of dead ends encountered

---

## Tech Stack

* Python 3
* Standard libraries only (os, sys)

## Concepts Used

* Constraint Satisfaction Problems (CSP)
* Arc Consistency (AC-style propagation)
* Backtracking Search
* Forward Checking
* Heuristic Variable Selection (MRV idea)

---

## Notes

* Performance depends heavily on puzzle difficulty
* Hard puzzles may require deeper backtracking
* Constraint propagation reduces search space significantly
