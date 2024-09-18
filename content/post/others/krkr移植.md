---
title: "Krkr移植"
description: 
date: 2024-09-17T20:48:52+08:00
hidden: false
comments: true
draft: false
tags: ["tech", "gal"]
---
看了好多篇，解包封包什么的，都去看了，但exe要怎么能在手机上用，不懂啊。

看了[KrkrExtract](https://github.com/xmoezzz/KrkrExtract)，GARbro等拆包软件，更是一头雾水，想玩的游戏的解密手段也不知道，使用[KrkrExtract](https://github.com/xmoezzz/KrkrExtract)甚至还报出

[Fatal Error Access Violation](https://github.com/xmoezzz/KrkrExtract/issues/119)，更是没能找出解决方法。

决定去看看[Kirikiroid2](https://github.com/zeas2/Kirikiroid2)，看个README就看出个大概了

```
Based on most code from Kirikiri2 and KirikiriZ

Video playback module modified from kodi

Some string code from glibc and Apple Libc.

Real-time texture codec modified from etcpak, pvrtccompressor, astcrt

Android storage accessing code from AmazeFileManager
```

在我理解，就是在手机上集成了游戏引擎，也因此能用xp3打开游戏。

把一些游戏的xp3文件拷到手机，试了试，还真能。

自己想玩游戏的xp3即使没有解密拆包再封包，直接拷到手机上，也行了。就这样得到解决了。

目前也有问题还在，plugin文件夹里都是dll，我想着手机上应该不能用吧，自己做了做变量控制实验，也没有发现差异。

另外，需要xp3filter.tjs转字符，找了同项目组以前项目的相应文件，成功了。[该网站](https://zeas2.github.io/Kirikiroid2_patch/patch/)不知道为什么没有更新。

还有，直接用[Kirikiroid2](https://github.com/zeas2/Kirikiroid2)玩刚刚弄的游戏挺卡的，看了看帧率挺低，不知原因。强制使用默认字体解决了。（这是因为使用不到想使用的字体导致的帧率低吗？为什么会用不到字体？我看钩不钩使用默认字体显示出来的都是同一种字体）

综上，不需要拆包封包也能完成移植。

又问了一下AI，看了一下[Kirikiroid2](https://github.com/zeas2/Kirikiroid2)。里面有JNI，说不定dll真能用。不知道，以后再看吧。

```
如果你有 .dll 文件的源代码，或者你能够找到它的等效代码并重新编译为 Android 支持的 .so 文件（共享库），你可以通过 C++ 和 JNI 将这些库集成到 Android 应用中。JNI 是 Android 的标准机制，允许你在 Java（或 Kotlin）代码中调用原生代码（如 C/C++ 编写的代码）。
```

不过exe是完全不需要的吗？那它在PC上起的作用又是什么，它的作用又该或又能怎样被代替？

还是xp3filter.tjs是和解密相关的？
