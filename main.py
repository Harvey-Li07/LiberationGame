import random, time, typing, shutil, os, multiprocessing

def centered_text_var(text: str):
    line = []
    width = shutil.get_terminal_size().columns
    spaces = (width - len(text)) // 2
    for x in range(0, spaces + 1):
        line.append(" ")
    line.append(text)
    return "".join(line)

# ---- Not Constant Definition ----
CurrentStoryCursor: tuple[str, int]
TitleLine: str = centered_text_var("[Add Game Title Here]")
CastLineTitle: str = centered_text_var("[Cast Members]")
MysteryVoiceTitle: str = centered_text_var(">        ???        <")
YouTitle: str = centered_text_var(">        YOU        <")
DeathCounter: int = 0
# ---- Constant Definitions ----
SPEAKING_SPEED: int = 40

GAME_STATEMENT: str = """
This is a product for the Game Jam for AP® Computer Science Principles [2024-2025]. Credits/Appriciations maybe found at the end of the
game or in the code section named '---- Credits and Appriciations ----' \n

  please raise your left hand if you are actually reading this.

Harvey Li presents ....
"""

GAME_OPENER: str = f"""

{TitleLine}

    Scientology Training Facility

    October 15th, 1998

    Location: (6?.1?????, -?1.6?????)
"""

WELCOME_LINE: str = """
Well, hello, initiate. At the heart of the middle of nowhere and stranded from all civilization, you, my friend, are here for one and only one reason: 
abandon your past and begin a new life from the second you leave this facility - your soul will be purified and liberated. 
"""

WHAT_BRING_HERE: str = """
So, what brings you here?
"""

ASK_FOR_REASON_RESTART:str = """
Why do you need your life to be restarted with the great power of Father Hubbard? 
"""

SURE: str = """
Sure. 
"""

HERE_WE_ARE_WELCOME: str = """
Here we are, welcome. This is the center and the sacred land of Scientology. 
We, as the masters of this organization, are obligated to accept these former sins from you and clean you. 
To do so, you need to complete four tasks that will purify you in all aspects - physically, mentally, socially, and goddamn spiritually. 
"""

TEMP_LIVE_SPACE: str = """
Your temporary living space is to the right, go in and relax for a minute, your task won’t start 
until fifteen hundred hours. Just … trust us, we did this many times. 
"""

TASK_ONE_INTRO: str = """
Welcome [pause] to task one. In this little activity, you will be shooting yourself, of course, not with an actual bullet. 
Our Father Hubbard mentioned, and of course you will know this, the Great Eight Dynamics. This is the very first - to 
let you abandon the will to sustain the living of your mortal being.
In just a second, my assistant will load this revolver with a bullet, and you will shoot yourself five times. 
You have successfully passed this activity if the gun is never fired, and you shall precede to the next level.
"""

LINE_A_ENCOURAGE: str = """
Well, I suppose you need a little more encouragement. 
Our great Father Hubbard once mentioned the Great Eight Dynamics. The first is the urge of one to continue one’s life, and is the one you
are currently suffering from. Through this Holy Revolver blessed by the power of Father Hubbard,
and once you successfully pass the challenge, you may ascend to the second level. So now, take your chance and pick up the revolver. 
"""

LINE_B_PRAISE: str = """
Good, you seemed to have the courage for it. Now put it below your jaw and pull the trigger. May Father Hubbard’s power bless you. 
"""

SCENE_2_A_ISSUE_NOW: str = """
Hmm… what seemed to be the issue now … don’t you want your life to be purified and redeemed from your mere mortal body? 
"""

PICK_UP_THE_GUN: str = """
Please pick up the gun. 
"""

NO_ACTION_GAME_OVER: str = """
Pick up the fucking gun initiate! Never mind, why do I even argue with you bastard. 
Your task is canceled. WITH ALL PREJUDICE. You will be transferred out of this facility, (without emotion, cold) 
but first, please turn around … 
"""

ONLY_FIVE_TO_GO: str = """
Good, it looks like you have passed this the first attempt, only five more to go. 
"""

DEATH: str = """
Perhaps Father Hubbard does not approve of your attempt. Our medic will transport you to your shelter. 
Once you recover, please make your way back here again. 
"""

NICELY_DONE: str = """
Good, it seems that Father Hubbard approved of your attempt. Nicely done, initiate. You will be promoted to the next challenge.
I will unlock the door shortly. Please follow me as we go on a short lecture of Scientology.
"""

