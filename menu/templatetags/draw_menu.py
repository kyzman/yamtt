from django import template
from django.forms import model_to_dict
from django.utils.datastructures import MultiValueDictKeyError

from menu.models import Menu

register = template.Library()


@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu):
    all_items = get_all_items_by_menu(menu)
    super_parents = [item for item in all_items if item['parent'] == all_items[0]['id']]
    try:
        selected_item = get_selected_id_item(all_items, context['request'].GET[menu])
        expanded_items_id_list = get_expanded_items_id_list(selected_item, all_items)
        for parent in super_parents:
            if parent['id'] in expanded_items_id_list:
                parent['child_items'] = get_child_items(
                    all_items, parent['id'], expanded_items_id_list
                )
        result_dict = {'items': super_parents}
    except MultiValueDictKeyError:
        result_dict = {'items': super_parents}

    result_dict['menu'] = menu
    return result_dict


def get_selected_id_item(all_items, selected_id):
    return [item for item in all_items if item['id'] == int(selected_id)][0]


def get_all_items_by_menu(menu):

    all_items = Menu.objects.raw(f'''WITH RECURSIVE rectree AS (
          SELECT * 
            FROM {Menu._meta.db_table} 
           WHERE title = '{menu}' 
        UNION ALL 
          SELECT t.* 
            FROM {Menu._meta.db_table} t 
            JOIN rectree
              ON t.parent_id = rectree.id
        ) SELECT * FROM rectree;
    ''')
    return [model_to_dict(item) for item in all_items]


def get_expanded_items_id_list(selected_item, all_items):
    """
    Формирует список всех развернутых пунктов меню.
    """
    expanded_items_id_list = []
    item = selected_item
    while item['parent']:
        expanded_items_id_list.append(item['id'])
        item = get_selected_id_item(all_items, item['parent'])
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
