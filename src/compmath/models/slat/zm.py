from compmath.models.slat.base import BaseSLATModel


class ZModel(BaseSLATModel):

    def __init__(self):
        super().__init__()

        self._title = "Метод Зейделя"
        self._description = "Метод Зейделя - модификация метода простых итераций..."

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
                s1 = sum(a_matrix[i][j] * x[j] for j in range(i))
                s2 = sum(a_matrix[i][j] * x_prev[j] for j in range(i + 1, n))
                x[i] = (b_vector[i] - s1 - s2) / a_matrix[i][i]

            # Оценка точности
            delta = max(abs(x[i] - x_prev[i]) for i in range(n))

            if delta <= self.eps or k > self.iters_limit:
                break

        print(x, delta, k)
        return x, delta, k
