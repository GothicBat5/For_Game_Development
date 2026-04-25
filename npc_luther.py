import random
import time

W = 30
H = 20

DIRECTIONS = ["up", "down", "left", "right"]

DIALOGUE = [
    "*Whistling*",
    "What a strange place.",
    "I feel like I'm being watched.",
    "Just another day...",
    "Woah! did you hear that?",
    "I should keep moving."
]

class NPC:
    def __init__(self, name = "NPC"):
        self.name = name
        self.x = random.randint(0, W - 1)
        self.y = random.randint(0, H - 1)
        self.direction = random.choice(DIRECTIONS)

    def walk(self):
        self.direction = random.choice(DIRECTIONS)

        if self.direction == "up" and self.y > 0:
            self.y -= 1
        elif self.direction == "down" and self.y < H - 1:
            self.y += 1
        elif self.direction == "left" and self.x > 0:
            self.x -= 1
        elif self.direction == "right" and self.x < W - 1:
            self.x += 1

        print(f"{self.name} walks {self.direction} to ({self.x}, {self.y})")

    def look(self):
        self.direction = random.choice(DIRECTIONS)
        print(f"{self.name} looks {self.direction}...")

    def speak(self):
        line = random.choice(DIALOGUE)
        print(f'{self.name} says: "{line}"')

    def idle(self):
        print(f"{self.name} is standing still...")

    def act(self):
        action = random.choice(["walk", "look", "speak", "idle"])

        if action == "walk":
            self.walk()
        elif action == "look":
            self.look()
        elif action == "speak":
            self.speak()
        else:
            self.idle()


def draw_world(npc):
    print("\n" + "-" * (W * 2))
    for y in range(H):
        row = ""
        for x in range(W):
            if x == npc.x and y == npc.y:
                row += "N "
            else:
                row += ". "
        print(row)
    print("-" * (W * 2))


npc = NPC("Echo")

while True:
    draw_world(npc)
    npc.act()

    time.sleep(random.uniform(0.8, 2.0))
