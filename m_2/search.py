def search(list: list, number: int) -> bool:
    left, right = 0, len(list) - 1
    while left <= right:
        middle = (left + right) // 2
        middle_value = list[middle]
        if middle_value == number:
            return True
        elif middle_value < number:
            left = middle + 1
        else:
            right = middle - 1
    return False

ex_list = [1, 2, 3, 45, 356, 569, 600, 705, 923]
print(search(ex_list, 923))
print(search(ex_list, 1))
print(search(ex_list, 356))
print(search(ex_list, 100))
print(search(ex_list, 600))
print(search(ex_list, 3))