from copy import deepcopy

from compmath.models.slat.base import BaseSLATModel
from compmath.utils.func import gauss_calc


class GModel(BaseSLATModel):

    def __init__(self):
        super().__init__()

        self._title = "Метод Гаусса"
        self._description = "Метод Гаусса - метод решения системы линейных уравнений..."

    def calc(self):
        self.results.clear()

        n = len(self.a())
        a_matrix = deepcopy(self.a())
        b_vector = deepcopy(self.b())
        x = deepcopy(self.x0)

        # Исходная матрица
        log_original = ["\nИсходная матрица\n"]
        for i, row in enumerate(a_matrix):
            log_original.append(
                "\t".join(str(cell) for cell in row) + "\t|   " + str(b_vector[i])
            )
        log_original.append("\nИсходный вектор свободных членов\n")
        log_original.append("\t".join(str(cell) for cell in b_vector))

        log_original.append("\nПрямой ход метода Гаусса\n")
        original_gauss_vector = gauss_calc(a_matrix, b_vector, n)
        log_original.append("\n".join(str(cell) for cell in original_gauss_vector[0]))

        log_original.append("\nВектор невязок\n")
        log_original.append("\n".join(str(cell) for cell in original_gauss_vector[1]))

        log_original.append("\nТреугольная матрица\n")
        for row in original_gauss_vector[2]:
            log_original.append("\t".join(str(round(cell, 2)) for cell in row))

        self.results.append((log_original, [], "Исходная матрица"))

        # Преобразованная матрица
        log_transformed = ["\nПреобразованная матрица\n"]
        ...
        self.results.append((log_transformed, [], "Преобразованная матрица"))

        # Нормализованная матрица
        log_normalized = ["\nНормализованная матрица\n"]
        normal_a_matrix, normal_b_vector = self.normal_matrix()
        for i, row in enumerate(normal_a_matrix):
            log_normalized.append(
                "\t".join(str(round(cell, 2)) for cell in row) + "\t|   " + str(round(normal_b_vector[i], 2))
            )

        log_normalized.append("\nРешение методом Гаусса\n")
        normal_gauss_vector = gauss_calc(normal_a_matrix, normal_b_vector, n)
        log_normalized.append("\n".join(str(cell) for cell in normal_gauss_vector[0]))

        log_normalized.append("\nВектор невязок\n")
        log_normalized.append("\n".join(str(round(cell, 2)) for cell in normal_gauss_vector[1]))

        log_normalized.append("\nТреугольная матрица\n")
        for row in normal_gauss_vector[2]:
            log_normalized.append("\t".join(str(round(cell, 2)) for cell in row))

        self.results.append((log_normalized, [], "Нормализованная матрица"))

        self.notify_observers()

