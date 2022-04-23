# Notepad Plus

##### 以文本编辑为主要操作方式的轻量工具包。致力于解放双手，使用键盘优雅而高效地工作

打包程序[【网盘链接】](https://pan.baidu.com/s/1TFbpujlFenKuSHdodM0xWA?pwd=ia3h)（说明：如果不需要quichem，只下载一个exe文件即可运行）

时间碎，程序也碎，修修补补凑合吧，有时间会重构

很多技巧对新手有些蹩脚~~就像在玩Dwarf Fortress~~，但适应了速度就会很快了

#### 程序包列表

- Basic Package 提供基础功能

- Chemical Mapping 帮助理解物质间转化反应关系
- Learn Words Better 将英文短语嵌入合适的语境并输出打印文档
- Baidu Translator 用于获取百度翻译，为Learn Words Better提供前置基础

## Basic Package

- 使用<kbd>Ctrl</kbd>+<kbd>滚轮</kbd>缩放字体

- 使用`:font 字体文件名 标题字体文件名`命令设置打印字体,默认使用系统目录下字体

- 每**10分钟**自动保存为文本文档（.\日期.txt）

- **正常退出**自动保存文档

- 启动自动读取今日文档

- 使用`r`命令读取文件

  eg:

  - `read`读取今日编辑文档

  - `read C:\Users\Lenovo\Desktop\timeMaster.py` 读取绝对路径下的文件

- 使用`-`代表注释掉这一行

## Chemical Mapping

可以将化学方程式配平并转化为结构思维导图的程序

#### 关于化学方程式的输入和解析

- 直接使用了开源项目[quichem](https://github.com/spamalot/quichem)
  - 一个**很棒**的化学方程式解析器，在输入方程式的时候**除了字母数字符号键以外，不使用任何修饰键（shift等）或鼠标点击**
  - 可以到[这里](https://github.com/spamalot/quichem/releases)下载，到[这里](https://cdn.rawgit.com/spamalot/quichem/263b840dbba5892106650a6fb93efed1749a900c/userguide/USERGUIDE.html)查看它的用户文档（如果不能访问文档页面，可以下载源码里的 [UserGuide](https://github.com/spamalot/quichem/tree/master/userguide)）
  - **或许你想了解它的[构词法](https://github.com/spamalot/quichem/blob/master/SYNTAX.rst)，让敲方程式速度快到起飞**
  - 已经将其嵌入到程序中
    - 可以看到程序目录里**直接包含了quichem的程序包**，如果不需要使用该包，可下载单个exe文件
    - 使用<kbd>Ctrl</kbd>+<kbd>q</kbd>启动独立进程（注意：它使用pyside(qt4)/wx框架，所以使用时主程序**无法响应**）
    - 快速输入程序中使用它快速输入和解析方程式，并将结果传给bce解析配平

- **快速输入程序**
  - 使用<kbd>Ctrl</kbd>+<kbd>Q</kbd>快速启动
  - 输入方程式，可以不配平，可以**按照quichem的规则**全部小写，具体见[这里](https://github.com/spamalot/quichem/blob/master/SYNTAX.rst)
- ~~使用一个原始输入文件作为方程式列表~~：-该部分待设计
  - 使用`cdb 数据库名称`(create database)创建一个方程式列表（将直接使用json存在./database/chemical mapping）
  - 使用<kbd>Ctrl</kbd>+<kbd>Enter</kbd>直接输入方程式（行末空格指定数据库）
- 作为中间文件，将生成save.json，存储了每种物质存在的转化关系
- ~~使用`upload`将本地文件同步到云~~（实现方向：heroku服务器）

#### 生成xmind思维导图

- 请在每一行内填充一个化学方程式

  （例如：`CaCO3+HCl=CaCl2+H2O+CO2`，不能存在：空格，催化剂（暂不支持），沉淀/气体符号（暂不支持），更多见[bce维基](https://github.com/bce-toolkit/bce/wiki) [关于你如何输入化学方程式（语法细节）](https://github.com/bce-toolkit/bce/wiki/Syntax)）

- 使用<kbd>toXmind</kbd>命令解析上文输入的所有方程式解析，可加位置参数：

  - Object 从什么物质开始递归

  - Depth 递归深度（default:10）

  - filename 生成xmind文件的路径（default:result.xmind）

  - except 除了什么物质（用空格分隔）

    eg: `toXmind H2O 2 result.xmind Fe2O3 H2CO3`

    以H2O为**中心**，找到相关反应物，然后再从每个反应物开始递归，其中将排除Fe2O3和H2CO3，保存在该目录下result.xmind文件内

- 使用 Xmind 8 打开生成的文件（**警告：使用 Xmind 2020+ 将无法打开生成的文档**）[官网](https://www.xmind.cn/xmind8-pro/)

- Xmind用的java，渲染跟不上可能会卡，可以导出为mindmaster等其他导图软件

#### 导图排列

- 使用`:mod`命令切换

  - 格式：`:mod [mod(randomJump, radio)] param1 param2...`

- ~~**方案一 Random Jump**~~

  - 实现

    如果文字存在重叠（距离过小），将浮动主题随机跳跃一段距离

  - 参数

    - jumpDistanceLimit 跳跃距离极限（real_dis^2，控制图表的**疏密程度**）default=100000
    - jumpDistanceMax 最远跳跃限制（更近的跳跃意味着更多的跳跃次数，**更多性能开销**，但也意味着**更紧凑的图表**）default=1000
    - jumpDistanceMin 最近跳跃限制 default=100

  - 评价

    简单粗暴，效果欠佳

  - 优化方向

    - 避免主题跳跃过远
    - 避免页面杂乱性

- 方案二**Radio**

  - 实现

    从root开始，呈放射树状生成

  - 参数

    - shootDistance（发散距离，default=-1，意味着随机值）
    - shootMax，shootMin 当shootDistance==-1时启用
    - shootAngle 发散角，默认为平均发散——不可设置
    - depthTimes 递归深度间的倍数关系default=2

  - 优化方向

    - 直接相邻但已经生成的topic

- 方案三**ShootJump**

#### 例子

- input:

  ![image-20220423145531209](https://github.com/GuoYangtuo/Notepad-Plus/tree/main/pngs/image-20220423145531209.png)

- output:

  ![Fe2O3](https://github.com/GuoYangtuo/Notepad-Plus/tree/main/pngs/Fe2O3.png)

- input:

  ```
  toXmind H2O
  ```

- output:

  ![H2O](https://github.com/GuoYangtuo/Notepad-Plus/tree/main/pngs/H2O.png)

## Baidu Translator

- 很简单实用~~抄的~~，直接translate方法获取json格式的返回值
- 可能会因为*一些原因*导致异常
- 原文找不到了，只从以前的代码里扒出来这样一个类封装

## Learn Words Better

#### 	句子搜索

- 输入一个单词或一个短语，按<kbd>Shift</kbd>+<kbd>Enter</kbd>打开搜索框（从百度翻译获取句源，包含牛津，柯林斯，英英，双语等句源）

- 搜索框中使用<kbd>↑↓</kbd>键可选择，或在用<kbd>滚轮</kbd>选择

- 点击下拉框里的选项，或<kbd>Enter</kbd>选定选项，下拉框关闭后，再次按<kbd>Enter</kbd>将句子格式化到文档，使用<kbd>Shift</kbd>+<kbd>Enter</kbd>则将翻译也带上

- 使用三个**英文**句点和**空格**隔开)表达sth / sb

  eg:`not only ... but`

  #### 打印档生成

- 一行的开头使用`$`表示此行为大标题，eg:`$Group 1`，`#`表示以下内容为一个新单词，eg:`#good`，也可以使用`#好的;优质的;____`，没有做中文翻译的部分

- `c`命令生成文档的打印版，添加`-mixed`参数打乱生成顺序

## 关于打包

- 修改spec文件，开头使用

  ```
  import sys
  sys.setrecursionlimit(2000)
  ```

- 在spec的datas里包含quichem程序包的路径

## 未处理的需求

- **警告：没有做容错系统，请按照以上规则操作**

- 沉淀，气体，催化剂
- 云档
- 相互反应物质线条重叠问题
- 导图主题位置排列问题
