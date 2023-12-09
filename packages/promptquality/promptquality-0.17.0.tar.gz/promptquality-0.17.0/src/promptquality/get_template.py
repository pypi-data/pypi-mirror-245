from pydantic import UUID4

from promptquality.helpers import get_project, get_templates
from promptquality.types.run import BaseTemplateResponse


def get_template(project_id: UUID4, template_name: str) -> BaseTemplateResponse:
    """
    Get a template for a specific project.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    template_name : str
        Name of the template to get.

    Returns
    -------
    BaseTemplateResponse
        Template response.
    """
    project = get_project(project_id)
    templates = get_templates(project.id)
    requested_template = None
    for template in templates:
        if template.name == template_name:
            requested_template = template
    if not requested_template:
        raise Exception(f"Template {template_name} not found.")
    return requested_template
