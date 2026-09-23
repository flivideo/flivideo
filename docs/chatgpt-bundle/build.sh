#!/bin/zsh
# Rebuilds the ChatGPT source bundle from the live per-app docs.
# Copies each app's SYSTEM.md / AGENT-NOTES.md, strips frontmatter noise, file:line anchors and absolute paths.
set -e
R=/Users/davidcruwys/dev/ad/flivideo
B=$R/docs/chatgpt-bundle
clean() { python3 - "$1" "$2" "$3" <<'PY'
import re,sys
src,dst,title=sys.argv[1:4]
t=open(src).read()
t=re.sub(r'\A---\n.*?\n---\n','',t,flags=re.S)                      # drop frontmatter
t=re.sub(r'/Users/davidcruwys/dev/ad/flivideo/','',t)                # absolute → repo-relative
t=re.sub(r'/Users/davidcruwys/','~/',t)
t=re.sub(r'([\w./-]+\.(?:ts|tsx|js|mjs|py|json|sh|md)):\d+(?:[-–]\d+)?',r'\1',t)  # file:line → file
open(dst,'w').write(f"<!-- FliVideo source bundle · {title} · generated from {src.replace('/Users/davidcruwys/dev/ad/flivideo/','')} -->\n\n"+t)
PY
}
clean $R/README.md                 $B/00-flivideo-map.md            "central map"
for a in flistudio flihub flicast flicut teletubby; do
  clean $R/$a/docs/SYSTEM.md       $B/10-$a-system.md               "$a SYSTEM"
  clean $R/$a/docs/AGENT-NOTES.md  $B/11-$a-agent-notes.md          "$a AGENT-NOTES"
done
clean $R/fli-core/README.md        $B/20-fli-core-readme.md         "fli-core README"
clean $R/flicast/docs/agent-drivable-reference.md $B/30-agent-drivable-reference.md "agent-drivable reference (FliCast)"
clean $R/docs/d03-autopilot-walkthrough.md $B/01-autopilot-walkthrough.md "end-to-end walkthrough"
echo built; ls $B
