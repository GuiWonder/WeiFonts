# 创建 Windows 中文字体代替字体
将字体转换为 Windows 雅黑、正黑、宋体的代替字体。
## 使用方法
#### 1. 思源类似字体，名称（指内部名称，下同）为 XXSans-Regular.otf，XXSerif-Regular.otf 类似名称
运行 `python winfont.py XX.otf` </br>
程序会自动根据字体名称在当前目录生成 msyhXX.otf msyhXXui.otf msyhXX.ttc msjhXX.otf msjhXXui.otf msjhXX.ttc 或 simsun.otf nsimsun.otf simsun.ttc
#### 2. 字体名称为 XX-Regular.otf类似名称
运行 `python winfont.py XX.otf Sans` 或 `python winfont.py XX.otf Serif`
#### 3. 其他无规则字体名称
黑体运行 `python winfont.py XX.otf Sans Regular` 其中 Regular 可以是 "Regular", "Bold", "Light", "ExtraLight","Heavy"
