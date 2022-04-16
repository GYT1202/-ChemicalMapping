# Notepad Plus

##### 以文本编辑为主要操作方式的便携工具包。致力于解放双手，使用键盘优雅而高效地工作

#### 程序包列表

- Basic Package 提供基础功能

- Chemical Mapping 帮助理解物质间转化反应关系
- Learn Words Better 将英文短语嵌入合适的语境并输出打印文档

## Basic Package

- 使用<kbd>Ctrl</kbd>+<kbd>滚轮</kbd>缩放字体
- 使用`:font 字体文件名 标题字体文件名`命令设置打印字体,默认使用系统目录下字体
- 每**10分钟**自动保存为文本文档（.\日期.txt）
- 正常退出自动保存文档

## Chemical Mapping

可以将化学方程式配平并转化为结构思维导图的程序

#### 生成xmind思维导图

- 请在每一行内填充一个化学方程式

  （例如：`CaCO3+HCl=CaCl2+H2O+CO2`，不能存在：空格，催化剂（暂不支持），沉淀/气体符号（暂不支持），更多见[bce维基](https://github.com/bce-toolkit/bce/wiki) [关于你如何输入化学方程式（语法细节）](https://github.com/bce-toolkit/bce/wiki/Syntax)）

- 使用<kbd>toXmind</kbd>命令解析上文输入的所有方程式解析，可加位置参数：

  - Object 从什么物质开始递归

  - Depth 递归深度（default:10）

  - filename 生成xmind文件的路径（default:result.xmind）

    eg: `toXmind H2O 2 result.xmind`

    以H2O为中心，与H2O有关的反应以及和这些反应中物质有关的反应，保存在该目录下result.xmind文件内

- 使用 Xmind 8 打开生成的文件（警告：使用 Xmind 2020+ 将无法打开生成的文档）[官网](https://www.xmind.cn/xmind8-pro/)
- 作为中间文件，将生成save.json

## Learn Words Better

- 输入一个单词或一个短语，按<kbd>Shift</kbd>+<kbd>Enter</kbd>打开搜索框（从百度翻译获取句源，包含牛津，柯林斯，英英，双语等句源）

- 搜索框中使用<kbd>↑↓</kbd>键可选择，或在用<kbd>滚轮</kbd>选择

- 点击下拉框里的选项，或<kbd>Enter</kbd>选定选项，下拉框关闭后，再次按<kbd>Enter</kbd>将句子格式化到文档，使用<kbd>Shift</kbd>+<kbd>Enter</kbd>则将翻译也带上

- 使用三个**英文**句点和**空格**隔开)表达sth / sb

  eg:`not only ... but`

- 一行的开头使用`$`表示此行为大标题，eg:`$Group 1`，`#`表示以下内容为一个新单词，eg:`#good`，也可以使用`#好的;优质的;____`，没有做中文翻译的部分

- `c`命令生成文档的打印版，添加`-mixed`参数打乱生成顺序
