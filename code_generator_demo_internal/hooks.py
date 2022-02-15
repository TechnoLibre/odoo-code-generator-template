import logging
import os

from odoo import SUPERUSER_ID, _, api, fields, models

_logger = logging.getLogger(__name__)

MODULE_NAME = "demo_internal"


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
            "shortdesc": "Demo internal",
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
        code_generator_id.add_module_dependency("mail")

        # Add/Update Demo Model Internal
        model_model = "demo.model.internal"
        model_name = "demo_model_internal"
        lst_depend_model = ["mail.thread", "mail.activity.mixin"]
        dct_model = {
            "description": "demo_model_internal",
            "enable_activity": True,
            "menu_name_keep_application": True,
        }
        dct_field = {
            "banana": {
                "code_generator_form_simple_view_sequence": 11,
                "code_generator_sequence": 4,
                "code_generator_tree_view_sequence": 11,
                "field_description": "Banana demo",
                "ttype": "boolean",
            },
            "date_end": {
                "code_generator_form_simple_view_sequence": 12,
                "code_generator_sequence": 5,
                "code_generator_tree_view_sequence": 12,
                "field_description": "Date end",
                "is_date_end_view": True,
                "ttype": "datetime",
            },
            "date_start": {
                "code_generator_form_simple_view_sequence": 13,
                "code_generator_sequence": 6,
                "code_generator_tree_view_sequence": 13,
                "field_description": "Date start",
                "is_date_start_view": True,
                "ttype": "datetime",
            },
            "name": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 3,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Name",
                "ttype": "char",
            },
        }
        model_demo_model_internal = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
            lst_depend_model=lst_depend_model,
        )

        # Add/Update Demo Model 2 Internal
        model_model = "demo.model_2.internal"
        model_name = "demo_model_2_internal"
        dct_model = {
            "description": "demo_model_2_internal",
            "menu_name_keep_application": True,
        }
        dct_field = {
            "model_1": {
                "code_generator_form_simple_view_sequence": 11,
                "code_generator_sequence": 3,
                "code_generator_tree_view_sequence": 11,
                "field_description": "Model 1",
                "relation": "demo.model.internal",
                "ttype": "many2one",
            },
            "name": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 2,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Name",
                "ttype": "char",
            },
        }
        model_demo_model_2_internal = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Generate view
        # Action generate view
        wizard_view = env["code.generator.generate.views.wizard"].create(
            {
                "code_generator_id": code_generator_id.id,
                "enable_generate_all": False,
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
