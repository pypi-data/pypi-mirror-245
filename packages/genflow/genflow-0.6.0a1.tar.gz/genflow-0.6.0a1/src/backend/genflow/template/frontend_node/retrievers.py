from typing import Optional

from genflow.template.field.base import TemplateField
from genflow.template.frontend_node.base import FrontendNode


class RetrieverFrontendNode(FrontendNode):
    @staticmethod
    def format_field(field: TemplateField, name: Optional[str] = None) -> None:
        FrontendNode.format_field(field, name)
        # Define common field attributes
        field.show = True
        if field.name == "parser_key":
            field.display_name = "Parser Key"
            field.password = False
