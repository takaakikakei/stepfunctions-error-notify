# 事前設定

## 端末にインストールが必要なもの

- serverless framework
- npm
- pipenv

## プラグインインストール

```
$ npm ci
```

## Python 必要パッケージインストール

```
$ pipenv install
```

## Slack App

以下のドキュメントを参照して、投稿先チャンネルの Incoming Webhook を取得します

[Slack での Incoming Webhook の利用](https://slack.com/intl/ja-jp/help/articles/115005265063)

## AWS Secrets Manager

AWS Secrets Manager に以下の情報を保管します

- キー：ALERT_HIGH_CHANNEL_WEBHOOK
  - 値：{緊急度高用の Slack チャネルの Incoming Webhook}
- キー：ALERT_MIDDLE_CHANNEL_WEBHOOK
  - 値：{緊急度中用の Slack チャネルの Incoming Webhook}
- キー：USERGROUP_ID
  - 値：{メンション先の Slack ユーザーグループ}

AWS Secrets Manager への保管方法は以下のブログを参照ください。

[Serverless Framework でクレデンシャル情報を扱う Lambda ファンクションを作成する -> 2. AWS Secrets Manager の設定 | DevelopersIO](https://dev.classmethod.jp/articles/serverless-framework-lambdafunc-secretsmanager/#toc-5)

Slack ユーザーグループ ID の取得方法は以下を参照ください。

[Mentioning groups](https://api.slack.com/reference/surfaces/formatting#mentioning-groups)

# デプロイ

```
$ sls deploy --stage {ステージ名}
```
