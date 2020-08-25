# Did the rocket launch yet?

Welcome to Did the rocket launch yet!

This is a very simple Telegram Bot that you can reach at [DidTheRocketLaunchYetBot](t.me/DidTheRocketLaunchYetBot).

The aim of the bot is to try to figure out, with the help of a real person, at what exact frame of a video the rocket launched. By using an API that returns one frame of a video, we show the image to the user, which would then reply with either yes or no. Internally, the bot will use the [bisection algorithm](https://en.wikipedia.org/wiki/Bisection_method) to make sure it finds a solution in the minimum amount of steps possible. Please, do note that we said _a solution_ and not the correct solution because it depends on the human knowledge of the user to find the correct answer. If the person makes a mistake, so will the bot.

## Bot usage

The bot has two available commands: **/start** and **/help**.

By sending **/start**, the user starts the game and the bot will start interacting with the user. In each step, it will show the user one frame from the video and ask if the rocket has launched yet in that frame or not. The user will have two button option from which to choose from (yes or no) and, depending on the user's input, the bisection algorithm will do its work to choose another frame for which to ask the customer if the rocket has launched yet or not. For this specific case and video, it will find the frame at which the rocket launches in exactly 16 steps.

By sending **/help**, the user will receive a message with information about the bot and the available commands.

## Bot definition
In order to develop the bot, we have used the BERNARD framework. You can check BERNARD's documentation [here](https://github.com/BernardFW/bernard).

This framework is able to give us a skeleton of a working bot for which we only need to define states and transitions as if it was a [Finite State Machine](https://github.com/BernardFW/bernard/blob/develop/doc/get-started/fsm.md). We needed to define the actions executed in each state as well as the conditions for a transition to happen and move over to another state.

As the bot is internally a Finite State Machine, you can check the following diagram to understand states and transitions for our bot:
![DidTheRocketLaunchYetDiagram](/docs/img/DidTheRocketLaunchYetStatesGraph.PNG)

### States
#### 1. Welcome
After the user executes the **/start** command to the bot, this state is called to welcome the user to the game, asking them if they want to play and showing two buttons with the possible affirmative and negative options. The coded class for this state is [`S001xWelcome`](/src/didtherocketlaunchyet/states.py#L80).
#### 2. Did the rocket launch yet? (Initial)
If the user replies **_yes_** to the previous state, the bot moves on to this state so it can show the user an image and ask if the rocket has launched yet in said image, giving the user two button options for either yes or no. This second state initializes the variables used for the bisection algorithm. The coded class for this state is [`S002xDidTheRocketLaunchYetInitial`](/src/didtherocketlaunchyet/states.py#L99).
#### 3. Did the rocket launch yet? (Loop)
This state is called in a loop fashion, until the bisection algorithm identifies the moment at which the rocket has launched. For each iteration, it shows two buttons with the values yes or no to the user and it modifies the value of either `left` or `right`, depending on the user input, and updates the value of `middle`. The coded class for this state is [`S003xDidTheRocketLaunchYetAgain`](/src/didtherocketlaunchyet/states.py#L122).
#### 4. Congratulations
Congratulates the user for a good job after the bisection algorithm determines that the take-off frame has been found. Returns the bot to the initial state where it's waiting for a bot command. The coded class for this state is [`S004xCongratulations`](/src/didtherocketlaunchyet/states.py#L137).
#### 5. Goodbye
If the user answers **_no_** to the initial question, the bot doesn't start the game and says goodbye to the user. The coded class for this state is [`S005xGoodbye`](/src/didtherocketlaunchyet/states.py#L157).
#### 6. Help
State reached when the command **/help** is invoked. It returns a message with information about the bot and the available commands. The coded class for this state is [`S006xHelp`](/src/didtherocketlaunchyet/states.py#L170).
### Transitions
Transitions are basically the lines in the diagram above, when do we decide to move from one state to the next. They are based on an origin state, a destination state and a condition that needs to be completed for the bot to move from origin to destination. The definition of these transitions can be found in [this file](/src/didtherocketlaunch/transitions.py).
### Triggers
Triggers are the conditions used in transitions to move from one state to the next. These triggers are not only conditionals that return boolean, but they can actually do much more in order to execute their own logic if needed. We have create a custom trigger, which you can also see in the `transitions.py` file, that is basically executing the bisection algorithm, modifying the values of `left`, `right`and `middle`according to the user input, and evaluating if the bisection algorithm has finished. You can find the definition of that trigger in [this file](/src/didtherocketlaunchyet/triggers.py).

## Contribute
In order to contribute to this project, any code will need to pass a pull request. Requirements to pass the review include:
- Follow PEP 8 coding convention
- Documented code, preferably by using DocString

Feel free to open a GitHub issue for any suggestion you may have or bug you might have found. You can also contact me directly at `vbalbp@gmail.com`.
