#!/usr/bin/env python3
"""
THE NARROW ROAD — Minecraft-style Sandbox Prototype
Keeps original virtue, loyalty, flag, and consequence systems.
Play loop: explore → gather/build → face moral events → shape the world.
"""

import random
import sys
from typing import Dict, List, Optional, Tuple

# ─────────────────────────────────────────────
# CORE SYSTEMS (unchanged from original)
# ─────────────────────────────────────────────

VIRTUES = ["Courage", "Wisdom", "Compassion", "Humility", "Temperance", "Justice"]

class GameState:
    def __init__(self):
        self.virtues: Dict[str, int] = {v: 5 for v in VIRTUES}
        self.companions: Dict[str, int] = {
            "Elara": 6,   # healer / mercy
            "Kael": 5,    # warrior / justice
            "Silas": 4,   # scholar / wisdom
        }
        self.inventory: Dict[str, int] = {
            "Wood": 0, "Stone": 0, "Food": 3, "Iron": 0, "Sacred Seed": 0
        }
        self.flags: Dict[str, bool] = {
            "spared_bandit": False,
            "took_gold": False,
            "helped_village": False,
            "trusted_whisper": False,
            "broke_oath": False,
            "showed_mercy_to_enemy": False,
            "chose_power": False,
            "chose_sacrifice": False,
            "restored_grove": False,
            "overharvested": False,
            "built_sanctuary": False,
            "fortress_only": False,
        }
        self.world = {
            "Whispering Woods": {"state": "healthy", "resources": ["Wood", "Food"]},
            "Burning Village": {"state": "ruined", "resources": ["Stone", "Food"]},
            "High Pass": {"state": "neutral", "resources": ["Stone", "Iron"]},
            "Northern Citadel": {"state": "corrupted", "resources": []},
        }
        self.location = "Whispering Woods"
        self.player_name = "Traveler"
        self.day = 1
        self.ending = None
        self.story_stage = "explore"

    def change_virtue(self, name: str, amount: int, silent: bool = False):
        if name in self.virtues:
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

    def add_item(self, item: str, amount: int = 1):
        self.inventory[item] = self.inventory.get(item, 0) + amount

    def has_item(self, item: str, amount: int = 1) -> bool:
        return self.inventory.get(item, 0) >= amount

# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────

def clear():
    print("\n" + "─" * 64)

def pause():
    input("\n[Enter]")

def choice(prompt: str, options: List[str]) -> int:
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        try:
            sel = int(input("\n> ").strip())
            if 1 <= sel <= len(options):
                return sel
        except ValueError:
            pass
        print("Enter a valid number.")

def show_status(state: GameState):
    clear()
    print(f"  {state.player_name}  |  Day {state.day}  |  {state.location}")
    print("─" * 64)
    print("  Virtues:")
    for v in VIRTUES:
        bar = "█" * state.virtues[v] + "░" * (10 - state.virtues[v])
        print(f"    {v:<12} [{bar}] {state.virtues[v]}")
    print("─" * 64)
    print("  Companions:")
    for name, loy in state.companions.items():
        hearts = "♥" * loy + "♡" * (10 - loy)
        print(f"    {name:<8} {hearts}")
    print("─" * 64)
    inv = [f"{k}:{v}" for k, v in state.inventory.items() if v > 0]
    print("  Inventory:", ", ".join(inv) if inv else "empty")
    print("─" * 64)
    print("  World state:")
    for place, data in state.world.items():
        print(f"    {place}: {data['state']}")
    print("═" * 64)
    pause()

# ─────────────────────────────────────────────
# WORLD ACTIONS (Minecraft-style loops)
# ─────────────────────────────────────────────

def gather(state: GameState):
    loc = state.world[state.location]
    if not loc["resources"]:
        print("\nNothing useful left to gather here.")
        return

    print(f"\nYou search the {state.location}...")
    resource = random.choice(loc["resources"])

    # Moral cost for over-harvesting
    if state.flags.get("overharvested") or random.random() < 0.3:
        print(f"You find {resource}, but the land feels thinner.")
        state.change_virtue("Temperance", -1)
        state.change_virtue("Compassion", -1)
        if state.location == "Whispering Woods":
            state.world["Whispering Woods"]["state"] = "thinning"
            state.flags["overharvested"] = True
    else:
        print(f"You carefully gather {resource}.")
        if resource == "Wood" and state.has_virtue("Humility", 6):
            state.change_virtue("Temperance", 1)

    state.add_item(resource, random.randint(1, 3))
    pause()

