# WeiFonts 伪装字体工具
将字体转换为指定字体的代替字体。

## 使用图形界面
### 1. 给定字体
创建一个给定字体的代替字体。
> NOTE1: 关于 Windows 内置字体的选择，可通过“Windows 资源管理器”进入 C:\Windows\Fonts，找到所需字体，用鼠标将字体拖入本工具窗口“模板字体”中即可。  
> NOTE2: 如有行距问题，可禁用“计算度量值”选项。
### 2. Windows 中文字体
将字体转换为 Windows 内置中日韩字体，如雅黑、正黑、宋体、细明体等代替字体。此功能可生成 Windows 字体原本没有的字重。
> NOTE1: 目标为 `yugoth` 时，不建议使用 `"Semilight"` 和 `"SemiBold"`。  
> NOTE2: 如有行距问题，可禁用“计算度量值”选项。
### 3. 16 苹方字体
6 种粗细的苹方字体。
### 4. 字体格式工具
可以使用[字体格式工具](https://github.com/GuiWonder/FontFormattingTools)对 TTC 分解和组合，此工具也可用于 OTF 与 TTF 格式之间的转换。

## 使用命令行
使用命令行需要先安装 [FontTools](https://github.com/fonttools/fonttools) 和 [AFDKO](https://github.com/adobe-type-tools/afdko/)。
### 1. 给定字体
运行 `python weiwei.py -i InFont -m Model -o OutFont`。
- `-i` 输入字体(Input)。
- `-m` 模板字体(Model)。
- `-o` 输出字体(Output)。
- `-mt` 计算度量值(Metrics)，可选, 根据模板字体计算新的度量值。
### 2. Windows 中文字体
运行 `python weiwin.py -i InFont -tg Target -wt Weight -d OutDirectory -r`。
- `-i` 输入字体(Input)。
- `-tg` 目标字体(Target)，具体如下表。

  | tg | 目标字体 |
  | ---- | :---- |
  | msyh/yahei | 微软雅黑、微软雅黑 UI |
  | msjh/jhenghei | 微軟正黑體、微軟正黑體 UI |
  | mingliu | 細明體、新細明體、細明體_HKSCS |
  | simsun/songti | 宋体、新宋体 |
  | simsun/heiti | 黑体 |
  | deng/dengxian | 等线 |
  | msgothic | MS Gothic、MS UI Gothic、MS PGothic |
  | msmincho | MS Mincho、MS PMincho |
  | meiryo | Meiryo、Meiryo UI |
  | malgun | Malgun Gothic |
  | yugoth/yugothic | Yu Gothic、Yu Gothic UI |
  | yumin/yumincho | Yu Mincho |
  | batang/gungsuh | Batang、BatangChe、Gungsuh、GungsuhChe |
  | gulim/dotum | Gulim、GulimChe、Dotum、DotumChe |
  | allsans | 以上所有无衬线字体 |
  | allserif | 以上所有衬线字体 |
  | all | 以上所有字体 |

  | tg | 目标字体 |
  | ---- | :---- |
  | mingliub/mingliuextb | 細明體-ExtB、新細明體-ExtB、細明體_HKSCS-ExtB |
  | simsunb/simsunextb | 宋体-ExtB |
  | simsunextg/simsung | 宋体-ExtG |
  | kaiu/dfkai | 標楷體 |
  | simkai/kaiti | 楷体 |
  | simfang | 仿宋 |

- `-wt` 字重(Weight)，可选，可使用 `"Thin", "ExtraLight", "Light", "Semilight", "DemiLight", "Normal", "Regular", "Medium", "Demibold", "SemiBold", "Bold", "ExtraBold", "Heavy", "Black", "ExtraBlack"`。如未指定字重，程序会自动判断字重。
- `-it` 斜体(Italic)，可选，可使用 `-it y` 指定为斜体字体，`-it n` 指定为非斜体字体。如未指定，程序会使用输入字体的斜体属性。
- `-d` 字体保存目录(Output Directory)，可选，如未指定，则使用当前目录。
- `-mt` 计算度量值(Metrics)，可选。
- `-r` TTC 打包完成后移除 TTF，可选。
## 下载地址
可从 [Releases](https://github.com/GuiWonder/WeiFonts/releases) 页面下载。
## 鸣谢
- [FontTools](https://github.com/fonttools/fonttools)
- [AFDKO](https://github.com/adobe-type-tools/afdko)

