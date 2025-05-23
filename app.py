import pyxel
from generator import MapGenerator

class MyApp:
    def __init__(self):
        self.mg = MapGenerator(4, 4, 5)
        self.tiles = self.mg.generate()
        self.width = self.mg.cells_x * self.mg.cell_size
        self.height = self.mg.cells_y * self.mg.cell_size

        self.player_x, self.player_y = self.mg.get_stairs_positions()[0]
        self.tile_size = 16
        self.camera_tiles_x = 16
        self.camera_tiles_y = 14
        self.screen_width = self.camera_tiles_x * self.tile_size
        self.screen_height = self.camera_tiles_y * self.tile_size

        pyxel.init(self.screen_width, self.screen_height, title="roguelike-sfc-style", display_scale=2)
        pyxel.load("assets/resource.pyxres")

        # タイル番号→resource.pyxres内の座標(16x16)　壁の8方向判定IDも追加
        self.tile_sprite_coords = {
            2: (0, 0),    # 床
            99: (16, 0),  # 階段下
            # 壁ID例：20〜28は壁の8方向判定用のタイル（ここは適宜調整）
            20: (32, 0),  # 壁基本
            21: (48, 0),  # 壁 上
            22: (64, 0),  # 壁 右上
            23: (80, 0),  # 壁 右
            24: (96, 0),  # 壁 右下
            25: (112, 0), # 壁 下
            26: (128, 0), # 壁 左下
            27: (144, 0), # 壁 左
            28: (160, 0), # 壁 左上
            # 必要ならもっと追加してね
        }

        pyxel.run(self.update, self.draw)

    def update(self):
        dx, dy = 0, 0
        if pyxel.btnp(pyxel.KEY_UP):
            dy = -1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            dy = 1
        elif pyxel.btnp(pyxel.KEY_LEFT):
            dx = -1
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            dx = 1

        next_tile = self.tiles.get((self.player_x + dx, self.player_y + dy), 1)
        # 歩けるIDに壁の8方向判定タイルは含めない（例：壁は歩けない）
        if next_tile in (2, 98, 99):
            self.player_x += dx
            self.player_y += dy

        if pyxel.btnp(pyxel.KEY_R):
            self.tiles = self.mg.generate()
            self.player_x, self.player_y = self.mg.get_stairs_positions()[0]

    def draw(self):
        pyxel.cls(0)
        cam_left = self.player_x - self.camera_tiles_x // 2
        cam_top = self.player_y - self.camera_tiles_y // 2

        for y in range(self.camera_tiles_y):
            for x in range(self.camera_tiles_x):
                map_x = cam_left + x
                map_y = cam_top + y
                tile = self.tiles.get((map_x, map_y), 0)
                if tile in self.tile_sprite_coords:
                    sx, sy = self.tile_sprite_coords[tile]
                    px = x * self.tile_size
                    py = y * self.tile_size
                    pyxel.blt(px, py, 1, sx, sy, self.tile_size, self.tile_size)
                else:
                    # 未対応タイルは黒で塗る
                    px = x * self.tile_size
                    py = y * self.tile_size
                    pyxel.rect(px, py, self.tile_size, self.tile_size, 0)

        # プレイヤーは単色四角（素材化もOK）
        px = (self.camera_tiles_x // 2) * self.tile_size
        py = (self.camera_tiles_y // 2) * self.tile_size
        pyxel.rect(px, py, self.tile_size, self.tile_size, 11)

MyApp()
