def data_binary_search(date, date_cost_list) -> int:
    # на входе - дата операции |
    # лист, содержащий цены данного товара в определенный период, элементы в нем расставлены по УБЫВНИЮ даты
    # пример [[2025:05:01, 230], [2025:04:01, 220], [2025:03:01, 200]]
    # [Дата изменения, Цена ДО ИЗМЕНЕНИЯ]

    # самая первая дата и стоимость в листе - ТЕКУЩАЯ, поэтому не нужно беспокоится о продажах, совершенных после нее,
    # т.е. о выходе за границу массива

    left_border = 0
    right_border = len(date_cost_list) - 1

    result_element_index = 0
    # переменная для постоянного запоминания индекса проверяемого элемента
    while left_border <= right_border:
        middle_element_index = (left_border + right_border) // 2
        middle_element = date_cost_list[middle_element_index]
        middle_date, _ = middle_element

        if middle_date > date:
            left_border = middle_element_index + 1
        # Если дата проверяемого элемента > значит он точно находится максимум в диапазоне его цены,
        # двигаем нижнюю границу
        else:
            right_border = middle_element_index - 1
        # Если дата проверяемого элемента <= значит он точно не находится в диапазоне его цены
        # двигаем верхнюю границу

        result_element_index = middle_element_index

    # часто поиск выдает пограничную для даты ситуацию:
    # Цена изменена 2025:03:01 Покупка осуществлена 2025:03:01
    # В таком случае необходимо брать цену, указанную следующем изменении

    result_element_date, _ = date_cost_list[result_element_index]
    if result_element_date <= date:
        _, cost = date_cost_list[result_element_index - 1]
    # Не забываем, что даты, больше первого элемента быть не может
    else:
        _, cost = date_cost_list[result_element_index]

    return cost

