import Generate
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from tkinter import filedialog
from solve import DFS, BFS, AStar
"""
导入了4个模块：
Generate.py: 迷宫生成、导入、保存

solve.py: 求解迷宫

tkinter: 图形化界面设计
    ttk: 界面
    filedialog: 对话框

PIL(pillow): 图像处理
    ImageTk: 创捷和生成图像
"""
class MazeUI: #迷宫界面设计类
    def __init__(self) -> None:
        # 窗口和画布
        self.window = tk.Tk()
        self.window.title('迷宫生成与破解')
        self.window.geometry('925x760')
        self.window.resizable(0, 0)
        self.window.iconbitmap('ico.ico')
        self.canvas = tk.Canvas(self.window, width=720, height=720, bg='black')
        self.canvas.place(width=720, height=720, x=20, y=20)
        """
        新建了MazeUI的两个属性：
        self.window
            为一个窗口
            窗口标题为'迷宫生成与破解'
            窗口大小为935*760
            禁用了改变窗口大小
            窗口图标为'ico.ico'  
        self.acnvas
            为窗口self.window中的一个画布，宽720，高720，背景为黑色
            画布位于(20,20)
        """

        # 迷宫的宽（标签和输入框）
        self.label_x = tk.Label(self.window, text="x:", font=("宋体", 12))
        self.label_x.place(width=20, height=20, x=740, y=20)
        self.text_x = tk.Entry(self.window)
        self.text_x.place(width=60, height=20, x=760, y=22)
        """
        新建了MazeUI的两个属性
        self.label_x
            为窗口self.window中的一个标签，标签内容为"x:",字体为宋体，大小为12
            标签宽20、高20，位于(740,20)
        self.text_x
            为窗口self.window中的一个输入框
            标签宽60、高20，位于(760,22)            
        """

        # 迷宫的高（标签和输入框）
        self.label_y = tk.Label(self.window, text="y:", font=("宋体", 12))
        self.label_y.place(width=20, height=20, x=830, y=20)
        self.text_y = tk.Entry(self.window)
        self.text_y.place(width=60, height=20, x=850, y=22)
        """
        新建了MazeUI的两个属性
        self.label_y
            为窗口self.window中的一个标签，标签内容为"y:",字体为宋体，大小为12
            标签宽20、高20，位于(830,20)
        self.text_y
            为窗口self.window中的一个输入框
            输入框宽60、高20，位于(850,22)
        """

        # 生成迷宫（下拉框和按钮）
        xVariable = tk.StringVar()
        self.com_generate = ttk.Combobox(self.window, textvariable=xVariable)
        self.com_generate.place(width=60, height=22, x=760, y=52)
        self.com_generate["value"] = ("DFS", "PRIM")
        self.generate_buttom = tk.Button(self.window, text="生成迷宫", font=("宋体", 10), command=self.generate_map)
        self.generate_buttom.place(width=60, height=24, x=850, y=50)
        """
        新建了一个变量
        xVarialbe
            为一个StringVar类型的变量(多行文本)

        新建了MazeUI的两个属性
        self.com_generate
            为窗口self.window中的一个下拉框，下拉框内容属性为xVarialbe变量的类型
            输入框宽60、高22，位于(760,52)      
            下拉框选项为"DFS", "PRIM"  
        self.generate_buttom
            为窗口self.window中的一个按钮，按钮内容为"生成迷宫"，字体为宋体，大小为10，按后执行generate_map()行为（生成迷宫，在下面）
            标签60、高24，位于(850,50)                  
        """

        # 拆墙（输入框和按钮）
        self.text_wall = tk.Entry(self.window)
        self.text_wall.place(width=60, height=20, x=760, y=82)
        self.wall_buttom = tk.Button(self.window, text="拆墙", font=("宋体", 10), command=self.dismantles_wall)
        self.wall_buttom.place(width=60, height=24, x=850, y=80)
        """
        新建了MazeUI的两个属性
        self.text_wall
            为窗口self.window中的一个输入框
            输入框宽60、高20，位于(760,82)
        self.wall_buttom
            为窗口self.window中的一个按钮，按钮内容为"拆墙"，字体为宋体，大小为10，按后执行dismantles_wall()行为（拆墙，在下面）
            标签60、高24，位于(850,80)
        """

        # 加载迷宫（按钮）
        self.generate_buttom = tk.Button(self.window, text="加载迷宫", font=("宋体", 10), command=self.load_maze)
        self.generate_buttom.place(width=60, height=24, x=760, y=110)
        """
        修改了属性self.generate_buttom
            为窗口self.window中的一个按钮，按钮内容改为"加载迷宫"，字体为宋体，大小为10，按后改为执行load_maze()行为（加载迷宫，在下面）
            标签60、高24，位于(760,110)
        """

        # 保存迷宫（按钮）
        self.generate_buttom = tk.Button(self.window, text="保存迷宫", font=("宋体", 10), command=self.save_maze)
        self.generate_buttom.place(width=60, height=24, x=850, y=110)
        """
        修改了属性self.generate_buttom
            为窗口self.window中的一个按钮，按钮内容改为"加载迷宫"，字体为宋体，大小为10，按后改为执行load_maze()行为（保存迷宫，在下面）
            标签60、高24，位于(760,110)
        """

        # 自动寻路（下拉框和按钮）
        xVariable = tk.StringVar()
        self.com_pathfinding = ttk.Combobox(self.window, textvariable=xVariable)
        self.com_pathfinding.place(width=60, height=22, x=760, y=140)
        self.com_pathfinding["value"] = ("DFS", "BFS", "AStar")
        self.generate_buttom = tk.Button(self.window, text="自动寻路", font=("宋体", 10), command=self.solve_map)
        self.generate_buttom.place(width=60, height=24, x=850, y=140)        
        """
        再次定义xVarialbe  
            为一个StringVar类型的变量(多行文本)

        修改了两个属性
        self.com_generate
            为窗口self.window中的一个下拉框，下拉框内容属性为xVarialbe变量的类型
            输入框宽60、高22，位置改为(760,140)      
            下拉框选项为"DFS", "BFS", "AStar" 
        self.generate_buttom
            为窗口self.window中的一个按钮，按钮内容改为"自动寻路"，字体为宋体，大小为10，按后改为执行solve_map()行为（自动寻路，在下面）
            按钮宽60、高24，位于(850,140)                  
        """

        # 文本（多行输入框）
        self.text_generate = tk.Text(self.window)
        self.text_generate.place(width=150, height=60, x=760, y=170)
        self.text_generate.config(state=tk.DISABLED)
        self.text_pathfinding = tk.Text(self.window)
        self.text_pathfinding.place(width=150, height=490, x=760, y=250)
        self.text_pathfinding.config(state=tk.DISABLED)
        """
        新建了MazeUI的三个属性
        self.text_generate
            为窗口self.window中的一个多行输入框
            文本框宽150、高60，位于(760,170)
            禁止输入
        self.text_pathfinding
            为窗口self.window中的一个多行输入框
            文本框宽60、高490，位于(760,250)
        """

        self.maze = Generate.MazeMap()
        self.window.mainloop()
        """
        根据MazeMap类创建的一个实例self.maze

        使窗口可持续刷新，一直显示
        """

    def generate_map(self):# 生成迷宫行为
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
    """
    新建了一个全局变量img

    新建了三个变量x, y, func
        通过get()方法，将从输入框self.text_x获取的值转换成整数，再传给变量x
        通过get()方法，将从输入框self.text_y获取的值转换成整数，再传给变量y
        通过get()方法，将从下拉框self.com_generate选择的值再传给变量func
    属性self.maze执行generate()行为（生成，Generate.py中的MazeMap类，fun -> generate,(x, y) -> size）
    
    属性self.maze执行init_maze()行为（初始化起点终点，Generate.py中的MazeMap类，无参数）
    新建了变量image，为一张图片，为get_figure()行为（转图片，Generate.py中的MazeMap类，无参数）的返回值
    修改了变量img，将图片image导入img
    修改了属性self.canvas，在画布canvas中插入了一张图片img， 图片中心位于画布(360, 360)处

    新建了一个变量str为一个字符串，内容略
    修改了属性self.text_generate，
        允许输入
        清除多行输入框里的内容   
        在输入框的内容末尾插入字符串str
        禁止输入
    """

    def save_maze(self):# 保存迷宫行为
        path_save = filedialog.asksaveasfilename(
            initialfile='保存迷宫模型',
            filetypes=[("npy文件", ".npy")]
        )
        self.maze.save_map(path_save)
    """
    新建了一个变量path_save
        为filedialog.asksaveasfilename()函数（文件保存对话框）返回的文件名，文件名默认是"保存迷宫模型"，文件类型为npy文件
        
    属性self.maze执行save_map()行为
        save_map()（保存，Generate.py中的MazeMap类，path_save -> save_path）
        
    """

    def load_maze(self):# 加载迷宫行为
        global img
        maze_path = filedialog.askopenfilename(filetypes=(("npy files","*.npy"), ))
        self.maze.load_map(maze_path)

        self.maze.init_maze()
        image = self.maze.get_figure()
        img = ImageTk.PhotoImage(image=image)
        self.canvas.create_image(360, 360, anchor='center', image=img)
    """
    再次声明img为全局变量

    新建了一个变量maze_path
        为filedialog.askopenfilename()函数（文件打开对话框）返回的路径，文件类型为npy文件
    属性self.maze执行load_map()行为（打开，Generate.py中的MazeMap类，maze_path -> path）

    属性self.maze执行init_maze()行为（初始化起点终点，Generate.py中的MazeMap类，无参数）
    修改了变量image，为一张图片，为get_figure()行为（转图片，Generate.py中的MazeMap类，无参数）的返回值
    修改了变量img，将图片image导入img
    修改了属性self.canvas，在画布canvas中插入了一张图片img， 图片中心位于画布(360, 360)处
    """

    def solve_map(self):# 自动寻路行为
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
    """
    再次声明img为全局变量

    eval(self.com_pathfinding.get())（通过eval()函数把从下拉框self.com_pathfinding选择的字符串转换成可调用的对象）
    根据 eval(self.com_pathfinding.get())类创建了一个实例func
    func执行solve()行为（求解，slove.py中的eval(self.com_pathfinding.get())类，无参数）

    属性self.maze执行init_maze()行为（初始化起点终点，Generate.py中的MazeMap类，无参数）
    修改了变量image，为一张图片，为get_figure()行为（转图片，Generate.py中的MazeMap类，无参数）的返回值
    修改了变量img，将图片image导入img
    修改了属性self.canvas，在画布canvas中插入了一张图片img， 图片中心位于画布(360, 360)处

    新建了一个变量str为一个字符串，内容为func执行get_info()行为的返回值
    （整理文本，slove.py中的eval(self.com_pathfinding.get())类，无参数）
    修改了属性text_pathfinding，
        允许输入
        清除多行输入框里的内容
        在输入框的内容末尾插入字符串str
        禁止输入
    """

    def dismantles_wall(self):# 拆墙行为
        global img
        wall = int(self.text_wall.get())
        self.maze.random_dismantles_wall(wall)

        self.maze.init_maze()
        image = self.maze.get_figure()
        img = ImageTk.PhotoImage(image=image)
        self.canvas.create_image(360, 360, anchor='center', image=img)
    """
    再次声明img为全局变量

    通过get()方法，将从输入框text_wall获取的值传给变量wall
    属性self.maze执行random_dismantles_wall()行为（拆墙，Generate.py中的MazeMap类，wall -> n）

    属性self.maze执行init_maze()行为（初始化起点终点，Generate.py中的MazeMap类，无参数）
    修改了变量image，为一张图片，为get_figure()行为（转图片，Generate.py中的MazeMap类，无参数）的返回值
    修改了变量img，将图片image导入img
    修改了属性self.canvas，在画布canvas中插入了一张图片img， 图片中心位于画布(360, 360)处
    """

if __name__ == "__main__":# 程序入口
    ui = MazeUI()# 根据MazeUI类创建的一个实例
