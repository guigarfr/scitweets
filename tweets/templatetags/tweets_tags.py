from django import template

register = template.Library()


@register.filter(safe=True)
def to_answer_by_user(question, user):
    return question.to_answer_by_user(user.profile)

@register.filter(safe=True)
def answered_by_user(question, user):
    return question.answered_by_user(user.profile)
