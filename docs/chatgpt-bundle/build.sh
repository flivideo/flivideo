#!/bin/zsh
# Rebuilds the ChatGPT source bundle from the live per-app docs.
# Copies each app's SYSTEM.md / AGENT-NOTES.md, strips frontmatter noise, file:line anchors and absolute paths.
set -e
R=/Users/davidcruwys/dev/ad/flivideo
B=$R/docs/chatgpt-bundle
clean() { python3 - "$1" "$2" "$3" "${4:-}" <<'PY'
import re,sys
src,dst,title,label=sys.argv[1:5]
t=open(src).read()
t=re.sub(r'\A---\n.*?\n---\n','',t,flags=re.S)                      # drop frontmatter
t=re.sub(r'/Users/davidcruwys/dev/ad/flivideo/','',t)                # absolute → repo-relative
t=re.sub(r'/Users/davidcruwys/','~/',t)
t=re.sub(r'([\w./-]+\.(?:ts|tsx|js|mjs|py|json|sh|md)):\d+(?:[-–]\d+)?',r'\1',t)  # file:line → file
open(dst,'w').write(f"<!-- FliVideo source bundle · {title} · generated from {(label or src).replace('/Users/davidcruwys/dev/ad/flivideo/','').replace('/Users/davidcruwys/','~/')} -->\n\n"+t)
PY
}
clean $R/README.md                 $B/00-flivideo-map.md            "central map"
for a in flistudio flihub flicast flicut teletubby; do
  clean $R/$a/docs/SYSTEM.md       $B/10-$a-system.md               "$a SYSTEM"
  clean $R/$a/docs/AGENT-NOTES.md  $B/11-$a-agent-notes.md          "$a AGENT-NOTES"
done
clean $R/fli-core/README.md        $B/20-fli-core-readme.md         "fli-core README"
clean $R/flicast/docs/agent-drivable-reference.md $B/30-agent-drivable-reference.md "agent-drivable reference (FliCast)"
clean $R/docs/d04-autopilot-walkthrough.md $B/01-autopilot-walkthrough.md "end-to-end walkthrough"
clean /Users/davidcruwys/dev/video-projects/v-appydave/d04-flivideo-autopilot/-run/run-report.md $B/50-d04-run-report.md "d04 autopilot UAT run report"
# combined files: concat sources (first one leads), then clean
cat_clean() { out=$1; title=$2; shift 2; tmp=$(mktemp); for f in "$@"; do python3 -c "import re,sys;t=open(sys.argv[1]).read();print(re.sub(r'\\A---\\n.*?\\n---\\n','',t,flags=re.S))" "$f" >> $tmp; printf '\n\n---\n\n' >> $tmp; done; clean $tmp $out "$title" "${(j:, :)@}"; rm -f $tmp; }
BR=/Users/davidcruwys/dev/ad/brains
cat_clean $B/60-filmstudio-study.md "FilmStudio study — verdict first (FliEdit blueprint; overlays via HyperFrames + FliTools; FliGate is an OPEN proposal)" \
  $BR/filmstudio/verdict.md $BR/filmstudio/flivideo-mapping.md $BR/filmstudio/overlay-comparison.md $BR/filmstudio/capability-inventory.md
cat_clean $B/70-flicut-ux.md "FliCut UX — the 18 jobs, David's observations, and the editor UX research (cut loupe, two-lane timeline, mode switch)" \
  $R/docs/briefs/flicut-usability-notes.md $BR/video-editing-as-code/editor-ux-research.md
echo built; ls $B
