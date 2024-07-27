# WeiFonts 伪装字体工具
将字体转换为指定字体的代替字体。

## 使用图形界面
### 1. 给定字体
创建一个给定字体的代替字体。
### 2. Windows 中文字体
将字体转换为 Windows 内置 CJK 字体，如雅黑、正黑、宋体、细明体等代替字体。可使用多种字重。
> NOTE: 目标为 `yugoth` 时，不建议使用 `"Semilight"` 和 `"SemiBold"`。
### 3. 16 苹方字体
6 种粗细的苹方字体。
### 4. 字体格式工具
基于 [AFDKO](https://github.com/adobe-type-tools/afdko/)，可以使用此工具对 TTC 分解和组合。

## 使用命令行
### 1. 给定字体
运行 `python weiwei.py -i InFont -m Model -o OutFont`。
- `-i` 输入字体(Input)。
- `-m` 模板字体(Model)。
- `-o` 输出字体(Output)。
### 2. Windows 中文字体
运行 `python weiwin.py -i InFont -tg Target -wt Weight -d OutDirectory -r`。
- `-i` 输入字体(Input)。
- `-tg` 目标字体(Target)，具体如下表。

  | tg | 目标字体 |
  | ---- | :---- |
  | msyh   | 微软雅黑、微软雅黑 UI |
  | msjh   | 微軟正黑體、微軟正黑體 UI |
  | mingliu | 細明體、新細明體、細明體_HKSCS |
  | simsun  | 宋体、新宋体 |
  | simsun  | 黑体 |
  | msgothic | MS Gothic、MS UI Gothic、MS PGothic |
  | msmincho | MS Mincho、MS PMincho |
  | meiryo  | Meiryo、Meiryo UI |
  | malgun  | Malgun Gothic |
  | yugoth  | Yu Gothic、Yu Gothic UI |
  | yumin  | Yu Mincho |
  | batang  | Batang、BatangChe、Gungsuh、GungsuhChe |
  | gulim  | Gulim、GulimChe、Dotum、DotumChe |
  | allsans  | 以上所有无衬线字体 |
  | allserif  | 以上所有衬线字体 |
  | all  | 以上所有字体 |

  | tg | 目标字体 |
  | ---- | :---- |
  | mingliub   | 細明體-ExtB、新細明體-ExtB、細明體_HKSCS-ExtB |
  | simsunb   | 宋体-ExtB |

- `-wt` 字重(Weight)，可选，可使用 `"Thin", "ExtraLight", "Light", "Semilight", "DemiLight", "Normal", "Regular", "Medium", "Demibold", "SemiBold", "Bold", "Black", "Heavy"`。如未指定字重，程序会自动判断字重。
- `-it` 斜体(Italic)，可选，可使用 `-it y` 指定为斜体字体，`-it n` 指定为非斜体字体。如未指定，程序会使用输入字体的斜体属性。
- `-d` 字体保存目录(Output Directory)，可选，如未指定，则使用当前目录。
- `-r` TTC 打包完成后移除 TTF，可选。

## 鸣谢
- [FontTools](https://github.com/fonttools/fonttools)
- [AFDKO](https://github.com/adobe-type-tools/afdko/)
- [otfcc](https://github.com/caryll/otfcc)

