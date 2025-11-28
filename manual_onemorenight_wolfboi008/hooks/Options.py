# Object classes from AP that represent different types of options that you can create
from Options import Option, FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, OptionGroup, PerGameCommonOptions, Visibility
# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value
from typing import Type, Any


####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#
class TotalCharactersToWinWith(Range):
    """Instead of having to beat the game with all characters, you can limit locations to a subset of character victory locations."""
    display_name = "Number of characters to beat the game with before victory"
    range_start = 10
    range_end = 50
    default = 50

class StartingDifficulty(Choice):
    """
    Choose which State of Mind (Difficulty) you want to start your game with.
    The ones that aren't chosen will be added to the pool, so they can be found at a later point in the Multiworld.
    It'd be a mouthful to write all of the changes to the various States of Mind here, so I'll give a brief
    explanation of each. The further details for each of them can be seen in the States of Mind area.
    
    Guilty: The base Difficulty. What you normally play on if you have never beaten TiTN (Trapped in the
    Nightmare), so probably the most familiar to you out of all of them.
    Calm: Less aggression and some more choices and health. However, you have less resources, so it's easier to get
    overwhelmed.
    Devastated: Threats are more aggressive, but you get some extra resources to support you.
    Scorched: You have a brand new Threat to deal with, Heat. However, other Threats are slightly less agressive
    and you start with some spare power and an extra Glass Life (once it is lost, it's gone for good).
    Soaked: Threats are less aggressive, one of your three hearts becomes Glass, and you only have to pick one 
    starting Threat instead of three. However, Jordi, Divine Punishment, and all of the J-Choices are added from
    the moment you begin. A rough challenge mostly focusing on the office. Good luck.
    
    If you're wondering "Where's Fooled"? It's a Trap. Sorry.
    """
    option_calm = 0
    option_guilty = 1
    option_devastated = 2
    option_scorched = 3
    option_soaked = 4
    default = 1
    display_name: "Starting Difficulty"

class SoloMode(DefaultOnToggle):
    """
    Enable Solo Mode, a setting that disables some Checks and makes some Items Useful instead of Progression.
    Recommended to enable if you plan on playing on your own instead of with friends.
    """
    display_name:"Solo Mode"

class HardAchievements(Toggle):
    """
    Enable checks for completing harder Achievements.
    This includes the following Achievements:
    - Empty-Handed (Beat the game itemless.)
    - No time to think (Beat the game in under 35 minutes.)
    - Bloodshed (Die 10 times in a run.)
    - Hard Worker (Beat the game with no Quickly Outs and 3 Overtimes. Forces nights to be 15 seconds longer unless you happen to circumvent some of the time with The Moon Tarot Card or Pocket Watch Starter Item.)
    - Burning with you (Beat the BiD Route on Scorched Difficulty.)
    - Soaked with Guilt (Beat the PtWP Route on Soaked Difficulty.)
    - Seen the Fish (Catch all 40 types of fish and complete the Fishing Book.)
    - THEY HAVE TO DO SOMETHING: Hit all 37 buttons in the Lobby. There are two in particular that are annoying to do. Speed Coil is expected for one of them, but still unsure of a consistent way to get the second one. You should probably exclude this if you turn this on for other Achievements you don't mind doing, honestly.
    - Strongest Hammer (Hit an almost Perfect score on the Hammer arcade game. Not easy to get consistently, so it's considered a Hard Achievement.)
    - Are you ready for Barry? (Survive Night 10 or later without letting Barry go past the Dining Area.)
    - Music of the Past (Complete the Lost Music Box Challenge. Also disables the Check for the mentioned Challenge.)
    - Quick Thinker (Complete the Constant QTE Challenge. Also disables the Check for the mentioned Challenge.)
    - Unmasked (Have Old Barry, Old Bunny, and Old Chicken active at the same time, then have your mask break but still survive the night. Considered a Hard Achievement because it can be a pain to setup without dying in the process.)
    - Empty Victory (Beat the game while having 0 Max HP.)
    - Green Runner (Beat the game on Guilty while using as little power as possible. The exact numbers are less than 225% + 50% extra per additional player. For example, 275% with 2 players, 325% with 3 players, etc.)
    In addition, the Unfortunate (Make the Wheel of Fortune explode) Achievement wiil have its logic shifted, depending on if this Option is enabled or disabled.
    - Enabled: Requires access to Night 13 or later (to account for if the player takes a bit to find the Wheel of Fortune, if at all. Ironically requires some luck to get.)
    - Disabled: Requires the Lucky Clover Starter Item and access to Night 8 or later.
    Overall, it's recommended to disable this Option if you don't feel confident in your skills (and maybe luck, too).
    (17 Checks)
    """
    display_name: "Hard Achievements"

