import logging
import os

from odoo import SUPERUSER_ID, _, api, fields, models

_logger = logging.getLogger(__name__)

MODULE_NAME = "demo_website_multiple_snippet"


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # The path of the actual file
        path_module_generate = (
            "addons/TechnoLibre_odoo-code-generator-template"
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
            "path_sync_code": path_module_generate,
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
        lst_depend_module = ["website", "demo_portal"]
        code_generator_id.add_module_dependency(lst_depend_module)

        # Generate snippet
        # Documentation Case 1
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "helloworld",
            "name": "helloworld static structure",
            "snippet_type": "structure",
            "debug_doc": "case 1",
        }
        env["code.generator.snippet"].create(value_snippet)

        # Documentation Case 2
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "helloworld",
            "enable_javascript": True,
            "name": "helloworld structure",
            "snippet_type": "structure",
            "debug_doc": "case 2",
        }
        env["code.generator.snippet"].create(value_snippet)

        # Documentation Case 3
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "model_show_item_individual",
            "enable_javascript": True,
            "model_name": "demo.model.portal",
            "name": "Individual item structure",
            "snippet_type": "structure",
            "debug_doc": "case 3",
        }
        env["code.generator.snippet"].create(value_snippet)

        # Documentation Case 4
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "model_show_item_list",
            "enable_javascript": True,
            "limitation_item": 3,
            "model_name": "demo.model.portal",
            "model_short_name": "portal_time",
            "name": "List show_time item structure",
            "show_diff_time": True,
            "show_recent_item": True,
            "snippet_type": "structure",
            "debug_doc": "case 4",
        }
        env["code.generator.snippet"].create(value_snippet)

        # Documentation Case 5
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "model_show_item_list",
            "enable_javascript": True,
            "limitation_item": 3,
            "model_name": "demo.model.portal",
            "model_short_name": "portal",
            "name": "List item structure",
            "show_diff_time": False,
            "show_recent_item": True,
            "snippet_type": "structure",
            "debug_doc": "case 5",
        }
        env["code.generator.snippet"].create(value_snippet)

        # Documentation Case 6
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "model_show_item_list",
            "enable_javascript": True,
            "limitation_item": 3,
            "model_name": "demo.model.portal",
            # "model_short_name": "portal",
            "name": "List item structure generic",
            "show_diff_time": True,
            "show_recent_item": True,
            "snippet_type": "structure",
            "debug_doc": "case 6",
        }
        env["code.generator.snippet"].create(value_snippet)

        # Documentation Case 7
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "model_show_item_list",
            "enable_javascript": True,
            "limitation_item": 3,
            "model_name": "demo.model.portal;demo.model_2.portal;demo.model_3.portal.diagram",
            "model_short_name": "double_portal",
            "name": "List item structure double",
            "show_diff_time": True,
            "show_recent_item": True,
            "snippet_type": "structure",
            "debug_doc": "case 7",
        }
        env["code.generator.snippet"].create(value_snippet)

        # Documentation Case 8
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "model_show_item_list",
            "enable_javascript": True,
            "limitation_item": 3,
            "model_name": "demo.model.portal;demo.model_2.portal;demo.model_3.portal.diagram",
            "model_short_name": "dp_dmp;dp_dm2p;dp_dm3pd",
            "name": "List item structure double short",
            "show_diff_time": True,
            "show_recent_item": True,
            "snippet_type": "structure",
            "debug_doc": "case 8",
        }
        env["code.generator.snippet"].create(value_snippet)

        # Documentation Case 9
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "helloworld",
            "enable_javascript": True,
            "name": "helloworld effect",
            "snippet_type": "effect",
            "debug_doc": "case 9",
        }
        env["code.generator.snippet"].create(value_snippet)

        # Documentation Case 10
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "model_show_item_individual",
            "enable_javascript": True,
            "model_name": "demo.model.portal",
            "name": "Individual item effect",
            "snippet_type": "effect",
            "debug_doc": "case 10",
        }
        env["code.generator.snippet"].create(value_snippet)

        # Documentation Case 11
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "helloworld",
            "enable_javascript": True,
            "name": "helloworld feature",
            "snippet_type": "feature",
            "debug_doc": "case 11",
        }
        env["code.generator.snippet"].create(value_snippet)

        # Documentation Case 12
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "model_show_item_individual",
            "enable_javascript": True,
            "model_name": "demo.model.portal",
            "name": "Individual item feature",
            "snippet_type": "feature",
            "debug_doc": "case 12",
        }
        env["code.generator.snippet"].create(value_snippet)

        # Documentation Case 13
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "helloworld",
            "enable_javascript": True,
            "name": "helloworld content",
            "snippet_type": "content",
            "debug_doc": "case 13",
        }
        env["code.generator.snippet"].create(value_snippet)

        # Documentation Case 14
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "model_show_item_individual",
            "enable_javascript": True,
            "model_name": "demo.model.portal",
            "name": "Individual item content",
            "snippet_type": "content",
            "debug_doc": "case 14",
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
