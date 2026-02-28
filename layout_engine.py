import random

ROOM_TYPES = ["Living Room", "Bedroom", "Kitchen", "Bathroom"]

def generate_layout(width, height, room_count):
    layout = []
    remaining_width = width

    for i in range(room_count):
        room_width = random.uniform(3, remaining_width / (room_count - i))
        layout.append({
            "name": random.choice(ROOM_TYPES),
            "width": round(room_width, 2),
            "height": round(height / room_count, 2)
        })
        remaining_width -= room_width

    return layout