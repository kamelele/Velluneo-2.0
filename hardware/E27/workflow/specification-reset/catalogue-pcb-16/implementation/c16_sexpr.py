"""Small lossless-token KiCad s-expression reader for bounded structural edits.
Native KiCad remains the parser/DRC/netlist authority after any write.
"""
import re,json
def parse(text):
 stack=[];root=None
 for token in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',text):
  if token=='(':
   item=[]
   if stack:stack[-1].append(item)
   else:
    assert root is None;root=item
   stack.append(item)
  elif token==')':assert stack;stack.pop()
  else:assert stack;stack[-1].append(token)
 assert not stack and root;return root
def dumps(obj,level=0):
 if not isinstance(obj,list):return obj
 head=[];children=[]
 for v in obj:
  if isinstance(v,list):children.append(dumps(v,level+1))
  else:head.append(v)
 # KiCad nodes put all atom arguments before child nodes.
 return '('+' '.join(head)+(' 'if children else'')+('\n'+' '*min(level,5)).join(children)+')'
def child(obj,tag):return next((x for x in obj if isinstance(x,list)and x and x[0]==tag),None)
def children(obj,tag):return[x for x in obj if isinstance(x,list)and x and x[0]==tag]
def string(token):return json.loads(token)if token.startswith('"')else token
def strip_tracks(path):
 t=parse(path.read_text(encoding='utf-8'));drop={'segment','via','arc'};removed=[x for x in t if isinstance(x,list)and x[0]in drop];t=[x for x in t if not(isinstance(x,list)and x[0]in drop)];path.write_text(dumps(t)+'\n',encoding='utf-8',newline='\n');return len(removed)
