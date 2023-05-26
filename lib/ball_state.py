import math


class ClassBall:
    """
    球类，用于初始化/更新球状态。
    """
    all_balls = []

    def __init__(self, x: float, y: float, block_height: float, angle: float, speed: float) -> None:
        self.x = x
        self.y = y
        self.r = block_height / 4  # 球的碰撞半径
        self.angle = angle  # 水平向左为 x轴，弧度制，范围在 0 <= angle < 2pi
        self.speed = speed * (block_height / 20)
        ClassBall.all_balls.append(self)

    def next_state(self) -> float:
        delta_x = math.cos(self.angle) * self.speed
        delta_y = - math.sin(self.angle) * self.speed
        return self.x + delta_x, self.y + delta_y

    def crash_block(self, block_height: int, layer: list) -> list:
        """
        判断球和砖块的碰撞，并更新状态。
        @return: 所有被碰撞到的砖块的坐标
        """
        crash_blocks = []
        # 判断当前位置是否发生碰撞
        line = int(self.y // block_height)
        num = int(self.x // (block_height * 3))
        if (num < 0) or (num >= 6):
            return crash_blocks
        # 判断上方的砖块
        if 0 < line < 28:
            if (layer[line - 1][num] == '1') and (0 < self.angle , math.pi):
                if self.y - self.r <= line * block_height:
                    self.angle = 2 * math.pi - self.angle
                    crash_blocks.append((line - 1, num))
        # 判断下方的砖块
        if line < 26:
            if (layer[line + 1][num] == '1') and (math.pi < self.angle < 2 * math.pi):
                if self.y + self.r >= (line + 1) * block_height:
                    self.angle = 2 * math.pi - self.angle
                    crash_blocks.append((line + 1, num))
        # 判断左方的砖块
        if num > 0 and line < 27:
            if (layer[line][num - 1] == '1') and (math.pi / 2 < self.angle < 3 * math.pi / 2):
                if self.x - self.r <= num * block_height * 3:
                    self.angle = math.pi - self.angle
                    if self.angle < 0:
                        self.angle += 2 * math.pi
                    crash_blocks.append((line, num - 1))
        # 判断右方的砖块
        if num < 5 and line < 27:
            if (layer[line][num + 1] == '1') and ((0 <= self.angle < math.pi / 2) or (3 * math.pi / 2 < self.angle < 2 * math.pi)):
                if self.x + self.r >= (num + 1) * block_height * 3:
                    self.angle = math.pi - self.angle
                    if self.angle < 0:
                        self.angle += 2 * math.pi
                    crash_blocks.append((line, num + 1))
        if len(crash_blocks) > 0:
            return crash_blocks


        # 判断下个位置是否碰撞过度，如球的中心陷入或穿过砖块了
        x_next, y_next = self.next_state()
        line_next = y_next // block_height
        num_next = x_next // (block_height * 3)
        if (line_next == line) and (num_next == num):
            return crash_blocks

        # 建立轨迹的方程
        k = - math.tan(self.angle)  # 斜率
        b = self.y - (k * self.x)  # 延长线与y轴的交点，y轴竖直向下

        # 分别判断上下左右砖块是否被过度碰撞
        if 0 < line < 28:
            if (layer[line - 1][num] == '1') and (0 < self.angle , math.pi):
                y = line * block_height  # 上砖块的底边
                x = (y - b) / k  # 求两直线交点
                # 判断交点是否在两线段上
                if (num * block_height * 3 < x < (num + 1) * block_height * 3) and (min(self.y, y_next) < y < max(self.y, y_next)):
                    self.angle = 2 * math.pi - self.angle
                    self.y = 2 * y - self.y
                    crash_blocks.append((line - 1, num))
        if line < 26:
            if (layer[line + 1][num] == '1') and (math.pi < self.angle < 2 * math.pi):
                y = (line + 1) * block_height  # 下砖块的顶边
                x = (y - b) / k  # 求两直线交点
                if (num * block_height * 3 < x < (num + 1) * block_height * 3) and (min(self.y, y_next) < y < max(self.y, y_next)):
                    self.angle = 2 * math.pi - self.angle
                    self.y = 2 * y - self.y
                    crash_blocks.append((line + 1, num))
        if num > 0 and line < 27:
            if (layer[line][num - 1] == '1') and (math.pi / 2 < self.angle < 3 * math.pi / 2):
                x = num * block_height * 3  # 左砖块的右边
                y = k * x + b  # 求两直线交点
                if (min(self.x, x_next) < x < max(self.x, x_next)) and (line * block_height < y < (line + 1) * block_height):
                    self.angle = math.pi - self.angle
                    if self.angle < 0:
                        self.angle += 2 * math.pi
                    self.x = 2 * x - self.x
                    crash_blocks.append((line, num - 1))
        if num < 5 and line < 27:
            if (layer[line][num + 1] == '1') and ((0 <= self.angle < math.pi / 2) or (3 * math.pi / 2 < self.angle < 2 * math.pi)):
                x = (num + 1) * block_height * 3  # 右砖块的左边
                y = k * x + b  # 求两直线交点
                if (min(self.x, x_next) < x < max(self.x, x_next)) and (line * block_height < y < (line + 1) * block_height):
                    self.angle = math.pi - self.angle
                    if self.angle < 0:
                        self.angle += 2 * math.pi
                    self.x = 2 * x - self.x
                    crash_blocks.append((line, num + 1))
        if len(crash_blocks) > 0:
            return crash_blocks
        
        # 分别判断左上、右上、左下、右下的砖块
        if (0 < line < 28) and (num > 0):
            if (layer[line - 1][num - 1] == '1') and (math.pi / 2 < self.angle < math.pi):
                y = line * block_height  # 砖块的底边
                x = (y - b) / k  # 求两直线交点
                # 判断交点是否在两线段上
                if ((num - 1) * block_height * 3 < x < num * block_height * 3) and (min(self.y, y_next) < y < max(self.y, y_next)):
                    self.angle = 2 * math.pi - self.angle  # 角度对称
                    self.y = 2 * y - self.y  # 位置对称
                    crash_blocks.append((line - 1, num - 1))

                x = num * block_height * 3  # 砖块的右边
                y = k * x + b  # 求两直线交点
                if (min(self.x, x_next) < x < max(self.x, x_next)) and ((line - 1) * block_height < y < line * block_height):
                    self.angle = math.pi - self.angle
                    if self.angle < 0:
                        self.angle += 2 * math.pi
                    self.x = 2 * x - self.x
                    crash_blocks.append((line - 1, num - 1))

        if (0 < line < 28) and (num < 5):
            if (layer[line - 1][num + 1] == '1') and (0 < self.angle < math.pi / 2):
                y = line * block_height  # 砖块的底边
                x = (y - b) / k  # 求两直线交点
                # 判断交点是否在两线段上
                if ((num + 1) * block_height * 3 < x < (num + 2) * block_height * 3) and (min(self.y, y_next) < y < max(self.y, y_next)):
                    self.angle = 2 * math.pi - self.angle
                    self.y = 2 * y - self.y
                    crash_blocks.append((line - 1, num + 1))

                x = (num + 1) * block_height * 3  # 砖块的左边
                y = k * x + b  # 求两直线交点
                if (min(self.x, x_next) < x < max(self.x, x_next)) and ((line - 1) * block_height < y < line * block_height):
                    self.angle = math.pi - self.angle
                    if self.angle < 0:
                        self.angle += 2 * math.pi
                    self.x = 2 * x - self.x
                    crash_blocks.append((line - 1, num + 1))

        if (line < 26) and (num > 0):
            if (layer[line + 1][num - 1] == '1') and (math.pi < self.angle < 3 * math.pi / 2):
                y = (line + 1) * block_height  # 砖块的顶边
                x = (y - b) / k  # 求两直线交点
                # 判断交点是否在两线段上
                if ((num - 1) * block_height * 3 < x < num * block_height * 3) and (min(self.y, y_next) < y < max(self.y, y_next)):
                    self.angle = 2 * math.pi - self.angle
                    self.y = 2 * y - self.y
                    crash_blocks.append((line + 1, num - 1))

                x = num * block_height * 3  # 砖块的右边
                y = k * x + b  # 求两直线交点
                if (min(self.x, x_next) < x < max(self.x, x_next)) and ((line + 1) * block_height < y < (line + 2) * block_height):
                    self.angle = math.pi - self.angle
                    if self.angle < 0:
                        self.angle += 2 * math.pi
                    self.x = 2 * x - self.x
                    crash_blocks.append((line + 1, num - 1))

        if (line < 26) and (num < 5):
            if (layer[line + 1][num + 1] == '1') and (3 * math.pi / 2 < self.angle < 2 * math.pi):
                y = (line + 1) * block_height  # 砖块的顶边
                x = (y - b) / k  # 求两直线交点
                # 判断交点是否在两线段上
                if ((num + 1) * block_height * 3 < x < (num + 2) * block_height * 3) and (min(self.y, y_next) < y < max(self.y, y_next)):
                    self.angle = 2 * math.pi - self.angle
                    self.y = 2 * y - self.y
                    crash_blocks.append((line + 1, num + 1))

                x = (num + 1) * block_height * 3  # 砖块的左边
                y = k * x + b  # 求两直线交点
                if (min(self.x, x_next) < x < max(self.x, x_next)) and ((line + 1) * block_height < y < (line + 2) * block_height):
                    self.angle = math.pi - self.angle
                    if self.angle < 0:
                        self.angle += 2 * math.pi
                    self.x = 2 * x - self.x
                    crash_blocks.append((line + 1, num + 1))

        return crash_blocks

    def crash_wall(self, block_height: int) -> bool:
        """
        判断球是否与墙壁相撞，并更新球状态。
        """
        is_crash = False
        # 判断当前位置是否发生碰撞
        line = int(self.y // block_height)
        num = int(self.x // (block_height * 3))
        # 判断上方墙壁
        if line == 0:
            if (self.y - self.r <= 0) and (0 < self.angle < math.pi):
                self.angle = 2 * math.pi - self.angle
                is_crash = True
        # 判断左方墙壁
        if num == 0:
            if (self.x - self.r <= 0) and (math.pi / 2 < self.angle < 3 * math.pi / 2):
                self.angle = math.pi - self.angle
                if self.angle < 0:
                    self.angle += 2 * math.pi
                is_crash = True
        # 判断右方墙壁
        if num == 5:
            if (self.x + self.r >= block_height * 18) and ((0 <= self.angle < math.pi / 2) or (3 * math.pi / 2 < self.angle < 2 * math.pi)):
                self.angle = math.pi - self.angle
                if self.angle < 0:
                    self.angle += 2 * math.pi
                is_crash = True
        if is_crash:
            return True
        
        # 判断下个位置是否碰撞过度
        x_next, y_next = self.next_state()
        if (y_next >= 0) and (0 <= x_next <= block_height * 6):
            return False
        # 分别判断上方、左方、右方
        if (y_next < 0) and (0 < self.angle < math.pi):
            self.angle = 2 * math.pi - self.angle
            self.y = - self.y
        if (x_next < 0) and (math.pi / 2 < self.angle < 3 * math.pi / 2):
            self.angle = math.pi - self.angle
            if self.angle < 0:
                self.angle += 2 * math.pi
            self.x = - self.x
        elif (x_next > block_height * 18) and ((0 <= self.angle < math.pi / 2) or (3 * math.pi / 2 < self.angle < 2 * math.pi)):
            self.angle = math.pi - self.angle
            if self.angle < 0:
                self.angle += 2 * math.pi
            self.x = block_height * 36 - self.x
        return True

    def update_state(self) -> None:
        self.x, self.y = self.next_state()

    def is_out(self, block_height) -> bool:
        """
        判断球是否掉出界面。
        """
        if self.y > block_height * 32:
            return True
        else:
            return False
    
    def crash_board(self, block_height: int, board_x_left: float) -> bool:
        """
        判断球是否和板子相撞，并更新球状态。
        """
        board_x_right = board_x_left + block_height * 6
        # 球中心低于木板，不能发生反弹
        if self.y > block_height * 29.5:
            return False

        # 碰撞
        if self.y + self.r >= block_height * 29.5:
            # 向下运动才碰撞
            if math.pi < self.angle < 2 * math.pi:
                if board_x_left <= self.x <= board_x_right:
                    self.angle = 2 * math.pi - self.angle
                    add_angle = (board_x_right - self.x) / (block_height * 6) * (2 * math.pi / 3) + (math.pi / 6)
                    self.angle = (self.angle + add_angle) / 2
                    return True

        # 碰撞过度
        x_next, y_next = self.next_state()
        k = - math.tan(self.angle)  # 斜率
        b = self.y - (k * self.x)  # 延长线与y轴的交点，y轴竖直向下
        y = block_height * 29.5  # 砖块的顶边
        x = (y - b) / k  # 求两直线交点
        # 判断交点是否在两线段上
        if (board_x_left <= x <= board_x_right) and (min(self.y, y_next) < y < max(self.y, y_next)):
            self.angle = 2 * math.pi - self.angle
            add_angle = (board_x_right - x) / (block_height * 6) * (2 * math.pi / 3) + (math.pi / 6)
            self.angle = (self.angle + add_angle) / 2
            self.y = 2 * y - self.y
            return True

        return False
