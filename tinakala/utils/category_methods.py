from django.shortcuts import get_object_or_404


def get_most_category(objects, model):
    categories_id = [item[0] for item in list(objects.values_list('category'))]
    most_repeated_category = get_object_or_404(model, pk=max(set(categories_id), key=categories_id.count))
    return most_repeated_category


def side_bar_categories_menu(category, model):
    if category.depth == 1:
        parent = []
        child = [model.objects.filter(category=category).first()]
        if child[0] is None:
            child = [{'category': {'title': category.title, 'en_title': category.en_title, }}]
    elif category.depth == 2:
        parent = [model.objects.filter(sub_category=category).first()]
        child = [model.objects.filter(category=category).first()]
        if child[0] is None:
            child = [{'category': {'title': category.title, 'en_title': category.en_title, }}]
    else:
        parent_a: model = model.objects.filter(sub_category=category).first()
        parent_b: model = model.objects.filter(sub_category=parent_a.category).first()
        parent = [{'category': {'title': parent_b.category.title, 'en_title': parent_b.category.en_title, }}, ]
        child = [{'category': {
            'title': parent_a.category.title,
            'en_title': parent_a.category.en_title,
            'single_category': {'title': category.title, 'en_title': category.en_title, },
        }}]
    return parent, child
