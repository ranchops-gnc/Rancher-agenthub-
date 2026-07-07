# secrets/ 目录

> 本目录用于存放敏感信息（密钥、密码等），不提交 Git。
>
> 以下为示例模板，实际使用时替换为真实内容。

---

## 模板文件

### accounts.yaml（账号模板）

```yaml
# 账号示例模板
example_service:
  username: "user@example.com"
  password: "your-password-here"
```

### api_keys.yaml（API 密钥模板）

```yaml
# API 密钥示例模板
openai:
  api_key: "sk-xxxxxxxxxxxxx"

github:
  pat: "ghp_xxxxxxxxxxxxx"
```

---

## 使用说明

1. 复制模板文件并重命名
2. 填入真实信息
3. 确保 .gitignore 已排除 secrets/ 目录

---

*示例模板 - 请勿包含真实密钥*