def prefix_function(text, debug=False):
    n = len(text)
    pref = [0] * n
    
    if debug:
        print(f"Вычисление префикс-функции для строки: '{text}'")

    for i in range(1, n):
        j = pref[i - 1]
        if debug:
            print(f"i={i}, символ='{text[i]}', начальное j={j}")
        
        while j > 0 and text[i] != text[j]:
            if debug:
                print(f"  Несовпадение: '{text[i]}' != '{text[j]}', переход к j={pref[j-1]}")
            j = pref[j - 1]
        
        if text[i] == text[j]:
            j += 1
            if debug:
                print(f"  Совпадение: '{text[i]}' == '{text[j-1]}', увеличиваем j до {j}")
        
        pref[i] = j

    if debug:
        print(f"Итоговая префикс-функция: {pref}")
    
    return pref

def kmp_optimized(pattern, text, debug=False):
    p = len(pattern)
    n = len(text)
    
    if debug:
        print(f"KMP_OPTIMIZED: поиск pattern='{pattern}' в text='{text}'")
    
    if p > n:
        if debug:
            print("Шаблон длиннее текста, совпадений нет")
        return [-1]
    
    pref = prefix_function(pattern, debug)
    
    matches = []
    j = 0
    
    if debug:
        print("Поиск совпадений:")
    
    for i in range(n):
        if debug:
            print(f"i={i}, символ text[{i}]='{text[i]}', j = {j}")
        
        while j > 0 and text[i] != pattern[j]:
            if debug:
                print(f"  Несовпадение: '{text[i]}' != '{pattern[j]}', переход к j={pref[j-1]}")
            j = pref[j - 1]
        
        if text[i] == pattern[j]:
            j += 1
            if debug:
                print(f"  Совпадение: '{text[i]}' == '{pattern[j-1]}', увеличиваем j до {j}")
        
        if j == p:
            match_pos = i - p + 1
            if debug:
                print(f"  Найдено полное совпадение на позиции {match_pos}")
            matches.append(match_pos)
            j = pref[j - 1]
    
    if debug:
        print(f"Все найденные совпадения: {matches if matches else [-1]}")
    
    return matches if matches else [-1]

def cyclic(a, b, debug=False):
    n = len(a)
    m = len(b)

    if debug:
        print(f"CYCLIC: поиск сдвига между a='{a}' и b='{b}'")

    if n != m:
        if debug:
            print("Строки разной длины, циклического сдвига не существует")
        return -1

    pref = prefix_function(b, debug)
    l = 0

    if debug:
        print(f"Поиск сдвига с использованием префикс-функции b:")

    for i in range(n * 2):
        c = a[i % n]
        if debug:
            print(f"i={i}, символ a[{i%n}] = '{c}', l={l}")
        
        while l > 0 and c != b[l]:
            if debug:
                print(f"  Несовпадение: '{c}' != '{b[l]}', переход к l={pref[l-1]}")
            l = pref[l - 1]
        
        if c == b[l]:
            l += 1
            if debug:
                print(f"  Совпадение: '{c}' == '{b[l-1]}', увеличиваем l до {l}")
        
        if l == m:
            result = (i - m + 1) % n
            if debug:
                print(f"  Найден циклический сдвиг: {result}")
            return result

    if debug:
        print("Циклический сдвиг не найден")
    return -1

def find_rot(debug=False):
    a = input()
    b = input()
    print(cyclic(a, b, debug))

def find_substr(debug=False):
    pattern = input()
    text = input()
    print(','.join(map(str,(kmp_optimized(pattern, text, debug)))))

if __name__ == '__main__':
    find_substr(debug=True)
    # find_rot(debug=True)

