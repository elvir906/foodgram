from rest_framework.serializers import (
    ModelSerializer,
    ReadOnlyField,
    SerializerMethodField,
    ValidationError
)
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404

from drf_extra_fields.fields import Base64ImageField

from recipes.models import (
    Ingredients,
    Recipes,
    Tags,
    IngredientsQuantity
)
from users.models import Follow
from users.serializers import UsresCustomSerializer


class IngredientsSerializer(ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'


class TagsSerializer(ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class IngredientsQuantitySerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredients.id')
    name = ReadOnlyField(source='ingredients.name')
    unit = ReadOnlyField(source='ingredients.unit')

    class Meta:
        model = IngredientsQuantity
        fields = ('id', 'name', 'unit', 'quantity')
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientsQuantity.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipesSerializer(ModelSerializer):
    author = UsresCustomSerializer(read_only=True)
    ingredients = IngredientsQuantitySerializer(
        source='ingredientamount_set',
        many=True,
        read_only=True,
    )
    tags = TagsSerializer(read_only=True, many=True)
    image = Base64ImageField()
    is_favorite = SerializerMethodField()
    is_in_cart = SerializerMethodField()

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'author', 'text', 'ingredients',
                  'image', 'tags', 'cooking_time', 'is_favorite'
                  'is_in_cart')

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipes.objects.filter(favorite__user=user, id=obj.id).exist()

    def get_is_in_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipes.objects.filter(cart__user=user, id=obj.id).exist()

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientsQuantity.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('quantity'),
            )

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientsQuantity.objects.filter(recipe=instance).all().delete()
        self.create_ingredients(validated_data.get('ingredients'), instance)
        instance.save()
        return instance

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise ValidationError(
                {'Ingredients':
                 'Для рецепта нужен как минимум один ингредиент'}
            )
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredients,
                                           id=ingredient_item['id'])
            if ingredient in ingredient_list:
                raise ValidationError('Ингридиенты не должны повторяться')
            ingredient_list.append(ingredient)
            if int(ingredient_item['quantity']) < 0:
                raise ValidationError({
                    'ingredients': ('Количество ингридиента д.б. больше 1')
                })
        data['ingredients'] = ingredients
        return data


class CropRecipeSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(ModelSerializer):
    id = ReadOnlyField(source='author.id')
    email = ReadOnlyField(source='author.email')
    username = ReadOnlyField(source='author.username')
    first_name = ReadOnlyField(source='author.first_name')
    last_name = ReadOnlyField(source='author.last_name')
    is_subscriber = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscriber', 'recipes', 'recipes_count')

    def get_is_subscriber(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipes.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return CropRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipes.objects.filter(author=obj.author).count()
