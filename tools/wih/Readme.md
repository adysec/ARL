## 介绍

WebInfoHunter（简称 wih）工具是一款功能强大、易用性高、扩展性强的命令行工具。

可以快速地获取指定网页中的各种特定信息。采用 Golang 编写。

旨在快速批量地查找指定网页中 JS 中的各种特定信息，例如子域名、路径、URL、邮箱、IP、手机号、AK 和 SecretKey 等。

wih 工具的规则非常灵活，可以根据自己的需求自定义规则，当前已经预设了 36 条规则。

此外，wih 工具还支持对 JWT Token 的有效期进行检验，以及对云 API 中的 AK 和 SK 进行有效性检验，节省验证时间。

wih 工具支持多种输出格式，包括文本、JSON、CSV、HTML 和 Markdown 等，可以根据自己的需求选择合适的格式进行输出。

而且，wih 工具还支持自动根据站点URL保存输出结果，方便对结果来源进行查找，同时还可以将 AK 和 SK 检出结果单独保存，提高工作效率。



## 命令行

```shell
Usage:
  WebInfoHunter（简称 wih） [flags]

Flags:
      --ak-sk-output string        AK/SK 单独保存的文件名 (default "ak_leak.txt")
  -a, --auto-save-name             根据站点自动生成保存的文件名
  -c, --concurrency int            并发数(针对站点) (default 2)
  -P, --concurrency-per-site int   每个站点的并发数 (default 3)
      --csv                        CSV 格式输出
      --dc                         禁止检查 AK/SK 有效性
      --dial-timeout float         Dial timeout (s) (default 5)
      --disable-ak-sk-output       禁止 AK/SK 单独保存
      --disable-check-ak-sk        禁止检查 AK/SK 有效性
      --disable-color              disable log color
  -f, --follow-redirect            跟随重定向
  -G, --generate-rule              生成规则
  -H, --header strings             Custom header (e.g. 'X-My-Header: value')
  -h, --help                       help for WebInfoHunter（简称
      --html                       HTML 格式输出
      --limit-reader-size int      Maximum response size (in bytes) (default 10485760)
      --log-file string            Path to log file (default "-")
  -v, --log-level string           Log level (zero,debug,info,success,error) (default "info")
  -M, --max-collect int            用于表示所有收集类型的最大收集数量, 对于每个站点 (default 600)
      --md                         Markdown 格式输出
  -o, --output string              结果输出文件的名称(- 为标准输出) (default "-")
  -J, --output-json                JSON 格式输出
  -x, --proxy string               HTTP proxy (e.g. http://localhost:8080)
  -r, --rule-config string         规则配置文件 (default "rules.yml")
      --size int                   设置表格分页大小
  -t, --target string              目标URL或者文件
  -T, --text                       文本格式输出
      --timeout float              Response timeout (s) (default 180)
      --version                    显示版本

```




## 例子


0. 生成规则

```shell
./wih -G
```


2. 对单个URL进行信息提取

```shell
./wih -t https://www.baidu.com
```


2. 批量对URL进行信息提取

-a 参数表示根据站点自动生成保存文件名，方便对结果来源进行查找。

```shell
./wih -t urls.txt -a
```

3. 第三方程序调用

```shell
./wih -t https://www.baidu.com -J -o result.json
```


## 内置规则

