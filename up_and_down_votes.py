def get_up_and_down(score, percentage):
    down = score / (percentage / (1 - percentage) - 1)
    up = down * (percentage / (1 - percentage))
    return (up, down)

print(get_up_and_down(15900, .95))