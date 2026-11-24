import csv,collections
G='005C000000B7DLFIA3'
BARRY='005PC000010bBqPYAU'; JOS='005PC00000vtAHFYA2'; JAMAL='0053b00000BpN5fAAF'; GUIDO='0053b00000BmgOyAAJ'
names={BARRY:'Barry',JOS:'Jos',JAMAL:'Jamal',GUIDO:'Guido'}
HOLD_ACCTS={'0013b00001pIEMqAAO','0013b00001t4u6eAAA','0013b00001t4xOdAAI'}  # no country, ask Fran
def terr_owner(t,country):
    if t in ('EU50','EU60'): return BARRY
    if t in ('EU42','EU43','EU70','AP20'): return JOS
    if t=='EU40': return JOS if country=='HU' else GUIDO
    return None
R=lambda f: list(csv.DictReader(open(f)))
plan={}; hold=collections.defaultdict(list)
acct_target={}
out=[]
for r in R('accounts.csv'):
    if r['Id'] in HOLD_ACCTS: hold['Account'].append((r['Id'],r['Name'],'no country - ask Fran')); continue
    o=terr_owner(r['Territory__r.Name'],r['BillingCountry'])
    if not o: hold['Account'].append((r['Id'],r['Name'],'territory '+r['Territory__r.Name'])); continue
    acct_target[r['Id']]=o; out.append((r['Id'],o))
plan['Account']=out
def related(rows,obj):
    out=[]
    for r in rows:
        a=r['AccountId']
        if a in HOLD_ACCTS: hold[obj].append((r['Id'],'','on held account')); continue
        if a and r['Account.OwnerId']==G:
            o=acct_target.get(a)
        elif a and r['Account.Owner.IsActive']=='true':
            o=r['Account.OwnerId']
        else:
            o=terr_owner(r['Account.Territory__r.Name'],r['Account.BillingCountry'])
        if not o: hold[obj].append((r['Id'],'',f"acct {a} terr {r['Account.Territory__r.Name']}")); continue
        out.append((r['Id'],o))
    return out
plan['Contact']=related(R('contacts.csv'),'Contact')
plan['Opportunity']=related(R('opps.csv'),'Opportunity')
plan['Lead']=[(r['Id'],JAMAL) for r in R('leads.csv')]
tdel=[];tre=[]
for r in R('tasks.csv'):
    if r['ActivityDate'] and r['ActivityDate']<'2025-11-24' or 'Lubricant Expo' in r['Subject']: tdel.append(r['Id']); continue
    tre.append(r)
for r in tre:
    a=r['AccountId']; o=acct_target.get(a) if r['Account.OwnerId']==G else (r['Account.OwnerId'] or None)
    if o: plan.setdefault('Task',[]).append((r['Id'],o))
    else: hold['Task'].append((r['Id'],r['Subject'],'no target'))
plan['City__c']=[(r['Id'],BARRY) for r in R('city.csv') if r['Name']=='Hyvinkää']
for r in R('city.csv'):
    if r['Name']!='Hyvinkää': hold['City__c'].append((r['Id'],r['Name'],'not in Barry region'))
for obj,rows in plan.items():
    with open(f'upd_{obj}.csv','w',newline='') as f:
        w=csv.writer(f); w.writerow(['Id','OwnerId']); w.writerows(rows)
    c=collections.Counter(names.get(o,o) for _,o in rows)
    print(obj,len(rows),dict(c))
with open('del_Task.csv','w') as f: f.write('Id\n'+'\n'.join(tdel)+'\n')
print('Task delete',len(tdel))
for k,v in hold.items(): print('HOLD',k,len(v),v[:8])
