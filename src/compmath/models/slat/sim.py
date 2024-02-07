from compmath.models.slat.base import BaseSLATModel


class SIModel(BaseSLATModel):

    def __init__(self):
        super().__init__()

        self._title = "Метод простых итераций"

    def calc(self):
        k = 0
        n = len(self.a())
        a_matrix = self.a()
        b_vector = self.b()
        x = self.x0.copy()

        while True:
            k += 1
            x_prev = x.copy()
            for i in range(n):
                s = sum(a_matrix[i][j] * x[j] for j in range(n) if j != i)
                x[i] = (b_vector[i] - s) / a_matrix[i][i]

            # Оценка точности
            delta = max(abs(x[i] - x_prev[i]) for i in range(n))

            if delta <= self.eps or k >= self.iters_limit:
                break

        print(x, delta, k)
        return x, delta, k
