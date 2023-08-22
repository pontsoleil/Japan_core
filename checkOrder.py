def is_valid_sublist(original, sublist):
    """
    Check if the sublist is a valid partial selection from the original list 
    while maintaining the order.
    """
    # 現在の位置を追跡するための変数
    current_index = 0
    # 部分リストの各要素に対して
    for item in sublist:
        # 要素が元のリストに存在する場合、その位置を取得
        try:
            index = original.index(item, current_index)
            current_index = index + 1
        except ValueError:
            # 要素が元のリストに存在しない場合、部分リストは無効
            return False
    # すべての要素が正しい順序で存在する場合、部分リストは有効
    return True

# 例
original = ['a','b','c','d','e']
print(is_valid_sublist(original, ['b','c','e']))  # True
print(is_valid_sublist(original, ['a','e']))      # True
print(is_valid_sublist(original, ['b','a','e']))  # False
print(is_valid_sublist(original, ['a','b','e','d'])) # False
print(is_valid_sublist(original, ['f','d','e']))  # False





