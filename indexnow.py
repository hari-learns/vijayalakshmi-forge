#!/usr/bin/env python3
"""Tell Bing (and the other IndexNow engines: Yandex, Seznam, Naver) that
pages changed, so they recrawl within minutes instead of weeks.

    python3 indexnow.py              # every URL in sitemap.xml
    python3 indexnow.py blog/new-post products   # only these paths
    python3 indexnow.py --dry        # show what would be sent

Run it after a push, once the site is live on its own domain. It refuses to
run while the site is a preview (NOINDEX in content.py), because the key file
has to be reachable at https://<domain>/<key>.txt for the ping to count.
"""
import json
import re
import sys
import urllib.request

import content as C


def main(args):
    dry = "--dry" in args
    paths = [a for a in args if not a.startswith("--")]
    if C.NOINDEX and not dry:
        sys.exit("The site is still a preview (NOINDEX = True in content.py). Launch first.")
    if paths:
        urls = [f"{C.SITE_URL}/{p.strip('/')}" for p in paths]
    else:
        urls = re.findall(r"<loc>(.*?)</loc>", open("sitemap.xml").read())
    body = {"host": C.DOMAIN, "key": C.INDEXNOW_KEY,
            "keyLocation": f"{C.SITE_URL}/{C.INDEXNOW_KEY}.txt", "urlList": urls}
    if dry:
        print(json.dumps(body, indent=2))
        return
    req = urllib.request.Request("https://api.indexnow.org/indexnow", method="POST",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=20) as r:
        # 200 and 202 both mean accepted
        print(r.status, f"sent {len(urls)} URLs to IndexNow")


if __name__ == "__main__":
    main(sys.argv[1:])
