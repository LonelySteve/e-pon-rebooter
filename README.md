# E-PON Rebooter

>“光猫”是光调制解调器（Optical modem）的简称，“光猫”也称为单端口光端机，是针对特殊用户环境而研发的一种三件一套的光纤传输设备。该设备采用大规模集成芯片，电路简单，功耗低，可靠性高，具有完整的告警状态指示和完善的网管功能。（引用自百度百科）我们可以使用简单的Python程序令光猫按我们的需要进行重启。

## 前言

这应该算是比较好玩的东西（也很有用，至于有什么用，自己体会去），所以我写了一个简单的Py程序，成功实现了命令式重启光猫。

另外，由于本人家里只有一台中国电信的光猫，所以我写的程序仅仅能够确保能在我家这个型号的光猫上使用。至于其他型号的光猫，可以根据我[Blog](https://lonelysteve.github.io/2018/07/28/China-telecom-e-pon-robooter/)里的编写过程，自己修改部分代码，这应该是不难实现的。

附 我家的光猫参数：

|名称|值|
|:--:|:--:|
|品牌|长虹|
|类型|AP 外置型EPON上行 e8-C家庭网关（2+1）|
|型号|CH801-A21|

## 环境配置

* Python 3.6
* Requests

## 命令行用法

```Python reboot.py <username> <password>```

返回 True 或 False ，表示是否成功向光猫发出重启请求

## 调用

```Python

>>> from e_pon.reboot import reboot,reboot_and_wait
>>> reboot("your username","your pwd")
True
>>> reboot_and_wait("your username","your pwd")
# Wait for a moment
True

```



