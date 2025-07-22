def simulate_fluid_level(initial_volume, rate_per_hour, total_time_hr):
    levels = []
    steps = int(total_time_hr * 10)
    decrement = initial_volume / steps
    current = initial_volume
    for _ in range(steps):
        current -= decrement
        if current < 0:
            current = 0
        levels.append(current)
    return levels