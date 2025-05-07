import random

firstnames = [
]

animals = [
    "Lion",
    "Elephant",
    "Tiger",
    "Giraffe",
    "Zebra",
    "Kangaroo",
    "Penguin",
    "Dolphin",
    "Eagle",
    "Shark",
    "Octopus",
    "Gorilla",
    "Panda",
    "Rhino",
    "Alligator",
]

adjectives = [
    "Majestic",
    "Gentle",
    "Powerful",
    "Graceful",
    "Striped",
    "Bouncy",
    "Adorable",
    "Intelligent",
    "Fearsome",
    "Mysterious",
    "Strong",
    "Cute",
    "Armored",
    "Stealthy",
]

colors = [
    "Red",
    "Blue",
    "Green",
    "Yellow",
    "Purple",
    "Orange",
    "Pink",
    "Black",
    "White",
    "Brown",
    "Gray",
    "Cyan",
    "Magenta",
    "Gold",
    "Silver",
]


def generate_name():
    # random.random() * firstnames.__len__()
    color = colors[round(random.random() * colors.__len__()) - 1]
    adjective = adjectives[round(random.random() * adjectives.__len__()) - 1]
    animal = animals[round(random.random() * animals.__len__()) - 1]
    return f"{adjective}-{color}-{animal}"
