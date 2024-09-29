import pyxel

SCREEN_WIDTH=160
SCREEN_HEIGHT=256
CELL_SIZE=8
ICON_SIZE=16
STATE_EDIT=False
STATE_GO=True

class App:
    def __init__(self):

        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.load("my_resource.pyxres")
        # 160x256
        self.today_state = [[False] * SCREEN_WIDTH for i in range(SCREEN_HEIGHT)]
        self.tommorow_state = [[False] * SCREEN_WIDTH for i in range(SCREEN_HEIGHT)]

        self.state = STATE_EDIT

        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def is_menu_area(self, px, py):
        return(py >= SCREEN_HEIGHT-CELL_SIZE*2 and py <=  SCREEN_HEIGHT)

    def is_edit_area(self, px, py):
        return(px >= 48 and px <= 62)

    def is_go_area(self, px, py):
        return(px >= 78 and px <= 94)

    def is_clear_area(self, px, py):
        return(px >= 16 and px <= 32)
        
    def is_in_edit_area(self, px, py):
        return(0 <= px <= SCREEN_WIDTH and 0 <= py <= SCREEN_HEIGHT-ICON_SIZE)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            px = pyxel.mouse_x
            py = pyxel.mouse_y

            # 画面に下部をクリックした
            #
            if self.is_menu_area(px, py):
                if self.is_edit_area(px, py):
                    self.state = STATE_EDIT
                elif self.is_go_area(px, py):
                    self.state = STATE_GO
                elif self.is_clear_area(px, py):
                    self.today_state = [[False] * SCREEN_WIDTH for i in range(SCREEN_HEIGHT)]
                    self.tommorow_state = [[False] * SCREEN_WIDTH for i in range(SCREEN_HEIGHT)]

            if self.is_in_edit_area(px, py):
                self.today_state[px // 8][py // 8] = not self.today_state[px // 8][py // 8]
                self.tommorow_state[px // 8][py // 8] = not self.tommorow_state[px // 8][py // 8]

        if self.state:

            surrounding =[
                [ 1,  0],
                [ 1,  1],
                [ 0,  1],
                [-1,  1],
                [-1,  0],
                [-1, -1],
                [ 0, -1],
                [ 1, -1]]

            
            for i in range(1, SCREEN_HEIGHT-ICON_SIZE-1):
                for j in range(1, SCREEN_WIDTH-1):
                    cells = 0

                    for k in range(8):
                        if self.today_state[i + surrounding[k][0]][j + surrounding[k][1]]:
                            cells += 1

                    if self.today_state[i][j]:
                        if cells <= 1:
                            self.tommorow_state[i][j] = False
                        elif cells >= 4:
                            self.tommorow_state[i][j] = False
                    else:
                        if cells == 3:
                            self.tommorow_state[i][j] = True

            for i in range(1, SCREEN_HEIGHT-ICON_SIZE-1):
                for j in range(1, SCREEN_WIDTH-1):
                    self.today_state[i][j] = self.tommorow_state[i][j]

    def draw(self):
        pyxel.cls(0)

        for i in range(SCREEN_HEIGHT):
            for j in range(SCREEN_WIDTH):
                if self.today_state[i][j]:
                    pyxel.rect(CELL_SIZE*i, CELL_SIZE*j, CELL_SIZE, CELL_SIZE, 6)

        # 消しゴムの表示
        pyxel.blt(ICON_SIZE, SCREEN_HEIGHT-ICON_SIZE, 0,  0,  0, 16, 16)

        # ペンの表示
        if not self.state:
            pyxel.blt(ICON_SIZE*3, SCREEN_HEIGHT-ICON_SIZE, 0, 16, 16, 16, 16)
        else:
            pyxel.blt(ICON_SIZE*3, SCREEN_HEIGHT-ICON_SIZE, 0, 16,  0, 16, 16)

        # 再生ボタンの表示
        if self.state:
            pyxel.blt(ICON_SIZE*5, SCREEN_HEIGHT-ICON_SIZE, 0, 32, 16, 16, 16)
        else:
            pyxel.blt(ICON_SIZE*5, SCREEN_HEIGHT-ICON_SIZE, 0, 32,  0, 16, 16)


App()
