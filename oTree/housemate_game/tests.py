from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
import math


def rand(num):
    ret = 1
    while random.randint(1, 100) < (num + 1):
        ret += 1
    return ret


def payout_calc(his_num, my_num):
    if my_num == his_num:
        return (Constants.reward * (Constants.diminishing_factor ** (his_num - 1))) - (Constants.tax / 2)
    if my_num < his_num:
        return (Constants.reward * (Constants.diminishing_factor ** (my_num - 1))) - Constants.tax
    return Constants.reward * (Constants.diminishing_factor ** (his_num - 1))


def goldfish_helper(his_num):
        if payout_calc(his_num, his_num+1) > payout_calc(his_num, his_num):
            if payout_calc(his_num, his_num+1) > payout_calc(his_num, 1):
                return his_num + 1
            return 1
        if payout_calc(his_num, his_num) > payout_calc(his_num, 1):
            return 1
        return his_num


class PlayerBot(Bot):

    def salami(self):
        if self.subsession.round_number == 1:
            return 1
        else:
            return self.player.in_round(self.round_number - 1).time_opponent_willing_to_wait + 1

    def goldfish(self):
        if self.subsession.round_number == 1:
            return 1
        else:
            return goldfish_helper(self.player.in_round(self.round_number - 1).time_opponent_willing_to_wait)

    def tit_for_tat(self):
        if self.subsession.round_number == 1:
            return 1
        else:
            return self.player.in_round(self.round_number - 1).time_opponent_willing_to_wait

    cases = range(36)

    def play_round(self):
        conservative = 1
        greedy = math.floor(math.log(Constants.tax/Constants.reward, Constants.diminishing_factor))
        strategies = [conservative, self.goldfish(), greedy, rand(90), self.salami(),
                      self.tit_for_tat()]
        if self.player.id_in_group == 1:
            yield(pages.Choice, {'time_willing_to_wait': strategies[math.floor(self.case / len(strategies))]})
        else:
            yield (pages.Choice, {'time_willing_to_wait': strategies[self.case % len(strategies)]})
