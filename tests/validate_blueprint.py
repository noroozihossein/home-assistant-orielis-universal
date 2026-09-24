import asyncio,tempfile
from pathlib import Path
from homeassistant.core import HomeAssistant,Context,callback
from homeassistant.util.yaml import load_yaml
from homeassistant.components.blueprint.models import Blueprint,BlueprintInputs
from homeassistant.components.automation.config import AUTOMATION_BLUEPRINT_SCHEMA,PLATFORM_SCHEMA
from homeassistant.helpers.script import Script,async_validate_actions_config
from homeassistant.helpers import condition
async def main():
 h=HomeAssistant(tempfile.mkdtemp()); from homeassistant import loader; loader.async_setup(h)
 from homeassistant.helpers import entity_registry as er
 await er.async_load(h)
 bp=Blueprint(load_yaml(str(Path(__file__).resolve().parents[1] / 'mrsmart_orielis_universal.yaml')),expected_domain='automation',schema=AUTOMATION_BLUEPRINT_SCHEMA)
 assert not bp.validate()
 calls=[]; tests=0
 @callback
 def svc(c):calls.append((c.domain+'.'+c.service,dict(c.data)))
 for dom,names in {'light':['turn_on','turn_off'],'media_player':['media_play','media_pause','volume_set','media_next_track','media_previous_track'],'cover':['open_cover','close_cover','stop_cover','set_cover_position'],'climate':['set_temperature'],'number':['set_value'],'input_number':['set_value'],'persistent_notification':['create']}.items():
  for name in names:h.services.async_register(dom,name,svc)
 async def run(a,**o):
  nonlocal tests
  x=BlueprintInputs(bp,{'use_blueprint':{'path':'x.yaml','input':{'orielis_device':'a'*32,'event_cooldown':0,**o}}});x.validate()
  cfg=PLATFORM_SCHEMA(x.async_substitute())
  seq=await async_validate_actions_config(h,cfg['actions'])
  v=cfg['variables'].async_render(h,{'trigger':{'id':a,'platform':'mqtt','payload':a}})
  calls.clear()
  for c in cfg['conditions']:
   check=await condition.async_from_config(h,c)
   if not check(h,v):tests+=1;return []
  await Script(h,seq,'test','automation',script_mode='single').async_run(v,Context())
  tests+=1;return calls.copy()
 def state(e,s,**kw):h.states.async_set(e,s,kw)
 def light(s='on',k=2800):state('light.a',s,brightness=120,supported_color_modes=['color_temp'],min_color_temp_kelvin=2700,max_color_temp_kelvin=6500,color_temp_kelvin=k)
 light()
 for n in range(1,5):
  opts={f'channel_{n}_targets':['light.a']}
  r=await run(f'light_{n}_brightness_up',**opts);assert r[0][1]['brightness_step_pct']==5,r
  r=await run(f'light_{n}_colortemp_down',**opts);assert r[0][1]['color_temp_kelvin']==2700,r
  for e in ['on','off','brightness_up','brightness_down','colortemp_up','colortemp_down','start','stop','position_open','position_close','scene']:
   a=f'scene_{n}' if e=='scene' else f'{"curtain" if e in ["start","stop","position_open","position_close"] else "light"}_{n}_{e}'
   key=f'channel_{n}_custom_'+('press' if e=='on' else e)
   r=await run(a,**{key:[{'action':'persistent_notification.create','data':{'message':'custom'}}]});assert len(r)==1 and r[0][0]=='persistent_notification.create',(a,r)
   assert not await run(a,**{**opts,f'channel_{n}_{e}_enabled':False})
 light(k=6490);r=await run('light_1_colortemp_up',channel_1_targets=['light.a']);assert r[0][1]['color_temp_kelvin']==6500
 light('off');assert not await run('light_1_brightness_up',channel_1_targets=['light.a']);assert not await run('light_1_colortemp_down',channel_1_targets=['light.a'])
 r=await run('light_1_on',channel_1_targets=['light.a']);assert r[0][0]=='light.turn_on'
 light();assert not await run('light_1_on',channel_1_targets=['light.a'])
 assert not await run('light_1_brightness_up',enabled=False,channel_1_targets=['light.a'])
 state('light.simple','on',supported_color_modes=['onoff']);state('light.dead','unavailable')
 assert not await run('light_1_colortemp_up',channel_1_targets=['light.simple','light.dead'])
 r=await run('light_1_brightness_up',channel_1_targets=['light.a','light.dead','light.a'],channel_1_reverse=True,channel_1_brightness_step=10);assert len(r)==1 and r[0][1]['brightness_step_pct']==-10
 state('media_player.a','playing',volume_level=.98,supported_features=1+4+16+32+16384)
 r=await run('light_1_brightness_up',channel_1_targets=['media_player.a']);assert r[0][1]['volume_level']==1
 for a,svcname in [('on','media_play'),('off','media_pause'),('colortemp_up','media_next_track'),('colortemp_down','media_previous_track')]:
  r=await run('light_1_'+a,channel_1_targets=['media_player.a']);assert r[0][0]=='media_player.'+svcname,r
 state('cover.a','open',current_position=97,supported_features=15)
 r=await run('curtain_1_position_open',blue_channel_1_targets=['cover.a']);assert r[0][1]['position']==100
 r=await run('curtain_1_position_open',blue_channel_1_targets=['cover.a'],blue_channel_1_reverse=True);assert r[0][1]['position']==87
 state('climate.a','heat',temperature=24,min_temp=16,max_temp=24,supported_features=1)
 r=await run('light_1_brightness_up',channel_1_targets=['climate.a']);assert r[0][1]['temperature']==24
 state('number.a','2',min=0,max=10)
 r=await run('light_1_brightness_down',channel_1_targets=['number.a']);assert r[0][1]['value']==1
 for n in range(1,5):assert not await run(f'light_{n}_on')
 assert not await run('invalid')
 for op,svcname in [('start','open_cover'),('stop','stop_cover')]:
  r=await run('curtain_1_'+op,blue_channel_1_targets=['cover.a']);assert r[0][0]=='cover.'+svcname
 state('cover.no_position','open',supported_features=15)
 assert not await run('curtain_1_position_open',blue_channel_1_targets=['cover.no_position'])
 state('media_player.unsupported','playing',supported_features=0)
 assert not await run('light_1_brightness_up',channel_1_targets=['media_player.unsupported'])
 r=await run('light_1_brightness_up',channel_1_targets=['light.a','media_player.a','cover.a','climate.a','number.a']);assert len(r)==5,r
 # Confirm single mode drops concurrent events instead of queuing work.
 x=BlueprintInputs(bp,{'use_blueprint':{'path':'x.yaml','input':{'orielis_device':'a'*32,'channel_1_targets':['light.a'],'event_cooldown':0.1}}})
 cfg=PLATFORM_SCHEMA(x.async_substitute());seq=await async_validate_actions_config(h,cfg['actions'])
 script=Script(h,seq,'concurrency','automation',script_mode=cfg['mode'],max_exceeded=cfg['max_exceeded'])
 v=cfg['variables'].async_render(h,{'trigger':{'id':'light_1_brightness_up'}})
 calls.clear();await asyncio.gather(*(script.async_run(v,Context()) for _ in range(10)))
 assert len(calls)==1,calls
 await asyncio.sleep(.15);assert len(calls)==1,'Unexpected delayed command'
 # Synchronized vs relative: independent settings in all four channels.
 state('light.b','on',brightness=230,supported_color_modes=['color_temp'],min_color_temp_kelvin=3000,max_color_temp_kelvin=6000,color_temp_kelvin=5900)
 light(k=2800)
 for n in range(1,5):
  opts={f'channel_{n}_targets':['light.a','light.b'],f'channel_{n}_group_mode':'synchronized'}
  r=await run(f'light_{n}_brightness_up',**opts);assert [x[1]['brightness'] for x in r]==[133,133],r
  r=await run(f'light_{n}_colortemp_down',**opts);assert [x[1]['color_temp_kelvin'] for x in r]==[3000,3000],r
  opts[f'channel_{n}_group_mode']='relative'
  r=await run(f'light_{n}_colortemp_down',**opts);assert [x[1]['color_temp_kelvin'] for x in r]==[2700,5750],r
 state('media_player.b','paused',volume_level=.2,supported_features=1+4+16384)
 for mode,expected in [('synchronized',[1,1]),('relative',[1,.25])]:
  r=await run('light_1_brightness_up',channel_1_targets=['media_player.a','media_player.b'],channel_1_group_mode=mode)
  assert [x[1]['volume_level'] for x in r]==expected,r
 for op,service in [('on','media_play'),('off','media_pause')]:
  r=await run('light_1_'+op,channel_1_targets=['media_player.a','media_player.b'],channel_1_group_mode='synchronized');assert len(r)==2 and all(x[0]=='media_player.'+service for x in r),r
 state('cover.b','open',current_position=10,supported_features=15)
 r=await run('curtain_1_position_close',blue_channel_1_targets=['cover.a','cover.b'],blue_channel_1_group_mode='synchronized');assert [x[1]['position'] for x in r]==[87,87],r
 state('climate.b','heat',temperature=18,min_temp=18,max_temp=22,supported_features=1)
 r=await run('light_1_brightness_up',channel_1_targets=['climate.a','climate.b'],channel_1_group_mode='synchronized');assert [x[1]['temperature'] for x in r]==[22,22],r
 state('input_number.b','9',min=0,max=20)
 r=await run('light_1_brightness_up',channel_1_targets=['number.a','input_number.b'],channel_1_group_mode='synchronized');assert [x[1]['value'] for x in r]==[3,3],r
 # Separate property groups coexist within one channel.
 r=await run('light_1_brightness_up',channel_1_targets=['light.a','light.b','media_player.a','media_player.b','cover.a','cover.b','climate.a','climate.b','number.a','input_number.b'],channel_1_group_mode='synchronized')
 assert len(r)==10,r
 for j in range(0,10,2):assert {k:v for k,v in r[j][1].items() if k!='entity_id'}=={k:v for k,v in r[j+1][1].items() if k!='entity_id'},r
 # Reference skips unavailable/on-off-only lights and duplicates.
 r=await run('light_1_brightness_down',channel_1_targets=['light.dead','light.simple','light.a','light.a','light.b'],channel_1_group_mode='synchronized');assert [x[1]['brightness'] for x in r]==[107,107],r
 # No shared CCT range: skip rather than send divergent or illegal values.
 state('light.no_overlap','on',supported_color_modes=['color_temp'],min_color_temp_kelvin=7000,max_color_temp_kelvin=8000,color_temp_kelvin=7500)
 assert not await run('light_1_colortemp_up',channel_1_targets=['light.a','light.no_overlap'],channel_1_group_mode='synchronized')
 light('off')
 r=await run('light_1_brightness_up',channel_1_targets=['light.a','light.b'],channel_1_group_mode='synchronized');assert len(r)==1 and r[0][1]['brightness']==243,r
 r=await run('light_1_brightness_up',channel_1_targets=['light.a','light.b'],channel_1_group_mode='synchronized',wake_lights=True);assert [x[1]['brightness'] for x in r]==[13,13],r
 light()
 # Snapshot is calculated once, even when earlier service calls change HA state.
 @callback
 def update_first(c):
  svc(c)
  if 'light.a' in c.data['entity_id']:
   state('light.a','on',brightness=250,supported_color_modes=['color_temp'],min_color_temp_kelvin=2700,max_color_temp_kelvin=6500,color_temp_kelvin=2800)
 h.services.async_register('light','turn_on',update_first)
 r=await run('light_1_brightness_up',channel_1_targets=['light.a','light.b'],channel_1_group_mode='synchronized');assert [x[1]['brightness'] for x in r]==[133,133],r
 light()
 ten=[]
 for j in range(10):
  e=f'light.group_{j}';ten.append(e);state(e,'on',brightness=50+j*20,supported_color_modes=['color_temp'],color_temp_kelvin=3000+j*250,min_color_temp_kelvin=2700,max_color_temp_kelvin=6500)
 r=await run('light_1_brightness_up',channel_1_targets=ten,channel_1_group_mode='synchronized');assert len(r)==10 and len({x[1]['brightness'] for x in r})==1,r
 r=await run('light_1_colortemp_up',channel_1_targets=ten,channel_1_group_mode='synchronized');assert len(r)==10 and {x[1]['color_temp_kelvin'] for x in r}=={3150},r
 r=await run('light_2_colortemp_up',channel_1_group_mode='synchronized',channel_2_targets=ten,channel_2_group_mode='relative');assert len({x[1]['color_temp_kelvin'] for x in r})==10,r
 r=await run('light_1_brightness_up',channel_1_targets=ten,channel_1_group_mode='synchronized',channel_1_reverse=True);assert {x[1]['brightness'] for x in r}=={37},r
 # All eight profiles independently dispatch audio, lights, climate and numbers.
 for n in range(1,5):
  opts={f'channel_{n}_targets':['light.a'],f'blue_channel_{n}_targets':['media_player.a','media_player.b'],f'blue_channel_{n}_usage':'media_player',f'blue_channel_{n}_volume_step':10,f'blue_channel_{n}_group_mode':'synchronized'}
  r=await run(f'curtain_{n}_position_close',**opts);assert len(r)==2 and all(abs(x[1]['volume_level']-.88)<.00001 for x in r),r
  r=await run(f'curtain_{n}_start',**opts);assert len(r)==2 and all(x[0]=='media_player.media_play' for x in r),r
  r=await run(f'curtain_{n}_stop',**opts);assert len(r)==2 and all(x[0]=='media_player.media_pause' for x in r),r
  r=await run(f'light_{n}_brightness_up',**opts);assert len(r)==1 and r[0][0]=='light.turn_on',r
  opts={f'blue_channel_{n}_targets':['light.a','light.b'],f'blue_channel_{n}_usage':'light',f'blue_channel_{n}_rotation':'secondary',f'blue_channel_{n}_group_mode':'synchronized'}
  r=await run(f'curtain_{n}_position_open',**opts);assert len(r)==2 and len({x[1]['color_temp_kelvin'] for x in r})==1,r
  opts={f'blue_channel_{n}_targets':['climate.a','number.a']}
  r=await run(f'curtain_{n}_position_close',**opts);assert len(r)==2 and {x[0] for x in r}=={'climate.set_temperature','number.set_value'},r
  assert not await run(f'curtain_{n}_position_open',**{f'channel_{n}_targets':['light.a']})
  assert not await run(f'scene_{n}',**{f'channel_{n}_targets':['light.a'],f'blue_channel_{n}_targets':['media_player.a']})
 # Control type filters unrelated targets; custom-only does not run automatic calls.
 r=await run('curtain_1_position_open',blue_channel_1_targets=['light.a','media_player.a'],blue_channel_1_usage='media_player');assert len(r)==1 and r[0][0]=='media_player.volume_set',r
 assert not await run('curtain_1_position_open',blue_channel_1_targets=['light.a'],blue_channel_1_usage='custom')
 r=await run('curtain_1_position_open',blue_channel_1_usage='custom',channel_1_custom_position_open=[{'action':'persistent_notification.create','data':{'message':'blue custom'}}]);assert len(r)==1,r
 # A failed endpoint must not abort commands for remaining targets.
 @callback
 def fail_one(c):
  from homeassistant.exceptions import HomeAssistantError
  if 'light.bad' in c.data['entity_id']:raise HomeAssistantError('Simulated disconnected endpoint')
  svc(c)
 h.services.async_register('light','turn_on',fail_one)
 state('light.bad','on',supported_color_modes=['brightness'])
 r=await run('light_1_brightness_up',channel_1_targets=['light.bad','light.a']);assert len(r)==1,r
 tests+=2
 print(f'PASS: blueprint + automation schema + recursive actions + {tests} real HA script cases; service endpoints simulated.')
 await h.async_stop()
asyncio.run(main())
