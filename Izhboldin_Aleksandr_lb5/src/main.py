from collections import deque

class Node:
    def __init__(self):
        self.transitions = {}       # Переходы по символам к другим узлам
        self.pattern_ids = []       # Список ID шаблонов, заканчивающихся в этом узле
        self.suffix_link = None     # Суффиксная ссылка
        self.terminal_link = None   # Терминальная ссылка (сжатая суффиксная ссылка)

class AhoCorasick:
    def __init__(self):
        self.root = Node()
        self.patterns_lengths = {}
    
    def add_pattern(self, pattern, pattern_id):
        current_node = self.root
        
        for char in pattern:
            if char not in current_node.transitions:
                current_node.transitions[char] = Node()
            current_node = current_node.transitions[char]
        
        current_node.pattern_ids.append(pattern_id)
        self.patterns_lengths[pattern_id] = len(pattern)
    
    def build_automat(self):
        queue = deque()
        
        self.root.suffix_link = self.root
        self.root.terminal_link = None
        
        for char, child in self.root.transitions.items():
            child.suffix_link = self.root
            queue.append(child)
        
        # BFS
        while queue:
            current = queue.popleft()
            
            for char, child in current.transitions.items():
                suffix_link = current.suffix_link
                
                while suffix_link != self.root and char not in suffix_link.transitions:
                    suffix_link = suffix_link.suffix_link
                
                if char in suffix_link.transitions:
                    child.suffix_link = suffix_link.transitions[char]
                else:
                    child.suffix_link = self.root
                
                if child.suffix_link.pattern_ids:
                    child.terminal_link = child.suffix_link
                else:
                    child.terminal_link = child.suffix_link.terminal_link
                
                queue.append(child)
    
    def get_next_state(self, state, char):
        while state != self.root and char not in state.transitions:
            state = state.suffix_link
        
        if char in state.transitions:
            return state.transitions[char]
        else:
            return self.root
    
    def search(self, text):
        result = []
        current = self.root
        
        for i, char in enumerate(text):
            current = self.get_next_state(current, char)
            
            if current.pattern_ids:
                for pattern_id in current.pattern_ids:
                    pattern_len = self.patterns_lengths[pattern_id]
                    position = i - pattern_len + 1 + 1
                    result.append((position, pattern_id))
            
            node = current.terminal_link
            while node:
                for pattern_id in node.pattern_ids:
                    pattern_len = self.patterns_lengths[pattern_id]
                    position = i - pattern_len + 1 + 1
                    result.append((position, pattern_id))
                node = node.terminal_link
        
        return sorted(result)
    
    def print_trie(self):
        print("=== СТРУКТУРА БОРА ===")
        self._print_node(self.root, "", "ROOT")
        
        print("\n=== ДЕТАЛЬНАЯ ИНФОРМАЦИЯ О УЗЛАХ ===")
        self._print_node_details(self.root, "ROOT")
    
    def _print_node(self, node, prefix, char_from_parent):
        pattern_info = f" [Шаблоны: {node.pattern_ids}]" if node.pattern_ids else ""
        print(f"{prefix}{char_from_parent}{pattern_info}")
        
        sorted_chars = sorted(node.transitions.keys())
        
        for i, char in enumerate(sorted_chars):
            child = node.transitions[char]
            if i == len(sorted_chars) - 1:
                new_prefix = prefix + "    "
                branch = "└── "
            else:
                new_prefix = prefix + "│   "
                branch = "├── "
            
            self._print_node(child, new_prefix, f"{branch}{char}")
    
    def _print_node_details(self, node, path, depth=0):
        print(f"\nУзел: {path}")
        print(f"\tГлубина: {depth}")
        print(f"\tШаблоны: {node.pattern_ids}")
        
        suffix_path = self._get_node_path(node.suffix_link) if node.suffix_link else "None"
        terminal_path = self._get_node_path(node.terminal_link) if node.terminal_link else "None"
        
        print(f"\tСуффиксная ссылка: {suffix_path}")
        print(f"\tТерминальная ссылка (сжатая суффиксная): {terminal_path}")
        
        if node.transitions:
            print("\tПереходы:")
            for char, child in sorted(node.transitions.items()):
                child_path = f"{path} -> {char}"
                print(f"\t\t{child_path}")
            
            for char, child in sorted(node.transitions.items()):
                child_path = f"{path} -> {char}"
                self._print_node_details(child, child_path, depth + 1)
    
    def _get_node_path(self, node):
        if node == self.root:
            return "ROOT"
        
        def find_path(current, target, path=[]):
            if current == target:
                return path
            
            for char, child in current.transitions.items():
                result = find_path(child, target, path + [char])
                if result:
                    return result
            
            return None
        
        path = find_path(self.root, node)
        if path:
            return "ROOT -> " + " -> ".join(path)
        else:
            return f"Node({id(node)})"
    
    def get_longest_suffix_chain(self):
        return self._traverse_and_check_suffix_chains(self.root)
    
    def _traverse_and_check_suffix_chains(self, node):
        max_chain_length = 0
        
        for char, child in node.transitions.items():
            current_chain_length = self._get_suffix_chain_length(child)
            max_chain_length = max(max_chain_length, current_chain_length)
            
            child_max_length = self._traverse_and_check_suffix_chains(child)
            max_chain_length = max(max_chain_length, child_max_length)
        
        return max_chain_length
    
    def _get_suffix_chain_length(self, start_node):
        if start_node is None:
            return 0
        
        visited_nodes = set()
        current = start_node
        chain_length = 0
        
        while current and current != self.root and current not in visited_nodes:
            visited_nodes.add(current)
            chain_length += 1
            current = current.suffix_link
        
        return chain_length
    
    def get_longest_terminal_chain(self):
        return self._traverse_and_check_terminal_chains(self.root)
    
    def _traverse_and_check_terminal_chains(self, node):
        max_chain_length = 0
        
        for char, child in node.transitions.items():
            current_chain_length = self._get_terminal_chain_length(child)
            max_chain_length = max(max_chain_length, current_chain_length)
            
            child_max_length = self._traverse_and_check_terminal_chains(child)
            max_chain_length = max(max_chain_length, child_max_length)
        
        return max_chain_length
    
    def _get_terminal_chain_length(self, start_node):
        if start_node is None or start_node.terminal_link is None:
            return 0
        
        visited_nodes = set()
        current = start_node.terminal_link
        chain_length = 1
        
        while current and current not in visited_nodes:
            visited_nodes.add(current)
            chain_length += 1
            current = current.terminal_link
            if current is None:
                break
        
        return chain_length

