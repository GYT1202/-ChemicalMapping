# Notepad Plus

以文本编辑为主要操作方式的便携工具包。

#### 基本用法

输入文本，使用命令操作(一行识别为一个命令)

#### 程序包列表

- Chemical Mapping 帮助理解物质间转化反应关系
- Learn Words Better 将英文短语嵌入合适的语境并输出打印文档

## Chemical Mapping

可以将化学方程式配平并转化为结构思维导图的程序

#### 生成xmind思维导图

- 请在每一行内填充一个化学方程式

  （例如：”CaCO3+HCl=CaCl2+H2O+CO2“，不能存在：空格，催化剂（暂不支持），沉淀/气体符号（暂不支持），更多见[bce维基](https://github.com/bce-toolkit/bce/wiki) [关于你如何输入化学方程式（语法细节）](https://github.com/bce-toolkit/bce/wiki/Syntax)）

- 使用<kbd>toXmind</kbd>命令解析上文输入的所有方程式解析，可加位置参数：

  - Object 从什么物质开始递归

  - Depth 递归深度（default:10）

  - filename 生成xmind文件的路径（default:result.xmind）

    eg: toXmind H2O 2 result.xmind

    以H2O为中心，与H2O有关的反应以及和这些反应中物质有关的反应，保存在该目录下result.xmind文件内

- 使用 Xmind 8 打开生成的文件（警告：使用 Xmind 2020+ 将无法打开生成的文档）[官网](https://www.xmind.cn/xmind8-pro/)
- 
