from genflow.template.field.base import TemplateField
from genflow.template.frontend_node.base import FrontendNode
from genflow.template.template.base import Template
from genflow.interface.custom.constants import DEFAULT_CUSTOM_COMPONENT_CODE


class CustomComponentFrontendNode(FrontendNode):
    name: str = "CustomComponent"
    display_name: str = "Custom Component"
    beta: bool = True
    template: Template = Template(
        type_name="CustomComponent",
        fields=[
            TemplateField(
                field_type="code",
                required=True,
                placeholder="",
                is_list=False,
                show=True,
                value=DEFAULT_CUSTOM_COMPONENT_CODE,
                name="code",
                advanced=False,
                dynamic=True,
            )
        ],
    )
    description: str = "Create any custom component you want!"
    base_classes: list[str] = []

    def to_dict(self):
        return super().to_dict()
