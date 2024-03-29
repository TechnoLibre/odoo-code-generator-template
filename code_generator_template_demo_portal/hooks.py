import logging
import os

from odoo import SUPERUSER_ID, _, api, fields, models

_logger = logging.getLogger(__name__)

# TODO HUMAN: change my module_name to create a specific demo functionality
MODULE_NAME = "code_generator_demo_portal"


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # The path of the actual file
        path_module_generate = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..")
        )

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
        }

        # TODO HUMAN: enable your functionality to generate
        value["enable_template_code_generator_demo"] = False
        value["template_model_name"] = (
            "demo.model.portal; demo.model_2.portal;"
            " demo.model_3.portal.diagram"
        )
        value["template_inherit_model_name"] = ""
        value["enable_template_wizard_view"] = True
        value["force_generic_template_wizard_view"] = True
        value["enable_cg_generate_portal"] = True
        value["enable_cg_portal_enable_create"] = True
        value["enable_template_website_snippet_view"] = True
        value["disable_fix_code_generator_sequence"] = True
        value["enable_sync_template"] = True
        value["post_init_hook_show"] = True
        value["uninstall_hook_show"] = True
        value["post_init_hook_feature_code_generator"] = True
        value["uninstall_hook_feature_code_generator"] = True

        new_module_name = MODULE_NAME
        if (
            not value["enable_template_code_generator_demo"]
            and "code_generator_" in MODULE_NAME
        ):
            new_module_name = MODULE_NAME[len("code_generator_") :]
            value["template_module_name"] = new_module_name
        value["hook_constant_code"] = f'MODULE_NAME = "{new_module_name}"'

        code_generator_id = env["code.generator.module"].create(value)

        # Add dependencies
        # TODO HUMAN: update your dependencies
        lst_depend = [
            "code_generator",
            "code_generator_portal",
            "code_generator_website_snippet",
        ]
        code_generator_id.add_module_dependency(lst_depend)
        lst_depend = [
            "portal",
        ]
        code_generator_id.add_module_dependency_template(lst_depend)

        # Generate module
        value = {"code_generator_ids": code_generator_id.ids}
        code_generator_writer = env["code.generator.writer"].create(value)

        new_module_path = os.path.join(path_module_generate, new_module_name)
        code_generator_writer.set_module_translator(
            new_module_name, new_module_path
        )


def uninstall_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        code_generator_id = env["code.generator.module"].search(
            [("name", "=", MODULE_NAME)]
        )
        if code_generator_id:
            code_generator_id.unlink()
