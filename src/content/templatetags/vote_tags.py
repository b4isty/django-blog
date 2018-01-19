from django import template

register = template.Library()


@register.filter()
def has_upvoted(user, obj):
    return user.id in obj.vote_set.all().values_list("user", flat=True)
