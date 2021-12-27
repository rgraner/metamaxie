from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import pandas as pd
import numpy as np
import time

from .models import Payment, TotalSlp, TotalScholarSlp
from tasks.models import Task
from scholarships.models import Scholarship, Ronin
from users.models import Scholar, ScholarTeam, ManagerTeam

from metamaxie_proj.local_api import local_api, currency


@login_required
def payment_view(request):

    api = local_api(request.user)

    ronins = Ronin.objects.all().filter(owner=request.user)
    ronin_list = []
    for ronin in ronins:
        ronin_list.append(str(ronin))

    for i in range(len(api)):
        api[i]['ronin'] = ronin_list[i]


    for item in api:
        p, _ = Payment.objects.get_or_create(last_claim = item['last_claim'])
        p.scholarship = item['name']
        p.ronin = item['ronin']
        p.ronin_slp = item['ronin_slp']
        p.lifetime_slp = item['lifetime_slp']
        s = Scholarship.objects.get(scholarship=p.scholarship)
        p.scholar = s.scholar
        p.owner = request.user
        p.save()

    qs = Payment.objects.all().values().filter(owner=request.user)
    df_payment = pd.DataFrame(qs)


    if len(qs)!=0:
        df_payment['built_up_slp'] = df_payment['ronin_slp'] + df_payment['lifetime_slp']
        df_payment['built_up_slp_shift'] = df_payment.groupby('scholarship')['built_up_slp'].shift(1)
        df_payment['last_claim_amount'] = df_payment['built_up_slp'] - df_payment['built_up_slp_shift']
        df_payment['last_claim_shift'] = df_payment.groupby('scholarship')['last_claim'].shift(1)
        df_payment['period'] = round((df_payment['last_claim'] - df_payment['last_claim_shift']) / np.timedelta64(1, 'D'))
        df_payment['average'] = df_payment['last_claim_amount'] / df_payment['period']

        manager = ManagerTeam.objects.get(manager=request.user)
        my_scholars = list(ScholarTeam.objects.filter(team_code=manager.id))

        scholars = Scholar.objects.filter(username__in=my_scholars).values()
        df_scholars = pd.DataFrame(scholars)

        scholars_team = ScholarTeam.objects.all().values()
        df_scholar_team = pd.DataFrame(scholars_team)

        df_scholars = df_scholars.rename(columns={'id': 'scholar_id'})

        if Payment.objects.filter(owner=request.user, scholar__isnull=False).count()>0:
            df_merged = pd.merge(df_payment[df_payment['scholar_id'].notna()], df_scholars, on="scholar_id")
            df_merged = pd.merge(df_merged, df_scholar_team, on="scholar_id")

            tasks = {}
            for my_scholar in my_scholars:
                my_scholars_task = list(my_scholar.task_set.all().values_list('id'))
                my_scholars_task = str(my_scholars_task)[1:-1]
                if len(my_scholars_task)==0:
                    tasks[my_scholar.id] = '-'
                else:
                    tasks[my_scholar.id] = my_scholars_task

            df_tasks = pd.DataFrame.from_dict(tasks, orient='index', columns=['task_id'])
            df_tasks['task_id'] = df_tasks['task_id'].str.replace(r"(","").str.replace(r")","").str.replace(r",","")
            df_tasks['scholar_team_id'] = df_tasks.index
            df_tasks = df_tasks.replace('-', np.nan)

            try:
                df_tasks['task_id'] = df_tasks['task_id'].fillna(0).astype(int)

                df_scholar_team = df_scholar_team.rename(columns={'id': 'scholar_team_id'})
                df_merged_b = pd.merge(df_scholar_team, df_tasks, on="scholar_team_id")
                df_merged_c = pd.merge(df_merged, df_merged_b, on="scholar_id")


                for index, row in df_merged_b.iterrows():
                    if row['task_id']==0:
                        df_merged_c.loc[(df_merged_c['task_id']==0) & (df_merged_c['last_claim_amount'].notna()), 'slp_earned'] = df_merged_c['average']* df_merged_c['period'] #round(df_merged_c['last_claim_amount']/2)
                        df_merged_c['slp_paid'] = df_merged_c['last_claim_amount'] - df_merged_c['slp_earned']
                    else:
                        pc = Task.objects.get(id=row['task_id'])
                        task_1 = pc.task_1
                        task_2 = pc.task_2
                        task_3 = pc.task_3
                        task_4 = pc.task_4
                        rate_1 = pc.rate_1
                        rate_2 = pc.rate_2
                        rate_3 = pc.rate_3
                        rate_4 = pc.rate_4
                        rate_5 = pc.rate_5
                        fixed_rate = pc.fixed_rate

                        if task_1!=None and task_2==None:
                            def tasks1(task_var1, rate_var1, rate_var2, fixed_rate_var):
                                df_merged_c.loc[(df_merged_c['average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['average']>=rate_var1), 'slp_earned'] = rate_var1 * df_merged_c['period']
                                df_merged_c.loc[(df_merged_c['average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['average']<rate_var1), 'slp_earned'] = df_merged_c['average'] * df_merged_c['period']
                                df_merged_c.loc[(df_merged_c['average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==False), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * rate_var1/100)
                                df_merged_c.loc[(df_merged_c['average']>=task_var1) & (df_merged_c['average']<2000) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate==False), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * rate_var2/100)
                            tasks1(task_1, rate_1, rate_2, fixed_rate)
                            df_merged_c['slp_paid'] = df_merged_c['last_claim_amount'] - df_merged_c['slp_earned']
                        else:
                            df_merged_c.loc[(df_merged_c['average']>=2000) & (df_merged_c['average']<3000), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * 50/100)
                            df_merged_c.loc[(df_merged_c['average']>=3000) & (df_merged_c['average']<4000), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * 50/100)
                            df_merged_c.loc[df_merged_c['average']>=4000, 'slp_earned'] = round(df_merged_c['last_claim_amount'] * 50/100)

                        if task_1!=None and task_2!=None and task_3==None:
                            def tasks12(task_var1, task_var2, rate_var1, rate_var2, rate_var3, fixed_rate_var):
                                df_merged_c.loc[(df_merged_c['average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['average']>=rate_var1), 'slp_earned'] = rate_var1 * df_merged_c['period']
                                df_merged_c.loc[(df_merged_c['average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['average']<rate_var1), 'slp_earned'] = df_merged_c['average'] * df_merged_c['period']
                                df_merged_c.loc[(df_merged_c['average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==False), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * rate_var1/100)
                                df_merged_c.loc[(df_merged_c['average']>=task_var1) & (df_merged_c['average']<task_var2) & (df_merged_c['task_id']==row['task_id']), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * rate_var2/100)
                                df_merged_c.loc[(df_merged_c['average']>=task_var2) & (df_merged_c['average']<3000) & (df_merged_c['task_id']==row['task_id']), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * rate_var3/100)
                            tasks12(task_1, task_2, rate_1, rate_2, rate_3, fixed_rate)
                            df_merged_c['slp_paid'] = df_merged_c['last_claim_amount'] - df_merged_c['slp_earned']
                        else:
                            df_merged_c.loc[(df_merged_c['average']>=3000) & (df_merged_c['average']<4000), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * 50/100)
                            df_merged_c.loc[df_merged_c['average']>=4000, 'slp_earned'] = round(df_merged_c['last_claim_amount'] * 50/100)

                        if task_1!=None and task_2!=None and task_3!=None and task_4==None:
                            def tasks123(task_var1, task_var2, task_var3, rate_var1, rate_var2, rate_var3, rate_var4, fixed_rate_var):
                                df_merged_c.loc[(df_merged_c['average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['average']>=rate_var1), 'slp_earned'] = rate_var1 * df_merged_c['period']
                                df_merged_c.loc[(df_merged_c['average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['average']<rate_var1), 'slp_earned'] = df_merged_c['average'] * df_merged_c['period']
                                df_merged_c.loc[(df_merged_c['average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==False), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * rate_var1/100)
                                df_merged_c.loc[(df_merged_c['average']>=task_var1) & (df_merged_c['average']<task_var2) & (df_merged_c['task_id']==row['task_id']), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * rate_var2/100)
                                df_merged_c.loc[(df_merged_c['average']>=task_var2) & (df_merged_c['average']<task_var3) & (df_merged_c['task_id']==row['task_id']), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * rate_var3/100)
                                df_merged_c.loc[(df_merged_c['average']>=task_var3) & (df_merged_c['average']<4000) & (df_merged_c['task_id']==row['task_id']), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * rate_var4/100)
                            tasks123(task_1, task_2, task_3, rate_1, rate_2, rate_3, rate_4, fixed_rate)
                            df_merged_c['slp_paid'] = df_merged_c['last_claim_amount'] - df_merged_c['slp_earned']
                        else:
                            df_merged_c.loc[df_merged_c['average']>=4000, 'slp_earned'] = round(df_merged_c['last_claim_amount'] * 50/100)

                        if task_1!=None and task_2!=None and task_3!=None and task_4!=None and rate_5!=None:
                            def tasks1234(task_var1, task_var2, task_var3, task_var4, rate_var1, rate_var2, rate_var3, rate_var4, rate_var5, fixed_rate_var):
                                df_merged_c.loc[(df_merged_c['average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['average']>=rate_var1), 'slp_earned'] = rate_var1 * df_merged_c['period']
                                df_merged_c.loc[(df_merged_c['average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['average']<rate_var1), 'slp_earned'] = df_merged_c['average'] * df_merged_c['period']
                                df_merged_c.loc[(df_merged_c['average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==False), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * rate_var1/100)
                                df_merged_c.loc[(df_merged_c['average']>=task_var1) & (df_merged_c['average']<task_var2) & (df_merged_c['task_id']==row['task_id']), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * rate_var2/100)
                                df_merged_c.loc[(df_merged_c['average']>=task_var2) & (df_merged_c['average']<task_var3) & (df_merged_c['task_id']==row['task_id']), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * rate_var3/100)
                                df_merged_c.loc[(df_merged_c['average']>=task_var3) & (df_merged_c['average']<task_var4) & (df_merged_c['task_id']==row['task_id']), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * rate_var4/100)
                                df_merged_c.loc[(df_merged_c['average']>=task_var4) & (df_merged_c['task_id']==row['task_id']), 'slp_earned'] = round(df_merged_c['last_claim_amount'] * rate_var5/100)                               
                            tasks1234(task_1, task_2, task_3, task_4, rate_1, rate_2, rate_3, rate_4, rate_5, fixed_rate)
                            df_merged_c['slp_paid'] = df_merged_c['last_claim_amount'] - df_merged_c['slp_earned']
                        
                df_merged_c.rename(columns={"username": "scholar"}, inplace=True)

                df = df_merged_c[[
                    'scholarship', 
                    'scholar',
                    'built_up_slp',
                    'last_claim',
                    'last_claim_amount',  
                    'average', 
                    'slp_paid',
                    'slp_earned',
                    ]]

                df = df.loc[df['last_claim_amount'].notna()]
                df['last_claim'] = pd.to_datetime(df['last_claim'].dt.strftime('%Y-%m-%d'))
                df['last_claim_amount'] = df['last_claim_amount'].astype(int)
                df['slp_paid'] = df['slp_paid'].astype(int)
                df['slp_earned'] = df['slp_earned'].astype(int)

                #////////////////////////////////////

                slp_usd = currency()
                slp_usd = slp_usd['smooth-love-potion']['usd']

                dict = df.to_dict('records')
        
                for item in dict:
                    p = Payment.objects.filter(owner=request.user, scholarship=item['scholarship']).last()
                    p.average = item['average']
                    p.slp_paid = item['slp_paid']
                    p.slp_earned = item['slp_earned']
                    p.buit_up_slp = item['built_up_slp']
                    p.owner = request.user
                    p.save()

                total_slp_earned = df['slp_earned'].sum()
                total_slp_paid = df['slp_paid'].sum()
                total_fiat_earned = slp_usd * df['slp_earned'].sum()
                total_fiat_paid = slp_usd * df['slp_paid'].sum()

                t, _ = TotalSlp.objects.get_or_create(owner=request.user)
                t.total_slp_earned = total_slp_earned
                t.total_slp_paid = total_slp_paid
                t.total_fiat_earned = total_fiat_earned
                t.total_fiat_paid = total_fiat_paid
                t.save()

                #////////////////////////////////////

                pd.options.display.float_format = '{:,.2f}'.format 
                        
                context = {
                    # 'df_payment': df_payment.to_html,
                    # 'df_scholars': df_scholars.to_html,
                    # 'df_merged': df_merged.to_html,
                    # 'df_scholar_team': df_scholar_team.to_html,
                    # 'df_tasks': df_tasks.to_html,
                    # 'df_merged_b': df_merged_b.to_html,
                    # 'df_merged_c': df_merged_c.to_html,             
                    'df': df.to_html(classes=["table", "table-bordered", "table-striped", "table-hover"]),
                    }

                return render(request, 'payments/payment.html', context)
            except:
                msg1 = 'please assign the scholar only one target...'
                return render(request, 'payments/payment.html', {'msg1':msg1})
        else:
            msg2 = 'there is no scholar added to scholarship.'
            return render(request, 'payments/payment.html', {'msg2':msg2})
    else:
        msg3 = 'No payments have been added yet.'
        return render(request, 'payments/payment.html', {'msg3':msg3})


def scholar_table(request):
    qs_scholar = Payment.objects.all().values().filter(scholar=request.user)
    if len(qs_scholar)!=0:
        df_scholar = pd.DataFrame(qs_scholar)
        df_scholar = df_scholar[[
            'last_claim',
            'average',
            'slp_paid'
        ]]
        df_scholar.rename(columns={"slp_paid": "slp_earned"}, inplace=True)
        df_scholar['last_claim'] = pd.to_datetime(df_scholar['last_claim'].dt.strftime('%Y-%m-%d'))

        slp_usd = currency()
        slp_usd = slp_usd['smooth-love-potion']['usd']

        total_slp_earned = df_scholar['slp_earned'].sum()
        total_fiat_earned = slp_usd * df_scholar['slp_earned'].sum()

        t, _ = TotalScholarSlp.objects.get_or_create(owner=request.user)
        t.total_slp_earned = total_slp_earned
        t.total_fiat_earned = total_fiat_earned
        t.owner = request.user
        t.save()

        df_scholar = df_scholar.dropna()

        df_scholar['slp_earned'] = df_scholar['slp_earned'].astype(int)

        pd.options.display.float_format = '{:,.2f}'.format

        context = {
            'df_scholar': df_scholar.to_html(classes=["table", "table-bordered", "table-striped", "table-hover"]),
        }

        return render(request, 'payments/scholar_table.html', context)
    else:
        msg = 'No payments have been added yet.'
        return render(request, 'payments/scholar_table.html', {'msg':msg})


