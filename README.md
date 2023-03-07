# 创建 Windows 中文字体代替字体
将字体转换为 Windows 雅黑、正黑、宋体、细明体等代替字体。
## 使用方法
### 1. 使用图形界面
可从 [Releases](https://github.com/GuiWonder/toWinFonts/releases) 页面下载应用包。
### 2. 使用命令行
运行 `python winfont.py -i InFont -tg Target -wt Weight -d OutDirectory`。
- `-i` 输入字体(Input)。
- `-tg` 目标字体(Target)，具体如下表。

  | tg | 目标字体 |
  | ---- | :---- |
  | msyh   | 微软雅黑、微软雅黑 UI |
  | msjh   | 微軟正黑體、微軟正黑體 UI |
  | mingliu | 細明體、新細明體、細明體_HKSCS |
  | simsun  | 宋体、新宋体 |
  | yugoth  | Yu Gothic、Yu Gothic UI |
  | msgothic | MS Gothic、MS UI Gothic、MS PGothic |
  | malgun  | Malgun Gothic |
  | msmincho | MS Mincho、MS PMincho |
  | meiryo  | Meiryo、Meiryo UI |
  | batang  | Batang、BatangChe、Gungsuh、GungsuhChe |
- `-wt` 字重(Weight)，可使用 `"ExtraLight", "Light", "Semilight", "Normal", "Regular", "Medium", "SemiBold", "Bold", "Heavy"`。如未指定字重，程序会自动判断字重。
- `-d` 字体保存目录(Output Directory)，如未指定，则使用当前目录。

> NOTE: 目标为 `yugoth` 时，不建议使用 `"Semilight"` 和 `"SemiBold"`。
