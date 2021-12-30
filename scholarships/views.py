import datetime
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core import serializers

from users.models import ManagerTeam, Scholar, ScholarTeam
from .forms import EditScholarshipForm, RoninForm
from .models import Scholarship, Ronin, TotalDailySlp
from tasks.models import Task
from payments.models import Payment
from payments.views import payment_view

import pandas as pd
import numpy as np
import json
import time

from metamaxie_proj.local_api import local_api, currency



@login_required
def scholarships_table(request):

    api = local_api(request.user)

    ronins = Ronin.objects.all().filter(owner=request.user)
    ronin_list = []
    for ronin in ronins:
        ronin_list.append(ronin)

    for i in range(len(api)):
        api[i]['ronin'] = ronin_list[i]

    for item in api:
        s = Scholarship.objects.filter(owner=request.user).get(ronin=item['ronin'])
        s.scholarship=item['name']
        s.lifetime_slp = item['lifetime_slp']
        s.last_claim = item['last_claim']
        s.total_slp = item['total_slp']
        s.in_game_slp = item['in_game_slp']
        s.built_up_slp = item['lifetime_slp'] + item['ronin_slp']
        s.mmr = item['mmr']
        s.owner = request.user
        s.save()

    qs = Scholarship.objects.all().values().filter(owner=request.user)
    if len(qs)!=0:
        df_scholarship = pd.DataFrame(qs)
        df_scholarship['now'] = timezone.now()
        df_scholarship['now'] = pd.to_datetime(df_scholarship['now'].dt.strftime('%Y-%m-%d'))
        df_scholarship['last_claim'] = pd.to_datetime(df_scholarship['last_claim'].dt.strftime('%Y-%m-%d'))
        #df_scholarship['daily_average'] = df_scholarship['in_game_slp'] / ((df_scholarship['now'] - df_scholarship['last_claim']) / np.timedelta64(1, 'D'))
        df_scholarship.loc[df_scholarship['in_game_slp']==0, 'daily_average'] = 0
        df_scholarship.loc[df_scholarship['in_game_slp']>0, 'daily_average'] = df_scholarship['in_game_slp'] / ((df_scholarship['now'] - df_scholarship['last_claim']) / np.timedelta64(1, 'D'))

        daily_average_list = df_scholarship['daily_average'].tolist()
        print('dadadadada', len(daily_average_list), daily_average_list)

        ronins = Ronin.objects.all().filter(owner=request.user)
        ronin_list = []
        for ronin in ronins:
            ronin_list.append(str(ronin))

        dict_scholarship = df_scholarship.to_dict('records')
        
        # for i in range(len(api)):
        #     api[i]['daily_average'] = daily_average_list[i]
        #     api[i]['ronin'] = ronin_list[i]

        for item in dict_scholarship:
            s, _ = Scholarship.objects.filter(owner=request.user).get_or_create(scholarship=item['scholarship'])
            s.daily_average = item['daily_average']
            s.owner = request.user
            s.save()

        manager = ManagerTeam.objects.get(manager=request.user)
        my_scholars = list(ScholarTeam.objects.filter(team_code=manager.id))
        scholars = Scholar.objects.filter(username__in=my_scholars).values()
        df_scholars = pd.DataFrame(scholars)

        df_scholars = df_scholars.rename(columns={'id': 'scholar_id'})
        
        if len(scholars)!=0:
            df_merged = pd.merge(df_scholarship[df_scholarship['scholar_id'].notna()], df_scholars, on="scholar_id")
            df_merged.rename(columns={"username": "scholar"}, inplace=True)

            # ////////////////////////////////
            # start add daily_slp_earned column

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

                scholars_team = ScholarTeam.objects.all().values()
                df_scholar_team = pd.DataFrame(scholars_team)
                df_scholar_team = df_scholar_team.rename(columns={'id': 'scholar_team_id'})
                df_merged_b = pd.merge(df_scholar_team, df_tasks, on="scholar_team_id")
                df_merged_c = pd.merge(df_merged, df_merged_b, on="scholar_id")


                for index, row in df_merged_c.iterrows():
                    if row['task_id']==0:
                        df_merged_c.loc[df_merged_c['task_id']==0, 'daily_slp_earned'] = df_merged_c['daily_average'] #round(df_merged_c['last_claim_amount']/2)
                        df_merged_c['daily_slp_paid'] = df_merged_c['daily_average'] - df_merged_c['daily_slp_earned']
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
                                df_merged_c.loc[(df_merged_c['daily_average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['daily_average']>=rate_var1), 'daily_slp_earned'] = rate_var1
                                df_merged_c.loc[(df_merged_c['daily_average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['daily_average']<rate_var1), 'daily_slp_earned'] = df_merged_c['daily_average']
                                df_merged_c.loc[(df_merged_c['daily_average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==False), 'daily_slp_earned'] = round(df_merged_c['daily_average'] * rate_var1/100)
                                df_merged_c.loc[(df_merged_c['daily_average']>=task_var1) & (df_merged_c['daily_average']<2000) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==False), 'daily_slp_earned'] = df_merged_c['daily_average'] * rate_var2/100
                            tasks1(task_1, rate_1, rate_2, fixed_rate)
                            df_merged_c['daily_slp_paid'] = df_merged_c['daily_average'] - df_merged_c['daily_slp_earned']
                        else:
                            df_merged_c.loc[(df_merged_c['daily_average']>=2000) & (df_merged_c['daily_average']<3000), 'daily_slp_earned'] = df_merged_c['daily_average'] * 50/100
                            df_merged_c.loc[(df_merged_c['daily_average']>=3000) & (df_merged_c['daily_average']<4000), 'daily_slp_earned'] = df_merged_c['daily_average'] * 50/100
                            df_merged_c.loc[df_merged_c['daily_average']>=4000, 'daily_slp_earned'] = round(df_merged_c['daily_average'] * 50/100)

                        if task_1!=None and task_2!=None and task_3==None:
                            def tasks12(task_var1, task_var2, rate_var1, rate_var2, rate_var3, fixed_rate_var):
                                df_merged_c.loc[(df_merged_c['daily_average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['daily_average']>=rate_var1), 'daily_slp_earned'] = rate_var1
                                df_merged_c.loc[(df_merged_c['daily_average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['daily_average']<rate_var1), 'daily_slp_earned'] = df_merged_c['daily_average']
                                df_merged_c.loc[(df_merged_c['daily_average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==False), 'daily_slp_earned'] = round(df_merged_c['daily_average'] * rate_var1/100)
                                df_merged_c.loc[(df_merged_c['daily_average']>=task_var1) & (df_merged_c['daily_average']<task_var2) & (df_merged_c['task_id']==row['task_id']), 'daily_slp_earned'] = df_merged_c['daily_average'] * rate_var2/100
                                df_merged_c.loc[(df_merged_c['daily_average']>=task_var2) & (df_merged_c['daily_average']<3000) & (df_merged_c['task_id']==row['task_id']), 'daily_slp_earned'] = df_merged_c['daily_average'] * rate_var3/100
                            tasks12(task_1, task_2, rate_1, rate_2, rate_3, fixed_rate)
                            df_merged_c['daily_slp_paid'] = df_merged_c['daily_average'] - df_merged_c['daily_slp_earned']
                        else:
                            df_merged_c.loc[(df_merged_c['daily_average']>=3000) & (df_merged_c['daily_average']<4000), 'daily_slp_earned'] = df_merged_c['daily_average'] * 50/100
                            df_merged_c.loc[df_merged_c['daily_average']>=4000, 'daily_slp_earned'] = df_merged_c['daily_average'] * 50/100

                        if task_1!=None and task_2!=None and task_3!=None and task_4==None:
                            def tasks123(task_var1, task_var2, task_var3, rate_var1, rate_var2, rate_var3, rate_var4, fixed_rate_var):
                                df_merged_c.loc[(df_merged_c['daily_average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['daily_average']>=rate_var1), 'daily_slp_earned'] = rate_var1
                                df_merged_c.loc[(df_merged_c['daily_average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['daily_average']<rate_var1), 'daily_slp_earned'] = df_merged_c['daily_average']
                                df_merged_c.loc[(df_merged_c['daily_average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==False), 'daily_slp_earned'] = round(df_merged_c['daily_average'] * rate_var1/100)
                                df_merged_c.loc[(df_merged_c['daily_average']>=task_var1) & (df_merged_c['daily_average']<task_var2) & (df_merged_c['task_id']==row['task_id']), 'daily_slp_earned'] = df_merged_c['daily_average'] * rate_var2/100
                                df_merged_c.loc[(df_merged_c['daily_average']>=task_var2) & (df_merged_c['daily_average']<task_var3) & (df_merged_c['task_id']==row['task_id']), 'daily_slp_earned'] = df_merged_c['daily_average'] * rate_var3/100
                                df_merged_c.loc[(df_merged_c['daily_average']>=task_var3) & (df_merged_c['daily_average']<4000) & (df_merged_c['task_id']==row['task_id']), 'daily_slp_earned'] = df_merged_c['daily_average'] * rate_var4/100
                            tasks123(task_1, task_2, task_3, rate_1, rate_2, rate_3, rate_4, fixed_rate)
                            df_merged_c['daily_slp_paid'] = df_merged_c['daily_average'] - df_merged_c['daily_slp_earned']
                        else:
                            df_merged_c.loc[df_merged_c['daily_average']>=4000, 'daily_slp_earned'] = df_merged_c['daily_average'] * 50/100

                        if task_1!=None and task_2!=None and task_3!=None and task_4!=None and rate_5!=None:
                            def tasks1234(task_var1, task_var2, task_var3, task_var4, rate_var1, rate_var2, rate_var3, rate_var4, rate_var5, fixed_rate_var):
                                df_merged_c.loc[(df_merged_c['daily_average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['daily_average']>=rate_var1), 'daily_slp_earned'] = rate_var1
                                df_merged_c.loc[(df_merged_c['daily_average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==True) & (df_merged_c['daily_average']<rate_var1), 'daily_slp_earned'] = df_merged_c['daily_average']
                                df_merged_c.loc[(df_merged_c['daily_average']<task_var1) & (df_merged_c['task_id']==row['task_id']) & (fixed_rate_var==False), 'daily_slp_earned'] = round(df_merged_c['daily_average'] * rate_var1/100)
                                df_merged_c.loc[(df_merged_c['daily_average']>=task_var1) & (df_merged_c['daily_average']<task_var2) & (df_merged_c['task_id']==row['task_id']), 'daily_slp_earned'] = df_merged_c['daily_average'] * rate_var2/100
                                df_merged_c.loc[(df_merged_c['daily_average']>=task_var2) & (df_merged_c['daily_average']<task_var3) & (df_merged_c['task_id']==row['task_id']), 'daily_slp_earned'] = df_merged_c['daily_average'] * rate_var3/100
                                df_merged_c.loc[(df_merged_c['daily_average']>=task_var3) & (df_merged_c['daily_average']<task_var4) & (df_merged_c['task_id']==row['task_id']), 'daily_slp_earned'] = df_merged_c['daily_average'] * rate_var4/100
                                df_merged_c.loc[(df_merged_c['daily_average']>=task_var4) & (df_merged_c['task_id']==row['task_id']), 'daily_slp_earned'] = df_merged_c['daily_average'] * rate_var5/100
                            tasks1234(task_1, task_2, task_3, task_4, rate_1, rate_2, rate_3, rate_4, rate_5, fixed_rate)
                            df_merged_c['daily_slp_paid'] = df_merged_c['daily_average'] - df_merged_c['daily_slp_earned']

                # ////////////////////////////////

                df = df_merged_c[[
                    'scholarship', 
                    'scholar', 
                    'last_claim',  
                    'built_up_slp', 
                    'in_game_slp', 
                    'mmr', 
                    'daily_average',
                    'daily_slp_earned',
                    'daily_slp_paid',
                ]].sort_values(by='mmr', ascending=False)

                df['next_claim'] = (df['last_claim'] + np.timedelta64(14, 'D')) - df_scholarship['now']

                df['next_claim'] = df['next_claim'].astype(str) # convert to string to remove time.

                pd.options.display.float_format = '{:,.2f}'.format

                df = df.dropna(how='any',axis=0)

                # ////////////////////////////////

                slp_usd = currency()
                slp_usd = slp_usd['smooth-love-potion']['usd']

                dict = df.to_dict('records')
            
                for item in dict:
                    s = Scholarship.objects.filter(owner=request.user, scholarship=item['scholarship']).last()
                    s.daily_slp_earned = item['daily_slp_earned']
                    s.daily_slp_paid = item['daily_slp_paid']
                    s.daily_fiat_earned = slp_usd * item['daily_slp_earned']
                    s.daily_fiat_paid = slp_usd * item['daily_slp_paid']
                    s.next_claim = item['next_claim']
                    s.save()

                total_daily_slp_earned = df['daily_slp_earned'].sum()
                total_daily_slp_paid = df['daily_slp_paid'].sum()
                total_daily_fiat_earned = slp_usd * df['daily_slp_earned'].sum()
                total_daily_fiat_paid = slp_usd * df['daily_slp_paid'].sum()

                t, _ = TotalDailySlp.objects.get_or_create(owner=request.user)
                t.total_daily_slp_earned = total_daily_slp_earned
                t.total_daily_slp_paid = total_daily_slp_paid
                t.total_daily_fiat_earned = total_daily_fiat_earned
                t.total_daily_fiat_paid = total_daily_fiat_paid
                t.save()

                # ////////////////////////////////

                context = {
                    # 'df_scholarship': df_scholarship.to_html,
                    # 'df_scholars': df_scholars.to_html,
                    # 'df_merged': df_merged.to_html,
                    # 'df_tasks': df_tasks.to_html,
                    # 'df_scholar_team': df_scholar_team.to_html,        
                    # 'df_merged_b': df_merged_b.to_html,
                    # 'df_merged_c': df_merged_c.to_html,
                    'df': df.to_html(classes=["table", "table-bordered", "table-striped", "table-hover"]),
                }

                return render(request, 'scholarships/scholarships_table.html', context)
            except:
                msg3 = 'Only one rule is allowed per scholar. Please remove the scholar from one of the rules.'
                return render(request, 'scholarships/scholarships_table.html', {'msg3': msg3})
        else:
            msg1 = 'You must assign a scholar to a scholarship in order to be listed in the table.'
            return render(request, 'scholarships/scholarships_table.html', {'msg1': msg1})
    else:
        msg2 = 'No scholarships have been added yet.'
        return render(request, 'scholarships/scholarships_table.html', {'msg2': msg2})

@login_required
def scholarships(request):
    scholarships = Scholarship.objects.order_by('last_claim', 'scholarship', 'scholar').filter(owner=request.user)
    scholarships_json = serializers.serialize("json", Scholarship.objects.filter(owner=request.user))

    if len(scholarships)!=0:
        #reload the scholarships table page to get daily average
        if request.user.type=='MANAGER':
            if Scholarship.objects.filter(owner=request.user).exists():
                if Scholarship.objects.filter(owner=request.user).last().daily_average==None:
                    scholarships_table(request)
                    time.sleep(5)
                    payment_view(request)

        # create message
        scholar_list = []
        scholarships = Scholarship.objects.filter(owner=request.user)
        for s in scholarships:
            if s.scholar!=None:
                scholar_list.append(s.scholar)
                if len(scholar_list)!=0:
                    if len(set(scholar_list))!=len(scholar_list):
                        msg = "Please, assign a scholar only one scholarship, otherwise, they will not be able to access their account. Click 'Assign a scholar' link again and in the dropdown menu select blank."
                    else:
                        msg = ''
            elif s.scholar==None and len(scholar_list)==0:
                msg = ''

        context = {
            'scholarships': scholarships,
            'scholarships_json': scholarships_json,
            'msg': msg,
            }

        #print('fefefefefe', scholar_list)

        print('bgbgbgbgb', request.user.type)

        return render(request, 'scholarships/scholarships_cards.html', context)
    else:
        msg2 = ''
        return render(request, 'scholarships/scholarships_cards.html', {'msg2': msg2})


@login_required
def add_scholarship(request):
    if request.method != 'POST':
        form = RoninForm()
    else:
        form = RoninForm(data=request.POST)
        if form.is_valid():
            add_scholarship = form.save(commit=False)
            add_scholarship.owner = request.user
            add_scholarship.save()
            return redirect('scholarships:scholarships_cards')

    context = {
        'form': form,
        }
    
    return render(request, 'scholarships/add_scholarship.html', context)


@login_required
def edit_scholarship(request, scholarship_id):
    try:
        scholarship = Scholarship.objects.filter(owner=request.user).get(id=scholarship_id)
    except Scholarship.DoesNotExist:
        raise Http404("Scholarship does not exist")

    manager = ManagerTeam.objects.get(manager=request.user)
    scholars = list(ScholarTeam.objects.filter(team_code=manager.id))

    if len(scholars)!=0:
        if request.method != 'POST':
            form = EditScholarshipForm(instance=scholarship)
        else:
            form = EditScholarshipForm(instance=scholarship, data=request.POST)
            if form.is_valid():
                edit_scholaship = form.save(commit=False)
                edit_scholaship.owner = request.user
                edit_scholaship.save()
                scholarships_table(request)
                #time.sleep(5)
                payment_view(request)
                return redirect('scholarships:scholarships_cards')

        context = {
            'scholarship': scholarship, 
            'form': form,
            }

        return render(request, 'scholarships/edit_scholarship.html', context)
    else:
        msg = ' '
        context = {
            'scholarship': scholarship, 
            'manager': manager,
            'msg': msg,
            }
        return render(request, 'scholarships/edit_scholarship.html', context)



@login_required
def remove_scholarship(request, scholarship_id):
    scholarship = Scholarship.objects.filter(owner=request.user).get(id=scholarship_id)
    ronin = Ronin.objects.filter(ronin=scholarship.ronin)
    payment = Payment.objects.filter(ronin=scholarship.ronin).first()

    if request.method=='POST':
        ronin.delete()
        payment.delete()
        scholarships_table(request)

        return HttpResponseRedirect("/")
    
    context = {'ronin': ronin, 'scholarship': scholarship}

    return render(request, 'scholarships/remove_scholarship.html', context)


@login_required
def scholars(request):
    manager = ManagerTeam.objects.get(manager=request.user)
    scholars = ScholarTeam.objects.filter(team_code=manager.id)

    context = {'scholars': scholars}

    return render(request, 'scholarships/scholars.html', context)


@login_required
def disconnect_scholar(request, scholar_id):
    scholar = ScholarTeam.objects.get(id=scholar_id)
    scholar2 = Scholar.objects.get(scholarteam=scholar)

    if request.method=='POST':
        scholar.team_code = None
        scholar.save()
        if Task.objects.filter(scholar=scholar).exists():
            task = Task.objects.get(scholar=scholar)
            taskscholar = task.scholar.get(id=scholar_id)
            task.scholar.remove(taskscholar)
            task.save()
        if Scholarship.objects.filter(scholar=scholar2).exists():
            scholarscholarships = Scholarship.objects.filter(scholar=scholar2)
            for s in scholarscholarships:
                s.scholar = None
                s.save()

        return HttpResponseRedirect("/scholars")

    context = {'scholar': scholar}

    return render(request, 'scholarships/disconnect_scholar.html', context)


def refresh(request):
    scholarships_table(request)
    return redirect('scholarships:scholarships_cards')



        