def build(state: GameState):
    print("\nWhat do you wish to raise?")
    options = [
        "Simple shelter (3 Wood) — basic protection",
        "Shared storehouse (5 Wood + 2 Stone) — helps the land and people",
        "Fortified outpost (8 Stone + 3 Iron) — strong defense, closed to outsiders",
        "Sanctuary garden (4 Wood + Sacred Seed) — restores the land (requires seed)"
    ]
    c = choice("Building choice:", options)

    if c == 1 and state.has_item("Wood", 3):
        state.inventory["Wood"] -= 3
        print("\nA simple shelter stands. You can rest more safely.")
        state.change_virtue("Temperance", 1)
    elif c == 2 and state.has_item("Wood", 5) and state.has_item("Stone", 2):
        state.inventory["Wood"] -= 5
        state.inventory["Stone"] -= 2
        print("\nThe storehouse is open to any who need it. Word spreads.")
        state.change_virtue("Compassion", 2)
        state.change_virtue("Humility", 1)
        state.change_loyalty("Elara", 1)
        state.flags["helped_village"] = True
        if state.location in state.world:
            state.world[state.location]["state"] = "recovering"
    elif c == 3 and state.has_item("Stone", 8) and state.has_item("Iron", 3):
        state.inventory["Stone"] -= 8
        state.inventory["Iron"] -= 3
        print("\nThick walls rise. Nothing enters without your leave.")
        state.change_virtue("Courage", 1)
        state.change_virtue("Justice", 1)
        state.change_virtue("Compassion", -1)
        state.change_virtue("Humility", -1)
        state.flags["fortress_only"] = True
        state.change_loyalty("Kael", 1)
        state.change_loyalty("Elara", -1)
    elif c == 4 and state.has_item("Wood", 4) and state.has_item("Sacred Seed"):
        state.inventory["Wood"] -= 4
        state.inventory["Sacred Seed"] -= 1
        print("\nYou plant the seed and raise a quiet garden around it.")
        state.change_virtue("Compassion", 2)
        state.change_virtue("Humility", 2)
        state.change_virtue("Temperance", 1)
        state.flags["restored_grove"] = True
        state.flags["built_sanctuary"] = True
        state.world["Whispering Woods"]["state"] = "restored"
        state.change_loyalty("Elara", 2)
        state.change_loyalty("Silas", 1)
    else:
        print("\nYou lack the materials or the seed.")
    pause()

def talk_companions(state: GameState):
    print("\nYour companions are nearby.")
    options = list(state.companions.keys()) + ["Never mind"]
    c = choice("Speak with:", options)
    if c == len(options):
        return

    name = options[c-1]
    loy = state.companions[name]

    if name == "Elara":
        if loy >= 7:
            print("\nElara: \"The land remembers kindness. So do I.\"")
            if not state.has_item("Sacred Seed") and state.flags.get("helped_village"):
                print("She presses a small glowing seed into your hand.")
                state.add_item("Sacred Seed")
        elif loy <= 3:
            print("\nElara looks away. \"I am not sure this road still leads where I hoped.\"")
        else:
            print("\nElara: \"We can still choose what kind of people we become.\"")
    elif name == "Kael":
        if state.has_virtue("Justice", 7):
            print("\nKael: \"Good. The world needs people who will stand when it costs them.\"")
            state.change_loyalty("Kael", 1)
        else:
            print("\nKael: \"Mercy is fine until the next village burns.\"")
    elif name == "Silas":
        if state.has_virtue("Wisdom", 6):
            print("\nSilas: \"The old texts speak of a lamp that cannot be seized, only tended.\"")
            state.change_virtue("Wisdom", 1)
        else:
            print("\nSilas is quiet, watching the horizon.")
    pause()

