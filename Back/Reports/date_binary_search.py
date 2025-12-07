from datetime import datetime

def data_binary_search(date, date_cost_list) -> int:

    left_border = 0
    right_border = len(date_cost_list) - 1

    result_element_index = 0

    while left_border <= right_border:
        middle_element_index = (left_border + right_border) // 2
        middle_element = date_cost_list[middle_element_index]
        middle_date, _ = middle_element

        result_element_index = middle_element_index
        if middle_date > date:
            right_border = middle_element_index - 1
        elif middle_date < date:
            left_border = middle_element_index + 1
        else:
            break

    if date < date_cost_list[result_element_index][0]:
        result_element_index -= 1

    return date_cost_list[result_element_index][1]

#datelist = [[datetime.strptime(f"01:0{i}:2025", "%d:%m:%Y"), i] for i in range(1, 10)]
#print(data_binary_search(datetime.strptime("02:03:2025", "%d:%m:%Y"), datelist))

