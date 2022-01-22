import logging
import os

from odoo import SUPERUSER_ID, _, api, fields, models

_logger = logging.getLogger(__name__)

MODULE_NAME = "demo_internal_inherit"


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
            "shortdesc": "Demo internal inherit",
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
        code_generator_id.add_module_dependency("demo_internal")

        # Add/Update Demo Model Internal
        model_model = "demo.model.internal"
        model_name = "demo_model_internal"
        lst_depend_model = ["demo.model.internal"]
        dct_model = {
            "menu_name_keep_application": True,
        }
        dct_field = {
            "feature_text": {
                "code_generator_sequence": 1,
                "field_description": "Feature demo",
                "is_show_whitelist_model_inherit": True,
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

        # Generate view
        lst_view_id = []
        # calendar view
        if True:
            lst_item_view = []
            # BODY
            view_item_body_xpath_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "xpath",
                    "expr": "//field[@name='banana']",
                    "position": "after",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_xpath_1.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "feature_text",
                    "action_name": "feature_text",
                    "parent_id": view_item_body_xpath_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_code_generator = env["code.generator.view"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "view_type": "calendar",
                    "view_name": "demo_model_internal_calendar",
                    "m2o_model": model_demo_model_internal.id,
                    "view_item_ids": [(6, 0, lst_item_view)],
                    "inherit_view_name": (
                        "demo_internal.demo_model_internal_view_calendar"
                    ),
                }
            )
            lst_view_id.append(view_code_generator.id)

        # form view
        if True:
            lst_item_view = []
            # BODY
            view_item_body_xpath_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "xpath",
                    "expr": "//field[@name='banana']",
                    "position": "after",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_xpath_1.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "feature_text",
                    "action_name": "feature_text",
                    "parent_id": view_item_body_xpath_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_code_generator = env["code.generator.view"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "view_type": "form",
                    "view_name": "demo_model_internal_form",
                    "m2o_model": model_demo_model_internal.id,
                    "view_item_ids": [(6, 0, lst_item_view)],
                    "inherit_view_name": (
                        "demo_internal.demo_model_internal_view_form"
                    ),
                }
            )
            lst_view_id.append(view_code_generator.id)

        # kanban view
        if True:
            lst_item_view = []
            # BODY
            view_item_body_xpath_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "xpath",
                    "expr": "//field[@name='banana']",
                    "position": "after",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_xpath_1.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "feature_text",
                    "action_name": "feature_text",
                    "parent_id": view_item_body_xpath_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item_body_xpath_2 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "xpath",
                    "expr": "//div[hasclass('oe_kanban_details')]/ul",
                    "position": "inside",
                    "sequence": 2,
                }
            )
            lst_item_view.append(view_item_body_xpath_2.id)

            view_item_body_li_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "li",
                    "class_attr": "mb4",
                    "parent_id": view_item_body_xpath_2.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_li_1.id)

            view_item_body_strong_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "strong",
                    "parent_id": view_item_body_li_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_strong_1.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "feature_text",
                    "action_name": "feature_text",
                    "parent_id": view_item_body_strong_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_code_generator = env["code.generator.view"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "view_type": "kanban",
                    "view_name": "demo_model_internal_kanban",
                    "m2o_model": model_demo_model_internal.id,
                    "view_item_ids": [(6, 0, lst_item_view)],
                    "inherit_view_name": (
                        "demo_internal.demo_model_internal_view_kanban"
                    ),
                }
            )
            lst_view_id.append(view_code_generator.id)

        # pivot view
        if True:
            lst_item_view = []
            # BODY
            view_item_body_xpath_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "xpath",
                    "expr": "//field[@name='banana']",
                    "position": "after",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_xpath_1.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "feature_text",
                    "action_name": "feature_text",
                    "parent_id": view_item_body_xpath_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_code_generator = env["code.generator.view"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "view_type": "pivot",
                    "view_name": "demo_model_internal_pivot",
                    "m2o_model": model_demo_model_internal.id,
                    "view_item_ids": [(6, 0, lst_item_view)],
                    "inherit_view_name": (
                        "demo_internal.demo_model_internal_view_pivot"
                    ),
                }
            )
            lst_view_id.append(view_code_generator.id)

        # tree view
        if True:
            lst_item_view = []
            # BODY
            view_item_body_xpath_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "xpath",
                    "expr": "//field[@name='banana']",
                    "position": "after",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_xpath_1.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "feature_text",
                    "action_name": "feature_text",
                    "parent_id": view_item_body_xpath_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_code_generator = env["code.generator.view"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "view_type": "tree",
                    "view_name": "demo_model_internal_tree",
                    "m2o_model": model_demo_model_internal.id,
                    "view_item_ids": [(6, 0, lst_item_view)],
                    "inherit_view_name": (
                        "demo_internal.demo_model_internal_view_tree"
                    ),
                }
            )
            lst_view_id.append(view_code_generator.id)

        # Action generate view
        wizard_view = env["code.generator.generate.views.wizard"].create(
            {
                "code_generator_id": code_generator_id.id,
                "enable_generate_all": False,
                "disable_generate_menu": True,
                "disable_generate_access": True,
                "code_generator_view_ids": [(6, 0, lst_view_id)],
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
