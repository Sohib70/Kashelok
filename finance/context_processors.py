from .models import UserBalance
from django.utils.formats import number_format

def user_balance(request):
    if request.user.is_authenticated:
        balance, created = UserBalance.objects.get_or_create(user=request.user)
        umumiy = (balance.cash or 0) + (balance.card or 0) + (balance.dollar or 0) * 12300

        return {
            "balance": balance,
            "umumiy_balans": number_format(umumiy, use_l10n=True, decimal_pos=0),
        }
    return {}