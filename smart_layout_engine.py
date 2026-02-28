def generate_smart_layout(width, height):

    layout = []

    # Entrance area
    layout.append({
        "name": "Living Room",
        "zone": "front",
        "width": width * 0.4,
        "height": height * 0.5
    })

    # Kitchen (not near bathroom)
    layout.append({
        "name": "Kitchen",
        "zone": "middle",
        "width": width * 0.3,
        "height": height * 0.4
    })

    # Bathroom (separate corner)
    layout.append({
        "name": "Bathroom",
        "zone": "corner",
        "width": width * 0.2,
        "height": height * 0.2
    })

    # Bedroom (quiet zone)
    layout.append({
        "name": "Bedroom",
        "zone": "back",
        "width": width * 0.4,
        "height": height * 0.5
    })

    # Garage (outer side)
    layout.append({
        "name": "Garage",
        "zone": "outer",
        "width": width * 0.3,
        "height": height * 0.4
    })

    return layout