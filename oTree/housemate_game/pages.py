from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Choice(Page):
    form_model = 'player'
    form_fields = ['time_willing_to_wait']

    def vars_for_template(self):
        return {
            'reward': Constants.reward,
            'Tax': Constants.tax,
            'Diminishing_factor': Constants.diminishing_factor*100,
            'is_first_round': self.subsession.round_number == 1,
            'player_in_previous_rounds': self.player.in_previous_rounds(),
        }


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class ResultsSummary(Page):

    def is_displayed(self):
        return Constants.num_rounds == self.subsession.round_number

    def vars_for_template(self):
        return {
            'player_in_all_rounds': self.player.in_all_rounds(),
            'total_payoff': sum([p.payoff for p in self.player.in_all_rounds()])
        }


page_sequence = [
    Choice,
    ResultsWaitPage,
    ResultsSummary
]
