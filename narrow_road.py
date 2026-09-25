#!/usr/bin/env python3
"""
THE NARROW ROAD
A narrative-driven fantasy adventure RPG
with virtue tracking, lasting consequences, and space for reflection.
"""

import random
import sys
from typing import Dict, List, Optional

# ─────────────────────────────────────────────
# CORE DATA
# ─────────────────────────────────────────────

VIRTUES = ["Courage", "Wisdom", "Compassion", "Humility", "Temperance", "Justice"]

class GameState:
    def __init__(self):
        self.virtues: Dict[str, int] = {v: 5 for v in VIRTUES}  # start balanced
        self.companions: Dict[str, int] = {  # loyalty 0–10
            "Elara": 6,   # healer / mercy
            "Kael": 5,    # warrior / justice
            "Silas": 4,   # scholar / wisdom
        }
        self.inventory: List[str] = ["Traveler's Cloak", "Simple Staff"]
        self.flags: Dict[str, bool] = {
            "spared_bandit": False,
            "took_gold": False,
            "helped_village": False,
            "trusted_whisper": False,
            "broke_oath": False,
            "showed_mercy_to_enemy": False,
            "chose_power": False,
            "chose_sacrifice": False,
        }
        self.story_stage = "prologue"
        self.player_name = "Traveler"
        self.ending = None

    def change_virtue(self, name: str, amount: int, silent: bool = False):
        if name in self.virtues:
            old = self.virtues[name]
            self.virtues[name] = max(0, min(10, self.virtues[name] + amount))
            if not silent and amount != 0:
                direction = "grew" if amount > 0 else "wavered"
                print(f"  › Your {name} {direction}.")

    def change_loyalty(self, name: str, amount: int):
        if name in self.companions:
            self.companions[name] = max(0, min(10, self.companions[name] + amount))

    def has_virtue(self, name: str, threshold: int = 7) -> bool:
        return self.virtues.get(name, 0) >= threshold

    def total_virtue(self) -> int:
        return sum(self.virtues.values())

    def dominant_virtue(self) -> str:
        return max(self.virtues, key=self.virtues.get)

# ─────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────

def clear():
    print("\n" + "─" * 60 + "\n")

def pause():
    input("\n[Press Enter to continue]")

def choice(prompt: str, options: List[str]) -> int:
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        try:
            sel = int(input("\nYour choice: ").strip())
            if 1 <= sel <= len(options):
                return sel
        except ValueError:
            pass
        print("Please enter a valid number.")

def show_status(state: GameState):
    clear()
    print("═" * 60)
    print(f"  {state.player_name}  |  Stage: {state.story_stage.title()}")
    print("─" * 60)
    print("  Virtues:")
    for v in VIRTUES:
        bar = "█" * state.virtues[v] + "░" * (10 - state.virtues[v])
        print(f"    {v:<12} [{bar}] {state.virtues[v]}")
    print("─" * 60)
    print("  Companions:")
    for name, loy in state.companions.items():
        hearts = "♥" * loy + "♡" * (10 - loy)
        print(f"    {name:<8} {hearts}")
    if state.inventory:
        print("─" * 60)
        print("  Inventory:", ", ".join(state.inventory))
    print("═" * 60)
    pause()

# ─────────────────────────────────────────────
# STORY SCENES
# ─────────────────────────────────────────────

def prologue(state: GameState):
    clear()
    print("""
You wake beside a dying fire on the edge of the Whispering Woods.
The stars above are the same ones your grandmother once named for you—
yet the world feels heavier than it did in her stories.

A sealed letter lies in your pack. The wax bears the mark of the old Order:
a simple lamp held against the dark.

Inside, the words are few:

    "The light is failing in the north.
     The people forget what was given freely.
     Come, if you still remember how to walk the narrow road."

Three figures wait nearby—travelers who answered the same summons.
""")
    pause()

    state.player_name = input("What name do you carry on this road? ").strip() or "Traveler"
    print(f"\nVery well, {state.player_name}. The road opens.")
    pause()

    state.story_stage = "crossroads"
    scene_crossroads(state)

