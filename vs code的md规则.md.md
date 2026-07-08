- [颜色和字号](#颜色和字号)
- [符号输入](#符号输入)
  - [表格](#表格)
- [vscode快捷键](#vscode快捷键)
  - [页面字体大小](#页面字体大小)
  - [标题折叠和展开](#标题折叠和展开)
  - [自动生成目录](#自动生成目录)

# 颜色和字号
可以自己填<font color=yellowgreen size=6>颜色</font>名
1. <font color="yellowgreen">yellowgreen 黄绿</font>
2. <font color="lightgreen">lightgreen 浅绿</font>
3. <font color="forestgreen">forestgreen 森林绿</font>
4. <font color="skyblue">skyblue 天蓝色</font>
5. <font color="royalblue">royalblue 宝蓝</font>
6. <font color="coral">coral 珊瑚橙</font>
7. <font color="tomato">tomato 番茄红</font>
8. <font color="hotpink">hotpink 艳粉</font>
9. <font color="gold">gold 金色</font>
10. <font color="slategray">slategray 石板灰</font>
# 符号输入
[↑ 返回目录](#)
1. 有序
* 无序
  * 无序  
1. 
>引用效果

**粗体** 或 __粗体__
• 实心圆点

○ 空心圆点

□ 方框

✓ 勾选框

箭头符号

→ 右箭头

← 左箭头

↑ 上箭头

↓ 下箭头

↔ 双向箭头
## 表格
[↑ 返回目录](#)

1. 简单表格

| 姓名 | 年龄 | 职业 |
|------|------|------|
| 张三 | 25   | 工程师 |
| 李四 | 30   | 设计师 |

2. 带对齐的表格

| 左对齐 | 居中对齐 | 右对齐 |
|:------|:--------:|-------:|
| 左    | 中       | 右    |
| 数据  | 数据     | 数据  |

对齐规则：

:--- 左对齐
:---: 居中对齐
---: 右对齐

3. 嵌套表格

| 主分类 | 子分类 |
|--------|--------|
| 编程语言 | [Python](#) [Java](#) [C++](#) |
| 数据库 | [MySQL](#) [MongoDB](#) [Redis](#) |

5. 多行单元格内容

| 功能 | 描述 |
|------|------|
| 代码高亮 | 支持多种编程语言的语法高亮 |
| 表格功能 | 可以创建对齐方式不同的表格 |
| 引用功能 | > 可以在表格中使用引用 |

6. 复杂表格示例
7. 
| 项目 | 状态 | 进度 | 负责人 |
|------|------|------|--------|
| 前端开发 | 进行中 | 75% | 张三 |
| 后端开发 | 已完成 | 100% | 李四 |
| 测试阶段 | 待开始 | 0% | 王五 |
| 部署上线 | 计划中 | - | 赵六 |
# vscode快捷键
[↑ 返回目录](#)
## 页面字体大小
ctrl++或者-就能缩放
## 标题折叠和展开
在行号右侧，鼠标放上就能显示箭头，点击就行
## 自动生成目录
命令：Create Table of Contents 生成文档目录（带锚点跳转）

保存文件自动刷新目录；光标放在目录上重新执行命令更新

支持 GitHub/GitLab/VSCode 多种标题 ID 锚点规则配置 
操作流程：
* 修改 / 新增 / 删除文档标题 → 按 Ctrl+S 保存文件 → 目录自动全部刷新
* 如果保存不自动更新：
Ctrl+, 打开设置，搜索 toc.updateOnSave，勾选「Update TOC on save」

[↑ 返回目录](#)