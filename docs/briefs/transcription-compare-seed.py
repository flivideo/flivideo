import json,glob,os,re,difflib,collections
ROOT='/Users/davidcruwys/dev/video-projects/v-appydave'
norm=lambda w: re.sub(r"[^\w'\[\]]","",w.lower())
def words(t):
    ws=t.get('words') or [w for s in t.get('segments',[]) for w in s.get('words',[])]
    if ws: return [norm(w.get('word',w.get('text',''))) for w in ws]
    return [norm(x) for s in t.get('segments',[]) for x in s.get('text','').split()]
out=[]
for proj in sorted(glob.glob(ROOT+'/d0[1-6]-*')):
    for cf in sorted(glob.glob(proj+'/hub/transcripts/engines/*.crisper.json')):
        take=os.path.basename(cf)[:-len('.crisper.json')]
        orig=None
        for e in ('mlx-flihub','groq','mlx'):
            p=f'{proj}/hub/transcripts/engines/{take}.{e}.json'
            if os.path.exists(p): orig=(e,p); break
        best=json.load(open(f'{proj}/hub/transcripts/{take}.json'))
        c=[w for w in words(json.load(open(cf))) if w]
        fill=sum(1 for w in c if w in ('[uh]','[um]'))
        row=dict(project=os.path.basename(proj)[:3],take=take,best=best['engine']['name'],crisper_words=len(c),fillers=fill,
                 restored=len((best.get('health') or {}).get('wordsFromWhisper') or []))
        if orig:
            o=[w for w in words(json.load(open(orig[1]))) if w]
            cc=[w for w in c if w not in ('[uh]','[um]')]
            sm=difflib.SequenceMatcher(None,o,cc,autojunk=False)
            row.update(orig_engine=orig[0],orig_words=len(o),agree=round(sm.ratio()*100,1))
            subs=[]
            for tag,i1,i2,j1,j2 in sm.get_opcodes():
                if tag!='equal' and (i2-i1)<=4 and (j2-j1)<=4: subs.append((tag,' '.join(o[i1:i2]),' '.join(cc[j1:j2])))
            row['changes']=subs
        out.append(row)
json.dump(out,open('/private/tmp/claude-501/-Users-davidcruwys-dev-ad-brains/7c6a3726-4270-4e8f-bcf3-baf10a76b63c/scratchpad/compare.json','w'),indent=1)
P=collections.defaultdict(lambda:collections.Counter())
for r in out:
    p=P[r['project']]; p['takes']+=1; p['cw']+=r['crisper_words']; p['ow']+=r.get('orig_words',0); p['fill']+=r['fillers']; p['rest']+=r['restored']; p['best_cw']+= r['best']=='crisperwhisper'; p['changes']+=len(r.get('changes',[])); p['agree']+=r.get('agree',0)
for k,p in P.items(): print(k,'takes',p['takes'],'| best=CW',p['best_cw'],'| words orig',p['ow'],'→ CW',p['cw'],'| fillers',p['fill'],'| restored',p['rest'],'| changes',p['changes'],'| avg agree %.1f%%'%(p['agree']/p['takes']))
print('orig engines:',collections.Counter(r.get('orig_engine') for r in out))
