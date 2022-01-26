import os

from odoo import SUPERUSER_ID, _, api, fields, models

# TODO HUMAN: change my module_name to create a specific demo functionality
MODULE_NAME = "code_generator_code_generator"


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # The path of the actual file
        path_module_generate = os.path.normpath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "TechnoLibre_odoo-code-generator",
            )
        )

        short_name = MODULE_NAME.replace("_", " ").title()

        # Add code generator
        value = {
            "shortdesc": short_name,
            "name": MODULE_NAME,
            "license": "AGPL-3",
            "author": "TechnoLibre",
            "website": "https://technolibre.ca",
            "application": True,
            "enable_sync_code": True,
            "path_sync_code": path_module_generate,
        }

        # TODO HUMAN: enable your functionality to generate
        value["enable_template_code_generator_demo"] = False
        value["template_model_name"] = (
            "code.generator.act_window; code.generator.add.controller.wizard;"
            " code.generator.add.model.wizard;"
            " code.generator.generate.views.wizard;"
            " code.generator.ir.model.dependency;"
            " code.generator.ir.model.fields; code.generator.menu;"
            " code.generator.model.code; code.generator.model.code.import;"
            " code.generator.module; code.generator.module.dependency;"
            " code.generator.module.external.dependency;"
            " code.generator.module.template.dependency;"
            " code.generator.pyclass; code.generator.view;"
            " code.generator.view.item; code.generator.writer;"
            " ir.model.server_constrain"
        )
        value["template_inherit_model_name"] = (
            "ir.actions.act_url; ir.actions.act_window; ir.actions.report;"
            " ir.actions.server; ir.actions.todo; ir.model;"
            " ir.model.constraint; ir.model.fields; ir.module.module;"
            " ir.module.module.dependency; ir.ui.menu; ir.ui.view;"
            " res.config.settings; res.groups"
        )
        value["enable_template_wizard_view"] = True
        value["force_generic_template_wizard_view"] = True
        value["enable_template_website_snippet_view"] = False
        value["enable_sync_template"] = True
        value["ignore_fields"] = ""
        value["post_init_hook_show"] = True
        value["uninstall_hook_show"] = True
        value["post_init_hook_feature_code_generator"] = True
        value["uninstall_hook_feature_code_generator"] = True

        new_module_name = MODULE_NAME
        if (
            MODULE_NAME != "code_generator_demo"
            and "code_generator_" in MODULE_NAME
        ):
            if "code_generator_template" in MODULE_NAME:
                if value["enable_template_code_generator_demo"]:
                    new_module_name = f"code_generator_{MODULE_NAME[len('code_generator_template_'):]}"
                else:
                    new_module_name = MODULE_NAME[
                        len("code_generator_template_") :
                    ]
            else:
                new_module_name = MODULE_NAME[len("code_generator_") :]
            value["template_module_name"] = new_module_name
        value["hook_constant_code"] = f'MODULE_NAME = "{new_module_name}"'

        code_generator_id = env["code.generator.module"].create(value)

        # Add dependencies
        # TODO HUMAN: update your dependencies
        lst_depend = [
            "code_generator",
            "code_generator_hook",
        ]
        code_generator_id.add_module_dependency(lst_depend)

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
