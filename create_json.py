def is_button_inside_window(window, button):
    # Проверка, находится ли центр кнопки внутри окна
    window_x1, window_y1, window_x2, window_y2 = window
    button_x1, button_y1, button_x2, button_y2 = button

    button_center_x = (button_x1 + button_x2) / 2
    button_center_y = (button_y1 + button_y2) / 2

    return (window_x1 <= button_center_x <= window_x2) and (window_y1 <= button_center_y <= window_y2)


def create_json(xy_list, cls_list):
    output_json = {"notification_windows": []}

    result_dict = {}
    for cls, xy in zip(cls_list, xy_list):
        if cls not in result_dict:
            result_dict[cls] = []
        result_dict[cls].append(xy)
    sorted_result_dict = dict(sorted(result_dict.items()))

    count_window = 0
    buttons = []

    if 2.0 in sorted_result_dict.keys():
        for i in sorted_result_dict[2.0]:
            buttons.append({'name': 'Button',
                            'coordinate':
                                {'top_left': {'x': i[0],
                                              'y': i[1]},
                                 'bottom_right': {'x': i[2],
                                                  'y': i[3]}}
                            })

    if 0.0 in sorted_result_dict.keys():
        for i in sorted_result_dict[0.0]:
            type_el = 'site'

            output_json['notification_windows'].append(
                {'order': count_window, 'type': type_el, 'coordinate': {'top_left': {'x': i[0], 'y': i[1]},
                                                                        'bottom_right': {'x': i[2], 'y': i[3]}},
                 'buttons': []})

            for j in buttons:
                b_list = [j['coordinate']['top_left']['x'], j['coordinate']['top_left']['y'],
                          j['coordinate']['bottom_right']['x'], j['coordinate']['bottom_right']['y']]
                if is_button_inside_window(i, b_list):
                    output_json['notification_windows'][count_window]['buttons'].append(j)
            count_window += 1

    if 1.0 in sorted_result_dict.keys():
        for i in sorted_result_dict[1.0]:
            type_el = 'site'

            output_json['notification_windows'].append(
                {'order': count_window, 'type': type_el, 'coordinate': {'top_left': {'x': i[0], 'y': i[1]},
                                                                        'bottom_right': {'x': i[2], 'y': i[3]}},
                 'buttons': []})

            for j in buttons:
                b_list = [j['coordinate']['top_left']['x'], j['coordinate']['top_left']['y'],
                          j['coordinate']['bottom_right']['x'], j['coordinate']['bottom_right']['y']]
                if is_button_inside_window(i, b_list):
                    output_json['notification_windows'][count_window]['buttons'].append(j)
            count_window += 1
    return output_json
