
reward = 100
tax = 30
diminishing_factor = 0.95


def payout_calc(his_num, my_num):
    if my_num == his_num:
        return (reward * (diminishing_factor ** (his_num - 1))) - (tax / 2)
    if my_num < his_num:
        return (reward * (diminishing_factor ** (my_num - 1))) - tax
    return reward * (diminishing_factor ** (his_num - 1))


def salami_helper(his_num):
    if payout_calc(his_num, his_num + 1) > payout_calc(his_num, his_num):
        if payout_calc(his_num, his_num + 1) > payout_calc(his_num, 1):
            return his_num + 1
        return 1
    if payout_calc(his_num, his_num) > payout_calc(his_num, 1):
        return 1
    return his_num


print(payout_calc(6, 1))
