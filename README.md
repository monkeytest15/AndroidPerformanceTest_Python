AndroidPermanceTest_Python
==========================
环境准备： 
> 1.本地还是需要有android sdk环境。至少adb能够使用
> 2.本地需要安装python2.x版本

使用教程：
> 1. git clone项目到本地
> 2. 电脑链接机器，adb识别出来机器
> 3. 打开终端，并且输入python Test_File.py <package name> <time(hour)>
> 4. 然后就进行测试
> 5. 测试结束之后，可以等设置的时间到了，也可以切换到终端，然后Ctrl+C，终止程序


> 这样就会在目录下生成三个统计并分析的GC pdf图标报告，本周后续再加上流量和cpu两个。这样这个工具就可以对任何app应用做性能测试了。