import random
import itertools

class MapGenerator:
    def __init__(self, cells_x, cells_y, cell_size=5):
        self.cells_x = cells_x
        self.cells_y = cells_y
        self.cell_size = cell_size
        self.tiles = {}
        self.stairs_up_pos = None
        self.stairs_down_pos = None

    def _astar(self, start, goal):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def reconstruct_path(n):
            if n == start:
                return [n]
            return reconstruct_path(came_from[n]) + [n]

        def neighbors(n):
            x, y = n
            return (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)

        closed = set()
        open_set = {start}
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_set:
            current = min(open_set, key=lambda o: f_score.get(o, float('inf')))
            if current == goal:
                return reconstruct_path(goal)

            open_set.remove(current)
            closed.add(current)

            for neighbor in neighbors(current):
                if neighbor in closed:
                    continue
                tentative_g = g_score[current] + 1

                if neighbor not in open_set or tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    open_set.add(neighbor)

        return []

    def generate(self):
        class Cell:
            def __init__(self, x, y, id):
                self.x = x
                self.y = y
                self.id = id
                self.connected = False
                self.connected_to = []
                self.room = None

            def connect(self, other):
                if other not in self.connected_to:
                    self.connected_to.append(other)
                if self not in other.connected_to:
                    other.connected_to.append(self)
                self.connected = True
                other.connected = True

        cells = {}
        for y in range(self.cells_y):
            for x in range(self.cells_x):
                c = Cell(x, y, len(cells))
                cells[(x, y)] = c

        current = last_cell = first_cell = random.choice(list(cells.values()))
        current.connected = True

        def get_neighbors(cell):
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = cells.get((cell.x + dx, cell.y + dy))
                if neighbor:
                    yield neighbor

        while True:
            unconnected = [n for n in get_neighbors(current) if not n.connected]
            if not unconnected:
                break
            neighbor = random.choice(unconnected)
            current.connect(neighbor)
            current = last_cell = neighbor

        while True:
            unconnected = [c for c in cells.values() if not c.connected]
            if not unconnected:
                break
            candidates = []
            for c in [c for c in cells.values() if c.connected]:
                nbs = [n for n in get_neighbors(c) if not n.connected]
                if nbs:
                    candidates.append((c, nbs))
            if not candidates:
                break
            cell, neighbors_ = random.choice(candidates)
            cell.connect(random.choice(neighbors_))

        extra_connections = random.randint(
            int((self.cells_x + self.cells_y) / 4),
            int((self.cells_x + self.cells_y) / 1.2)
        )
        retries = 10
        while extra_connections > 0 and retries > 0:
            cell = random.choice(list(cells.values()))
            neighbor = random.choice(list(get_neighbors(cell)))
            if neighbor in cell.connected_to:
                retries -= 1
                continue
            cell.connect(neighbor)
            extra_connections -= 1

        rooms = []
        for cell in cells.values():
            w = random.randint(3, self.cell_size - 2)
            h = random.randint(3, self.cell_size - 2)
            x = cell.x * self.cell_size + random.randint(1, self.cell_size - w - 1)
            y = cell.y * self.cell_size + random.randint(1, self.cell_size - h - 1)
            floor_tiles = [(x + i, y + j) for i in range(w) for j in range(h)]
            cell.room = floor_tiles
            rooms.append(floor_tiles)

        connections = {}
        for c in cells.values():
            for other in c.connected_to:
                pair = tuple(sorted((c.id, other.id)))
                connections[pair] = (c.room, other.room)

        for room_a, room_b in connections.values():
            start = random.choice(room_a)
            goal = random.choice(room_b)
            corridor = []
            for tile in self._astar(start, goal):
                if tile not in room_a and tile not in room_b:
                    corridor.append(tile)
            rooms.append(corridor)

        width = self.cells_x * self.cell_size
        height = self.cells_y * self.cell_size
        self.tiles = {(x, y): 0 for x in range(width) for y in range(height)}

        for tile in itertools.chain.from_iterable(rooms):
            self.tiles[tile] = 2

        for (x, y), tile in list(self.tiles.items()):
            if tile == 0:
                for nx in range(x - 1, x + 2):
                    for ny in range(y - 1, y + 2):
                        if self.tiles.get((nx, ny)) == 2:
                            self.tiles[(x, y)] = 1
                            break

        # 壁ID振り分けを追加！
        self.assign_wall_patterns()

        self.stairs_up_pos = random.choice(first_cell.room)
        self.stairs_down_pos = random.choice(last_cell.room)
        self.tiles[self.stairs_up_pos] = 98
        self.tiles[self.stairs_down_pos] = 99

        return self.tiles

    def assign_wall_patterns(self):
        new_tiles = self.tiles.copy()
        for (x, y), tile in self.tiles.items():
            if tile == 1:  # 壁の場合
                up = self.tiles.get((x, y - 1), 0) == 2
                down = self.tiles.get((x, y + 1), 0) == 2
                left = self.tiles.get((x - 1, y), 0) == 2
                right = self.tiles.get((x + 1, y), 0) == 2

                up_left = self.tiles.get((x - 1, y - 1), 0) == 2
                up_right = self.tiles.get((x + 1, y - 1), 0) == 2
                down_left = self.tiles.get((x - 1, y + 1), 0) == 2
                down_right = self.tiles.get((x + 1, y + 1), 0) == 2

                # 壁IDの割り当て例（ここから自由に拡張してOK！）
                if up and down and left and right and up_left and up_right and down_left and down_right:
                    new_tiles[(x, y)] = 20
                elif up and left and not right and not down:
                    new_tiles[(x, y)] = 21
                elif up and right and not left and not down:
                    new_tiles[(x, y)] = 22
                elif down and left and not up and not right:
                    new_tiles[(x, y)] = 23
                elif down and right and not up and not left:
                    new_tiles[(x, y)] = 24
                elif up:
                    new_tiles[(x, y)] = 10
                elif down:
                    new_tiles[(x, y)] = 11
                elif left:
                    new_tiles[(x, y)] = 12
                elif right:
                    new_tiles[(x, y)] = 13
                else:
                    new_tiles[(x, y)] = 1

        self.tiles = new_tiles

    def get_stairs_positions(self):
        return self.stairs_up_pos, self.stairs_down_pos
