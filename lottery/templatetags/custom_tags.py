from django import template

register = template.Library()


@register.simple_tag
def loop_counter(counter, num):
    # count_num = counter / num
    # print(count_num)
    if counter % num == 0:
        return '<br><br>'
    else:
        return ''

