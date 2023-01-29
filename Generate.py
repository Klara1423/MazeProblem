# 迷宫生成
# 提供两种生成模式：PRIM、DFS

import time
import random
import numpy as np
from PIL import Image
from copy import deepcopy
"""
导入了5个模块：
time: 时间处理

random: 伪随机数生成

numpy: 快速处理数组

PIL(pillow):图像处理
    Image: 图像处理

copy: 变量拷贝
    deepcopy: 深拷贝，父对象、子对象都拷贝
"""

class MazeMap: #迷宫生成、导入、保存类
    def __init__(self):
        self._maze_map = None
        self.generate_time = 0
    """
    新建了MazeMap的两个属性：
    _maze_map
        一个空数组，用于记录迷宫
    generate_time
        一个浮点数，用于记录时间
    """

    def init_maze(self):# 初始化迷宫行为
        self.start = np.array([0, 0])
        self.road = np.argwhere(self._maze_map == 0)
        self.end = self.road[np.argmax(np.sum(self.road * 2, axis=1))]
    """
    新建了MazeMap的两个属性：
    start
        一维数组[0, 0]，记录迷宫起点
    road
        数组self._maze_map中 = 0的元素的索引组成的新一维数组
    end
        数组self.road中索引为self.road中？？？？？？？？？？？？？？？？的元素
    """

    def _generate_map(self, generate, size):# 生成迷宫行为1
        self.generate_time = time.time()
        maze_map = None
        if generate == "DFS":
            maze_map = self._DFS(size)
        elif generate == "PRIM":
            maze_map = self._PRIM(size)
        self.generate_time = time.time() - self.generate_time
        print(self.generate_time)
        return maze_map
    """
    两个参数generate（字符串，将从下拉框com_generate选择的值）, size（元组,(x, y)）

    修改属性generate_time为当前的时间戳（time.time()返回值，浮点数，自1970年1月1日08:00:00AM到当前时刻之间的秒数UTC+8）

    新建了一个变量maze_map并初始化（一个二维数组）

    如果参数generate的值是"DFS"，通过_DFS行为（DFS生成，在下面）修改变量maze_map
    如果参数generate的值是"PRIM"，通过_PRIM行为（PRIM生成，在下面）修改变量maze_map

    修改属性generate_time为当前的时间戳与上次的差值（记录花费时间）

    输出属性generate_time

    返回变量maze_map（二位数组）
    """

    def PRIM_det(self, maze, memory, size):
        index = np.array(memory[random.randint(0, len(memory)-1)])
        direction = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])
        legal_direction = []
        for item in range(len(direction)):
            new_index = index + direction[item]
            if not (0 <= new_index[0] < size[0] and 0 <= new_index[1] < size[1]):
                continue
            if maze[new_index[0], new_index[1], 0] == 1:
                continue
            legal_direction.append(item)
        if len(legal_direction) > 0:
            dire = legal_direction[random.randint(0, len(legal_direction)-1)]
            new_index = index + direction[dire]
            # print(index, new_index, direction[dire])
            if 0 != np.sum(np.abs((np.array(memory) - new_index)), axis=1).min():
                memory.append(list(new_index))
                maze[index[0], index[1], dire+1] = 0
                maze[new_index[0], new_index[1], (dire + 2) % 4 + 1] = 0
                maze[new_index[0], new_index[1], 0] = 1
            else:
                memory.remove(list(index))
        else:
            memory.remove(list(index))

    def PRIM2map(self, maze):
        shape = maze.shape[:2]
        maze_map = np.ones((shape[0]*2-1, shape[1]*2-1))
        for i in range(maze_map.shape[0]):
            for j in range(maze_map.shape[1]):
                if i % 2 == 0 and j % 2 == 0:
                    maze_map[i, j] = 0
                elif i % 2 == 0 and j % 2 == 1:
                    maze_map[i, j] = maze[i//2, j//2, 1] + maze[i//2, j//2+1, 3]
                elif i % 2 == 1 and j % 2 == 0:
                    maze_map[i, j] = maze[i//2, j//2, 2] + maze[i//2+1, j//2, 4]
        return maze_map

    def _PRIM(self, size):# PRIM生成行为
        size = (size[0]//2, size[1]//2)
        maze = np.empty((*size, 5), dtype=np.uint8)
        maze[:, :, 0] = 0
        maze[:, :, 1:] = 1
        maze[0, 0, 0] = 1
        memory = [[0, 0]]
        while len(memory) > 0:
            self.PRIM_det(maze, memory, size)
        return self.PRIM2map(maze)

    def _DFS(self, size):# DFS生成行为
        maze = np.empty((*size, 2), dtype=np.uint8)# (x, y, 2)
        maze[:, :, 0] = 1
        maze[:, :, 1] = 0
        maze[0][0][0], maze[0][0][1] = 0, 1
        memory = [np.array([0, 0])]
        while len(memory) > 0:
            legal_direction = self.judge_direction(maze, memory[-1], size)
            if len(legal_direction) == 0:
                memory.pop()
            else:
                new_index = legal_direction[random.randint(0, len(legal_direction)-1)]
                memory.append(new_index)
                maze[new_index[0], new_index[1]] = np.array([0, 1])
        maze = maze[:, :, 0]
        return maze
    """
    用方法np.empty()生成了一个未初始化的三维数组maze（当成一个元素都是一维数组的二维数组，x -> 行，y -> 列，2 -> 元素长度），数组形状为(x, y, 2)，数据类型为8字节无符号整数，记录迷宫形状和访问状态
    maze数组所有元素修改为[1, 0]， 第一行第一列为[0, 1]（[迷宫形状，访问状态]）

    新建了一个由二维数组构成的空列表memory，记录DFS状态（生成的路径）

    当列表memory长度大于为0时循环
        新建了一个列表legal_direction，通过judge_direction()方法
        进行了修改（可以继续生成的位置）

        如果列表legal_direction长度为0，删除列表memory最后一个元素（走投无路就往回退）
        否则
            新建一个变量new_index（一维数组），值为列表legal_direction中的随机一个元素（随机选一个可生成的位置）
            将变量new_index添加到列表memory里（选好了就走呗）

    修改三维数组maze（只保留迷宫，删除状态，变成二维数组）
    返回二维数组maze
    """

    @staticmethod
    # 静态方法：无slef参数,不需要实例即可调用，相当于封装在类里的的函数
    def judge_direction(maze, index, size):# 判断方向方法
        direction = np.array([[0, 1], [1, 0], [-1, 0], [0, -1]])
        legal_direction = []
        for item in direction:
            new_index = index + item
            if not (0 <= new_index[0] < size[0] and 0 <= new_index[1] < size[1]):
                continue
            if maze[new_index[0], new_index[1], 1] == 1:
                continue
            pass_value = 0
            for dire in direction:
                temp_index = new_index + dire
                pass_value += maze[temp_index[0], temp_index[1], 0] if temp_index[0] < size[0] and temp_index[1] < size[1] else 1
            if pass_value < 3:
                maze[new_index[0], new_index[1], 1] = 1
                continue
            legal_direction.append(new_index)
        return legal_direction
    """
    三个参数maze（三维数组）, index（列表memory最后一个元素，一维数组）, size（元组，(x, y)）

    新建了一个二维数组direction，每一行代表一个方向

    新建了一个空列表legal_direction

    循环遍历列表direction
        新建了一个一维数组new_index，值为new_index + item



    列表egal_direction添加一个元素new_index（一维数组）
    返回列表legal_direction
    """

    def load_map(self, path):
        self._maze_map = np.load(path)

    def get_map(self):
        return self._maze_map
    
    def save_map(self, save_path):
        np.save(save_path, self._maze_map)

    def generate(self, generate, size):# 生成迷宫行为0
        self._maze_map = self._generate_map(generate, size)
    """
    通过_generate_map行为（生成迷宫1，在上面）修改了属性_maze_map（二维数组）
    """

    def get_figure(self, figure_size=(720, 720)):# 转图片行为
        maze = deepcopy(self._maze_map)
        maze[maze == 0] = 255
        maze[maze == 1] = 0
        maze[maze == 2] = 0
        maze[self.start[0], self.start[1]] = 128
        maze[self.end[0], self.end[1]] = 128
        maze_dis = np.zeros((maze.shape[0]+2, maze.shape[1]+2), dtype=np.uint8)
        maze_dis[1:-1, 1:-1] = maze
        maze_dis = Image.fromarray(maze_dis)
        image = maze_dis.resize(figure_size, Image.NEAREST)
        return image
    """
    新建一个变量maze，把_maze_map（之前储存迷宫的二维数组）复制过来
        数组中等于0的元素改为255，等于1或2的元素改为0
        把起点和种终点对应的元素改为128

    新建了一个变量maze_dis（就是加了个边框）
        用方法np.zores()生成了一个初始化的二维数组maze_dis()，行和列在maze基础上+2，数据类型还是8字节无符号整数
        把数组maze的值复制到maze_dis中间

    通过Image.fromarray()方法把数组maze_dis转换成image图片

    新建了一个变量image
        图片maze_dis缩放成720*720传给image，采用最近邻法缩放（速度快但精度低）

    返回image
    """

    def random_dismantles_wall(self, n):
        while n > 0 and (self._maze_map > 0).sum() > n:
            x = random.randint(0, self._maze_map.shape[0]-1)
            y = random.randint(0, self._maze_map.shape[1]-1)
            if self._maze_map[x, y] > 0:
                self._maze_map[x, y] = 0
                n -= 1

if __name__ == "__main__":
    maze = MazeMap()
    maze.generate("PRIM", (32, 32))
    maze.init_maze()
    maze.get_figure()