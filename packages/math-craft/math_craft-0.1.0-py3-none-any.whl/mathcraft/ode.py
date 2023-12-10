from beartype import beartype


class RungeKuttaFirstOrder:
    def __init__(self, function):
        self.function = function

    def solve(self, initial_condition, h, num_steps):
        result = [initial_condition]
        current_state = initial_condition

        for _ in range(num_steps):
            k1 = h * self.function(current_state)
            current_state = current_state + k1
            result.append(current_state)

        return result
