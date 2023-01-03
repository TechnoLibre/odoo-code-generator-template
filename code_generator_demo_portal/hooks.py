import logging
import os

from odoo import SUPERUSER_ID, _, api, fields, models

_logger = logging.getLogger(__name__)

MODULE_NAME = "demo_portal"


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # The path of the actual file
        # path_module_generate = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

        short_name = MODULE_NAME.replace("_", " ").title()

        # Add code generator
        categ_id = env["ir.module.category"].search(
            [("name", "=", "Uncategorized")], limit=1
        )
        value = {
            "shortdesc": short_name,
            "name": MODULE_NAME,
            "license": "AGPL-3",
            "category_id": categ_id.id,
            "summary": "",
            "author": "TechnoLibre",
            "website": "https://technolibre.ca",
            "application": True,
            "enable_sync_code": True,
            # "path_sync_code": path_module_generate,
            "icon": os.path.join(
                os.path.dirname(__file__),
                "static",
                "description",
                "code_generator_icon.png",
            ),
        }

        # TODO HUMAN: enable your functionality to generate
        value["enable_sync_template"] = True
        value["ignore_fields"] = ""
        value["post_init_hook_show"] = False
        value["uninstall_hook_show"] = False
        value["post_init_hook_feature_code_generator"] = False
        value["uninstall_hook_feature_code_generator"] = False

        value["hook_constant_code"] = f'MODULE_NAME = "{MODULE_NAME}"'

        code_generator_id = env["code.generator.module"].create(value)

        # Add dependencies
        lst_depend_module = ["mail", "portal", "website"]
        code_generator_id.add_module_dependency(lst_depend_module)

        # Generate snippet
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "template_generate_website_snippet_controller_feature": (
                "model_show_item_individual"
            ),
            "enable_javascript": True,
            "model_name": "demo.model.portal",
            "snippet_type": "structure",
        }
        env["code.generator.snippet"].create(value_snippet)

        # Add/Update Demo Model Portal
        model_model = "demo.model.portal"
        model_name = "demo_model_portal"
        lst_depend_model = [
            "mail.thread",
            "mail.activity.mixin",
            "portal.mixin",
        ]
        dct_model = {
            "description": "demo_model_portal",
            "enable_activity": True,
            "menu_name_keep_application": True,
        }
        dct_field = {
            "demo_binary": {
                "field_description": "Binary demo",
                "ttype": "binary",
            },
            "demo_binary_image": {
                "field_description": "Binary image demo",
                "force_widget": "image",
                "ttype": "binary",
            },
            "demo_boolean": {
                "field_description": "Boolean demo",
                "ttype": "boolean",
            },
            "demo_char": {
                "field_description": "Char demo",
                "track_visibility": "onchange",
                "ttype": "char",
            },
            "demo_date": {
                "field_description": "Date demo",
                "is_date_end_view": True,
                "ttype": "date",
            },
            "demo_date_time": {
                "field_description": "Datetime demo",
                "is_date_start_view": True,
                "ttype": "datetime",
            },
            "demo_external_link": {
                "field_description": "External link demo",
                "force_widget": "link_button",
                "ttype": "char",
            },
            "demo_float": {
                "field_description": "Float demo",
                "ttype": "float",
            },
            "demo_float_time": {
                "field_description": "Float time demo",
                "force_widget": "float_time",
                "ttype": "float",
            },
            "demo_html": {
                "field_description": "HTML demo",
                "ttype": "html",
            },
            "demo_integer": {
                "field_description": "Integer demo",
                "ttype": "integer",
            },
            "demo_many2many": {
                "field_description": "Many2many demo",
                "relation": "demo.model_2.portal",
                "ttype": "many2many",
            },
            "demo_selection": {
                "field_description": "Selection demo",
                "selection": (
                    "[('test1', 'Test 1'), ('test2', 'Test 2'), ('test3',"
                    " 'Test 3')]"
                ),
                "ttype": "selection",
            },
            "demo_text": {
                "field_description": "Text demo",
                "ttype": "text",
            },
            "diagram_id": {
                "field_description": "Diagram",
                "relation": "demo.model_3.portal.diagram",
                "ttype": "many2one",
            },
            "name": {
                "field_description": "Name",
                "ttype": "char",
            },
            "xpos": {
                "default": 50,
                "field_description": "Diagram position x",
                "ttype": "integer",
            },
            "ypos": {
                "default": 50,
                "field_description": "Diagram position y",
                "ttype": "integer",
            },
        }
        model_demo_model_portal = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code model
            lst_value = [
                {
                    "code": """# This is a comment need it for test, thanks
super(DemoModelPortal, self)._compute_access_url()
for demo_model_portal in self:
    demo_model_portal.access_url = (
        "/my/demo_model_portal/%s" % demo_model_portal.id
    )""",
                    "name": "_compute_access_url",
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_demo_model_portal.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Demo Model 2 Portal
        model_model = "demo.model_2.portal"
        model_name = "demo_model_2_portal"
        lst_depend_model = [
            "mail.thread",
            "mail.activity.mixin",
            "portal.mixin",
        ]
        dct_model = {
            "description": "demo_model_2_portal",
            "enable_activity": True,
            "menu_name_keep_application": True,
        }
        dct_field = {
            "demo_many2one_dst": {
                "field_description": "Many2one dst",
                "relation": "demo.model.portal",
                "ttype": "many2one",
            },
            "demo_many2one_src": {
                "field_description": "Many2one src",
                "relation": "demo.model.portal",
                "ttype": "many2one",
            },
            "diagram_id": {
                "field_description": "Diagram",
                "relation": "demo.model_3.portal.diagram",
                "ttype": "many2one",
            },
            "name": {
                "field_description": "Name",
                "track_visibility": "onchange",
                "ttype": "char",
            },
        }
        model_demo_model_2_portal = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code model
            lst_value = [
                {
                    "code": """super(DemoModel2Portal, self)._compute_access_url()
for demo_model_2_portal in self:
    demo_model_2_portal.access_url = (
        "/my/demo_model_2_portal/%s" % demo_model_2_portal.id
    )""",
                    "name": "_compute_access_url",
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_demo_model_2_portal.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Demo Model 3 Portal Diagram
        model_model = "demo.model_3.portal.diagram"
        model_name = "demo_model_3_portal_diagram"
        lst_depend_model = ["portal.mixin"]
        dct_model = {
            "description": "demo_model_3_portal_diagram",
            "diagram_arrow_dst_field": "demo_many2one_dst",
            "diagram_arrow_label": "['name']",
            "diagram_arrow_object": "demo.model_2.portal",
            "diagram_arrow_src_field": "demo_many2one_src",
            "diagram_label_string": (
                "Caution, all modification is live. Diagram model:"
                " demo.model_3.portal.diagram, node model: demo.model.portal"
                " and arrow model: demo.model_2.portal"
            ),
            "diagram_node_form_view_ref": "demo_model_portal_view_form",
            "diagram_node_object": "demo.model.portal",
            "diagram_node_shape_field": "rectangle:True",
            "diagram_node_xpos_field": "xpos",
            "diagram_node_ypos_field": "ypos",
            "menu_name_keep_application": True,
        }
        dct_field = {
            "name": {
                "field_description": "Name",
                "ttype": "char",
            },
        }
        model_demo_model_3_portal_diagram = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
            lst_depend_model=lst_depend_model,
        )

        # Added one2many field, many2one need to be create before add one2many
        model_model = "demo.model.portal"
        dct_field = {
            "demo_one2many_dst": {
                "field_description": "One2Many demo dst",
                "ttype": "one2many",
                "relation": "demo.model_2.portal",
                "relation_field": "demo_many2one_dst",
            },
            "demo_one2many_src": {
                "field_description": "One2Many demo src",
                "ttype": "one2many",
                "relation": "demo.model_2.portal",
                "relation_field": "demo_many2one_src",
            },
        }
        code_generator_id.add_update_model_one2many(model_model, dct_field)

        model_model = "demo.model_3.portal.diagram"
        dct_field = {
            "diagram_demo2_ids": {
                "field_description": "One2Many demo 2",
                "ttype": "one2many",
                "relation": "demo.model_2.portal",
                "relation_field": "diagram_id",
            },
            "diagram_demo_ids": {
                "field_description": "One2Many demo",
                "ttype": "one2many",
                "relation": "demo.model.portal",
                "relation_field": "diagram_id",
            },
        }
        code_generator_id.add_update_model_one2many(model_model, dct_field)

        # Generate code
        if True:
            # Generate code model
            lst_value = [
                {
                    "code": """# This is a comment need it for test, thanks
super(DemoModel3PortalDiagram, self)._compute_access_url()
for demo_model_3_portal_diagram in self:
    demo_model_3_portal_diagram.access_url = (
        "/my/demo_model_3_portal_diagram/%s"
        % demo_model_3_portal_diagram.id
    )""",
                    "name": "_compute_access_url",
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_demo_model_3_portal_diagram.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Generate view
        # Action generate view
        wizard_view = env["code.generator.generate.views.wizard"].create(
            {
                "code_generator_id": code_generator_id.id,
                "enable_generate_all": False,
                "enable_generate_portal": True,
                "portal_enable_create": True,
            }
        )

        wizard_view.button_generate_views()

        # Generate module
        value = {"code_generator_ids": code_generator_id.ids}
        env["code.generator.writer"].create(value)


def uninstall_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        code_generator_id = env["code.generator.module"].search(
            [("name", "=", MODULE_NAME)]
        )
        if code_generator_id:
            code_generator_id.unlink()
