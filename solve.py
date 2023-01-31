# 走迷宫算法
# 提供两种算法：DFS、A*

import time
import queue
import numpy as np
from PIL import Image
from copy import deepcopy
"""
导入了5个模块：
time: 时间处理

queue: 队列

numpy: 快速处理数组

PIL(pillow):图像处理
    Image: 图像处理

copy: 变量拷贝
    deepcopy: 深拷贝，父对象、子对象都拷贝
"""


class DFS:# DFS求解类
    def __init__(self, maze, start, end) -> None:
        self.maze = maze
        self.h, self.w = maze.shape
        self.start = start
        self.end = end
        self.flag = np.zeros_like(maze)
        self.direction = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])
        self.memory = [{"step": self.start, "dire": [0, 1]}]
        self.run = True
        self.cost_time = 0
    """
    三个参数 maze（二维数组，迷宫）, start（一维数组，起点）, end（一维数组，终点）
    新建了一堆属性
    self.maze 为参数迷宫maze
    self.h 为迷宫高
    self.w 为迷宫宽
    self.start 为参数起点
    self.end 为参数终点
    self.flag 和maze shape一样的空数组
    self.direction 二维数组，每一行代表一个方向（下，左，右，上）
    self.memory 为一个字典，有两个键值对，目前分别为起点和起点元素
    self.run = True
    self.cost_time 记录花费时间
    """

    def solve(self):# 求解行为
        star_time = time.time()
        while self.run!=False:
            self.step()
        self.cost_time = time.time() - star_time
    """
        新建变量star_time记录开始时间
        当属性self.run!=False时进行循环，执行step()行为
        属性self.cost_time通过记录结束时间在相减，得到执行时间
    """

    def step(self):
        index = self.memory[-1]["step"]
        if len(self.memory[-1]["dire"]) == 0:      # 当前坐标没有方向的时候退栈
            self.memory.pop()
        else:
            new_index = index + self.direction[self.memory[-1]["dire"][-1]]
            self.flag[new_index[0], new_index[1]] = 1
            self.memory[-1]["dire"].pop()
            dires = self._get_dire(new_index)
            self.memory.append({"step": new_index, "dire": dires})
    """
    
    """    
    def _get_dire(self, index):
        dires = []
        for dire in range(len(self.direction)):
                new_index = index + self.direction[dire]
                if new_index[0] == self.end[0] and new_index[1] == self.end[1]:
                    self.run = False
                if not (0 <= new_index[0] < self.h and 0 <= new_index[1] < self.w):
                    continue
                elif self.maze[new_index[0], new_index[1]] + self.flag[new_index[0], new_index[1]] > 0:
                    continue
                dires.append(dire)
        return dires

    def get_figure(self, figure_size=(720, 720)):
        maze = deepcopy(self.maze)
        maze[self.flag == 1] = 196
        for item in self.memory:
            maze[item["step"][0], item["step"][1]] = 64
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

    def get_info(self):# 整理文本行为
        cost_time = self.cost_time
        exploration = self.flag.sum()
        path_length = len(self.memory)
        info = "耗费时间: %7.4fs\n探索方格: %7d\n路径长度: %7d\n" % (cost_time, exploration, path_length)
        # memory = ["(%3d,%3d)"%(item["step"][0], item["step"][1]) for item in self.memory]
        # info += ">".join(memory)
        return info
    """
    新建了四个变量
    cost_time
        值为属性self.cost_time的值
    exploration

    path_length

    info
        字符串，内容略
    返回字符串info
    """

