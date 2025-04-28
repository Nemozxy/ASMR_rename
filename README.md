# ASMR_rename
一个由Deepseek-R1生成的Python脚本，用于将命名为RJ号的文件夹重命名为“RJ号+项目名称”  
只会修改一级目录下的文件夹名。默认不开启无头模式、开启无图模式  
  
使用说明：  
安装依赖：pip install selenium webdriver-manager  
运行示例：python rename_folders.py "D:\ASMR目录"  

功能说明：  
自动处理页面跳转，支持两种URL格式  
使用显式等待确保元素加载  
提供浏览器模式选项：  
--headless 启用无头模式  
--no-images 禁用无图模式（默认开启）  
包含错误处理和礼貌等待机制  
自动管理ChromeDriver版本  

# Check_ASMR_Chinese
一个由AI生成的Python脚本，用于检查ASMR是否更新了中文版本或字幕  
逐行检查urls.txt中的链接是否包含“中文”、“字幕”等字样  
只适用于ASMR Online  
默认不开启无头模式、开启无图模式  
