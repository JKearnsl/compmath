from compmath.models.slat.base import BaseSLATModel, TableRow


class SIModel(BaseSLATModel):

    def __init__(self):
        super().__init__()

        self._title = "Метод простых итераций"

    def calc(self):
        self.table.clear()

        k = 0
        n = len(self.a())
        a_matrix = self.a()
        b_vector = self.b()
        x = self.x0.copy()
        delta = 0

        while True:
            k += 1
            x_prev = x.copy()
            for i in range(n):
                s = sum(a_matrix[i][j] * x[j] for j in range(n) if j != i)
                x[i] = (b_vector[i] - s) / a_matrix[i][i]

            # Оценка точности
            delta = max(abs(x[i] - x_prev[i]) for i in range(n))

            self.table.append(
                TableRow(
                    iter_num=k,
                    vector=x.copy(),
                    delta=delta
                )
            )

            if delta <= self.eps or k >= self.iters_limit:
                break

        self.was_calculated()
