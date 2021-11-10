from .models import IngredientAmount


def get_shopping_data(user):
    shopping_data = {}
    ingredients = IngredientAmount.objects.filter(
        recipe__shopping_cart__user=user
    ).values_list('name__name', 'name__measurement_unit', 'amount')
    for ingredient in ingredients:
        name, measure, amount = ingredient[0], ingredient[1], ingredient[2]
        if name not in shopping_data:
            shopping_data[name] = {
                'measurement_unit': measure,
                'amount': amount
            }
        else:
            shopping_data[name]['amount'] += amount
    return shopping_data


def make_shopping_list(shopping_data):
    shopping_list = []
    for key in shopping_data.keys():
        measurement_unit = shopping_data[key]['measurement_unit']
        amount = shopping_data[key]['amount']
        line = str(key) + ' (' + measurement_unit + ') - ' + str(amount) + '\n'
        shopping_list.append(line)
    return shopping_list


def get_shopping_list(user):
    shopping_data = get_shopping_data(user)
    shopping_list = make_shopping_list(shopping_data)
    return shopping_list
