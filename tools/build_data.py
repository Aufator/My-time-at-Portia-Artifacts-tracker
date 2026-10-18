import json,re,os,collections,pandas as pd
U='/mnt/user-data/uploads/'; OUT='/home/claude/portia-wiki/data/'
R=lambda f:pd.read_csv(U+f,sep=';',dtype=str,encoding='utf-8-sig').fillna('')
tr={r['ID']:r for r in json.load(open(U+'Translation_hint_en_ru.json',encoding='utf-8'))}
clean=lambda s:re.sub(r'<[^>]+>','',s).replace('\r','').strip()
ru=lambda k:clean(tr.get(k,{}).get('Russian','')) if k else ''
rep=collections.OrderedDict()
it=R('portia_all_items_ru.csv')
items={}
hidden=0
for r in it.to_dict('records'):
    name=r['Name_RU'].strip()
    if not name: hidden+=1; continue
    items[r['Props_Id']]=dict(id=r['Props_Id'],ru=name,en=r['Name_EN'].strip(),type=r['Item_Type'].strip(),
      desc=ru(r['Props_Explain_One']),effect=ru(r['Effect']),buy=int(r['Buy_Price'] or 0),sell=(int(r['Sell_Price']) if re.fullmatch(r'-?\d+',r['Sell_Price'] or '0') else r['Sell_Price']),
      rare=r['Rare_Lv'],gift=r['IsGift']=='True' or r['IsGift']=='1',tag=r['Gift_TagID'],
      icon=os.path.basename(r['Icon_Path']),src=r['SourceDes'],ver=r['InVersion'])
rep['items']=len(items); rep['sell_price_nonnumeric']=[(i['ru'],i['sell']) for i in items.values() if isinstance(i['sell'],str)]; rep['items_hidden_no_name']=hidden
rep['items_no_desc']=sum(1 for i in items.values() if not i['desc'])
# NPC
npc=R('portia_npcs.csv'); g=R('portia_npc_gifts_final.csv')
N={}
for r in npc.to_dict('records'):
    N[r['npc_id']]=dict(id=r['npc_id'],ru=r['name_ru'],en=r['name_en'],birthday=r['birthday'],sex=r['sex'],faction=r['faction'],gifts={'Отличный':[],'Хороший':[],'Не нравится':[],'Ненавистный':[]})
conf=[]
seen={}
for r in g.to_dict('records'):
    n=N[r['NPC_ID']]; k=(r['NPC_ID'],r['Item_ID'])
    if k in seen and seen[k]!=r['Реакция']: conf.append((n['ru'],r['Подарок_RU'],seen[k],r['Реакция']))
    seen[k]=r['Реакция']; n['gifts'][r['Реакция']].append(r['Item_ID'])
rep['npcs']=len(N); rep['gift_rows']=len(g); rep['gift_conflicts']=len(conf); rep['gift_conflict_list']=conf
rep['gift_items_missing_in_items']=sorted({r['Item_ID'] for r in g.to_dict('records')}-set(items))[:10]
# crafting
def recipes(df,idc,extra):
    out={};
    for r in df.to_dict('records'):
        x=out.setdefault(r[idc],dict(id=r[idc],result=r['result_item_id'],name=r.get('recipe_name_ru') or r['result_name_ru'],mats=[],**{k:r[k] for k in extra}))
        if r['material_id']:
            m=(r['material_id'],int(r['material_count'] or 1))
            if m not in x['mats']: x['mats'].append(m)
    return list(out.values())
craft=recipes(R('portia_crafting_recipes.csv'),'recipe_id',['crafting_time','experience','cost','unlock_level'])
station=recipes(R('Рецепты_станция_крафта.csv'),'recipe_id',['station_level','crafting_time','experience'])
rep['craft']=len(craft); rep['station']=len(station)
rep['craft_unlock99']=sum(1 for c in craft if c['unlock_level']=='99')
rep['recipe_ids_not_in_items']=sorted(({m[0] for c in craft+station for m in c['mats']}|{c['result'] for c in craft+station})-set(items))[:10]
# cooking
ck=R('portia_cooking_recipes.csv').drop_duplicates()
cook={}
for r in ck.to_dict('records'):
    x=cook.setdefault(r['recipe_id'],dict(id=r['recipe_id'],food=r['food_id'],name=r['food_name_ru'],ings=[]))
    x['ings'].append((r['material_id'],r['material_name_ru'] or None,int(r['material_count'] or 1)))
rep['cook']=len(cook); rep['cook_group_ings']=sum(1 for c in cook.values() for i in c['ings'] if i[1] is None)
rep['cook_food_not_in_items']=sorted({c['food'] for c in cook.values()}-set(items))[:10]
for n,o in [('items',items),('npcs',N),('craft',craft),('station',station),('cooking',list(cook.values()))]:
    json.dump(o,open(OUT+n+'.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
json.dump(rep,open(OUT+'_report.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(json.dumps(rep,ensure_ascii=False,indent=1)[:2500])
