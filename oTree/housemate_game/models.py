from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Uzi Friedman'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'housemate_game'
    players_per_group = 2
    num_rounds = 5
    reward = 100
    tax = 20
    diminishing_factor = 0.95


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.time_opponent_willing_to_wait = p2.time_willing_to_wait
        p2.time_opponent_willing_to_wait = p1.time_willing_to_wait
        time_before_end = min(p1.time_willing_to_wait, p2.time_willing_to_wait)
        winner_payoff = Constants.reward * (Constants.diminishing_factor ** (time_before_end-1))
        loser_payoff = winner_payoff - Constants.tax
        tie_payoff = winner_payoff - Constants.tax/2
        # both try to take out the trash
        if p1.time_willing_to_wait == p2.time_willing_to_wait:
            p1.payoff = tie_payoff
            p2.payoff = tie_payoff
        # p1 won
        elif p2.time_willing_to_wait < p1.time_willing_to_wait:
            p1.payoff = winner_payoff
            p2.payoff = loser_payoff
        # p2 won
        else:
            p1.payoff = loser_payoff
            p2.payoff = winner_payoff


class Player(BasePlayer):
    time_willing_to_wait = models.IntegerField()
    time_opponent_willing_to_wait = models.IntegerField()
    payoff = models.IntegerField()
