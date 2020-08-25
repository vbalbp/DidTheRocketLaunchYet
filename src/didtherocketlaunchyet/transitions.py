# coding: utf-8
from bernard import (
    layers as lyr,
)
from bernard.engine import (
    Tr,
    triggers as trg,
)
from bernard.platforms.telegram.layers import (
    BotCommand
)

from .states import *
from .triggers import *

transitions = [
    Tr(
        dest=S001xWelcome,
        factory=trg.Equal.builder(BotCommand('/start')),
    ),
    Tr(
        dest=S002xDidTheRocketLaunchYetInitial,
        origin=S001xWelcome,
        factory=trg.Equal.builder(lyr.Postback('yes')),
    ),
    Tr(
        dest=S005xGoodbye,
        origin=S001xWelcome,
        factory=trg.Equal.builder(lyr.Postback('no')),
    ),
    Tr(
        dest=S003xDidTheRocketLaunchYetAgain,
        origin=S002xDidTheRocketLaunchYetInitial,
        factory=Bisection.builder(is_found=False),
    ),
    Tr(
        dest=S003xDidTheRocketLaunchYetAgain,
        origin=S003xDidTheRocketLaunchYetAgain,
        factory=Bisection.builder(is_found=False),
    ),
    Tr(
        dest=S004xCongratulations,
        origin=S003xDidTheRocketLaunchYetAgain,
        factory=Bisection.builder(is_found=True),
    ),
    Tr(
        dest=S006xHelp,
        factory=trg.Equal.builder(BotCommand('/help')),
    )
]
