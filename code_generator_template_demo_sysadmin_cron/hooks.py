from odoo import _, api, models, fields, SUPERUSER_ID

# TODO HUMAN: change my module_name to create a specific demo functionality
MODULE_NAME = "code_generator_auto_backup"


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
            "enable_sync_code": True,
            # "path_sync_code": path_module_generate,
        }

        # TODO HUMAN: enable your functionality to generate
        value["enable_template_code_generator_demo"] = False
        value["template_model_name"] = "db.backup"
        value["enable_template_wizard_view"] = True
        value["enable_template_website_snippet_view"] = False
        value["enable_sync_template"] = True
        value["enable_cron_template"] = True
        value["ignore_fields"] = "value_field_message_follower_ids;value_field_message_ids;" \
                                 "value_field_website_message_ids;message_attachment_count;message_channel_ids;" \
                                 "message_follower_ids;message_has_error;message_has_error_counter;message_ids;" \
                                 "message_is_follower;message_main_attachment_id;message_needaction;" \
                                 "message_needaction_counter;message_partner_ids;message_unread;" \
                                 "message_unread_counter;website_message_ids"
        value["post_init_hook_show"] = True
        value["uninstall_hook_show"] = True
        value["post_init_hook_feature_code_generator"] = True
        value["uninstall_hook_feature_code_generator"] = True

        new_module_name = MODULE_NAME
        if MODULE_NAME != "code_generator_demo" and "code_generator_" in MODULE_NAME:
            if "code_generator_template" in MODULE_NAME:
                if value["enable_template_code_generator_demo"]:
                    new_module_name = f"code_generator_{MODULE_NAME[len('code_generator_template_'):]}"
                else:
                    new_module_name = MODULE_NAME[len("code_generator_template_"):]
            else:
                new_module_name = MODULE_NAME[len("code_generator_"):]
            new_module_name = "auto_backup"
            value["template_module_name"] = new_module_name
            value["template_module_path_generated_extension"] = "'..', 'OCA_server-tools'"
        value["hook_constant_code"] = f'''import os

MODULE_NAME = "{new_module_name}"'''

        code_generator_id = env["code.generator.module"].create(value)

        # Add dependencies
        # TODO HUMAN: update your dependencies
        lst_depend = [
            "code_generator",
            "code_generator_cron",
        ]
        lst_dependencies = env["ir.module.module"].search([("name", "in", lst_depend)])
        for depend in lst_dependencies:
            value = {
                "module_id": code_generator_id.id,
                "depend_id": depend.id,
                "name": depend.display_name,
            }
            env["code.generator.module.dependency"].create(value)

        # Generate module
        value = {
            "code_generator_ids": code_generator_id.ids
        }
        code_generator_writer = env["code.generator.writer"].create(value)


def uninstall_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        code_generator_id = env["code.generator.module"].search([("name", "=", MODULE_NAME)])
        if code_generator_id:
            code_generator_id.unlink()
