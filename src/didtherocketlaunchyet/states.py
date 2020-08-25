# coding: utf-8
from bernard import (
    layers as lyr,
)
from bernard.analytics import (
    page_view,
)
from bernard.engine import (
    BaseState,
)
from bernard.i18n import (
    translate as t,
)
from bernard.platforms.telegram import (
    layers as tlg,
)
from .store import (
    cs,
)
from bernard.conf import (
    settings
)


class DidTheRocketLaunchYetState(BaseState):
    """
    Root class for DidTheRocketLaunchYet.

    "error" and "confused" are the default
    functions called when something goes wrong.
    The ERROR and CONFUSED texts are defined in `i18n/en/responses.csv`.
    """

    def ask_question(self, middle) -> None:
        """
        Parameters:
            middle(int): Frame we are currently analyzing

        This function is a module used when asking the user
        if the rocket has launched yet or not.
        Used in states S002 and S003.

        Shows the frame first and asks the question afterwards,
        giving two button options to answer either yes or no.
        """
        url = settings.API_URL.format(middle)
        self.send(
            lyr.Text(t('URL', url=url))
        )
        self.send(
            lyr.Text(t('DID_IT_LAUNCH', middle=middle)),
            tlg.InlineKeyboard([[
                tlg.InlineKeyboardCallbackButton(t.YES, payload='yes'),
                tlg.InlineKeyboardCallbackButton(t.NO, payload='no'),
            ]]),
        )

    @page_view('/bot/error')
    async def error(self) -> None:
        """
        This happens when something goes wrong (it's the equivalent of the
        HTTP error 500).
        """

        self.send(lyr.Text(t.ERROR))

    @page_view('/bot/confused')
    async def confused(self) -> None:
        """
        This is called when the user sends a message that triggers no
        transitions.
        """

        self.send(lyr.Text(t.CONFUSED))

    async def handle(self) -> None:
        raise NotImplementedError


class S001xWelcome(DidTheRocketLaunchYetState):
    """
    Initial state that welcomes the user and introduces them to the game.

    It is triggered by the bot command `/start`.
    """
    @page_view('bot/welcome')
    async def handle(self) -> None:
        name = await self.request.user.get_friendly_name()

        self.send(
            lyr.Text(t('WELCOME', name=name)),
            tlg.InlineKeyboard([[
                tlg.InlineKeyboardCallbackButton(t.YES, payload='yes'),
                tlg.InlineKeyboardCallbackButton(t.NO, payload='no'),
            ]]),
        )


class S002xDidTheRocketLaunchYetInitial(DidTheRocketLaunchYetState):
    """
    First state to initiate the game, it initializes the variables
    `left` and `right` for the use of the bisection algorithm.
    After this state is finished, we move over to S003,
    changing the values of the context based on the choice of the user.

    Shows a frame of the video to the user and asks
    if the rocket seen in the video has launched yet.

    Triggered by choosing yes to play the game.
    """
    @page_view('/bot/did-the-rocket-launch-yet')
    @cs.inject()
    async def handle(self, context) -> None:
        context['left'] = left = 0
        context['right'] = right = settings.N_FRAMES
        context['middle'] = middle = int(
            (left + right)/2
        )
        self.ask_question(middle)


class S003xDidTheRocketLaunchYetAgain(DidTheRocketLaunchYetState):
    """
    Shows a frame of the video to the user and asks
    if the rocket seen in the video has launched yet.
    Gives the user two buttons as options to answer either 'yes' or 'no'.

    Triggered after the user chooses one option.
    """
    @page_view('/bot/did-the-rocket-launch-yet-again')
    @cs.inject()
    async def handle(self, context) -> None:
        middle = context.get('middle')
        self.ask_question(middle)


class S004xCongratulations(DidTheRocketLaunchYetState):
    """
    Finishes the process and shows the user the
    frame number at which the rocket launched.

    Triggered after exactly 16 steps when the
    value of `left` + 1 is equal or greater than the value of `right`.

    The number of steps to reach the solution will be equal
    to the logarithm to base two of the number of frames of the video.
    """
    @page_view('/bot/congrats')
    @cs.inject()
    async def handle(self, context) -> None:
        launch_frame = context.get('right')
        self.send(
            lyr.Text(t('CONGRATULATIONS', frame=launch_frame))
        )


class S005xGoodbye(DidTheRocketLaunchYetState):
    """
    Doesn't initialize the game if the user chooses not to play.

    Triggered by choosing no to play the game.
    """
    @page_view('/bot/goodbye')
    async def handle(self) -> None:
        self.send(
            lyr.Text(t('GOODBYE')),
        )


class S006xHelp(DidTheRocketLaunchYetState):
    """
    Will provide the user with an explanation of
    what the bot is used for and the available commands.

    Triggered by the bot command `/help`.
    """
    @page_view('/bot/help')
    async def handle(self) -> None:
        self.send(
            lyr.Text(t('HELP', new_line='\n')),
        )