def scene_crossroads(state: GameState):
    clear()
    print("""
The path forks at a weathered stone.

To the east, smoke rises from a village. Cries carry on the wind.
To the west, a merchant's caravan is under attack by bandits.
The northern road climbs toward the mountains—and the summons that called you.
""")
    c = choice("Where do you turn first?", [
        "East — toward the burning village",
        "West — toward the embattled caravan",
        "North — press on without delay"
    ])

    if c == 1:
        state.flags["helped_village"] = True
        scene_village(state)
    elif c == 2:
        scene_caravan(state)
    else:
        state.change_virtue("Temperance", 1)
        state.change_virtue("Compassion", -1)
        print("\nYou keep your eyes on the northern road.")
        pause()
        scene_mountain_path(state)

def scene_village(state: GameState):
    clear()
    print("""
Flames lick the thatched roofs. A child clutches a scorched doll.
An old woman points toward the well: "They took the water. Left us the fire."

Elara is already moving toward the wounded.
Kael grips his sword. "We can still catch the raiders."
Silas studies the smoke. "This was no random attack."
""")
    c = choice("What do you do?", [
        "Help the wounded and put out the fires (Compassion)",
        "Pursue the raiders immediately (Justice / Courage)",
        "Question the survivors carefully before acting (Wisdom)"
    ])

    if c == 1:
        state.change_virtue("Compassion", 2)
        state.change_loyalty("Elara", 2)
        state.change_loyalty("Kael", -1)
        print("\nYou and Elara work through the night. Lives are saved. The raiders escape.")
        state.flags["helped_village"] = True
    elif c == 2:
        state.change_virtue("Courage", 1)
        state.change_virtue("Justice", 1)
        state.change_loyalty("Kael", 2)
        state.change_loyalty("Elara", -1)
        print("\nYou ride hard. The raiders are caught—but the village burns hotter in your absence.")
        state.flags["spared_bandit"] = False  # will be set later if mercy shown
        scene_raiders(state)
        return
    else:
        state.change_virtue("Wisdom", 2)
        state.change_loyalty("Silas", 2)
        print("\nYou learn the raiders were paid by someone in the north. A name is whispered: Malakar.")
        state.flags["helped_village"] = True

    pause()
    scene_mountain_path(state)

def scene_raiders(state: GameState):
    clear()
    print("""
You overtake the raiders in a narrow gorge. Their leader is young—
scarred, angry, and clearly following orders he does not fully understand.
""")
    c = choice("He is at your mercy.", [
        "Strike him down. Justice demands it.",
        "Spare him and demand answers.",
        "Offer him a chance to walk a different road."
    ])

    if c == 1:
        state.change_virtue("Justice", 1)
        state.change_virtue("Compassion", -2)
        state.change_virtue("Temperance", -1)
        print("\nSteel flashes. The gorge falls silent.")
        state.flags["spared_bandit"] = False
    elif c == 2:
        state.change_virtue("Wisdom", 1)
        state.change_virtue("Justice", 1)
        print("\nHe talks. The name Malakar surfaces again. You bind him and leave him for the law.")
        state.flags["spared_bandit"] = True
    else:
        state.change_virtue("Compassion", 2)
        state.change_virtue("Humility", 1)
        state.change_virtue("Justice", -1)
        print("\nHe stares at you as if seeing a ghost. Slowly, he drops his blade.")
        state.flags["spared_bandit"] = True
        state.flags["showed_mercy_to_enemy"] = True

    pause()
    scene_mountain_path(state)

def scene_caravan(state: GameState):
    clear()
    print("""
Merchants fight desperately against masked bandits. Gold spills across the road.
One merchant sees you and shouts: "Help us and half is yours!"
""")
    c = choice("What do you do?", [
        "Fight to protect the caravan (Courage / Justice)",
        "Demand the gold first, then help (Temptation)",
        "Try to negotiate a bloodless end (Wisdom / Temperance)"
    ])

    if c == 1:
        state.change_virtue("Courage", 2)
        state.change_virtue("Justice", 1)
        state.change_loyalty("Kael", 1)
        print("\nTogether you drive the bandits off. The merchants are grateful.")
        state.inventory.append("Merchant's Token")
    elif c == 2:
        state.change_virtue("Temperance", -2)
        state.change_virtue("Humility", -1)
        state.flags["took_gold"] = True
        print("\nGold changes hands. The fighting continues—some of it now directed at you.")
        state.change_loyalty("Elara", -1)
        state.change_loyalty("Silas", -1)
    else:
        state.change_virtue("Wisdom", 1)
        state.change_virtue("Temperance", 2)
        print("\nWords prove stronger than steel this day. The bandits leave with empty hands.")
        state.inventory.append("Quiet Victory")

    pause()
    scene_mountain_path(state)

