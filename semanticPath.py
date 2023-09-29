import re

def semPath(data, query):
    results = []

    def lookup(node, query_elements, path=""):
        nonlocal results
        if not query_elements:
            results.append(node)
            return

        first, *rest = query_elements
        if "[" in first and "]" in first:
            if '[*]'==first:
                if isinstance(node, list):
                    for item in node:
                        lookup(item, rest, path + '/' + first)
            else:
                key, condition = re.split(r'\[|\]', first)[:2]
                match = re.search(r"([\w/_]+)='(\w+)'", condition)
                if match:
                    condition_key_path = match.group(1)
                    condition_value = match.group(2)

                    if isinstance(node, dict):
                        if key:
                            target = node.get(key, {})
                        else:
                            target = node

                        for ck in condition_key_path.split('/'):
                            if isinstance(target, dict):
                                target = target.get(ck, {})

                        if target == condition_value:
                            if not key:
                                key = condition_key_path
                                lookup(node, rest, path + '/' + first)
                            else:
                                lookup(node.get(key, {}), rest, path + '/' + first)
                        elif isinstance(target, list):
                            for item in target:
                                lookup(item, query_elements, path)

                    elif isinstance(node, list):
                        for item in node:
                            lookup(item, query_elements, path)

        elif isinstance(node, list):
            for item in node:
                lookup(item, query_elements, path)

        elif isinstance(node, dict) and first in node:
            lookup(node[first], rest, path + '/' + first)

    elements = re.findall(r"(\w*\[[^\]]+\]|\w+)", query.strip("/"))
    lookup(data, elements)
    
    if len(results) == 1:
        return results[0]
    return results

# サンプルデータ
d = {
    'JC00': [
        {
            'JC0a': {'JC0a_15': 'iv01'},
            'JC55_a_JC2d': [
                {'JC55_a_JC2d_01':5000, 'JC55_a_JC2d_04': 'S', 'JC55_a_JC2d_07': 10},
                {'JC55_a_JC2d_01':400, 'JC55_a_JC2d_04': 'AA', 'JC55_a_JC2d_07': 8}
            ],
            'JC6e_JC62': [
                {   'JC6e_JC62_01': '1',
                    'JC6d_JC2d': {'JC6d_JC2d_02': 100, 'JC6d_JC2d_03':'S', 'JC6d_JC2d_04':10},
                    'JC64_JC6b': {'JC64_JC6b_04':1}
                },
                {   'JC6e_JC62_01': '2',
                    'JC6d_JC2d': {'JC6d_JC2d_02': 200, 'JC6d_JC2d_03':'S', 'JC6d_JC2d_04':10}
                }
            ]
        },
        {
            'JC0a': {'JC0a_15': 'iv02'},
            'JC55_a_JC2d': [
                {'JC55_a_JC2d_01':1000, 'JC55_a_JC2d_04': 'S', 'JC55_a_JC2d_07': 10},
                {'JC55_a_JC2d_01':0, 'JC55_a_JC2d_04': 'AA', 'JC55_a_JC2d_07': 8}
            ]
        }
    ]
}

# テスト
# print(semPath(d, "/JC00/JC0a"))
print(semPath(d, "/JC00/[JC0a/JC0a_15='iv01']"))
print(semPath(d, "/JC00/[JC0a/JC0a_15='iv01']/JC6e_jc62/[JC6e_JC62_01='2']"))

print(semPath(d, "/JC00/JC0a[JC0a_15='iv01']/JC55_a_JC2d"))

print(semPath(d, "/JC00/[*]/JC0a_01"))
print(semPath(d, "/JC00/JC0a_01"))
print(semPath(d, "/JC00//JC55_a_JC2d/[JC55_a_JC2d_04='S']/JC55_a_JC2d_01")) # [5000, 1000]

setPath(d, "/JC00/JC0a[JC0a_15='iv01']/JC55_a_JC2d")