AFTER_DEATH_WAKE_UP: str = """
Wake up! Wake up! It is a new day, initiate; you have plenty to do. 
"""

SCI_LECTURE_PT1 = """
Well, this is the hall of fame of the notable figures from our Great Church. 
These people, either alive or ascended into the state of immortality, did good to us. 
It is every member’s goal to be like them and live with them. You should always stride towards excellence and do good deeds to the Church 
- that will be your motto from this instant. Of course, by the end of the hallway is the figure of our great Father Hubbard - 
the founder and creator of the Church. Although the world did not appreciate the presence of us, and many of our preachers were prosecuted under 
various crimes that they did not commit. 
"""

NEVER_THE_ACCEPTED: str = """
We were never the accepted ones, and some of our ideas were outlawed by the current legislature. 
Tell me, initiate, is assisted suicide truly a crime?
"""

I_SUPPOSE_UR_RIGHT = """
I suppose you are right. But it was for the good of the Church, what he needed was just … some … encouragement and agency. 
He left us way too early; after his life being ruined by the government and their correctional facilities, he joined us to start a new life. 
By all means that he is a great student and possibly the one with the most potential to be the next pope. But he snitched on us. 
THAT BASTARD SNITCHED ON US. It is an act of a desperate man, initiate. It is the only right thing we can do in that case.
"""

BACK_ON_TOPIC = """
Anyway, we are off topic, the Church’s goal is always to preserve the spiritual living of any member, regardless of their status.
"""

ALONG_IDEO = """
Hah, it seems that you are on board with the ideology of us. Good. You are on the right track, my frie… [she pauses] (coldly) initiate. 
"""

LAST_LINE = """
But it will soon change! The power is raising from the earth and from the sky! FOR ONCE AND FOR ALL, 
THE WORLD SHALL ACCEPT AND PRAISE OUR EXISTANCE. Although for the ones rejected us and prosecuted us, that day will be their 
judgment day when not only will their body be crushed by the power of the Great Eight Dynamics but their soul! 
OH their soul will suffer in the eternal furnace - being tortured for every single piece of sin they committed to the Church. 
But you, initiate, is not like them. You are one of the firm believer of us. You should know that one of the things we 
accomplished through the purification of the soul is the acceptance that your very mortal body is subject to injuries and death, 
but your spirit is not. By the end of this transformation, you will be allowed to leave your very body and ascend to heaven, 
not in a Christian sense, of course, but in a Scientological sense. For a place where judgement can be carried with good faith and 
sincere affections, you shall raise and perform fruitful labor to not only our Great Father Hubbard but also to the rest of the members. 
May the power of R.K.C. Triangle and Father Hubbard bless you, initiate. 
"""

APPRICIATIONS: str = f"""
Music used in the game opener is by [artist name] and can be found at [link]

{CastLineTitle}

[character name]: [cast member name]


"""

def ConsolePrint(argument: str, cps: int = SPEAKING_SPEED, title: str = MysteryVoiceTitle):
    '''A custom version of print but can control the speed at which the characters displays on screen. 
    Requires sys and time. \n
    * argument: the string to be displayed
    * cps: character per second, default to SPEAKING_SPEED (delay 0.02 seconds after each character)

    **PRO TIP!** \t To find the delay after each character, do 1/cps. 
    '''
    if cps < 0:
        cps = abs(cps)
    elif cps == 0:
        cps = 1
    print(title)
    for x in list(argument):
        print(x, end="", flush=True)
        time.sleep(1/abs(cps))
    print('\n')

class Russian_Roulett:

    '''The game of Russian Roulett'''

    def __init__(self):
        self.wheel: list[int] = [0, 0, 0, 0, 0, 0]
        #self.wheel.insert(random.randint(0,6), 1)
    
    def Fire(self):
        if self.wheel.__len__() > 0:
            return (1, 0)[self.wheel.pop(0) == 0]
        else:
            return -1
        
