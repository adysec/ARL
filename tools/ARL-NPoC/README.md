## 说明

集漏洞验证和任务运行的一个框架

**注：源开源项目被删除，所以建立了本开源项目留作备份，本项目所有内容均来自于[1c3z/ARL-NPoC](https://github.com/1c3z/ARL-NPoC)最新版本**


## 依赖
https://nmap.org/ncrack/


## 安装
```
pip3 install -r requirements.txt
pip3 install -e .
```

## 使用

```
xing -h

usage: xing [-h] [--version] [--quit]
            [--log {debug,info,success,warning,error}]
            {list,scan,sniffer,exploit,brute,listener} ...

positional arguments:
  {list,scan,sniffer,exploit,brute,listener}
                        子命令
    list                显示插件
    scan                扫描
    sniffer             协议识别
    exploit             漏洞利用
    brute               弱口令爆破
    listener            监听

optional arguments:
  -h, --help            show this help message and exit
  --version, -V         show program's version number and exit
  --quit, -q            安静模式 (default: False)
  --log {debug,info,success,warning,error}, -L {debug,info,success,warning,error}
                        日志等级 (default: info)
```

其中子命令的`-t`参数可以为文件名也可以为单个指定的目标，`-n` 按照文件名筛选`PoC`

## 备注
本项目是ARL中的子模块

https://github.com/TophantTechnology/ARL

## 免责声明
如果您下载、安装、使用、修改本系统及相关代码，即表明您信任本系统。
在使用本系统时造成对您自己或他人任何形式的损失和伤害，我们不承担任何责任。
如您在使用本系统的过程中存在任何非法行为，您需自行承担相应后果，我们将不承担任何法律及连带责任。
请您务必审慎阅读、充分理解各条款内容，特别是免除或者限制责任的条款，并选择接受或不接受。
除非您已阅读并接受本协议所有条款，否则您无权下载、安装或使用本系统。
您的下载、安装、使用等行为即视为您已阅读并同意上述协议的约束。
