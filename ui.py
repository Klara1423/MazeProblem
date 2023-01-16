import Generate
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from tkinter import filedialog
from solve import DFS, BFS, AStar
"""
导入了4个模块：
Generate.py: 迷宫生成

solve.py:求解迷宫
    
tkinter: 图形化界面设计
    ttk:界面
    filedialog:对话框
    
PIL(pillow):图像处理
    ImageTk:创捷和生成图像
"""

class MazeUI: #迷宫界面设计类
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title('迷宫生成与破解')
        self.window.geometry('925x760')
        self.window.resizable(0,0)
        self.window.iconbitmap('ico.ico')
        self.canvas = tk.Canvas(self.window, width=720, height=720, bg='black')
        self.canvas.place(width=720, height=720, x=20, y=20)
        """
        建立了MazeUI的两个属性：
        window
            为一个窗口window
            窗口标题为'迷宫生成与破解'
            窗口大小为935*760
            禁用了改变窗口大小
            窗口图标为'ico.ico'  
        acnvas
            为一个window中的画布，宽720，高720，背景为黑色
            画布位于(20,20)
        """
        # 生成地图的宽
        self.label_x = tk.Label(self.window, text="x:", font=("宋体", 12))
        self.label_x.place(width=20, height=20, x=740, y=20)
        self.text_x = tk.Entry(self.window)
        self.text_x.place(width=60, height=20, x=760, y=22)
        """
        建立了MazeUI的两个属性
        label_x
            为一个window中的标签，标签内容为"x:",字体为宋体，大小为12
            标签宽20、高20，位于(740,20)
        text_x
            为一个window中的输入窗口
            标签宽60、高20，位于(760,22)            
        """
        # 生成地图的高
        self.label_y = tk.Label(self.window, text="y:", font=("宋体", 12))
        self.label_y.place(width=20, height=20, x=830, y=20)
        self.text_y = tk.Entry(self.window)
        self.text_y.place(width=60, height=20, x=850, y=22)
        """
        建立了MazeUI的两个属性
        label_y
            为一个window中的标签，标签内容为"y:",字体为宋体，大小为12
            标签宽20、高20，位于(830,20)
        text_y
            为一个window中的输入框
            输入框宽60、高20，位于(850,22)
        """
        # 生成地图的算法
        xVariable = tk.StringVar()
        self.com_generate = ttk.Combobox(self.window, textvariable=xVariable)
        self.com_generate.place(width=60, height=22, x=760, y=52)
        self.com_generate["value"] = ("DFS", "PRIM")
        """
        新建了一个变量
        xVarialbe
            为一个StringVar类型的变量(多行文本)               
        建立了MazeUI的一个属性
        com_generate
            为一个window中的下拉框，下拉框内容属性为xVarialbe变量的类型
            输入框宽60、高22，位于(760,52)      
            下拉框内容为"DFS", "PRIM"                    
        """
        # 生成地图
        self.generate_buttom = tk.Button(self.window, text="生成地图", font=("宋体", 10), command=self.generate_map)
        self.generate_buttom.place(width=60, height=24, x=850, y=50)

        self.text_wall = tk.Entry(self.window)
        self.text_wall.place(width=60, height=20, x=760, y=82)
        self.wall_buttom = tk.Button(self.window, text="拆墙", font=("宋体", 10), command=self.dismantles_wall)
        self.wall_buttom.place(width=60, height=24, x=850, y=80)

        # 加载迷宫
        self.generate_buttom = tk.Button(self.window, text="加载迷宫", font=("宋体", 10), command=self.load_maze)
        self.generate_buttom.place(width=60, height=24, x=760, y=110)

        # 保存迷宫
        self.generate_buttom = tk.Button(self.window, text="保存迷宫", font=("宋体", 10), command=self.save_maze)
        self.generate_buttom.place(width=60, height=24, x=850, y=110)

        # 生成地图的算法
        xVariable = tk.StringVar()
        self.com_pathfinding = ttk.Combobox(self.window, textvariable=xVariable)
        self.com_pathfinding.place(width=60, height=22, x=760, y=140)
        self.com_pathfinding["value"] = ("DFS", "BFS", "AStar")

        # 自动寻路
        self.generate_buttom = tk.Button(self.window, text="自动寻路", font=("宋体", 10), command=self.solve_map)
        self.generate_buttom.place(width=60, height=24, x=850, y=140)

        self.text_generate = tk.Text(self.window)
        self.text_generate.place(width=150, height=60, x=760, y=170)
        self.text_generate.config(state=tk.DISABLED)

        self.text_pathfinding = tk.Text(self.window)
        self.text_pathfinding.place(width=150, height=490, x=760, y=250)
        self.text_pathfinding.config(state=tk.DISABLED)

        self.maze = Generate.MazeMap()

        self.window.mainloop()
        
    def generate_map(self):
        global img
        x, y = int(self.text_x.get()), int(self.text_y.get())
        func = self.com_generate.get()
        self.maze.generate(func, (x, y))
        self.maze.init_maze()
        image = self.maze.get_figure()
        img = ImageTk.PhotoImage(image=image)
        self.canvas.create_image(360, 360, anchor='center', image=img)
        self.text_generate.config(state=tk.NORMAL)
        str = "通过%s算法生成模型\n迷宫大小:%4dx%4d\n花费时间:%7.5fs\n"%(func, x, y, self.maze.generate_time)
        self.text_generate.delete(1.0, "end")
        self.text_generate.insert(tk.END, str)
        self.text_generate.config(state=tk.DISABLED)

    def save_maze(self):
        path_save = filedialog.asksaveasfilename(
            defaultextension='保存地图模型',
            filetypes=[("npy文件", ".npy")]
        )
        self.maze.save_map(path_save)

    def load_maze(self):
        global img
        maze_path = filedialog.askopenfilename(filetypes=(("npy files","*.npy"), ))
        self.maze.load_map(maze_path)
        self.maze.init_maze()
        image = self.maze.get_figure()
        img = ImageTk.PhotoImage(image=image)
        self.canvas.create_image(360, 360, anchor='center', image=img)

    def solve_map(self):
        global img
        func = eval(self.com_pathfinding.get())(self.maze.get_map(), self.maze.start, self.maze.end)
        func.solve()
        image = func.get_figure()
        img = ImageTk.PhotoImage(image=image)
        self.canvas.create_image(360, 360, anchor='center', image=img)
        self.text_pathfinding.config(state=tk.NORMAL)
        str = func.get_info()
        self.text_pathfinding.delete(1.0, "end")
        self.text_pathfinding.insert(tk.END, str)
        self.text_pathfinding.config(state=tk.DISABLED)

    def dismantles_wall(self):
        global img
        wall = int(self.text_wall.get())
        self.maze.random_dismantles_wall(wall)
        self.maze.init_maze()
        image = self.maze.get_figure()
        img = ImageTk.PhotoImage(image=image)
        self.canvas.create_image(360, 360, anchor='center', image=img)

if __name__ == "__main__":
    ui = MazeUI()
