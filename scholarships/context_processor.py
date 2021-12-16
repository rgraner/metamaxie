from .models import TotalDailySlp
from payments.models import TotalSlp


def total_slp(request):
    if request.user.is_authenticated:
        total_daily_slp = TotalDailySlp.objects.filter(owner=request.user).last()
        total_slp = TotalSlp.objects.filter(owner=request.user).last()
        return {
            'total_daily_slp': total_daily_slp,
            'total_slp': total_slp
            }
    else:
        return {}