class BFS:# BFS求解类
    def __init__(self, maze, start, end) -> None:
        self.maze = maze
        self.h, self.w = maze.shape
        self.start = start
        self.end = end
        self.flag = np.zeros_like(maze)
        self.direction = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])
        self.memory = {tuple(self.start.tolist()): None}
        self.wall = [self.start]
        self.run = True
        self.cost_time = 0

    def solve(self):
        star_time = time.time()
        while self.run!=False:
            self.step()
        memory_list = []
        for item in self.memory.keys():
            if item == tuple(self.end.tolist()):
                memory_list.append(self.memory[item])
        while tuple(memory_list[-1].tolist()) != tuple(self.start.tolist()):
            memory_list.append(self.memory[tuple(memory_list[-1].tolist())])
        self.memory = memory_list
        self.cost_time = time.time() - star_time

    def step(self):
        new_wall = []
        for item in self.wall:
            dires = self._get_dire(item)
            for dire in dires:
                new_index = item + self.direction[dire]
                self.flag[new_index[0], new_index[1]] = 1
                new_wall.append(new_index)
                self.memory[tuple(new_index.tolist())] = item
        self.wall = new_wall

    def _get_dire(self, index):
        dires = []
        for dire in range(len(self.direction)):
                new_index = index + self.direction[dire]
                if new_index[0] == self.end[0] and new_index[1] == self.end[1]:
                    self.run = False
                if not (0 <= new_index[0] < self.h and 0 <= new_index[1] < self.w):
                    continue
                elif self.maze[new_index[0], new_index[1]] + self.flag[new_index[0], new_index[1]] > 0:
                    continue
                dires.append(dire)
        return dires

    def get_figure(self, figure_size=(720, 720)):
        maze = deepcopy(self.maze)
        maze[self.flag == 1] = 196
        for item in self.memory:
            maze[item[0], item[1]] = 64
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

    def get_info(self):
        cost_time = self.cost_time
        exploration = self.flag.sum()
        path_length = len(self.memory)
        info = "耗费时间: %7.4fs\n探索方格: %7d\n路径长度: %7d\n" % (cost_time, exploration, path_length)
        # memory = ["(%3d,%3d)"%(item[0], item[1]) for item in self.memory]
        # info += ">".join(memory)
        return info


class AStar:# Astar求解类
    def __init__(self, maze, start, end) -> None:
        self.maze = maze
        self.h, self.w = maze.shape
        self.start = start
        self.end = end
        self.flag = np.zeros_like(maze)
        self.cost = queue.PriorityQueue()
        self.cost.put((np.abs((self.start-self.end)).sum(), 0, self.start))
        self.direction = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])
        self.memory = {tuple(self.start.tolist()): None}
        self.run = True
        self.cost_time = 0

    def solve(self):
        star_time = time.time()
        while self.run!=False:
            self.step()
        memory_list = []
        for item in self.memory.keys():
            if item == tuple(self.end.tolist()):
                memory_list.append(self.memory[item])
        while tuple(memory_list[-1].tolist()) != tuple(self.start.tolist()):
            memory_list.append(self.memory[tuple(memory_list[-1].tolist())])
        self.memory = memory_list
        self.cost_time = time.time() - star_time

    def step(self):
        cost, re_cost, item = self.cost.get()
        item = np.array(item)
        dires = self._get_dire(item)
        for dire in dires:
            new_index = item + self.direction[dire]
            self.flag[new_index[0], new_index[1]] = 1
            self.cost.put((re_cost + 1 + int(np.abs((new_index-self.end)).sum()), re_cost+1, new_index.tolist()))
            self.memory[tuple(new_index.tolist())] = item
        # print(item)
        # time.sleep(0.05)

    def _get_dire(self, index):
        dires = []
        for dire in range(len(self.direction)):
                new_index = index + self.direction[dire]
                if new_index[0] == self.end[0] and new_index[1] == self.end[1]:
                    self.run = False
                if not (0 <= new_index[0] < self.h and 0 <= new_index[1] < self.w):
                    continue
                elif self.maze[new_index[0], new_index[1]] + self.flag[new_index[0], new_index[1]] > 0:
                    continue
                dires.append(dire)
        return dires

    def get_figure(self, figure_size=(720, 720)):
        maze = deepcopy(self.maze)
        maze[self.flag == 1] = 196
        for item in self.memory:
            maze[item[0], item[1]] = 64
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

    def get_info(self):
        cost_time = self.cost_time
        exploration = self.flag.sum()
        path_length = len(self.memory)
        info = "耗费时间: %7.4fs\n探索方格: %7d\n路径长度: %7d\n" % (cost_time, exploration, path_length)
        # memory = ["(%3d,%3d)"%(item[0], item[1]) for item in self.memory]
        # info += ">".join(memory)
        return info