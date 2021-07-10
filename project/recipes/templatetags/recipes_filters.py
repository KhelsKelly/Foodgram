from django import template

register = template.Library()


@register.filter
def trunc_params(url):
    '''
    Returns an absolute URL path without any query params.
    '''
    qmark_idx = url.find('?')
    return url[:qmark_idx] if qmark_idx != -1 else url


@register.filter
def is_favorite(recipe, user):
    '''
    Checks if a given recipe is in user's favorites.
    '''
    return user.favorites.filter(recipe=recipe).exists()


@register.filter
def is_subscribed(user, author):
    '''
    Checks if a given user is subscribed to another user (author).
    '''
    return user.subscriptions.filter(author=author).exists()


@register.filter()
def is_purchased(recipe, cart):
    '''
    Checks if a given recipe is already in user's shopping list
    '''
    return recipe in cart