def scene_mountain_path(state: GameState):
    clear()
    print("""
The northern road climbs into mist. At a high pass you find a lone hermit
tending a small lamp that never seems to gutter.

He looks at each of you in turn, then at you.
"The road ahead divides those who seek light from those who merely fear the dark.
What do you carry that cannot be taken from you?"
""")
    c = choice("How do you answer?", [
        "My strength and my blade.",
        "The bonds I share with these companions.",
        "Nothing that belongs to me alone.",
        "I do not know yet."
    ])

    if c == 1:
        state.change_virtue("Humility", -1)
        state.change_virtue("Courage", 1)
    elif c == 2:
        state.change_virtue("Compassion", 1)
        state.change_loyalty("Elara", 1)
        state.change_loyalty("Kael", 1)
        state.change_loyalty("Silas", 1)
    elif c == 3:
        state.change_virtue("Humility", 2)
        state.change_virtue("Wisdom", 1)
    else:
        state.change_virtue("Humility", 1)
        state.change_virtue("Wisdom", 1)

    print("\nThe hermit nods, as if the answer itself was less important than the honesty of it.")
    print("He presses a small clay lamp into your hands. 'Keep it trimmed.'")
    state.inventory.append("Clay Lamp")
    pause()

    state.story_stage = "temptation"
    scene_temptation(state)

