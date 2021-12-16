from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import EditScholarForm, EditManagerForm, EditScholarFormMore
from users.models import User, ManagerTeam, ScholarTeam
from scholarships.models import Scholarship
from payments.models import Payment, TotalScholarSlp


@login_required
def my_profile(request):
    profile = User.objects.get(username=request.user)    
    if profile.type==User.Type.MANAGER:
        team_code = ManagerTeam.objects.get(manager=request.user)

        context = {
            'profile': profile, 
            'team_code': team_code,
            }

        return render(request, 'profiles/my_profile.html', context)
    else:
        scholarteam = ScholarTeam.objects.get(scholar=request.user)
        team_code = scholarteam.team_code 

        if team_code!=None and Scholarship.objects.filter(scholar=request.user).exists()==False:                        
            context = {
                        'profile': profile, 
                        'team_code': team_code,
                        }
            return render(request, 'profiles/my_profile.html', context)

        elif team_code!=None and Scholarship.objects.filter(scholar=request.user).exists():
            payment = Payment.objects.filter(scholar=request.user).last()
            scholarship = Scholarship.objects.get(scholar=request.user)
            scholar_payment = TotalScholarSlp.objects.get(owner=request.user)

            context = {
                'profile': profile, 
                'team_code': team_code,
                'scholarship': scholarship,
                'payment': payment,
                'scholar_payment': scholar_payment,
                }

            return render(request, 'profiles/my_profile.html', context)
        else:
            msg = 'Please ask your manager for the team code'
            return render(request, 'profiles/my_profile.html', {'msg': msg})


@login_required
def edit_profile(request):
    user = User.objects.get(username=request.user)
    if user.type==User.Type.MANAGER:
        if request.method!='POST':
            form = EditManagerForm(instance=request.user)
        else:
            form = EditManagerForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profiles:my_profile')

        context = {
            'user': user, 
            'form': form,
            }

        return render(request, 'profiles/edit_profile.html', context)

    else:
        team_code = ScholarTeam.objects.get(scholar=request.user)
        if request.method!='POST':
            form = EditScholarForm(instance=request.user)
            form_more = EditScholarFormMore(instance=team_code)
        else:
            form = EditScholarForm(request.POST, request.FILES, instance=request.user)
            form_more = EditScholarFormMore(instance=team_code, data=request.POST)
            if form.is_valid():
                form.save()
            if form_more.is_valid():
                form_more.save()
                return redirect('profiles:my_profile')

        context = {
            'user': user, 
            'form': form, 
            'form_more': form_more
            }

        return render(request, 'profiles/edit_profile.html', context)


@login_required
def rules(request):
    scholarteam = ScholarTeam.objects.get(scholar=request.user)
    task = scholarteam.task_set.all()
    context = {'task': task}

    return render(request, 'profiles/rules.html', context)




