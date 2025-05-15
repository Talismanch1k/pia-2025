def prefix_function(text, debug=False):
    n = len(text)
    pref = [0] * n
    
    if debug:
        print("\n" + "="*50)
        print(f"АЛГОРИТМ ПРЕФИКС-ФУНКЦИИ для строки: '{text}'")
        print("="*50)
        print("Назначение: находит для каждой позиции длину наибольшего собственного префикса, \nкоторый является суффиксом для подстроки, заканчивающейся в этой позиции.")
        print("Позиция 0 всегда имеет значение 0")
        print(f"Символы строки: {' | '.join(text)}")
        print(f"Индексы:        {' | '.join([str(i) for i in range(n)])}")
        print("-"*50)

    j = 0
    for i in range(1, n):
        if debug:
            print(f"\nШаг {i}: Рассматриваем символ '{text[i]}' в позиции {i}")
            print(f"Текущий префикс имеет длину j = {j} ('{text[:j]}')")
        
        while j > 0 and text[i] != text[j]:
            if debug:
                print(f"  Несовпадение: '{text[i]}' != '{text[j]}'")
                print(f"  Сокращаем префикс с {j} до {pref[j-1]} (переходим по префикс-функции)")
            j = pref[j - 1]
        
        if text[i] == text[j]:
            j += 1
            if debug:
                print(f"  Совпадение: '{text[i]}' == '{text[j-1]}'")
                print(f"  Увеличиваем длину префикса до j = {j}")
        
        pref[i] = j
        if debug:
            print(f"  Значение префикс-функции для позиции {i}: pref[{i}] = {j}")
            current_pref = [str(x) for x in pref[:i+1]]
            while len(current_pref) < n:
                current_pref.append(" ")
            print(f"  Текущий массив префикс-функции: [{' | '.join(current_pref)}]")

    if debug:
        print("\nИтоговая префикс-функция:")
        print(f"Символы строки:    {' | '.join(text)}")
        print(f"Индексы:           {' | '.join([str(i) for i in range(n)])}")
        print(f"Значения префикса: {' | '.join([str(x) for x in pref])}")
        print("="*50)
    
    return pref

# abacaba
# 

def kmp_optimized(pattern, text, debug=False):
    p = len(pattern)
    n = len(text)
    
    if debug:
        print("\n" + "="*50)
        print(f"АЛГОРИТМ КМП (КНУТА-МОРРИСА-ПРАТТА)")
        print("="*50)
        print(f"Шаблон для поиска: '{pattern}', длина = {p}")
        print(f"Текст для поиска:   '{text}', длина = {n}")
        print("-"*50)
    
    if p > n:
        if debug:
            print("Шаблон длиннее текста, поиск невозможен")
        return [-1]
    
    if debug:
        print("\nШаг 1: Вычисляем префикс-функцию для шаблона")
    
    pref = prefix_function(pattern, debug)
    
    matches = []
    j = 0
    
    if debug:
        print("\nШаг 2: Выполняем поиск шаблона в тексте")
        print("-"*50)
    
    for i in range(n):
        if debug:
            current_match = text[:i] + "[" + text[i] + "]" + text[i+1:]
            ptr_pattern = " " * (i-j) + pattern if j > 0 else " " * i + pattern
            print(f"\nПозиция текста: {i}, символ '{text[i]}'")
            print(f"Текст:   {current_match}")
            if j > 0:
                print(f"Шаблон:  {ptr_pattern} (сдвиг = {i-j}, совпало {j} символов)")
            else:
                print(f"Шаблон:  {ptr_pattern}")
        
        while j > 0 and text[i] != pattern[j]:
            if debug:
                print(f"  Несовпадение: '{text[i]}' != '{pattern[j]}'")
                print(f"  Сокращаем префикс с {j} до {pref[j-1]} (переходим по префикс-функции pref[{j-1}] = {pref[j-1]})")
            j = pref[j - 1]
            if debug and j > 0:
                ptr_pattern = " " * (i-j) + pattern
                print(f"  Новое положение шаблона: {ptr_pattern} (сдвиг = {i-j})")
        
        if text[i] == pattern[j]:
            if debug:
                print(f"  Совпадение: '{text[i]}' == '{pattern[j]}'")
            j += 1
            if debug:
                print(f"  Увеличиваем счетчик совпадений: j = {j}")
        
        if j == p:
            match_pos = i - p + 1
            if debug:
                print(f"\n  НАЙДЕНО ПОЛНОЕ СОВПАДЕНИЕ!")
                print(f"  Начальная позиция: {match_pos}")
                match_visual = text[:match_pos] + "[" + text[match_pos:match_pos+p] + "]" + text[match_pos+p:]
                print(f"  {match_visual}")
                print(f"  Сокращаем префикс с {j} до {pref[j-1]} (переходим по префикс-функции pref[{j-1}] = {pref[j-1]})")
            
            matches.append(match_pos)
            j = pref[j - 1]
    
    if debug:
        print("\n" + "="*50)
        if matches:
            print(f"Результат: найдено {len(matches)} совпадений на позициях {matches}")
        else:
            print("Результат: совпадений не найдено")
        print("="*50)
    
    return matches if matches else [-1]

