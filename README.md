# 创建 Windows 中文字体代替字体
将字体转换为 Windows 雅黑、正黑、宋体的代替字体。
## 使用方法
程序可支持 8 种字重 "ExtraLight", "Light", "Normal", "Regular", "Medium", "SemiBold", "Bold", "Heavy"
#### 1. 字体名称（指内部名称，下同）中包含“Sans”或“Serif”
运行 `python winfont.py XX.otf` </br>
程序会自动判断字重根据字体名称在当前目录生成 msyhXX.otf msyhXXui.otf msyhXX.ttc msjhXX.otf msjhXXui.otf msjhXX.ttc 或 simsunXX.otf nsimsunXX.otf simsunXX.ttc
#### 2. 字体名称中不包含“Sans”或“Serif”，或强制指定“Sans”或“Serif”
运行 `python winfont.py XX.otf Sans` 或 `python winfont.py XX.otf Serif` 程序会自动判断字重
#### 3. 程序无法判断字重，或强制指定字重
黑体运行 `python winfont.py XX.otf Sans Regular` 其中 "Regular" 可以是 "ExtraLight", "Light", "Normal", "Regular", "Medium", "SemiBold", "Bold", "Heavy"。
