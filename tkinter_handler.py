import tkinter as tk

class BaseWindow(tk.Tk):
    """基础窗口类，封装通用窗口功能"""
    def __init__(self, width=400, height=50, x_offset=50, alpha=0.9):
        super().__init__()
        
        # 基础配置
        self.overrideredirect(True)    # 无边框
        self.attributes('-transparentcolor', 'black')  # 透明背景设置
        # self.config(bg='black', alpha=alpha)
        self.attributes('-alpha', 0.9)  # 整体透明度90%

        # 配置窗口背景为透明色
        self.config(bg='black')
        
        # 计算屏幕中心位置
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x = (self.screen_width - width) // 2
        self.y = 50
        
        # 动态布局
        self.geometry(f"{width}x{height}+{self.x}+{self.y}")

        self.attributes('-alpha', 0.9)  # 整体透明度90%
        
    def show(self, duration=1500):
        # 保持窗口置顶
        self.attributes('-topmost', True)
        # 自动关闭窗口
        self.after(duration, self.destroy) 
        # 启动主循环
        self.mainloop()
    
    def close_window(self):
        """立即关闭窗口并清除定时器"""
        if self.timer is not None:
            self.after_cancel(self.timer)
        self.destroy()

class MessageWindow(BaseWindow):
    """消息提示窗口类"""
    def __init__(self, message, 
                 width=400, height=200, 
                 x_offset=50, alpha=0.9, 
                 font=('Microsoft YaHei', 14), 
                 text_color='white'):
        super().__init__(width, height, x_offset, alpha)
        
        # 创建消息标签
        self.label = tk.Label(
            self,
            text=message,
            font=font,
            fg=text_color,
            bg='black',
            justify='center'
        )
        self.label.pack(expand=True)
        
    def show(self, duration=1500):
        super().show(duration)

class ShiningCircleWindow(BaseWindow):
    """闪烁动画窗口类"""
    def __init__(self, 
                 radius=20, 
                 initial_color='gold', 
                 blink_interval=500,
                 x_offset=50, alpha=0.9):
        super().__init__(width=50, height=50, x_offset=x_offset, alpha=alpha)
        
        # 创建画布
        self.canvas = tk.Canvas(self, width=50, height=50, bg='black', highlightthickness=0)
        self.canvas.pack()
        
        # 绘制初始圆
        self.circle = self.canvas.create_oval(10, 10, 40, 40, 
                                           fill=initial_color, 
                                           outline='goldenrod', 
                                           width=5)
        
        # 闪烁状态
        self.current_color = initial_color
        self.blink_timer = None
        
    def start_blinking(self):
        """启动闪烁动画"""
        def toggle_color():
            new_color = '#FFFF00' if self.current_color == 'gold' else 'gold'
            self.canvas.itemconfig(self.circle, fill=new_color)
            self.current_color = new_color
            self.blink_timer = self.after(500, toggle_color)
        
        self.blink_timer = self.after(0, toggle_color)  # 立即开始
    
    def show(self, duration=5000):
        super().show(duration)
        self.start_blinking()  # 启动动画
    
    def close_window(self):
        super().close_window()
        if self.blink_timer is not None:
            self.after_cancel(self.blink_timer)

# 使用示例
if __name__ == "__main__":
    # 显示消息窗口
    msg_window = MessageWindow("Hello World!")
    msg_window.show(3000)  # 显示3秒
    
    # 显示闪烁窗口
    flash_window = ShiningCircleWindow()
    flash_window.show(3000)  # 显示5秒