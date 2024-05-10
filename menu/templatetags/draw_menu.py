import pprint

from django import template
from django.forms import model_to_dict
from django.urls import reverse, NoReverseMatch

from menu.models import Menu

register = template.Library()


@register.inclusion_tag('menu/draw_menu.html', takes_context=False)
def draw_menu_all_expanded(menu):
    all_items = get_all_items_by_menu(menu)
    expanded_items_id_list = []
    result_dict = {'menu': menu}
    super_parents = [item for item in all_items if item['parent'] == all_items[0]['id']]
    for item in all_items:
        expanded_items_id_list.append(item['id'])
    for parent in super_parents:
        if parent['id'] in expanded_items_id_list:
            parent['child_items'] = get_child_items(
                all_items, parent['id'], expanded_items_id_list
            )
    result_dict.update({'items': super_parents})
    return result_dict


@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu):
    all_items = get_all_items_by_menu(menu)
    expanded_items_id_list = []
    result_dict = {'menu': menu}
    super_parents = [item for item in all_items if item['parent'] == all_items[0]['id']]
    try:
        if selected_item := get_selected_item_by_id(all_items, context['request'].GET[menu]):
            result_dict['selected'] = selected_item['id']
            expanded_items_id_list = get_expanded_items_id_list(selected_item, all_items)
        for parent in super_parents:
            if parent['id'] in expanded_items_id_list:
                parent['child_items'] = get_child_items(
                    all_items, parent['id'], expanded_items_id_list
                )
    except:
        pass
    finally:
        result_dict.update({'items': super_parents})
    return result_dict


def get_selected_item_by_id(all_items, selected_id):
    """Поиск и выдача элемента в списке по ID"""
    try:
        return [item for item in all_items if item['id'] == int(selected_id)][0]
    except:
        return None


def get_all_items_by_menu(menu):
    """Формирование списка из элементов меню с заменой named url на абсолютные"""
    all_items = Menu.objects.raw(f'''WITH RECURSIVE rectree AS (
          SELECT * 
            FROM {Menu._meta.db_table} 
           WHERE title = %s AND parent_id IS NULL
        UNION ALL 
          SELECT t.* 
            FROM {Menu._meta.db_table} t 
            JOIN rectree
              ON t.parent_id = rectree.id
        ) SELECT * FROM rectree;
    ''', [menu])
    result = []
    count = 0
    for item in all_items:
        result.append(model_to_dict(item))
        fragmented = str.partition(item.url, '#')
        parted = str.partition(fragmented[0], '?')
        try:
            absolute_url = f"{reverse(parted[0])}{parted[1]}{parted[2]}"
        except NoReverseMatch:  # если не получилось получить абсолютный url по полю, значит считаем что указан прямой.
            absolute_url = fragmented[0]
        result[count]['url'] = f"{absolute_url}&{menu}={item.id}" if '?' in absolute_url else f"{absolute_url}?{menu}={item.id}"
        result[count]['url'] += f"{fragmented[1]}{fragmented[2]}"
        count += 1
    return result


def get_expanded_items_id_list(selected_item, all_items):
    """
    Формирует список всех развернутых пунктов меню выбранного элемента.
    """
    expanded_items_id_list = []
    item = selected_item
    while item['parent']:
        expanded_items_id_list.append(item['id'])
        item = get_selected_item_by_id(all_items, item['parent'])
    return expanded_items_id_list


def get_child_items(item_values, current_parent_id, expanded_items_id_list):
    """
    Для переданного в аргументе текущего родителя рекурсивно
    формирует список дочерних элементов.
    """
    current_parent_child_list = [
        item for item in item_values if item['parent'] == int(current_parent_id)
    ]
    for child in current_parent_child_list:
        if child['id'] in expanded_items_id_list:
            child['child_items'] = get_child_items(
                item_values, child['id'], expanded_items_id_list
            )
    return current_parent_child_list
