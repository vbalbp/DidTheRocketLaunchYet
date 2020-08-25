# coding: utf-8
from bernard import (
    layers as lyr,
)
from bernard.engine.triggers import (
    BaseTrigger,
)
from .store import (
    cs,
)


class Bisection(BaseTrigger):
    """
    This is a custom trigger to move from one state to the next.
    It is called after the user chooses yes or no to the question
    `Did the rocket launch yet?` and modifies the values of the
    context variables `left`, `right` and `middle` according to the answer.

    The variable `is_found` is a boolean that identifies if we have found
    the exact moment when the rocket launches by using the bisection algorithm.
    """
    def __init__(self, request, is_found):
        super().__init__(request)
        self.user_answer = None
        self.is_found = is_found

    @cs.inject()
    async def rank(self, context) -> float:
        right = context.get('right')
        left = context.get('left')
        middle = context.get('middle')
        try:
            self.user_answer = self.request.get_layer(lyr.Postback).payload
        except(KeyError, ValueError, TypeError):
            return .0
        if self.user_answer == 'yes':
            context['right'] = middle
        elif self.user_answer == 'no':
            context['left'] = middle
        context['middle'] = int((context.get('left')+context.get('right'))/2)
        is_found = context.get('left') + 1 >= context.get('right')
        return 1. if is_found == self.is_found else .0