def cyclic(a, b, debug=False):
    n = len(a)
    m = len(b)

    if debug:
        print("\n" + "="*50)
        print(f"АЛГОРИТМ ПОИСКА ЦИКЛИЧЕСКОГО СДВИГА")
        print("="*50)
        print(f"Строка a: '{a}', длина = {n}")
        print(f"Строка b: '{b}', длина = {m}")
        print("Задача: найти такое k, что циклический сдвиг строки a на k позиций даст строку b")
        print("-"*50)

    if n != m:
        if debug:
            print("Строки имеют разную длину, циклический сдвиг не существует")
        return -1

    if debug:
        print("\nШаг 1: Вычисляем префикс-функцию для строки b")
    
    pref = prefix_function(b, debug)
    j = 0

    if debug:
        print("\nШаг 2: Ищем b в строке a+a (конкатенация a с самой собой)")
        print(f"Строка a+a: '{a+a}'")
        print("-"*50)

    for i in range(n * 2):
        c = a[i % n]
        
        if debug:
            aa = a + a
            ptr = aa[:i] + "[" + aa[i] + "]" + aa[i+1:2*n]
            pattern_vis = " " * max(0, i-j) + b if j > 0 else " " * i + b
            print(f"\nИндекс i = {i} (в строке a это позиция {i % n})")
            print(f"a+a:    {ptr}")
            if j > 0:
                print(f"b:      {pattern_vis} (совпало {j} символов)")
            else:
                print(f"b:      {pattern_vis}")
        
        while j > 0 and c != b[j]:
            if debug:
                print(f"  Несовпадение: '{c}' != '{b[j]}'")
                print(f"  Сокращаем префикс с {j} до {pref[j-1]} (переходим по префикс-функции pref[{j-1}] = {pref[j-1]})")
            j = pref[j - 1]
            if debug and j > 0:
                pattern_vis = " " * max(0, i-j) + b
                # print(f"  Новое положение b: {pattern_vis}")
        
        if c == b[j]:
            if debug:
                print(f"  Совпадение: '{c}' == '{b[j]}'")
            j += 1
            if debug:
                print(f"  Увеличиваем счетчик совпадений: l = {j}")
        
        if j == m:
            result = (i - m + 1) % n
            if debug:
                print("\n" + "="*50)
                print(f"НАЙДЕН ЦИКЛИЧЕСКИЙ СДВИГ: k = {result}")
                print(f"a = '{a}'")
                print(f"Циклический сдвиг a на {result} позиций: '{a[result:] + a[:result]}'")
                print(f"b = '{b}'")
                print("="*50)
            return result

    if debug:
        print("\n" + "="*50)
        print("Циклический сдвиг не найден")
        print("="*50)
    return -1

def find_rot(debug=False):
    if debug:
        print("\nПОИСК ЦИКЛИЧЕСКОГО СДВИГА")
        print("Введите две строки. Программа найдет, является ли вторая строка циклическим сдвигом первой.")
        print("Строка 1:", end=" ")
    a = input()
    if debug:
        print("Строка 2:", end=" ")
    b = input()
    
    result = cyclic(a, b, debug)

def find_substr(debug=False):
    if debug:
        print("\nПОИСК ПОДСТРОКИ В ТЕКСТЕ (АЛГОРИТМ КМП)")
        print("Введите шаблон для поиска и текст, в котором нужно искать.")
        print("Шаблон:", end=" ")

    pattern = input()

    if debug:
        print("Текст:", end=" ")

    text = input()
    
    matches = kmp_optimized(pattern, text, debug)

if __name__ == '__main__':
    debug_mode = True
    find_substr(debug=debug_mode)
    # find_rot(debug=debug_mode)

