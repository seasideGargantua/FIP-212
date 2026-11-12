# W8 Git 与 GitHub 课后作业

**组号：** 第 5 组

**提交人：** `lbgs-1`（记录员提交一份）

## 1. GitHub 仓库 HTTPS 链接

`https://github.com/lbgs-1/fip-w8-lab`

## 2. Commit 记录证明

本组 `fip-w8-lab` 仓库的提交历史如下（`git log --oneline` 实际输出）：

```text
47a6f26 添加 gitignore
da7db98 W8 研讨：第一次提交
```

| 项目 | 内容 |
|:---|:---|
| 有效 commit 短哈希 | `da7db98` |
| 完整哈希 | `da7db98ab7d6c6e8df6401458ef05ed67a9d28f7` |
| commit 说明 | `W8 研讨：第一次提交` |
| 作者 | `lbgs-1 <3628747901@qq.com>` |
| commit 链接 |`https://github.com/lbgs-1/fip-w8-lab/commit/da7db98` |

> 哈希是本地仓库生成时就固定的，`git push` 不会改变它，所以先把哈希填进本文件、推送后再补链接也来得及。

## 3. 仓库内容与复现命令

`fip-w8-lab` 里只有本次要求的两个文件（按课件“只提交 README 和 .gitignore”的要求）：

```text
w8_lab/
  README.md      组号、成员、日期
  .gitignore     __pycache__/、*.pyc、.vscode/、.DS_Store
```

实际执行的命令：

```bash
git config --global user.name "lbgs-1"
git config --global user.email "3628747901@qq.com"
git config --global init.defaultBranch main

cd w8_lab
git init -b main
git add README.md
git commit -m "W8 研讨：第一次提交"      # → da7db98
git add .gitignore
git add .
git commit -m "添加 gitignore"            # → 47a6f26

git remote add origin https://github.com/lbgs-1/fip-w8-lab.git
git branch -M main
git push -u origin main
```

`git status` 在推送前为 `## main`（工作区干净、无待提交内容），`git log --oneline` 只有上面两条提交，没有把 `__pycache__`、`.vscode` 之类的东西带进仓库。
