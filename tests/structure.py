from pathlib import Path
import yaml,hashlib
class Loader(yaml.SafeLoader): pass
Loader.add_constructor('!input',lambda l,n:('input',l.construct_scalar(n)))
p=Path(__file__).resolve().parents[1]/'mrsmart_orielis_universal.yaml'
new=yaml.load(p.read_text(),Loader=Loader)
base=yaml.load((p.parent/'github-baseline.yaml').read_text(),Loader=Loader)
assert new['triggers']==base['triggers']
assert new['mode']==base['mode']=='single'
assert new['actions'][-1]==base['actions'][-1]
assert new['blueprint']['input']['connection']==base['blueprint']['input']['connection']
for n in range(1,5):
 green=new['blueprint']['input'][f'green_{n}']['input']
 old=base['blueprint']['input'][f'green_{n}']['input']
 assert all(green[k]==v for k,v in old.items())
 for key in ['min','max']:
  number=green[f'channel_{n}_brightness_{key}']['selector']['number']
  assert number['mode']=='box' and number['min']==1 and number['max']==100
 blue=new['blueprint']['input'][f'blue_{n}']['input']
 assert blue[f'blue_channel_{n}_usage']['default']=='cover'
 assert not any(x['value']=='light' for x in blue[f'blue_channel_{n}_usage']['selector']['select']['options'])
 assert not any(x['domain']=='light' for x in blue[f'blue_channel_{n}_targets']['selector']['entity']['filter'])
 assert new['blueprint']['input'][f'red_{n}']==base['blueprint']['input'][f'red_{n}']
 for k,v in blue.items():
  if 'number' in v.get('selector',{}):
   assert v==base['blueprint']['input'][f'blue_{n}']['input'][k]
inputs={k for section in new['blueprint']['input'].values() for k in section['input']}
def check(v):
 if isinstance(v,tuple) and v[0]=='input':assert v[1] in inputs,v
 elif isinstance(v,dict):
  for x in v.values():check(x)
 elif isinstance(v,list):
  for x in v:check(x)
check(new)
print('PASS: YAML, input references, baseline triggers/timing/GREEN controls/RED unchanged, BLUE default and filters.')
print('SHA256',hashlib.sha256(p.read_bytes()).hexdigest())
