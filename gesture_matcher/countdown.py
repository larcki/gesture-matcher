def countdown(label_to_update, action, final_text, final_text_color, suffix):
    current_value = label_to_update.text[-1]
    new_value = int(current_value) - 1
    if new_value <= 0:
        action()
        label_to_update.text = final_text()
        label_to_update.color = final_text_color()
        return False
    label_to_update.text = suffix + str(new_value)
    return True