def scene_temptation(state: GameState):
    clear()
    print("""
Night falls in the high country. A figure steps from the mist—neither friend nor foe.
His voice is calm, almost kind.

"You have walked far. You have made hard choices. I can make the rest easier.
Power enough to end the darkness in a single stroke. No more villages burning.
No more hard roads. Only the will to take what is offered."

A black key rests in his open palm.
""")
    c = choice("What do you do?", [
        "Refuse. Some prices are too high.",
        "Ask what the key truly costs.",
        "Take the key. The ends justify the means."
    ])

    if c == 1:
        state.change_virtue("Temperance", 2)
        state.change_virtue("Humility", 1)
        state.change_virtue("Courage", 1)
        print("\nThe figure smiles—almost sadly—and vanishes. The mist thins.")
        state.flags["chose_power"] = False
    elif c == 2:
        state.change_virtue("Wisdom", 2)
        print("\nHe answers: 'Only the part of you that still believes the light must be earned,
not seized.' You step back. The key dissolves.")
        state.flags["chose_power"] = False
    else:
        state.change_virtue("Temperance", -3)
        state.change_virtue("Humility", -2)
        state.change_virtue("Courage", 1)
        state.flags["chose_power"] = True
        state.inventory.append("Black Key")
        print("\nThe key is cold. For a moment the world feels lighter—and emptier.")

    pause()
    state.story_stage = "climax"
    scene_climax(state)

def scene_climax(state: GameState):
    clear()
    print("""
You stand before the gates of the northern citadel.
Malakar waits—no longer a shadow, but a man who once walked the same road you walk.

"I tired of waiting for the light," he says. "I decided to become it."

Behind him the citadel burns with a cold fire. Your companions look to you.
""")
    # Available options depend on virtues and earlier choices
    options = []
    results = []

    # Always available
    options.append("Confront him with the truth of what he has become (Justice)")
    results.append("confront")

    if state.has_virtue("Compassion", 7) or state.flags["showed_mercy_to_enemy"]:
        options.append("Offer him a path back—mercy even now (Compassion)")
        results.append("mercy")

    if state.has_virtue("Wisdom", 7) and "Clay Lamp" in state.inventory:
        options.append("Hold up the clay lamp and speak of the hermit's words (Wisdom)")
        results.append("lamp")

    if state.flags["chose_power"] and "Black Key" in state.inventory:
        options.append("Use the Black Key to end him instantly (Power)")
        results.append("key")

    if state.has_virtue("Humility", 6) and state.total_virtue() >= 35:
        options.append("Kneel and confess your own failures before judging his (Humility)")
        results.append("humble")

    c = choice("The final choice is yours.", options)
    decision = results[c - 1]

    # Resolve
    if decision == "confront":
        state.change_virtue("Justice", 2)
        state.change_virtue("Courage", 1)
        print("\nYour words cut deeper than any blade. Malakar falters.")
        if state.companions["Kael"] >= 7:
            print("Kael stands with you. The citadel begins to crack.")
        state.ending = "justice"
    elif decision == "mercy":
        state.change_virtue("Compassion", 2)
        state.change_virtue("Humility", 1)
        print("\nHe laughs—then the laugh breaks. Something old and human surfaces in his eyes.")
        state.flags["showed_mercy_to_enemy"] = True
        state.ending = "mercy"
    elif decision == "lamp":
        state.change_virtue("Wisdom", 2)
        print("\nThe small flame does not fight the cold fire. It simply remains.
Malakar stares at it as if remembering a name he once knew.")
        state.ending = "wisdom"
    elif decision == "key":
        state.change_virtue("Temperance", -2)
        state.change_virtue("Justice", 1)
        print("\nThe key turns. Malakar is unmade in an instant.
The cold fire dies—yet the silence that follows is not peace.")
        state.ending = "power"
    elif decision == "humble":
        state.change_virtue("Humility", 3)
        state.change_virtue("Compassion", 1)
        print("\nYou speak of your own failures first.
Malakar has no answer for that. The citadel's light shifts.")
        state.ending = "humility"

    pause()
    state.story_stage = "ending"
    ending(state)

def ending(state: GameState):
    clear()
    print("═" * 60)
    print("  THE ROAD CONTINUES")
    print("═" * 60)

    # Determine narrative outcome based on ending type + virtues + flags
    if state.ending == "power":
        print("""
You ended the immediate threat. The north is quiet.
Yet the people look at you with a new kind of fear.
The clay lamp in your pack has gone dark.
""")
        if state.virtues["Temperance"] < 4:
            print("Something in you has grown used to taking what it wants.")
    elif state.ending == "mercy":
        print("""
Malakar lives—broken, but alive. Some call you weak.
Others begin to speak of a different kind of strength.
Elara stays by your side. The road ahead is longer, but less lonely.
""")
    elif state.ending == "wisdom":
        print("""
The citadel does not fall in fire. It is reclaimed, slowly.
Silas records what happened. Future travelers will read of a lamp
that refused to become a sword.
""")
    elif state.ending == "humility":
        print("""
You did not defeat Malakar so much as refuse to become him.
The people do not raise statues. They raise ordinary lamps instead.
""")
    else:  # justice
        print("""
Justice was done. The cost was real.
Kael understands the weight you both now carry.
The road is cleaner—and quieter.
""")

    # Companion epilogues
    print("\nYour companions:")
    for name, loy in state.companions.items():
        if loy >= 8:
            print(f"  {name} remains fiercely loyal. The bond was tested and held.")
        elif loy >= 5:
            print(f"  {name} walks with you still, though not without questions.")
        else:
            print(f"  {name} parts ways when the road allows. Some distances cannot be closed.")

    # Final virtue reflection (subtle, not preachy)
    print("\n" + "─" * 60)
    print("What you carried with you:")
    for v in VIRTUES:
        val = state.virtues[v]
        if val >= 8:
            print(f"  {v} — deeply rooted")
        elif val >= 5:
            print(f"  {v} — present, still growing")
        else:
            print(f"  {v} — tested, and found wanting")

    print("\n" + "─" * 60)
    print("""
The story ends here—but the road does not.
Every choice you made left a mark, not only on the world,
but on the one who walked it.

What you become next is still unwritten.
""")
    print("═" * 60)
    show_status(state)
    print("\nThank you for walking the narrow road.\n")

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║                    THE NARROW ROAD                       ║
║         A narrative fantasy of choice and consequence    ║
╚══════════════════════════════════════════════════════════╝
""")
    state = GameState()
    try:
        prologue(state)
    except KeyboardInterrupt:
        print("\n\nThe road can wait. Farewell.")
        sys.exit(0)

if __name__ == "__main__":
    main()
