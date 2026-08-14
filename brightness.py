import screen_brightness_control as sbc


def brightness_up():

    current = sbc.get_brightness(display=0)[0]

    new = min(current + 10, 100)

    sbc.set_brightness(new)

    return f"Brightness increased to {new}%."


def brightness_down():

    current = sbc.get_brightness(display=0)[0]

    new = max(current - 10, 0)

    sbc.set_brightness(new)

    return f"Brightness decreased to {new}%."


def brightness_max():

    sbc.set_brightness(100)

    return "Brightness set to maximum."


def brightness_min():

    sbc.set_brightness(0)

    return "Brightness set to minimum."


def set_brightness(level):

    level = max(0, min(int(level), 100))

    sbc.set_brightness(level)

    return f"Brightness set to {level}%."