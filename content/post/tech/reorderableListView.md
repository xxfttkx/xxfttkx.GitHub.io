---
title: "Flutter：ReorderableListView + removeWhere 引发的坑"
description: 
date: 2025-07-24T23:42:51+08:00
comments: true
draft: false
tags: ["diary"]
---
在最近开发 [command_manager](https://github.com/xxfttkx/command_manager) 项目时，我遇到了一个奇怪的问题：
当我在 `ReorderableListView` 使用 `removeWhere + insert` 操作列表时，触发了 `_TypeError (Null check operator used on a null value)` 的异常，而改用 `indexWhere + removeAt + insert` 却完全正常。

这个问题困扰没有我很久，GPT分析了 `ReorderableListView` 的实现后就告诉我原因了。

---

## 问题代码

原先我想在运行某条命令后，把它移动到列表顶部：

```dart
if (settings.runCommandOnTop) {
  _commands.removeWhere((cmd) => cmd.name == action.name);
  _commands.insert(0, action);
}
```

看起来很简单：找到同名命令，删掉，然后插到第一个位置。
但是，当列表有拖拽排序 (`ReorderableListView`) 时，这段代码会触发异常：

```
_TypeError (Null check operator used on a null value)
```

---

## 原因分析

**关键点：`ReorderableListView` 依赖于 Key 来识别每个 item 的状态**。

* 在 Flutter 的 Widget Diff 算法中，`Key` 是识别“同一个元素”的唯一依据。
* 当我用 `removeWhere` 时，这一步会：

  1. 遍历整个列表。
  2. 找到匹配的 item 后移除。
  3. 然后再用 `insert` 插入新的对象（即使 `name` 一样，**对于 Flutter 这就是一个新对象**）。

换句话说，`removeWhere + insert` 让 `ReorderableListView` 认为：

> 有一个旧的 item 被删除了，一个新的 item 被添加到了列表头部。

如果此时 `ReorderableListView` 还处于拖拽或重建状态，它的内部 `Element` 树会找不到对应的 Key，从而触发 `_TypeError`。

---

### 为什么 `removeAt + insert` 没问题？

```dart
final index = _commands.indexWhere((cmd) => cmd.name == action.name);
if (index != -1) {
  final cmd = _commands.removeAt(index);
  _commands.insert(0, cmd);
}
```

* `removeAt` 是**对单个位置的精确操作**，Flutter 能够理解这是一个 item 的位置变化，而不是“销毁 + 重建”。
* 在 diff 算法中，Key 能正常匹配，Element 树不会乱掉，所以没有异常。

---

## 总结

* **`removeWhere + insert`** 在普通 `ListView` 下没问题，但在 `ReorderableListView` 下容易触发 Key 同步问题。
* **`removeAt + insert`** 是更安全的移动方式。
* 关键原因在于 **`ReorderableListView` 依赖 Key 和内部缓存**，批量删除/重建会打乱它的 Element 树。

## 我的理解

`removeAt + insert` 没有新对象的产生，Flutter 能够识别这是一个简单的“位置变化”，Element 仍然被复用。

`removeWhere + insert` 即便 key 相同，也会让旧 Element 被销毁，再重新创建一个新的 Element，这可能让 `ReorderableListView` 的内部引用失效，导致 TypeError。

从表现上看，这像是 `ReorderableListView` 的 bug，但其实是它的使用限制。如果想要安全地移动元素，应该优先使用 `removeAt + insert`。

其实应该沿用最初为 `ReorderableListView` 编写的 `reorder` 方法:

```
  void reorder(int oldIndex, int newIndex) {
    if (newIndex > oldIndex) newIndex--; // ReorderableListView 的特殊行为

    final item = _commands.removeAt(oldIndex);
    _commands.insert(newIndex, item);

    ConfigStorage.saveCommands(_commands);
    notifyListeners();
  }
```

怎么还在绕大圈子，sbr还在追我。

> [遠回りこそが俺の最短の道だった](https://dic.pixiv.net/a/%E3%80%8E%E9%81%A0%E5%9B%9E%E3%82%8A%E3%81%93%E3%81%9D%E3%81%8C%E4%BF%BA%E3%81%AE%E6%9C%80%E7%9F%AD%E3%81%AE%E9%81%93%E3%81%A0%E3%81%A3%E3%81%9F%E3%80%8F)
