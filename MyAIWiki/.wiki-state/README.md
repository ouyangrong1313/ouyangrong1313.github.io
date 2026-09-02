# Wiki Ingest State

`ingests/<url-sha256-prefix>.json` records the lifecycle of a fetched source:

`fetched -> drafted -> polished -> validated -> published`

It stores normalized URLs, timestamps, relative artifact paths, content hashes, and failure summaries. It must not store article bodies, cookies, browser profiles, access tokens, or chat data. Wiki pages, indexes, and `log.md` remain the authoritative content records; this directory only supports safe retries and auditability.