def travel(state: GameState):
    places = [p for p in state.world if p != state.location]
    c = choice("Travel to:", places + ["Stay here"])
    if c == len(places) + 1:
        return
    state.location = places[c-1]
    state.day += 1
    print(f"\nYou travel to the {state.location}.")
    # Random or triggered events
    if state.location == "Burning Village" and not state.flags["helped_village"]:
        event_village(state)
    elif state.location == "High Pass":
        event_hermit(state)
    elif state.location == "Northern Citadel":
        if state.total_virtue() >= 30 or state.day >= 8:
            climax(state)
        else:
            print("\nThe gates are sealed by a cold light. You are not yet ready.")
    pause()

# ─────────────────────────────────────────────
# KEY MORAL EVENTS (same systems)
# ─────────────────────────────────────────────

def event_village(state: GameState):
    clear()
    print("""
The village still smolders. A child clutches a scorched doll.
An old woman points to the well: "They took the water. Left us the fire."
""")
    c = choice("What do you do?", [
        "Help the wounded and share your Food (Compassion)",
        "Hunt the raiders immediately (Justice / Courage)",
        "Study the signs left behind (Wisdom)",
        "Take what little remains and leave (Temptation)"
    ])
    if c == 1 and state.has_item("Food", 1):
        state.inventory["Food"] -= 1
        state.change_virtue("Compassion", 2)
        state.change_loyalty("Elara", 2)
        state.flags["helped_village"] = True
        state.world["Burning Village"]["state"] = "recovering"
        print("\nYou and Elara work through the day. Lives are saved.")
    elif c == 2:
        state.change_virtue("Courage", 1)
        state.change_virtue("Justice", 1)
        state.change_loyalty("Kael", 2)
        print("\nYou pursue. The raiders are caught—but the village suffers more in your absence.")
        # mini raider choice
        c2 = choice("Their young leader is at your mercy.", [
            "End him.", "Spare and question him.", "Offer him another road."
        ])
        if c2 == 1:
            state.change_virtue("Compassion", -2)
            state.flags["spared_bandit"] = False
        elif c2 == 2:
            state.change_virtue("Wisdom", 1)
            state.flags["spared_bandit"] = True
        else:
            state.change_virtue("Compassion", 2)
            state.change_virtue("Humility", 1)
            state.flags["spared_bandit"] = True
            state.flags["showed_mercy_to_enemy"] = True
    elif c == 3:
        state.change_virtue("Wisdom", 2)
        state.change_loyalty("Silas", 2)
        print("\nYou learn the name Malakar. The attack was paid for from the north.")
        state.flags["helped_village"] = True
    else:
        state.change_virtue("Temperance", -2)
        state.change_virtue("Compassion", -2)
        state.add_item("Food", 2)
        state.add_item("Stone", 1)
        print("\nYou take what you can carry. The villagers watch in silence.")
        state.flags["took_gold"] = True
    pause()

def event_hermit(state: GameState):
    clear()
    print("""
At the High Pass a hermit tends a small lamp that never gutters.
"What do you carry that cannot be taken from you?"
""")
    c = choice("Your answer:", [
        "My strength and my tools.",
        "The bonds with those who walk with me.",
        "Nothing that belongs to me alone.",
        "I do not know yet."
    ])
    if c == 1:
        state.change_virtue("Humility", -1)
        state.change_virtue("Courage", 1)
    elif c == 2:
        state.change_virtue("Compassion", 1)
        for k in state.companions:
            state.change_loyalty(k, 1)
    elif c == 3:
        state.change_virtue("Humility", 2)
        state.change_virtue("Wisdom", 1)
    else:
        state.change_virtue("Humility", 1)
        state.change_virtue("Wisdom", 1)

    if not state.has_item("Sacred Seed") and state.has_virtue("Humility", 6):
        print("\nHe presses a clay lamp and a single seed into your hands.")
        state.add_item("Sacred Seed")
        state.add_item("Clay Lamp")
    else:
        print("\nHe nods and returns to his lamp.")
    pause()

