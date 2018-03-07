def safe_get(lst, idx):
    try:
        return lst[idx]
    except IndexError:
        return None


def subtract_from_tuple_value(tup, value_idx, subtract):
    tup = list(tup)
    tup[value_idx] -= subtract
    return tuple(tup)


def subtract_one_of_each(lst_of_tuples, ignore_index, grater_than):
    for j in range(len(lst_of_tuples)):
        if j != ignore_index:
            print(lst_of_tuples[j])
            _, _hand_index = lst_of_tuples[j]
            print(_hand_index, grater_than)
            if _hand_index > grater_than:
                lst_of_tuples[j] = subtract_from_tuple_value(lst_of_tuples[j], 1, 1)
