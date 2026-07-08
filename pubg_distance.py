import keyboard
import json
import os
import math
import ctypes
import ctypes.wintypes
import subprocess

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

MAP_NAMES = ["艾伦格", "米拉玛", "萨诺", "维寒迪", "荣都", "帝斯顿", "泰戈", "利维克", "卡拉金"]
CALIBRATE_DISTANCE = 1000

class PUBGDistanceTool:
    def __init__(self):
        self.points = []
        self.mode = "calibrate"
        self.load_config()
        
        self.setup_hotkeys()
        self.print_help()
        
        keyboard.wait('ctrl+q')
        self.cleanup()
        print("\n程序已退出")
        os._exit(0)
    
    def print_help(self):
        print("=" * 50)
        print("PUBG 距离测量工具 已启动")
        print("=" * 50)
        print("操作说明:")
        print("  Ctrl + Shift + C -> 校准当前地图")
        print("  T键              -> 标记点位(点两次)")
        print("  Ctrl + 1~9       -> 切换地图")
        print("  Ctrl + Q         -> 退出程序")
        print("=" * 50)
        self.print_map_status()
    
    def print_map_status(self):
        current = MAP_NAMES[self.current_map]
        pixels = self.maps.get(self.current_map)
        if pixels:
            print(f"当前地图: {current} | 已校准: {CALIBRATE_DISTANCE}米 = {pixels:.1f} 像素")
            self.mode = "measure"
        else:
            print(f"当前地图: {current} | 未校准 - 请按 Ctrl+Shift+C 校准")
        print("=" * 50)
    
    def load_config(self):
        self.current_map = 0
        self.maps = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.current_map = data.get("current_map", 0)
                    self.maps = data.get("maps", {})
                    return
            except:
                pass
    
    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"current_map": self.current_map, "maps": self.maps}, f)
    
    def setup_hotkeys(self):
        keyboard.add_hotkey('ctrl+shift+c', self.start_calibrate)
        keyboard.add_hotkey('t', self.on_t_press)
        for i in range(1, 10):
            keyboard.add_hotkey(f'ctrl+{i}', lambda idx=i-1: self.switch_map(idx))
    
    def get_cursor_pos(self):
        point = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
        return point.x, point.y
    
    def switch_map(self, idx):
        if 0 <= idx < len(MAP_NAMES):
            self.current_map = idx
            self.save_config()
            name = MAP_NAMES[idx]
            print(f"\n[切换地图] {name}")
            self.speak_async(name)
            self.print_map_status()
            self.points = []
    
    def on_t_press(self):
        x, y = self.get_cursor_pos()
        self.points.append((x, y))
        self.flash_screen(x, y)
        
        if self.mode == "calibrate":
            print(f"  校准点{len(self.points)}: ({x}, {y})")
            if len(self.points) == 2:
                self.finish_calibrate()
        else:
            print(f"  点{len(self.points)}: ({x}, {y})")
            if len(self.points) == 2:
                self.calculate_distance()
    
    def start_calibrate(self):
        self.mode = "calibrate"
        self.points = []
        name = MAP_NAMES[self.current_map]
        print(f"\n[校准模式] {name} - 请按T键标记两个相距{CALIBRATE_DISTANCE}米的点")
    
    def finish_calibrate(self):
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        pixels_per_ref = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
        self.maps[str(self.current_map)] = pixels_per_ref
        self.save_config()
        
        name = MAP_NAMES[self.current_map]
        print(f"\n[校准完成] {name}: {CALIBRATE_DISTANCE}米 = {pixels_per_ref:.1f} 像素")
        print("现在可以直接按T键两次测量距离了\n")
        self.speak_async("校准完成")
        
        self.mode = "measure"
        self.points = []
    
    def calculate_distance(self):
        pixels_per_ref = self.maps.get(str(self.current_map))
        if len(self.points) < 2 or not pixels_per_ref:
            self.points = []
            return
        
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        pixel_distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        meters = (pixel_distance / pixels_per_ref) * CALIBRATE_DISTANCE
        
        name = MAP_NAMES[self.current_map]
        print(f"\n  [{name}] 距离: {meters:.1f} 米")
        self.speak_async(f"{name} 距离 {meters:.0f} 米")
        self.points = []
    
    def speak_async(self, text):
        ps_cmd = f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text}")'
        subprocess.Popen(['powershell', '-Command', ps_cmd], 
                        creationflags=0x08000000)
    
    def flash_screen(self, x, y):
        try:
            from tkinter import Tk, Canvas, BOTH
            root = Tk()
            root.overrideredirect(True)
            root.attributes('-topmost', True)
            root.attributes('-alpha', 0.7)
            root.geometry(f"20x20+{x-10}+{y-10}")
            root.configure(bg='red')
            
            c = Canvas(root, bg='red', highlightthickness=0)
            c.pack(fill=BOTH, expand=True)
            c.create_oval(3, 3, 17, 17, fill='yellow', outline='red')
            
            root.after(300, root.destroy)
            root.mainloop()
        except:
            pass
    
    def cleanup(self):
        keyboard.unhook_all()

if __name__ == "__main__":
    app = PUBGDistanceTool()