def climax(state: GameState):
    clear()
    print("""
You stand before the Northern Citadel.
Malakar waits. "I tired of waiting for the light. I decided to become it."
""")
    options = []
    results = []

    options.append("Confront him with the truth (Justice)")
    results.append("confront")

    if state.has_virtue("Compassion", 7) or state.flags["showed_mercy_to_enemy"]:
        options.append("Offer him a path back (Compassion)")
        results.append("mercy")

    if state.has_virtue("Wisdom", 7) and state.has_item("Clay Lamp"):
        options.append("Hold up the clay lamp (Wisdom)")
        results.append("lamp")

    if state.flags.get("chose_power"):
        options.append("Use the power you claimed (Power)")
        results.append("key")

    if state.has_virtue("Humility", 6) and state.total_virtue() >= 35:
        options.append("Speak first of your own failures (Humility)")
        results.append("humble")

    if state.flags.get("restored_grove") or state.flags.get("built_sanctuary"):
        options.append("Point to the restored land behind you (Stewardship)")
        results.append("steward")

    c = choice("Final choice:", options)
    decision = results[c-1]

    if decision == "confront":
        state.change_virtue("Justice", 2)
        state.ending = "justice"
    elif decision == "mercy":
        state.change_virtue("Compassion", 2)
        state.ending = "mercy"
    elif decision == "lamp":
        state.change_virtue("Wisdom", 2)
        state.ending = "wisdom"
    elif decision == "key":
        state.change_virtue("Temperance", -2)
        state.ending = "power"
    elif decision == "humble":
        state.change_virtue("Humility", 3)
        state.ending = "humility"
    elif decision == "steward":
        state.change_virtue("Compassion", 1)
        state.change_virtue("Temperance", 2)
        state.ending = "steward"

    state.story_stage = "ending"
    ending(state)

def ending(state: GameState):
    clear()
    print("═" * 64)
    print("  THE WORLD YOU SHAPED")
    print("═" * 64)

    if state.ending == "power":
        print("\nYou ended the immediate threat. The north is quiet.\nThe people look at you differently now.")
    elif state.ending == "mercy":
        print("\nMalakar lives—broken, but alive. Some call it weakness.\nOthers begin planting again.")
    elif state.ending == "wisdom":
        print("\nThe citadel is reclaimed slowly. Future travelers will read of a lamp\nthat refused to become a sword.")
    elif state.ending == "humility":
        print("\nYou did not defeat him so much as refuse to become him.\nOrdinary lamps appear in windows across the land.")
    elif state.ending == "steward":
        print("\nThe land itself answers. Where you restored, life returns.\nThe citadel's cold fire finally gutters out.")
    else:
        print("\nJustice was done. The cost remains.")

    print("\nCompanions:")
    for name, loy in state.companions.items():
        if loy >= 8:
            print(f"  {name} remains with you.")
        elif loy >= 5:
            print(f"  {name} continues, with questions.")
        else:
            print(f"  {name} parts ways.")

    print("\nFinal virtues:")
    for v in VIRTUES:
        val = state.virtues[v]
        status = "deeply rooted" if val >= 8 else "present" if val >= 5 else "tested and found wanting"
        print(f"  {v}: {status}")

    print("\nWorld state:")
    for place, data in state.world.items():
        print(f"  {place}: {data['state']}")

    print("\n" + "═" * 64)
    print("The story ends here—but the road does not.")
    print("═" * 64 + "\n")

# ─────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║              THE NARROW ROAD (Sandbox Edition)           ║
║       Explore. Build. Make Choices. Shape the World.     ║
╚══════════════════════════════════════════════════════════╝
""")
    state = GameState()
    state.player_name = input("What name do you carry on this road? ").strip() or "Traveler"
    print(f"\nVery well, {state.player_name}. The road opens.\n")
    pause()

    while state.story_stage == "explore":
        clear()
        print(f"Day {state.day} — {state.location}")
        print("What do you do?")
        c = choice("Choose:", [
            "Gather resources",
            "Build something",
            "Talk with companions",
            "Travel elsewhere",
            "Check your status"
        ])
        if c == 1:
            gather(state)
        elif c == 2:
            build(state)
        elif c == 3:
            talk_companions(state)
        elif c == 4:
            travel(state)
        elif c == 5:
            show_status(state)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nThe road can wait. Farewell.")
        sys.exit(0)
