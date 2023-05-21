from django import template

register = template.Library()


def range(start, end):
    return range(start, end)

register.filter('range', range)