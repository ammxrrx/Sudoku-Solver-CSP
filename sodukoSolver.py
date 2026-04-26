import os
import sys
class PuzzleSolver:
    def __init__(self, filepath):
        self.grid = self.load_data(filepath)
        self.cells = [(row, col) for row in range(9) for col in range(9)]
        self.possibilities = {}
        self.related = {c: set() for c in self.cells}
        self.nodes_visited = 0
        self.dead_ends = 0
        for r, c in self.cells:
            v = self.grid[r][c]
            self.possibilities[(r, c)] = set(range(1, 10)) if v == 0 else {v}
        self.map_dependencies()
    def load_data(self, filepath):
        matrix = []
        try:
            with open(filepath, 'r') as file_obj:
                for txt in file_obj:
                    clean_txt = txt.strip()
                    if clean_txt:
                        matrix.append([int(x) for x in clean_txt])
        except FileNotFoundError:
            print(f"Error: {filepath} missing.")
            sys.exit(1)
        return matrix
    def map_dependencies(self):
        for r, c in self.cells:
            for idx in range(9):
                if idx != c: self.related[(r, c)].add((r, idx))
                if idx != r: self.related[(r, c)].add((idx, c))
            br, bc = (r // 3) * 3, (c // 3) * 3
            for i in range(br, br + 3):
                for j in range(bc, bc + 3):
                    if (i, j) != (r, c):
                        self.related[(r, c)].add((i, j))
    def prune_options(self, n1, n2):
        changed = False
        for val in set(self.possibilities[n1]):
            if len(self.possibilities[n2]) == 1 and val in self.possibilities[n2]:
                self.possibilities[n1].remove(val)
                changed = True
        return changed
    def enforce_consistency(self):
        q = [(n1, n2) for n1 in self.cells for n2 in self.related[n1]]
        while q:
            curr, peer = q.pop(0)
            if self.prune_options(curr, peer):
                if not self.possibilities[curr]:
                    return False
                for other in self.related[curr]:
                    if other != peer:
                        q.append((other, curr))
        return True
    def pick_next_cell(self, current_state):
        best_cell = None
        min_len = 10
        for cell in self.cells:
            opts = len(current_state[cell])
            if 1 < opts < min_len:
                min_len = opts
                best_cell = cell
        return best_cell
    def look_ahead(self, pos, num, current_state):
        next_state = {k: set(v) for k, v in current_state.items()}
        for peer in self.related[pos]:
            if num in next_state[peer]:
                next_state[peer].remove(num)
                if not next_state[peer]:
                    return None
        return next_state
    def search_solution(self, state):
        self.nodes_visited += 1
        target = self.pick_next_cell(state)
        if not target:
            return state
        for guess in state[target]:
            next_step = self.look_ahead(target, guess, state)
            if next_step:
                next_step[target] = {guess}
                outcome = self.search_solution(next_step)
                if outcome:
                    return outcome
        self.dead_ends += 1
        return False
    def execute(self):
        if not self.enforce_consistency():
            return False
        final_map = self.search_solution(self.possibilities)
        if final_map:
            res = [[0]*9 for _ in range(9)]
            for (row, col), val_set in final_map.items():
                res[row][col] = list(val_set)[0]
            return res
        return False
    def display_grid(self, matrix):
        for i in range(9):
            if i % 3 == 0 and i > 0:
                print("-" * 21)
            line = []
            for j in range(9):
                if j % 3 == 0 and j > 0:
                    line.append("|")
                line.append(str(matrix[i][j]))
            print(" ".join(line))
if __name__ == "__main__":
    target_files = ["easy.txt", "medium.txt", "hard.txt", "veryhard.txt"]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for item in target_files:
        print(f"\n---> Working on {item} <---")
        full_path = os.path.join(base_dir, item)
        engine = PuzzleSolver(full_path)
        ans = engine.execute()
        if ans:
            engine.display_grid(ans)
        else:
            print("Failed to find a valid arrangement.")
        print(f"Nodes expanded: {engine.nodes_visited}")
        print(f"Dead ends hit: {engine.dead_ends}")