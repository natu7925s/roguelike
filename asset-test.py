import pyxel

TILE_SIZE = 16

tile_defs = {
    0: (0, 0),
    1: (32, 0),
    2: (64, 0),
}

tile_map = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

class App:
    def __init__(self):
        pyxel.init(160, 160, caption="Tile Dictionary & Map")
        pyxel.load("assets.pyxres")  # 必要ならアセット読み込み
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        for y, row in enumerate(tile_map):
            for x, tile_id in enumerate(row):
                u, v = tile_defs[tile_id]
                pyxel.blt(x * TILE_SIZE, y * TILE_SIZE, 0, u, v, TILE_SIZE, TILE_SIZE, 0)

App()
