from django import template
from ..models import Project, Position


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
def select_distinct_positions_from_project_position_set(context):
    positions = context['project'].position_set.all()
    return set([position for position in positions])

@register.simple_tag(takes_context=True)
def select_distinct_positions_from_projects(context):
    """Returns set of titles from more multiple passed in projects

    Arguments:
        context {Projects} -- Queryset of Projects

    Returns:
    (set) -- distinct titles
    """
    if context.get('query') is not None:
        positions = Position.objects.filter(
            project__in=context['object_list']
        )
        return set([position.title for position in positions])
    else:    
        positions = Position.objects.filter(
            project__status='A'
        ).values('title')
        return set([obj['title'] for obj in positions])


@register.simple_tag(takes_context=True)
def already_applied(context, position):
    for application in position.applications.all():
        if application.user == context['user']:
            return application.status
    return False
