from odoo import SUPERUSER_ID, _, api, fields, models

MODULE_NAME = "demo_website_snippet"


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # The path of the actual file
        # path_module_generate = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

        short_name = MODULE_NAME.replace("_", " ").title()

        # Add code generator
        value = {
            "shortdesc": short_name,
            "name": MODULE_NAME,
            "license": "AGPL-3",
            "author": "TechnoLibre",
            "website": "https://technolibre.ca",
            "application": True,
            "category_id": env.ref("base.module_category_website").id,
            "enable_sync_code": True,
            # "path_sync_code": path_module_generate,
        }

        # TODO HUMAN: enable your functionality to generate
        code_generator_id = env["code.generator.module"].create(value)

        # Add dependencies
        lst_depend = [
            "website",
        ]
        code_generator_id.add_module_dependency(lst_depend)

        # Generate snippet
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "helloworld",
            "enable_javascript": True,
            "snippet_type": "effect",
        }
        env["code.generator.snippet"].create(value_snippet)

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
