from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from recipes.forms import RecipeForm
from recipes.models import Recipe, RecipeIngredient
from recipes.views.helpers import (check_slug, get_ingredients_from_request,
                                   get_tags_from_request, save_ingredients)


@check_slug('recipe_edit')
@login_required
def recipe_edit(request, recipe_id, slug):
    '''
    Render the page with recipe edit form and
    save edited/newly added ingredients separately.
    '''
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe_view', recipe_id=recipe_id, slug=recipe.slug)
    form = RecipeForm(
        request.POST or None,
        request.FILES or None,
        instance=recipe,
    )
    if form.is_valid():
        recipe = form.save()
        # delete old recipe's ingredients
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        save_ingredients(request, recipe)  # save updated ingredients
        recipe.save()
        return redirect('recipe_view', recipe_id=recipe_id, slug=recipe.slug)
    tags = recipe.tags.all()
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe).all()
    if request.method == 'POST':
        tags = get_tags_from_request(request)
        ingredients = get_ingredients_from_request(request)
    return render(
        request,
        'recipes/formChangeRecipe.html',
        {'form': form, 'tags': tags, 'recipe': recipe,
         'recipe_ingredients': recipe_ingredients},
    )