```yaml
rules:
  # 域名，内置规则
  - id: domain
    enabled: true
  # IP， 内置规则
  - id: ip
    enabled: true
  # 路径，内置规则
  - id: path
    enabled: true
  # URL主机部分为域名，内置规则
  - id: domain_url
    enabled: true
  # URL主机部分为IP，内置规则
  - id: ip_url
    enabled: true
  # 邮箱
  - id: email
    enabled: true
    pattern: \b[A-Za-z0-9._\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,61}\b
  # 二代身份证
  - id: id_card
    enabled: true
    pattern: \b([1-9]\d{5}(19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx])\b
  # 手机号
  - id: phone
    enabled: true
    pattern: \b1[3-9]\d{9}\b
  # jwt token (不要修改ID)
  - id: jwt_token
    enabled: true
    pattern: eyJ[A-Za-z0-9_/+\-]{10,}={0,2}\.[A-Za-z0-9_/+\-\\]{15,}={0,2}\.[A-Za-z0-9_/+\-\\]{10,}={0,2}
  # 阿里云 AccessKey ID (不要修改ID)
  - id: Aliyun_AK_ID
    enabled: true
    pattern: \bLTAI[A-Za-z\d]{12,30}\b
  # 腾讯云 AccessKey ID (不要修改ID)
  - id: QCloud_AK_ID
    enabled: true
    pattern: \bAKID[A-Za-z\d]{13,40}\b
  # 京东云 AccessKey ID (不要修改ID)
  - id: JDCloud_AK_ID
    enabled: true
    pattern: \bJDC_[0-9A-Z]{25,40}\b
  # 亚马逊 AccessKey ID
  - id: AWS_AK_ID
    enabled: true
    pattern: '["''](?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}["'']'
  # 火山引擎 AccessKey ID
  - id: VolcanoEngine_AK_ID
    enabled: true
    pattern: \b(?:AKLT|AKTP)[a-zA-Z0-9]{35,50}\b
  # 金山云 AccessKey ID
  - id: Kingsoft_AK_ID
    enabled: true
    pattern: \bAKLT[a-zA-Z0-9-_]{16,28}\b
  # 谷歌云 AccessKey ID
  - id: GCP_AK_ID
    enabled: true
    pattern: \bAIza[0-9A-Za-z_\-]{35}\b
  # 提取 SecretKey, 内置规则
  - id: secret_key
    enabled: true
  # Bearer Token
  - id: bearer_token
    enabled: true
    pattern: \b[Bb]earer\s+[a-zA-Z0-9\-=._+/\\]{20,500}\b
  # Basic Token
  - id: basic_token
    enabled: true
    pattern: \b[Bb]asic\s+[A-Za-z0-9+/]{18,}={0,2}\b
  # Auth Token
  - id: auth_token
    enabled: true
    pattern: '["''\[]*[Aa]uthorization["''\]]*\s*[:=]\s*[''"]?\b(?:[Tt]oken\s+)?[a-zA-Z0-9\-_+/]{20,500}[''"]?'
  # PRIVATE KEY
  - id: private_key
    enabled: true
    pattern: -----\s*?BEGIN[ A-Z0-9_-]*?PRIVATE KEY\s*?-----[a-zA-Z0-9\/\n\r=+]*-----\s*?END[ A-Z0-9_-]*? PRIVATE KEY\s*?-----
  #Gitlab V2 Token
  - id: gitlab_v2_token
    enabled: true
    pattern: \b(glpat-[a-zA-Z0-9\-=_]{20,22})\b
  #Github Token
  - id: github_token
    enabled: true
    pattern: \b((?:ghp|gho|ghu|ghs|ghr|github_pat)_[a-zA-Z0-9_]{36,255})\b
  #腾讯云 API网关 APPKEY
  - id: qcloud_api_gateway_appkey
    enabled: true
    pattern: \bAPID[a-zA-Z0-9]{32,42}\b
  #微信 公众号/小程序 APPID
  - id: wechat_appid
    enabled: true
    pattern: '["''](wx[a-z0-9]{15,18})["'']'
  #企业微信 corpid
  - id: wechat_corpid
    enabled: true
    pattern: '["''](ww[a-z0-9]{15,18})["'']'
  #微信公众号
  - id: wechat_id
    enabled: true
    pattern: '["''](gh_[a-z0-9]{11,13})["'']'
  # 密码
  - id: password
    enabled: true
    pattern: (?i)(?:admin_?pass|password|[a-z]{3,15}_?password|user_?pass|user_?pwd|admin_?pwd)\\?['"]*\s*[:=]\s*\\?['"][a-z0-9!@#$%&*]{5,20}\\?['"]
  # 企业微信 webhook
  - id: wechat_webhookurl
    enabled: true
    pattern: \bhttps://qyapi.weixin.qq.com/cgi-bin/webhook/send\?key=[a-zA-Z0-9\-]{25,50}\b
  # 钉钉 webhook
  - id: dingtalk_webhookurl
    enabled: true
    pattern: \bhttps://oapi.dingtalk.com/robot/send\?access_token=[a-z0-9]{50,80}\b
  # 飞书 webhook
  - id: feishu_webhookurl
    enabled: true
    pattern: \bhttps://open.feishu.cn/open-apis/bot/v2/hook/[a-z0-9\-]{25,50}\b
  # slack webhook
  - id: slack_webhookurl
    enabled: true
    pattern: \bhttps://hooks.slack.com/services/[a-zA-Z0-9\-_]{6,12}/[a-zA-Z0-9\-_]{6,12}/[a-zA-Z0-9\-_]{15,24}\b
  # grafana api key
  - id: grafana_api_key
    enabled: true
    pattern: \beyJrIjoi[a-zA-Z0-9\-_+/]{50,100}={0,2}\b
  # grafana cloud api token
  - id: grafana_cloud_api_token
    enabled: true
    pattern: \bglc_[A-Za-z0-9\-_+/]{32,200}={0,2}\b
  # grafana service account token
  - id: grafana_service_account_token
    enabled: true
    pattern: \bglsa_[A-Za-z0-9]{32}_[A-Fa-f0-9]{8}\b
  - id: app_key
    enabled: true
    pattern: \b(?:VUE|APP|REACT)_[A-Z_0-9]{1,15}_(?:KEY|PASS|PASSWORD|TOKEN|APIKEY)['"]*[:=]"(?:[A-Za-z0-9_\-]{15,50}|[a-z0-9/+]{50,100}==?)"

# 排除规则， 支持字段 id, content, target , source 逻辑为 and ，如果是正则匹配，需要使用 regex: 开头
# source 包括 page(网站首页), js (js 文件), system (系统生成)
exclude_rules:
  # 排除站点 https://cc.163.com 中 类型为 secret_key 的内容
  - name: "不收集 cc.163.com 的 secret_key" # 排除规则名称，无实际意义
    id: secret_key
    target: regex:cc\.163\.com
    enabled: true

  - name: "不收集 open.work.weixin.qq.com 的 bearer_token"
    id: bearer_token
    target: https://open.work.weixin.qq.com
    content: regex:Bearer\s+
    enabled: true

  - name: "过滤来自首页的内容"
    source_tag: page
    enabled: false

```



## 更新日志

### 2023-12（v1.5.4-beta）

- 新增：根据来源（source_tag）进行排除
- 新增：命令行参数 --disable-check-ak-sk ，用于禁用 sk 有效性检测
- 新增：规则 1 条
- 修复：检验AK有效性时，如果不联网标记为(Network Error)
- 修复：检验腾讯云 SK 有效时，正确输出 AppId

## 已经集成到 ARL


https://tophanttechnology.github.io/ARL-doc/function_desc/web_info_hunter/