class AchievementChallenges(Toggle):
    """
    Enable Checks for beating Challenges that are tied to Achievements.
    (12 Checks)
    """
    display_name: "Achievement Challenges"

class NonAchievementChallenges(Toggle):
    """
    Enable Checks for beating Challenges that are NOT tied to Achievements.
    (2 Checks)
    """
    display_name: "Non-Achievement Challenges"

class Fishsanity(Choice):
    """
    Enable Checks for catching fish with the Fishing Rod. Please read the below informaation for details:

    Colors Only: The 10 colored fish are the only ones with Checks on them.
    They all have an equal 2.6% chance to be fished up.
    
    Colors and Characters: The 10 colored fish and 34 character fish are Checks, totaling to 44 Checks.
    Note that this also includes the Ticket and Fish Emoji...because yes.
    
    True Fishsanity: EVERY fish is a Check.
    CAUTION: This includes the 8 rarest fish in the game, each of which having a <2% chance of appearing. Be aware that completing your Checks may take a while with this enabled.
    (52 Checks)
    """
    option_disabled = 0
    option_colors_only = 1
    option_colors_and_characters = 2
    option_true_fishsanity = 3
    display_name: "Fishsanity"

class Jumpscaresanity(DefaultOnToggle):
    """
    Enable Checks for being jumpscared by each of the game's Threats.
    This includes Myself on Night 20, Scorched Myself on BiD Night 21, and False Savior on FS Night 21.
    (52 Checks)
    """
    display_name: "Jumpscaresanity"

class BellLogic(Toggle):
    """
    Enabling this Option will make it so the Pocket Bell Main Item to be considered for logic in places such as
    the "I'm Prepared" Achievement. If this is disabled, the Pocket Bell will be a Filler Item, meaning there's a chance it may not even show up in the Manual.
    (which honestly might be for the better)
    """
    display_name: "Bell Logic"

class FlashlightSkins(DefaultOnToggle):
    """
    Enable Flashlight Skins as items.
    Note that these are all Filler, so enabling this is completely optional.
    """
    display_name: "Flashlight Skins"

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict[str, Type[Option[Any]]]) -> dict[str, Type[Option[Any]]]:
    options["startingdifficulty"] = StartingDifficulty
    options["solo_mode"] = SoloMode
    options["hardachievements"] = HardAchievements
    options["achievement_challenges"] = AchievementChallenges
    options["nonachievementchallenges"] = NonAchievementChallenges
    options["fishsanity"] = Fishsanity
    options["jumpscaresanity"] = Jumpscaresanity
    options["bell_logic"] = BellLogic
    options["flashlight_skins"] = FlashlightSkins
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: Type[PerGameCommonOptions]):
    # To access a modifiable version of options check the dict in options.type_hints
    # For example if you want to change DLC_enabled's display name you would do:
    # options.type_hints["DLC_enabled"].display_name = "New Display Name"

    #  Here's an example on how to add your aliases to the generated goal
    # options.type_hints['goal'].aliases.update({"example": 0, "second_alias": 1})
    # options.type_hints['goal'].options.update({"example": 0, "second_alias": 1})  #for an alias to be valid it must also be in options
    options.type_hints["placeholder"].visibility = Visibility.none
    options.type_hints["fragments"].visibility = Visibility.none
    options.type_hints["coop"].visibility = Visibility.none
    options.type_hints["fishsanity_achievements"].visibility = Visibility.none
    options.type_hints["colored_fish"].visibility = Visibility.none
    options.type_hints["character_fish"].visibility = Visibility.none
    options.type_hints["rare_fish"].visibility = Visibility.none
    pass

# Use this Hook if you want to add your Option to an Option group (existing or not)
def before_option_groups_created(groups: dict[str, list[Type[Option[Any]]]]) -> dict[str, list[Type[Option[Any]]]]:
    # Uses the format groups['GroupName'] = [TotalCharactersToWinWith]
    return groups

def after_option_groups_created(groups: list[OptionGroup]) -> list[OptionGroup]:
    return groups
