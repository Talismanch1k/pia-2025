def can_place_square(board: list[int], x: int, y: int, w: int, n: int) -> bool:
    if x + w > n or y + w > n:
        return False

    mask = ((1 << w) - 1) << (n - x - w)

    for i in range(y, y + w):
        if (board[i] & mask) != 0:
            return False

    return True


def fill_square(board: list[int], x: int, y: int, w: int, n: int):
    mask = ((1 << w) - 1) << (n - x - w)

    for i in range(y, y + w):
        board[i] |= mask


def find_empty(board: list[int], n: int) -> tuple[int, int]:
    for y in range(n):
        row = board[y]
        if row == (1 << n) - 1:
            continue

        masked = (~row) & ((1 << n) - 1)

        if masked == 0:
            continue

        x = n - masked.bit_length()
        return x, y

    return -1, -1


def get_greedy_solution(n: int) -> list[tuple[int, int, int]]:
    W = (n + 1) // 2
    board = [0] * n
    places = [(0, 0, W), (0, W, n - W), (W, 0, n - W)]
    remain = n * n

    for x, y, w in places:
        fill_square(board, x, y, w, n)
        remain -= w * w

    while remain > 0:
        x, y = find_empty(board, n)
        if x == -1:
            break
        max_size = min(n - x, n - y)
        while max_size > 0 and not can_place_square(board, x, y, max_size, n):
            max_size -= 1
        if max_size == 0:
            break
        fill_square(board, x, y, max_size, n)
        places.append((x, y, max_size))
        remain -= max_size * max_size

    return places


def squaring(n: int) -> list[tuple[int, int, int]]:
    best_solution = get_greedy_solution(n)  # ищем жадное решение

    if len(best_solution) > 2 * n:
        best_solution = [None] * (2 * n)

    W = (n + 1) // 2
    places0 = [(0, 0, W), (0, W, n - W), (W, 0, n - W)]
    board0 = [0] * n
    remain0 = n * n

    for x, y, w in places0:
        fill_square(board0, x, y, w, n)
        remain0 -= w * w

    stack = [(board0, places0, remain0)]

    while stack:
        board, places, remain = stack.pop()

        if len(places) >= len(best_solution):
            continue

        if not remain:
            best_solution = places.copy()
            continue

        x, y = find_empty(board, n)

        max_size = min(n - x, n - y)
        min_squares_needed = (remain + max_size * max_size - 1) // (max_size * max_size)
        if len(places) + min_squares_needed >= len(best_solution):
            continue

        for size in range(max_size, 0, -1):
            if not can_place_square(board, x, y, size, n):
                continue

            new_board = board.copy()
            fill_square(new_board, x, y, size, n)

            new_remain = remain - size * size

            new_places = places.copy()
            new_places.append((x, y, size))

            stack.append((new_board, new_places, new_remain))

    return best_solution


def get_div(n: int) -> int:
    d = 2
    while d * d <= n:
        if n % d == 0:
            return d
        d += 1
    return n


def solve_squaring(n: int):
    d = get_div(n)  # сжатие квадрата до наим. простого множителя
    ans = squaring(d)

    # восстановление ответа + исправление координат
    res = n // d
    ans = [(x * res + 1, y * res + 1, w * res) for x, y, w in ans]

    return ans

if __name__ == '__main__':
    n = int(input())
    ans = solve_squaring(n)
    print(len(ans))
    for coords in ans:
        print(*coords)
