#!/bin/bash
# Deploy Minion Bageecha to production.
# Vercel account: aryaninternships-netizen (aryaninternships@gmail.com)
# GitHub:        aryaninternships-netizen/minions-garden
# Domain:        minionbageecha.in  (A @ -> 76.76.21.21 at GoDaddy, www 308s to apex)
set -e
cd "$(dirname "$0")"
VT=$(security find-generic-password -a "$USER" -s vercel-aryaninternships -w)
GT=$(gh auth token -u aryaninternships-netizen)
MSG="${1:-Update}"
# stamp the build so a stale browser copy is obvious
python3 - "$MSG" <<'PY'
import re, datetime, json
stamp = 'build ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M IST')
s = open('index.html').read()
s = re.sub(r'build 2026-\d\d-\d\d \d\d:\d\d IST', stamp, s)
open('index.html', 'w').write(s)
# the running page polls this to notice it has gone stale
json.dump({'build': stamp}, open('version.json', 'w'))
PY
git add -A && git commit -qm "$MSG" || echo "(nothing to commit)"
REM=$(git remote get-url origin)
git remote set-url origin "https://aryaninternships-netizen:${GT}@github.com/aryaninternships-netizen/minions-garden.git"
git push -q origin HEAD || true
git remote set-url origin "$REM"
vercel deploy --prod --yes --token="$VT" | grep -iE "error|Production"
sleep 6
echo "live build: $(curl -s https://minionbageecha.in/ | grep -o 'build 2026[^<]*' | head -1)"