def search_with_wildcard(text, pattern, wildcard, debug=False):
    subpatterns = pattern.split(wildcard)
    
    valid_subpatterns = []
    subpattern_positions = []
    
    pos = 0
    for subpattern in subpatterns:
        if subpattern:
            valid_subpatterns.append(subpattern)
            subpattern_positions.append(pos)
        pos += len(subpattern) + 1
    
    aho = AhoCorasick()
    for i, subpattern in enumerate(valid_subpatterns, 1):
        aho.add_pattern(subpattern, i)
    
    aho.build_automat()

    if debug:
        aho.print_trie()

    # if debug:
    #     suffix_chain_length = aho.get_longest_suffix_chain()
    #     terminal_chain_length = aho.get_longest_terminal_chain()
    #     print(f"Длина самой длинной цепочки суффиксных ссылок: {suffix_chain_length}")
    #     print(f"Длина самой длинной цепочки терминальных ссылок: {terminal_chain_length}")
    
    subpattern_matches = aho.search(text)
    if debug:
        print("Позиции подстрок в тексте:", subpattern_matches)
    
    C = [0] * (len(text) + 1)
    
    for position, pattern_id in subpattern_matches:
        start_pos = position - subpattern_positions[pattern_id-1]
        
        if start_pos > 0:
            C[start_pos] += 1
    
    if debug:
        print("Массив C:", C)
    
    pattern_positions = []
    k = len(valid_subpatterns)
    
    for i in range(1, len(text) - len(pattern) + 2):
        if C[i] == k:
            match = True

            for j in range(len(pattern)):
                if i + j - 1 >= len(text):
                    match = False
                    break

                if pattern[j] != wildcard and pattern[j] != text[i+j-1]:
                    match = False
                    break
            
            if match:
                pattern_positions.append(i)
    
    return pattern_positions

def aho_default_test():
    text = "abcabeabcabd"
    patterns = ["ab", "abc", "aba", "bca", "c", "d"]
    
    print(f"Текст: {text}")
    print("Шаблоны:")
    for i, pattern in enumerate(patterns, 1):
        print(f"{i}. {pattern}")
    
    aho = AhoCorasick()
    for i, pattern in enumerate(patterns, 1):
        aho.add_pattern(pattern, i)
    
    print("\nСтруктура бора до построения автомата:")
    aho.print_trie()
    
    aho.build_automat()
    
    print("\nСтруктура бора после построения автомата:")
    aho.print_trie()
    
    suffix_chain_length = aho.get_longest_suffix_chain()
    terminal_chain_length = aho.get_longest_terminal_chain()
    
    print(f"\nДлина самой длинной цепочки суффиксных ссылок: {suffix_chain_length}")
    print(f"Длина самой длинной цепочки терминальных ссылок: {terminal_chain_length}")
    
    print("\nРезультаты поиска:")
    matches = aho.search(text)
    for position, pattern_id in matches:
        print(f"Шаблон {pattern_id} найден на позиции {position}")

def aho_wildcard_test():
    text = "ACTANCA"
    pattern = "A$$A$"
    wildcard = "$"
    
    print(f"Текст: {text}")
    print(f"Шаблон: {pattern}")
    print(f"Джокер: {wildcard}")
    
    positions = search_with_wildcard(text, pattern, wildcard, debug=True)
    print("\nРезультаты поиска:")
    for pos in positions:
        print(pos)

def aho_default(debug=False):
    text = input().strip()
    n = int(input().strip())
    patterns = []
    
    for _ in range(n):
        pattern = input().strip()
        patterns.append(pattern)
    
    aho = AhoCorasick()
    
    for i, pattern in enumerate(patterns, 1):
        aho.add_pattern(pattern, i)
    
    if debug:
        print("\nСтруктура бора до построения автомата:")
        aho.print_trie()

    aho.build_automat()

    if debug:
        print("\nСтруктура бора после построения автомата:")
        aho.print_trie()
    
    suffix_chain_length = aho.get_longest_suffix_chain()
    terminal_chain_length = aho.get_longest_terminal_chain()
    
    if debug:
        print(f"Длина самой длинной цепочки суффиксных ссылок: {suffix_chain_length}")
        print(f"Длина самой длинной цепочки терминальных ссылок: {terminal_chain_length}")
    
    matches = aho.search(text)

    for position, pattern_id in matches:
        print(position, pattern_id)
        if debug:
            print(f"Шаблон {pattern_id} найден на позиции {position}")

def aho_wildcard(debug=False):
    text = input().strip()
    pattern = input().strip()
    wildcard = input().strip()

    positions = search_with_wildcard(text, pattern, wildcard, debug)

    for pos in positions:
        print(pos)

if __name__ == "__main__":
    debug = False
    # aho_wildcard_test()
    # aho_default_test()

    # aho_wildcard(debug)
    aho_default(debug)
