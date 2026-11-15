# Re:Filter для Shadowrocket

Re:Filter публикует списки только в виде голых доменов/CIDR, а Shadowrocket ждёт `DOMAIN-SUFFIX,...` / `IP-CIDR,...`.
`convert.py` конвертирует, GitHub Actions обновляет `lists/` каждый день в 04:00 UTC.

| Файл | Источник |
|---|---|
| lists/refilter_domains.list | Re:Filter domains_all.lst |
| lists/refilter_ip.list | Re:Filter ipsum.lst |
| lists/community.list | community.antifilter.download |
| (по прямой ссылке) | itdoginfo/allow-domains Russia/inside |

Локальный запуск: `/usr/bin/python3 convert.py`
