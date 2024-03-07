from copy import deepcopy

from compmath.models.slat.base import BaseSLATModel
from compmath.utils.func import gauss_calc, is_diagonal_dominance


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
        log_transformed = ["\nИсходная матрица\n"]
        for i, row in enumerate(a_matrix):
            log_transformed.append(
                "\t".join(str(cell) for cell in row) + "\t|   " + str(b_vector[i])
            )
        log_transformed.append("")

        for i, row in enumerate(a_matrix):
            sum_row = sum(abs(cell) for j, cell in enumerate(row) if j != i)
            log_transformed.append(
               f"sum({", ".join(f'|{cell}|' for j, cell in enumerate(row) if j != i)}) = "
               f"{sum_row}   {'>' if sum_row > abs(row[i]) else '<='}   |{row[i]}|"
               f"\t[{'-' if sum_row > abs(row[i]) else '+'}]"
            )
        log_transformed.append("")

        if is_diagonal_dominance(a_matrix):
            log_transformed.append("Матрица обладает диагональным преобладанием")
            log_transformed.append("Необходимости в элементарных преобразованиях исходной матрицы нет")
        else:
            log_transformed.append("Матрица не обладает диагональным преобладанием")
            log_transformed.append("Необходимо преобразовать исходную матрицу")

            log_transformed.append("\nПреобразованная матрица\n")
            transformed_a_matrix, transformed_b_vector, log = self.transform_matrix()
            log_transformed.append("Шаги:")
            log_transformed.extend(log)
            log_transformed.append("")
            for i, row in enumerate(transformed_a_matrix):
                log_transformed.append(
                    "\t".join(str(round(cell, 2)) for cell in row) + "\t|   " + str(round(transformed_b_vector[i], 2))
                )

            log_transformed.append("\nРешение методом Гаусса\n")

            transformed_gauss_vector = gauss_calc(transformed_a_matrix, transformed_b_vector, n)
            log_transformed.append("\n".join(str(cell) for cell in transformed_gauss_vector[0]))

            log_transformed.append("\nВектор невязок\n")
            log_transformed.append("\n".join(str(round(cell, 2)) for cell in transformed_gauss_vector[1]))

            log_transformed.append("\nТреугольная матрица\n")
            for row in transformed_gauss_vector[2]:
                log_transformed.append("\t".join(str(round(cell, 2)) for cell in row))

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