class Assets:

    '''Here defines the common assets and methods to manipulate them. \n
    * def Audio - Construct an audio object
    * def GetStoryLineCursor - return the current location of the story as a tuple
    * def ClearCurrentScreen - clear the console screen
    * def RetrieveInputs - get the input from the user and pack it into a processable block. 
    '''

    def Audio(Path_to_File: str, Add_to_Queue_List: bool = False, auto_play: bool = False):
        if auto_play:
            ...
        else:
            ...

    def GetStoryLineCursor() -> tuple: ...

    def ClearCurrentScreen():
        for x in range(1, os.get_terminal_size().columns):
            print()

    def RetrieveInputs(options: dict[int: str], prompt: str) -> tuple[str, int]:
        ConsolePrint(prompt, SPEAKING_SPEED, title="")
        while True:
            std_in: str = input("   Enter Choice > ")
            try:
                int(std_in)

            except Exception:
                ConsolePrint(MysteryVoiceTitle, SPEAKING_SPEED)
                ConsolePrint("What do you mean? I do not understand", SPEAKING_SPEED)
            else:
                if int(std_in) in options.keys():
                    ConsolePrint(f"{options[int(std_in)]}", SPEAKING_SPEED, title=YouTitle)
                    return (std_in, int(std_in))

    def ThreadSpawner(target: any) -> None: ...

def Russian_Roulette_Game() -> typing.Literal["Death", "Pass"]:
    ConsolePrint("Press enter to shoot")
    local_game = Russian_Roulett()
    success_counter: int = 0
    while True:
        input("Press Enter Now > ")
        result = local_game.Fire()
        if result == 1:
            return "Death"
        elif result == 0 and success_counter == 0:
            success_counter += 1
            ConsolePrint(ONLY_FIVE_TO_GO)
        elif result == 0 and success_counter > 0 :
            success_counter += 1
        elif result == -1 and success_counter > 5:
            return "Pass"

def main() -> None:
    ConsolePrint(GAME_STATEMENT, cps = 100, title="")
    time.sleep(2)
    Assets.ClearCurrentScreen()
    ConsolePrint(GAME_OPENER, title="")

    ConsolePrint(WELCOME_LINE, cps=SPEAKING_SPEED)
    ConsolePrint(WHAT_BRING_HERE)
    Assets.RetrieveInputs(options = {1: "Sorrow. Depression - life from the past"}, prompt = "1 > Sorrow. Depression - life from the past")
    ConsolePrint(ASK_FOR_REASON_RESTART)
    Assets.RetrieveInputs(options = {1: "I have told you once", 2:"*silence*"}, prompt = "1 > I have told you once \n 2 > *silence*")
    ConsolePrint(SURE)
    time.sleep(2)
    Assets.ClearCurrentScreen()
    ConsolePrint(HERE_WE_ARE_WELCOME)
    ConsolePrint(TEMP_LIVE_SPACE)
    while True:
        ConsolePrint(TASK_ONE_INTRO)
        Input = Assets.RetrieveInputs(options = {1: "*silence* *picking up the gun*", 2: "I don't understand"},  \
                                        prompt= "1 > *silence* *picking up the gun* \n 2: I don't understand")
        if Input[1] == 1:
            ConsolePrint(LINE_B_PRAISE)
        else:
            ConsolePrint(LINE_A_ENCOURAGE)

        if Russian_Roulette_Game() == "Death":
            ConsolePrint(DEATH)
            time.sleep(5)
            Assets.ClearCurrentScreen()
            time.sleep(5)
            ConsolePrint(AFTER_DEATH_WAKE_UP)
        else:
            ConsolePrint(NICELY_DONE)
            break
    ConsolePrint(SCI_LECTURE_PT1)
    Assets.RetrieveInputs(options = {1: "Who is this?"}, prompt = "1 > Who is this?")
    ConsolePrint(NEVER_THE_ACCEPTED)
    Input = Assets.RetrieveInputs(options = {1: "Yes", 2:"No"}, prompt = "1 > Yes \n 2 > No")
    if Input[1] == 1:
        ConsolePrint(I_SUPPOSE_UR_RIGHT)
        Assets.RetrieveInputs(options = {1: "What did he snitched about?"}, prompt = "1 > What did he snitched about?")
        ConsolePrint(BACK_ON_TOPIC)
    else:
        ConsolePrint(ALONG_IDEO)
    
    ConsolePrint(LAST_LINE)

    input("Press Enter to enter the next chapter.> ")

    Assets.ClearCurrentScreen()

    ConsolePrint("It is not the end of the game yet! Wait until the final game! Please! Give me some money!", title=centered_text_var("Harvey"))

main()
ConsolePrint(APPRICIATIONS)