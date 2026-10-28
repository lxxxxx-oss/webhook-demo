# EvalAgent Webhook Demo

本仓库用于演示 EvalAgent 如何接收 GitHub Pull Request Webhook、审查新增代码并回写报告。

## 仓库内容

- `app.py`：正常基线，只把表达式作为数据返回，不执行表达式。
- `.gitignore`：排除 Python 缓存、本地环境和数据库。

EvalAgent 服务在另一处运行。本仓库不需要复制 EvalAgent 源码，也不需要 GitHub Actions。

## 演示流程

1. 在 EvalAgent 中配置 Webhook Secret 和演示仓库所需的 GitHub 权限。
2. 在本仓库 Settings → Webhooks 中添加公网 HTTPS 地址，以 `/webhooks/github` 结尾，选择 Pull requests 事件。
3. 建立 `demo/unsafe-change` 分支，把 `app.py` 改成下方版本并提交。
4. 创建该分支到 `main` 的 Pull Request，观察 Webhook 的 HTTP 202 响应。
5. 在 EvalAgent 管理台查看审查任务和报告；开启自动回帖时，在 PR Conversation 中查看报告评论。
6. 向同一 PR 分支追加提交，观察 `synchronize` 事件触发的新任务。

Webhook 必须先配置，再创建 PR；系统不会自动补发配置前的 PR 创建事件。

## 供审查的演示改动

以下代码故意包含风险，仅用于代码审查演示，不要执行或合并。凭据字符串是虚构值。

```python
def calculate(expression):
    password = "DEMO_ONLY_NOT_A_REAL_SECRET"
    result = eval(expression)
    print(result)
    return result
```

当这些代码作为 `app.py` 的新增行出现在 PR Diff 中，本地规则可报告：

| 规则 | 问题 | 严重度 |
|---|---|---|
| SEC-HARDCODED-SECRET | 硬编码凭据 | high |
| SEC-EVAL | 动态代码执行 | critical |
| REL-DEBUG-PRINT | 调试输出 | low |

自动修复需要单独触发；当前确定性修复器支持该示例中的凭据和调试输出，不会自动修复 `eval`。

不要把真实 Token、Webhook Secret 或 `.env` 提交到仓库。
