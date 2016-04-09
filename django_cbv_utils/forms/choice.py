
def add_empty_choice(choices, empty_value="", empty_label="---------"):
    choices_with_empty = [(empty_value, empty_label)]
    choices_with_empty.extend(choices)
    return choices_with_empty

