from django import template


register = template.Library()

@register.simple_tag(takes_context=True)
def select_distinct_projects(context):
    applications = context['object_list']
    projects = set()
    for application in applications:
        title = application.position.project.title
        projects.add(title)
    return list(projects)

@register.simple_tag(takes_context=True)
def select_distinct_positions(context):
    applications = context['object_list']
    positions = set()
    for application in applications:
        title = application.position.title
        positions.add(title)
    return list(positions)

@register.simple_tag(takes_context=True)
def select_distinct_positions_from_projects(context):
    projects = context['object_list']
    positions = set()
    for project in projects:
        for position in project.position_set.all():
            title = position.title
            positions.add(title)
    return list(positions)
