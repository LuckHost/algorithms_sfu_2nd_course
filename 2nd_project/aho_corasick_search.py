class AhoCorasickNode:
    def __init__(self):
        self.children = {}
        self.fail = None
        self.output = []

class AhoCorasick:
    def __init__(self, patterns: list[str]):
        self.root = AhoCorasickNode()
        self.build_trie(patterns)
        self.build_failure_links()

    def build_trie(self, patterns: list[str]):
        for pattern in patterns:
            node = self.root
            for char in pattern:
                if char not in node.children:
                    node.children[char] = AhoCorasickNode()
                node = node.children[char]
            node.output.append(pattern)

    def build_failure_links(self):
        from collections import deque
        queue = deque()

        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)

        while queue:
            current_node = queue.popleft()
            for char, child in current_node.children.items():
                fail_state = current_node.fail
                while fail_state is not None and char not in fail_state.children:
                    fail_state = fail_state.fail
                child.fail = fail_state.children[char] if fail_state else self.root
                child.output += child.fail.output
                queue.append(child)

    def search(self, text: str) -> dict[str, tuple[int, ...]]:
        node = self.root
        indices = {pattern: [] for pattern in node.output}

        for i, char in enumerate(text):
            while node is not None and char not in node.children:
                node = node.fail
            if node is None:
                node = self.root
                continue
            node = node.children[char]
            for pattern in node.output:
                indices[pattern].append(i - len(pattern) + 1)

        return {k: tuple(v) for k, v in indices.items() if v}

def aho_corasick_search(text: str, patterns: list[str]) -> dict[str, tuple[int, ...]]:
    ac = AhoCorasick(patterns)
    return ac.search(text)
