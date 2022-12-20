import logging
import os

from odoo import SUPERUSER_ID, _, api, fields, models

_logger = logging.getLogger(__name__)

MODULE_NAME = "code_generator"


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
            [("name", "=", "Extra Tools")], limit=1
        )
        value = {
            "shortdesc": short_name,
            "name": MODULE_NAME,
            "license": "AGPL-3",
            "category_id": categ_id.id,
            "summary": "Code Generator Module",
            "author": "Mathben (mathben@technolibre.ca)",
            "website": "",
            "application": False,
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
        lst_depend_module = ["base", "mail"]
        code_generator_id.add_module_dependency(lst_depend_module)

        # Add/Update Code Generator Act Window
        model_model = "code.generator.act_window"
        model_name = "code_generator_act_window"
        dct_model = {
            "description": "Code Generator Act Window",
        }
        dct_field = {
            "code_generator_id": {
                "code_generator_sequence": 3,
                "field_description": "Code Generator",
                "relation": "code.generator.module",
                "required": True,
                "ttype": "many2one",
            },
            "id_name": {
                "code_generator_sequence": 4,
                "field_description": "Action id",
                "help": "Specify id name of this action window.",
                "ttype": "char",
            },
            "model_name": {
                "code_generator_sequence": 5,
                "field_description": "Model Name",
                "help": "The associate model, if empty, no association.",
                "ttype": "char",
            },
            "name": {
                "code_generator_sequence": 2,
                "field_description": "name",
                "ttype": "char",
            },
        }
        model_code_generator_act_window = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_act_window.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Code Generator Add Controller Wizard
        model_model = "code.generator.add.controller.wizard"
        model_name = "code_generator_add_controller_wizard"
        dct_model = {
            "description": "Code Generator Add Controller Wizard",
        }
        dct_field = {
            "code_generator_id": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 2,
                "field_description": "Code Generator",
                "relation": "code.generator.module",
                "required": True,
                "ttype": "many2one",
            },
            "field_ids": {
                "code_generator_sequence": 3,
                "field_description": "Fields",
                "help": "Select the field you want to inherit or import data.",
                "relation": "ir.model.fields",
                "ttype": "many2many",
            },
            "model_ids": {
                "code_generator_form_simple_view_sequence": 12,
                "code_generator_sequence": 4,
                "field_description": "Models",
                "help": "Select the model you want to inherit or import data.",
                "relation": "ir.model",
                "ttype": "many2many",
            },
            "user_id": {
                "code_generator_form_simple_view_sequence": 11,
                "code_generator_sequence": 5,
                "default_lambda": "lambda s: s.env.user.id",
                "field_description": "User",
                "relation": "res.users",
                "required": True,
                "ttype": "many2one",
            },
        }
        model_code_generator_add_controller_wizard = (
            code_generator_id.add_update_model(
                model_model,
                model_name,
                dct_field=dct_field,
                dct_model=dct_model,
            )
        )

        # Generate code
        if True:
            # Generate code model
            lst_value = [
                {
                    "code": """field_ids = [
    field_id.id
    for model_id in self.model_ids
    for field_id in model_id.field_id
]
self.field_ids = [(6, 0, field_ids)]""",
                    "name": "_onchange_model_ids",
                    "decorator": '@api.onchange("model_ids")',
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_add_controller_wizard.id,
                },
                {
                    "code": """pass""",
                    "name": "button_generate_add_controller",
                    "decorator": "@api.multi",
                    "param": "self",
                    "sequence": 1,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_add_controller_wizard.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Code Generator Add Model Wizard
        model_model = "code.generator.add.model.wizard"
        model_name = "code_generator_add_model_wizard"
        dct_model = {
            "description": "Code Generator Model Wizard",
        }
        dct_field = {
            "clear_fields_blacklist": {
                "code_generator_form_simple_view_sequence": 14,
                "code_generator_sequence": 2,
                "field_description": "Clear field blacklisted",
                "help": "Erase all blacklisted fields when enable.",
                "ttype": "boolean",
            },
            "code_generator_id": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 3,
                "field_description": "Code Generator",
                "relation": "code.generator.module",
                "required": True,
                "ttype": "many2one",
            },
            "field_ids": {
                "code_generator_form_simple_view_sequence": 16,
                "code_generator_sequence": 4,
                "field_description": "Fields",
                "help": "Select the field you want to inherit or import data.",
                "relation": "ir.model.fields",
                "ttype": "many2many",
            },
            "model_ids": {
                "code_generator_form_simple_view_sequence": 15,
                "code_generator_sequence": 5,
                "field_description": "Models",
                "help": "Select the model you want to inherit or import data.",
                "relation": "ir.model",
                "ttype": "many2many",
            },
            "option_adding": {
                "code_generator_form_simple_view_sequence": 12,
                "code_generator_sequence": 6,
                "default": "nomenclator",
                "field_description": "Option Adding",
                "help": """Inherit to inherit a new model.
Nomenclator to export data.""",
                "required": True,
                "selection": (
                    "[('inherit', 'Inherit Model'), ('nomenclator',"
                    " 'Nomenclator')]"
                ),
                "ttype": "selection",
            },
            "option_blacklist": {
                "code_generator_form_simple_view_sequence": 13,
                "code_generator_sequence": 7,
                "default": "whitelist",
                "field_description": "Option Blacklist",
                "help": """When whitelist, all selected fields will be added.
When blacklist, all selected fields will be ignored.""",
                "required": True,
                "selection": (
                    "[('blacklist', 'Blacklist'), ('whitelist', 'Whitelist')]"
                ),
                "ttype": "selection",
            },
            "user_id": {
                "code_generator_form_simple_view_sequence": 11,
                "code_generator_sequence": 8,
                "default_lambda": "lambda s: s.env.user.id",
                "field_description": "User",
                "relation": "res.users",
                "required": True,
                "ttype": "many2one",
            },
        }
        model_code_generator_add_model_wizard = (
            code_generator_id.add_update_model(
                model_model,
                model_name,
                dct_field=dct_field,
                dct_model=dct_model,
            )
        )

        # Generate code
        if True:
            # Generate code model
            lst_value = [
                {
                    "code": """field_ids = [
    field_id.id
    for model_id in self.model_ids
    for field_id in model_id.field_id
]
self.field_ids = [(6, 0, field_ids)]""",
                    "name": "_onchange_model_ids",
                    "decorator": '@api.onchange("model_ids")',
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_add_model_wizard.id,
                },
                {
                    "code": """if self.clear_fields_blacklist:
    field_ids = self.env["code.generator.ir.model.fields"].search(
        [("m2o_module", "=", self.code_generator_id.id)]
    )
    field_ids.unlink()

is_nomenclator = self.option_adding == "nomenclator"
lst_field_id = [a.id for a in self.field_ids]
lst_ignore_model = ["website_theme_install"]
for model_id in self.model_ids:
    # model_name = model_id.model

    # Ignore base model
    if model_id.model not in ("ir.ui.view",):
        module_name = model_id.modules
        lst_module_name = []
        if "," in module_name:
            lst_module_name = [
                a.strip() for a in module_name.split(",")
            ]
        else:
            lst_module_name.append(module_name)

        for module_name in lst_module_name:
            if module_name in lst_ignore_model:
                continue
            # Add dependency
            # check not exist before added
            module_id = self.env["ir.module.module"].search(
                [("name", "=", module_name)]
            )
            dependencies_len = self.env[
                "code.generator.module.dependency"
            ].search_count(
                [
                    ("module_id", "=", self.code_generator_id.id),
                    ("depend_id", "=", module_id.id),
                ]
            )
            if not dependencies_len:
                value_dependencies = {
                    "module_id": self.code_generator_id.id,
                    "depend_id": module_id.id,
                    "name": module_id.display_name,
                }
                self.env["code.generator.module.dependency"].create(
                    value_dependencies
                )

    if is_nomenclator:
        self.code_generator_id.nomenclator_only = True
        model_id.nomenclator = True
        model_id.m2o_module = self.code_generator_id.id

        # Disable nomenclator for unused fields
        for field_id in model_id.field_id:
            if field_id.id in lst_field_id:
                value = {
                    "m2o_module": self.code_generator_id.id,
                    "m2o_fields": field_id.id,
                    "nomenclature_blacklist": self.option_blacklist
                    == "blacklist",
                    "nomenclature_whitelist": self.option_blacklist
                    == "whitelist",
                }
                self.env["code.generator.ir.model.fields"].create(
                    value
                )""",
                    "name": "button_generate_add_model",
                    "decorator": "@api.multi",
                    "param": "self",
                    "sequence": 1,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_add_model_wizard.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Code Generator Generate Views Wizard
        model_model = "code.generator.generate.views.wizard"
        model_name = "code_generator_generate_views_wizard"
        dct_model = {
            "description": "Code Generator Generate Views Wizard",
        }
        dct_field = {
            "all_model": {
                "code_generator_form_simple_view_sequence": 13,
                "code_generator_sequence": 3,
                "default": True,
                "field_description": "All models",
                "help": (
                    "Generate with all existing model, or select manually."
                ),
                "ttype": "boolean",
            },
            "clear_all_access": {
                "code_generator_form_simple_view_sequence": 14,
                "code_generator_sequence": 4,
                "default": True,
                "field_description": "Clear access",
                "help": "Clear all access/permission before execute.",
                "ttype": "boolean",
            },
            "clear_all_act_window": {
                "code_generator_form_simple_view_sequence": 15,
                "code_generator_sequence": 5,
                "default": True,
                "field_description": "Clear actions windows",
                "help": "Clear all actions windows before execute.",
                "ttype": "boolean",
            },
            "clear_all_menu": {
                "code_generator_form_simple_view_sequence": 16,
                "code_generator_sequence": 6,
                "default": True,
                "field_description": "Clear menus",
                "help": "Clear all menus before execute.",
                "ttype": "boolean",
            },
            "clear_all_view": {
                "code_generator_form_simple_view_sequence": 17,
                "code_generator_sequence": 7,
                "default": True,
                "field_description": "Clear views",
                "help": "Clear all views before execute.",
                "ttype": "boolean",
            },
            "code_generator_id": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 8,
                "field_description": "Code Generator",
                "relation": "code.generator.module",
                "required": True,
                "ttype": "many2one",
            },
            "code_generator_view_ids": {
                "code_generator_sequence": 9,
                "field_description": "Code Generator View",
                "relation": "code.generator.view",
                "ttype": "many2many",
            },
            "date": {
                "code_generator_sequence": 10,
                "default_lambda": "fields.Date.context_today",
                "field_description": "Date",
                "required": True,
                "ttype": "date",
            },
            "disable_generate_access": {
                "code_generator_sequence": 11,
                "field_description": "Disable Generate Access",
                "help": "Disable security access generation.",
                "ttype": "boolean",
            },
            "disable_generate_menu": {
                "code_generator_sequence": 12,
                "field_description": "Disable Generate Menu",
                "help": "Disable menu generation.",
                "ttype": "boolean",
            },
            "enable_generate_all": {
                "code_generator_form_simple_view_sequence": 12,
                "code_generator_sequence": 13,
                "default": True,
                "field_description": "Enable all feature",
                "help": "Generate with all feature.",
                "ttype": "boolean",
            },
            "name": {
                "code_generator_sequence": 2,
                "field_description": "Name",
                "ttype": "char",
            },
            "selected_model_calendar_view_ids": {
                "code_generator_sequence": 14,
                "field_description": "Selected Model Calendar View",
                "relation": "ir.model",
                "ttype": "many2many",
            },
            "selected_model_diagram_view_ids": {
                "code_generator_sequence": 15,
                "field_description": "Selected Model Diagram View",
                "relation": "ir.model",
                "ttype": "many2many",
            },
            "selected_model_form_view_ids": {
                "code_generator_form_simple_view_sequence": 19,
                "code_generator_sequence": 16,
                "field_description": "Selected Model Form View",
                "relation": "ir.model",
                "ttype": "many2many",
            },
            "selected_model_graph_view_ids": {
                "code_generator_sequence": 17,
                "field_description": "Selected Model Graph View",
                "relation": "ir.model",
                "ttype": "many2many",
            },
            "selected_model_kanban_view_ids": {
                "code_generator_sequence": 18,
                "field_description": "Selected Model Kanban View",
                "relation": "ir.model",
                "ttype": "many2many",
            },
            "selected_model_pivot_view_ids": {
                "code_generator_sequence": 19,
                "field_description": "Selected Model Pivot View",
                "relation": "ir.model",
                "ttype": "many2many",
            },
            "selected_model_search_view_ids": {
                "code_generator_sequence": 20,
                "field_description": "Selected Model Search View",
                "relation": "ir.model",
                "ttype": "many2many",
            },
            "selected_model_timeline_view_ids": {
                "code_generator_sequence": 21,
                "field_description": "Selected Model Timeline View",
                "relation": "ir.model",
                "ttype": "many2many",
            },
            "selected_model_tree_view_ids": {
                "code_generator_form_simple_view_sequence": 18,
                "code_generator_sequence": 22,
                "field_description": "Selected Model Tree View",
                "relation": "ir.model",
                "ttype": "many2many",
            },
            "user_id": {
                "code_generator_form_simple_view_sequence": 11,
                "code_generator_sequence": 23,
                "default_lambda": "lambda s: s.env.user.id",
                "field_description": "User",
                "relation": "res.users",
                "required": True,
                "ttype": "many2one",
            },
        }
        model_code_generator_generate_views_wizard = (
            code_generator_id.add_update_model(
                model_model,
                model_name,
                dct_field=dct_field,
                dct_model=dct_model,
            )
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """import logging
import time
import uuid
from collections import defaultdict

import unidecode
from lxml import etree as ET
from lxml.builder import E

from odoo import _, api, fields, models
from odoo.models import MAGIC_COLUMNS

_logger = logging.getLogger(__name__)

MAGIC_FIELDS = MAGIC_COLUMNS + [
    "display_name",
    "__last_update",
    "access_url",
    "access_token",
    "access_warning",
]""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_generate_views_wizard.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """if self.clear_all_access and self.code_generator_id.o2m_model_access:
    self.code_generator_id.o2m_model_access.unlink()
if self.clear_all_menu and self.code_generator_id.o2m_menus:
    self.code_generator_id.o2m_menus.unlink()
if self.clear_all_act_window:
    if self.code_generator_id.o2m_model_act_window:
        self.code_generator_id.o2m_model_act_window.unlink()
    if self.code_generator_id.o2m_model_act_todo:
        self.code_generator_id.o2m_model_act_todo.unlink()
    if self.code_generator_id.o2m_model_act_url:
        self.code_generator_id.o2m_model_act_url.unlink()""",
                    "name": "clear_all",
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """self.ensure_one()

# Add dependencies
self._add_dependencies()

self.clear_all()

# TODO refactor this part to control generation
dct_value_to_create = defaultdict(list)

before_time = time.process_time()

if not self.code_generator_view_ids:
    status = self.generic_generate_view(dct_value_to_create)
else:
    model_id = None
    lst_view_generated = []
    lst_model_id = []
    for code_generator_view_id in self.code_generator_view_ids:
        view_id = self._generate_specific_form_views_models(
            code_generator_view_id, dct_value_to_create
        )
        lst_view_generated.append(view_id.type)
        lst_model_id.append(view_id.m2o_model)
    lst_model_id = list(set(lst_model_id))
    for model_id in lst_model_id:
        self._generate_model_access(model_id)
    if model_id:
        self._generate_menu(
            model_id,
            model_id.m2o_module,
            lst_view_generated,
            self.code_generator_id.o2m_models,
        )
    status = True
# Accelerate creation in batch
for model_name, lst_value in dct_value_to_create.items():
    self.env[model_name].create(lst_value)

after_time = time.process_time()
_logger.info(
    "DEBUG time execution button_generate_views"
    f" {after_time - before_time}"
)
return status""",
                    "name": "button_generate_views",
                    "decorator": "@api.multi",
                    "param": "self",
                    "sequence": 1,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """o2m_models_view_tree = (
    self.code_generator_id.o2m_models
    if self.all_model
    else self.selected_model_tree_view_ids
)
o2m_models_view_form = (
    self.code_generator_id.o2m_models
    if self.all_model
    else self.selected_model_form_view_ids
)
o2m_models_view_kanban = (
    self.code_generator_id.o2m_models
    if self.all_model
    else self.selected_model_kanban_view_ids
)
o2m_models_view_search = (
    self.code_generator_id.o2m_models
    if self.all_model
    else self.selected_model_search_view_ids
)
o2m_models_view_pivot = (
    self.code_generator_id.o2m_models
    if self.all_model
    else self.selected_model_pivot_view_ids
)
o2m_models_view_calendar = (
    self.code_generator_id.o2m_models
    if self.all_model
    else self.selected_model_calendar_view_ids
)
o2m_models_view_graph = (
    self.code_generator_id.o2m_models
    if self.all_model
    else self.selected_model_graph_view_ids
)
o2m_models_view_timeline = (
    self.code_generator_id.o2m_models
    if self.all_model
    else self.selected_model_timeline_view_ids
)
o2m_models_view_diagram = (
    self.code_generator_id.o2m_models.filtered(
        lambda model: model.diagram_node_object
        and model.diagram_arrow_object
        and model.diagram_node_xpos_field
        and model.diagram_node_ypos_field
        and model.diagram_arrow_src_field
        and model.diagram_arrow_dst_field
    )
    if self.all_model
    else self.selected_model_diagram_view_ids
)
# Get unique list order by name of all model to generate
lst_model = sorted(
    set(
        o2m_models_view_tree
        + o2m_models_view_form
        + o2m_models_view_kanban
        + o2m_models_view_search
        + o2m_models_view_pivot
        + o2m_models_view_calendar
        + o2m_models_view_graph
        + o2m_models_view_timeline
    ),
    key=lambda model: model.name,
)
lst_model_id = self.env["ir.model"].browse([a.id for a in lst_model])

for model_id in lst_model_id:
    lst_view_generated = []

    # Support enable_activity
    if model_id.enable_activity:
        model_id.add_model_inherit(
            ["mail.thread", "mail.activity.mixin"]
        )
        # inherit_model_ids
        lst_view_generated.append("activity")

    # Different view
    if model_id in o2m_models_view_tree:
        is_whitelist = any(
            [a.is_show_whitelist_list_view for a in model_id.field_id]
        )
        # model_created_fields_tree = list(
        #     filter(
        #         lambda x: x.name not in MAGIC_FIELDS
        #                   and not x.is_hide_blacklist_list_view
        #                   and (
        #                           not is_whitelist
        #                           or (is_whitelist and x.is_show_whitelist_list_view)
        #                   ),
        #         [a for a in model_id.field_id],
        #     )
        # )
        model_created_fields_tree = model_id.field_id.filtered(
            lambda field: field.name not in MAGIC_FIELDS
            and not field.is_hide_blacklist_list_view
            and (
                not is_whitelist
                or (is_whitelist and field.is_show_whitelist_list_view)
            )
        )
        model_created_fields_tree = self._update_model_field_tree_view(
            model_created_fields_tree
        )
        self._generate_list_views_models(
            model_id,
            model_created_fields_tree,
            model_id.m2o_module,
            dct_value_to_create,
        )
        lst_view_generated.append("tree")

    if model_id in o2m_models_view_form:
        is_whitelist = any(
            [
                a.is_show_whitelist_form_view
                for b in model_id
                for a in b.field_id
            ]
        )
        # model_created_fields_form = list(
        #     filter(
        #         lambda x: x.name not in MAGIC_FIELDS
        #                   and not x.is_hide_blacklist_form_view
        #                   and (
        #                           not is_whitelist
        #                           or (is_whitelist and x.is_show_whitelist_form_view)
        #                   ),
        #         [a for a in model_id.field_id],
        #     )
        # )
        model_created_fields_form = model_id.field_id.filtered(
            lambda field: field.name not in MAGIC_FIELDS
            and not field.is_hide_blacklist_form_view
            and (
                not is_whitelist
                or (is_whitelist and field.is_show_whitelist_form_view)
            )
        )
        self._generate_form_views_models(
            model_id,
            model_created_fields_form,
            model_id.m2o_module,
            dct_value_to_create,
        )
        lst_view_generated.append("form")

    if model_id in o2m_models_view_kanban:
        is_whitelist = any(
            [
                a.is_show_whitelist_kanban_view
                for b in model_id
                for a in b.field_id
            ]
        )
        # model_created_fields_kanban = list(
        #     filter(
        #         lambda x: x.name not in MAGIC_FIELDS
        #                   and not x.is_hide_blacklist_kanban_view
        #                   and (
        #                           not is_whitelist
        #                           or (is_whitelist and x.is_show_whitelist_kanban_view)
        #                   ),
        #         [a for a in model_id.field_id],
        #     )
        # )
        model_created_fields_kanban = model_id.field_id.filtered(
            lambda field: field.name not in MAGIC_FIELDS
            and not field.is_hide_blacklist_kanban_view
            and (
                not is_whitelist
                or (
                    is_whitelist
                    and field.is_show_whitelist_kanban_view
                )
            )
        )
        self._generate_kanban_views_models(
            model_id,
            model_created_fields_kanban,
            model_id.m2o_module,
            dct_value_to_create,
        )
        lst_view_generated.append("kanban")

    if model_id in o2m_models_view_search:
        is_whitelist = any(
            [
                a.is_show_whitelist_search_view
                for b in model_id
                for a in b.field_id
            ]
        )
        # model_created_fields_search = list(
        #     filter(
        #         lambda x: x.name not in MAGIC_FIELDS
        #                   and not x.is_hide_blacklist_search_view
        #                   and (
        #                           not is_whitelist
        #                           or (is_whitelist and x.is_show_whitelist_search_view)
        #                   ),
        #         [a for a in model_id.field_id],
        #     )
        # )
        model_created_fields_search = model_id.field_id.filtered(
            lambda field: field.name not in MAGIC_FIELDS
            and not field.is_hide_blacklist_search_view
            and (
                not is_whitelist
                or (
                    is_whitelist
                    and field.is_show_whitelist_search_view
                )
            )
        )
        self._generate_search_views_models(
            model_id,
            model_created_fields_search,
            model_id.m2o_module,
            dct_value_to_create,
        )
        lst_view_generated.append("search")

    if model_id in o2m_models_view_pivot:
        is_whitelist = any(
            [
                a.is_show_whitelist_pivot_view
                for b in model_id
                for a in b.field_id
            ]
        )
        # model_created_fields_pivot = list(
        #     filter(
        #         lambda x: x.name not in MAGIC_FIELDS
        #                   and not x.is_hide_blacklist_pivot_view
        #                   and (
        #                           not is_whitelist
        #                           or (is_whitelist and x.is_show_whitelist_pivot_view)
        #                   ),
        #         [a for a in model_id.field_id],
        #     )
        # )
        model_created_fields_pivot = model_id.field_id.filtered(
            lambda field: field.name not in MAGIC_FIELDS
            and not field.is_hide_blacklist_pivot_view
            and (
                not is_whitelist
                or (
                    is_whitelist and field.is_show_whitelist_pivot_view
                )
            )
        )
        self._generate_pivot_views_models(
            model_id,
            model_created_fields_pivot,
            model_id.m2o_module,
            dct_value_to_create,
        )
        lst_view_generated.append("pivot")

    if model_id in o2m_models_view_calendar:
        is_whitelist = any(
            [
                a.is_show_whitelist_calendar_view
                for b in model_id
                for a in b.field_id
            ]
        )
        # model_created_fields_calendar = list(
        #     filter(
        #         lambda x: x.name not in MAGIC_FIELDS
        #                   and not x.is_hide_blacklist_calendar_view
        #                   and (
        #                           not is_whitelist
        #                           or (is_whitelist and x.is_show_whitelist_calendar_view)
        #                   ),
        #         [a for a in model_id.field_id],
        #     )
        # )
        model_created_fields_calendar = model_id.field_id.filtered(
            lambda field: field.name not in MAGIC_FIELDS
            and not field.is_hide_blacklist_calendar_view
            and (
                not is_whitelist
                or (
                    is_whitelist
                    and field.is_show_whitelist_calendar_view
                )
            )
        )
        has_start_date = any(
            [
                a.is_date_start_view
                for a in model_created_fields_calendar
            ]
        )
        if has_start_date:
            self._generate_calendar_views_models(
                model_id,
                model_created_fields_calendar,
                model_id.m2o_module,
                dct_value_to_create,
            )
            lst_view_generated.append("calendar")

    if model_id in o2m_models_view_graph:
        is_whitelist = any(
            [
                a.is_show_whitelist_graph_view
                for b in model_id
                for a in b.field_id
            ]
        )
        # model_created_fields_graph = list(
        #     filter(
        #         lambda x: x.name not in MAGIC_FIELDS
        #                   and not x.is_hide_blacklist_graph_view
        #                   and (
        #                           not is_whitelist
        #                           or (is_whitelist and x.is_show_whitelist_graph_view)
        #                   ),
        #         [a for a in model_id.field_id],
        #     )
        # )
        model_created_fields_graph = model_id.field_id.filtered(
            lambda field: field.name not in MAGIC_FIELDS
            and not field.is_hide_blacklist_graph_view
            and (
                not is_whitelist
                or (
                    is_whitelist and field.is_show_whitelist_graph_view
                )
            )
        )
        self._generate_graph_views_models(
            model_id,
            model_created_fields_graph,
            model_id.m2o_module,
            dct_value_to_create,
        )
        lst_view_generated.append("graph")

    if model_id in o2m_models_view_timeline:
        model_created_fields_timeline = model_id.field_id.filtered(
            lambda field: field.name not in MAGIC_FIELDS
            and field.ttype in ("date", "datetime")
            and (field.is_date_start_view or field.is_date_end_view)
        )

        if model_created_fields_timeline:
            self._generate_timeline_views_models(
                model_id,
                model_created_fields_timeline,
                model_id.m2o_module,
                dct_value_to_create,
            )
            lst_view_generated.append("timeline")

    if model_id in o2m_models_view_diagram:
        lst_view_generated.append("diagram")

    # Menu and action_windows
    self._generate_menu(
        model_id,
        model_id.m2o_module,
        lst_view_generated,
        lst_model_id,
    )

# Need form to be created before create diagram
for model_id in o2m_models_view_diagram:
    self._generate_diagram_views_models(
        model_id,
        model_id.m2o_module,
        dct_value_to_create,
    )

# for model_id in o2m_models_view_form:
#     print(model_id)
# model_created_fields = model_id.field_id.filtered(lambda field: field.name not in MAGIC_FIELDS).mapped(
#     'name')
#

for model_id in self.code_generator_id.o2m_models:
    self._generate_model_access(model_id)

# after_time = time.process_time()
# _logger.info(
#     "DEBUG time execution generic_generate_view"
#     f" {after_time - before_time}"
# )
return True""",
                    "name": "generic_generate_view",
                    "decorator": "@api.multi",
                    "param": "self, dct_value_to_create",
                    "sequence": 2,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """for code_generator in self.code_generator_id:
    need_mail_depend = any(
        [a.enable_activity for a in code_generator.o2m_models]
    )
    if not need_mail_depend:
        continue

    code_generator.add_module_dependency("mail")""",
                    "name": "_add_dependencies",
                    "param": "self",
                    "sequence": 3,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """return model_created_fields_tree""",
                    "name": "_update_model_field_tree_view",
                    "param": "self, model_created_fields_tree",
                    "sequence": 4,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """model_name = model_created.model
model_name_str = model_name.replace(".", "_")

lst_field_to_remove = ("active",)

has_sequence = False
for field_id in model_created_fields:
    if field_id.code_generator_tree_view_sequence >= 0:
        has_sequence = True
        break

if not has_sequence:
    lst_order_field_id = [[], [], []]
    # code_generator_tree_view_sequence all -1, default value
    # Move rec_name in beginning
    # Move one2many at the end
    for field_id in model_created_fields:
        if field_id.name == model_created.rec_name:
            # TODO write this value
            lst_order_field_id[0].append(field_id.id)
            # field_id.code_generator_tree_view_sequence = 0
        elif field_id.ttype == "one2many":
            lst_order_field_id[2].append(field_id.id)
            # field_id.code_generator_tree_view_sequence = 2
        else:
            lst_order_field_id[1].append(field_id.id)
            # field_id.code_generator_tree_view_sequence = 1
    new_lst_order_field_id = (
        lst_order_field_id[0]
        + lst_order_field_id[1]
        + lst_order_field_id[2]
    )
    # TODO this can slow, can we accumulate this data for the end?
    # field_sorted_sequence_0 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[0]
    # )
    # field_sorted_sequence_1 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[1]
    # )
    # field_sorted_sequence_2 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[2]
    # )
    # field_sorted_sequence_0.write(
    #     {"code_generator_form_simple_view_sequence": 0}
    # )
    # field_sorted_sequence_1.write(
    #     {"code_generator_form_simple_view_sequence": 1}
    # )
    # field_sorted_sequence_2.write(
    #     {"code_generator_form_simple_view_sequence": 2}
    # )
    # field_sorted_ids = (
    #     field_sorted_sequence_0
    #     + field_sorted_sequence_1
    #     + field_sorted_sequence_2
    # )
    lst_field_sorted = (
        self.env["ir.model.fields"]
        .browse(new_lst_order_field_id)
        .filtered(
            lambda field: not field.ignore_on_code_generator_writer
        )
    )
else:
    # Use tree view sequence, or generic sequence
    lst_field_sorted = model_created_fields.filtered(
        lambda field: not field.ignore_on_code_generator_writer
    ).sorted(lambda field: field.code_generator_tree_view_sequence)

# lst_field = [E.field({"name": a.name}) for a in model_created_fields]
lst_field = []
for field_id in lst_field_sorted:
    if field_id.name in lst_field_to_remove:
        continue
    # TODO validate code_generator_tree_view_sequence is supported
    # if a.code_generator_tree_view_sequence >= 0
    dct_value = {"name": field_id.name}
    if field_id.force_widget:
        dct_value["widget"] = field_id.force_widget
    dct_value = dict(sorted(dct_value.items(), key=lambda kv: kv[0]))
    lst_field.append(E.field(dct_value))
arch_xml = E.tree(
    {
        # TODO enable this when missing form
        # "editable": "top",
    },
    *lst_field,
)
str_arch = ET.tostring(arch_xml, pretty_print=True)
str_arch = b'<?xml version="1.0"?>\\n' + str_arch
# ir_ui_view_value = {
#     "name": f"{model_name_str}_tree",
#     "type": "tree",
#     "model": model_name,
#     "arch": str_arch,
#     "m2o_model": model_created.id,
# }
# dct_value_to_create["ir.ui.view"].append(ir_ui_view_value)
view_value = self.env["ir.ui.view"].search(
    [
        ("name", "=", f"{model_name_str}_tree"),
        ("type", "=", "tree"),
        ("model", "=", model_name),
        # ("arch", "=", str_arch),
        ("m2o_model", "=", model_created.id),
    ]
)
if not view_value:
    view_value = self.env["ir.ui.view"].create(
        {
            "name": f"{model_name_str}_tree",
            "type": "tree",
            "model": model_name,
            "arch": str_arch,
            "m2o_model": model_created.id,
        }
    )

return view_value""",
                    "name": "_generate_list_views_models",
                    "param": (
                        "self, model_created, model_created_fields, module,"
                        " dct_value_to_create"
                    ),
                    "sequence": 5,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """model_name = model_created.model
model_name_str = model_name.replace(".", "_")
lst_item_sheet = []
key = "geo_"

lst_field_to_transform_button_box = ("active",)

has_sequence = False
for field_id in model_created_fields:
    if field_id.code_generator_form_simple_view_sequence >= 0:
        has_sequence = True
        break

if not has_sequence:
    lst_order_field_id = [[], [], []]
    # code_generator_form_simple_view_sequence all -1, default value
    # Move rec_name in beginning
    # Move one2many at the end
    for field_id in model_created_fields:
        if field_id.name == model_created.rec_name:
            # TODO write this value
            lst_order_field_id[0].append(field_id.id)
            # field_id.code_generator_form_simple_view_sequence = 0
        elif field_id.ttype == "one2many":
            lst_order_field_id[2].append(field_id.id)
            # field_id.code_generator_form_simple_view_sequence = 2
        else:
            lst_order_field_id[1].append(field_id.id)
            # field_id.code_generator_form_simple_view_sequence = 1
    new_lst_order_field_id = (
        lst_order_field_id[0]
        + lst_order_field_id[1]
        + lst_order_field_id[2]
    )

    # TODO this can slow, can we accumulate this data for the end?
    # field_sorted_sequence_0 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[0]
    # )
    # field_sorted_sequence_1 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[1]
    # )
    # field_sorted_sequence_2 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[2]
    # )
    # field_sorted_sequence_0.write(
    #     {"code_generator_form_simple_view_sequence": 0}
    # )
    # field_sorted_sequence_1.write(
    #     {"code_generator_form_simple_view_sequence": 1}
    # )
    # field_sorted_sequence_2.write(
    #     {"code_generator_form_simple_view_sequence": 2}
    # )
    # field_sorted_ids = (
    #     field_sorted_sequence_0
    #     + field_sorted_sequence_1
    #     + field_sorted_sequence_2
    # )
    field_sorted_ids = (
        self.env["ir.model.fields"]
        .browse(new_lst_order_field_id)
        .filtered(
            lambda field: not field.ignore_on_code_generator_writer
        )
    )
else:
    field_sorted_ids = model_created_fields.filtered(
        lambda field: not field.ignore_on_code_generator_writer
    ).sorted(
        lambda x: x.code_generator_form_simple_view_sequence,
    )

lst_button_box = []
for field_id in field_sorted_ids:
    if field_id.name in lst_field_to_transform_button_box:
        item_field = E.field(
            {"name": field_id.name, "widget": "boolean_button"}
        )
        item_button = E.button(
            {
                "class": "oe_stat_button",
                "icon": "fa-archive",
                "name": "toggle_active",
                "type": "object",
            },
            item_field,
        )
        lst_button_box.append(item_button)

if lst_button_box:
    item = E.div(
        {"class": "oe_button_box", "name": "button_box"},
        *lst_button_box,
    )
    lst_item_sheet.append(item)

for field_id in field_sorted_ids:
    if field_id.name in lst_field_to_transform_button_box:
        continue
    lst_value = []
    value = {"name": field_id.name}
    lst_value.append(value)

    if field_id.force_widget:
        if field_id.force_widget != "link_button":
            # TODO add a configuration to force edible mode, if not editable, choose widget = link button
            # special case, link button is readonly in form,
            value["widget"] = field_id.force_widget
    elif key in field_id.ttype:
        value["widget"] = "geo_edit_map"
        # value["attrs"] = "{'invisible': [('type', '!=', '"f"{model[len(key):]}')]""}"
    # lst_field.append(value)
    lst_item_sheet.append(E.group({}, E.field(value)))

lst_item_form = [E.sheet({}, *lst_item_sheet)]

if model_created.enable_activity:
    xml_activity = E.div(
        {"class": "oe_chatter"},
        E.field(
            {
                # "groups": "base.group_user",
                # "help": "",
                "name": "message_follower_ids",
                "widget": "mail_followers",
            }
        ),
        E.field({"name": "activity_ids", "widget": "mail_activity"}),
        E.field(
            {
                "name": "message_ids",
                "options": "{'post_refresh': 'recipients'}",
                "widget": "mail_thread",
            }
        ),
    )
    lst_item_form.append(xml_activity)

arch_xml = E.form(
    {
        "string": "Titre",
    },
    *lst_item_form,
)
str_arch = ET.tostring(arch_xml, pretty_print=True)
str_arch = b'<?xml version="1.0"?>\\n' + str_arch
# ir_ui_view_value = {
#     "name": f"{model_name_str}_form",
#     "type": "form",
#     "model": model_name,
#     "arch": str_arch,
#     "m2o_model": model_created.id,
# }
# dct_value_to_create["ir.ui.view"].append(ir_ui_view_value)
view_value = self.env["ir.ui.view"].search(
    [
        ("name", "=", f"{model_name_str}_form"),
        ("type", "=", "form"),
        ("model", "=", model_name),
        # ("arch", "=", str_arch),
        ("m2o_model", "=", model_created.id),
    ]
)
if not view_value:
    view_value = self.env["ir.ui.view"].create(
        {
            "name": f"{model_name_str}_form",
            "type": "form",
            "model": model_name,
            "arch": str_arch,
            "m2o_model": model_created.id,
        }
    )

    model_data_value = self.env["ir.model.data"].create(
        {
            "name": f"{model_name_str}_view_form",
            "model": "ir.ui.view",
            "module": module.name,
            "res_id": view_value.id,
            "noupdate": True,  # If it's False, target record (res_id) will be removed while module update
        }
    )

return view_value""",
                    "name": "_generate_form_views_models",
                    "param": (
                        "self, model_created, model_created_fields, module,"
                        " dct_value_to_create"
                    ),
                    "sequence": 6,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """model_name = model_created.model
model_name_str = model_name.replace(".", "_")

lst_field_to_remove = ("active",)

has_sequence = False
for field_id in model_created_fields:
    if field_id.code_generator_kanban_view_sequence >= 0:
        has_sequence = True
        break

if not has_sequence:
    lst_order_field_id = [[], [], []]
    # code_generator_kanban_view_sequence all -1, default value
    # Move rec_name in beginning
    # Move one2many at the end
    for field_id in model_created_fields:
        if field_id.name == model_created.rec_name:
            # TODO write this value
            lst_order_field_id[0].append(field_id.id)
            # field_id.code_generator_kanban_view_sequence = 0
        elif field_id.ttype == "one2many":
            lst_order_field_id[2].append(field_id.id)
            # field_id.code_generator_kanban_view_sequence = 2
        else:
            lst_order_field_id[1].append(field_id.id)
            # field_id.code_generator_kanban_view_sequence = 1
    new_lst_order_field_id = (
        lst_order_field_id[0]
        + lst_order_field_id[1]
        + lst_order_field_id[2]
    )
    # TODO this can slow, can we accumulate this data for the end?
    # field_sorted_sequence_0 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[0]
    # )
    # field_sorted_sequence_1 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[1]
    # )
    # field_sorted_sequence_2 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[2]
    # )
    # field_sorted_sequence_0.write(
    #     {"code_generator_form_simple_view_sequence": 0}
    # )
    # field_sorted_sequence_1.write(
    #     {"code_generator_form_simple_view_sequence": 1}
    # )
    # field_sorted_sequence_2.write(
    #     {"code_generator_form_simple_view_sequence": 2}
    # )
    # field_sorted_ids = (
    #     field_sorted_sequence_0
    #     + field_sorted_sequence_1
    #     + field_sorted_sequence_2
    # )
    lst_field_sorted = (
        self.env["ir.model.fields"]
        .browse(new_lst_order_field_id)
        .filtered(
            lambda field: not field.ignore_on_code_generator_writer
        )
    )
else:
    # Use kanban view sequence, or generic sequence
    lst_field_sorted = model_created_fields.filtered(
        lambda field: not field.ignore_on_code_generator_writer
    ).sorted(lambda field: field.code_generator_kanban_view_sequence)

# lst_field = [E.field({"name": a.name}) for a in model_created_fields]
lst_field = []
lst_field_template = []
for field_id in lst_field_sorted:
    if field_id.name in lst_field_to_remove:
        continue
    # TODO validate code_generator_kanban_view_sequence is supported
    # if a.code_generator_kanban_view_sequence >= 0
    dct_value = {"name": field_id.name}
    if field_id.force_widget:
        dct_value["widget"] = field_id.force_widget
    dct_value = dict(sorted(dct_value.items(), key=lambda kv: kv[0]))
    lst_field.append(E.field(dct_value))

    if field_id.ttype == "boolean":
        # TODO detect type success/danger or another type of boolean
        dct_templates_value = E.li(
            {
                "class": "text-success float-right mb4",
                "t-if": f"record.{field_id.name}.raw_value",
            },
            E.i(
                {
                    "aria-label": "Ok",
                    "class": "fa fa-circle",
                    "role": "img",
                    "title": "Ok",
                }
            ),
        )
        lst_field_template.append(dct_templates_value)

        dct_templates_value = E.li(
            {
                "class": "text-danger float-right mb4",
                "t-if": f"!record.{field_id.name}.raw_value",
            },
            E.i(
                {
                    "aria-label": "Invalid",
                    "class": "fa fa-circle",
                    "role": "img",
                    "title": "Invalid",
                }
            ),
        )
        lst_field_template.append(dct_templates_value)
    else:
        dct_templates_value = E.li(
            {"class": "mb4"},
            E.strong(E.field({"name": field_id.name})),
        )
        lst_field_template.append(dct_templates_value)

template_item = E.templates(
    {},
    E.t(
        {"t-name": "kanban-box"},
        E.div(
            {"t-attf-class": "oe_kanban_global_click"},
            E.div(
                {"class": "oe_kanban_details"},
                E.ul({}, *lst_field_template),
            ),
        ),
    ),
)
lst_item_kanban = lst_field + [template_item]
arch_xml = E.kanban(
    {
        "class": "o_kanban_mobile",
    },
    *lst_item_kanban,
)
str_arch = ET.tostring(arch_xml, pretty_print=True)
str_arch = b'<?xml version="1.0"?>\\n' + str_arch
# ir_ui_view_value = {
#     "name": f"{model_name_str}_kanban",
#     "type": "kanban",
#     "model": model_name,
#     "arch": str_arch,
#     "m2o_model": model_created.id,
# }
# dct_value_to_create["ir.ui.view"].append(ir_ui_view_value)
view_value = self.env["ir.ui.view"].search(
    [
        ("name", "=", f"{model_name_str}_kanban"),
        ("type", "=", "kanban"),
        ("model", "=", model_name),
        # ("arch", "=", str_arch),
        ("m2o_model", "=", model_created.id),
    ]
)
if not view_value:
    view_value = self.env["ir.ui.view"].create(
        {
            "name": f"{model_name_str}_kanban",
            "type": "kanban",
            "model": model_name,
            "arch": str_arch,
            "m2o_model": model_created.id,
        }
    )

return view_value""",
                    "name": "_generate_kanban_views_models",
                    "param": (
                        "self, model_created, model_created_fields, module,"
                        " dct_value_to_create"
                    ),
                    "sequence": 7,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """model_name = model_created.model
model_name_str = model_name.replace(".", "_")
model_name_display_str = model_name_str.replace("_", " ").capitalize()

lst_field_to_remove = ("active",)

has_sequence = False
for field_id in model_created_fields:
    if field_id.code_generator_search_view_sequence >= 0:
        has_sequence = True
        break

if not has_sequence:
    lst_order_field_id = [[], [], []]
    # code_generator_search_view_sequence all -1, default value
    # Move rec_name in beginning
    # Move one2many at the end
    for field_id in model_created_fields:
        if field_id.name == model_created.rec_name:
            # TODO write this value
            lst_order_field_id[0].append(field_id.id)
            # field_id.code_generator_search_view_sequence = 0
        elif field_id.ttype == "one2many":
            lst_order_field_id[2].append(field_id.id)
            # field_id.code_generator_search_view_sequence = 2
        else:
            lst_order_field_id[1].append(field_id.id)
            # field_id.code_generator_search_view_sequence = 1
    new_lst_order_field_id = (
        lst_order_field_id[0]
        + lst_order_field_id[1]
        + lst_order_field_id[2]
    )
    # TODO this can slow, can we accumulate this data for the end?
    # field_sorted_sequence_0 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[0]
    # )
    # field_sorted_sequence_1 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[1]
    # )
    # field_sorted_sequence_2 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[2]
    # )
    # field_sorted_sequence_0.write(
    #     {"code_generator_form_simple_view_sequence": 0}
    # )
    # field_sorted_sequence_1.write(
    #     {"code_generator_form_simple_view_sequence": 1}
    # )
    # field_sorted_sequence_2.write(
    #     {"code_generator_form_simple_view_sequence": 2}
    # )
    # field_sorted_ids = (
    #     field_sorted_sequence_0
    #     + field_sorted_sequence_1
    #     + field_sorted_sequence_2
    # )
    lst_field_sorted = (
        self.env["ir.model.fields"]
        .browse(new_lst_order_field_id)
        .filtered(
            lambda field: not field.ignore_on_code_generator_writer
        )
    )
else:
    # Use search view sequence, or generic sequence
    lst_field_sorted = model_created_fields.filtered(
        lambda field: not field.ignore_on_code_generator_writer
    ).sorted(lambda field: field.code_generator_search_view_sequence)

# lst_field = [E.field({"name": a.name}) for a in model_created_fields]
lst_field = []
lst_field_filter = []
lst_item_search = []
for field_id in lst_field_sorted:
    if field_id.name in lst_field_to_remove:
        # Add inactive
        dct_templates_value = E.filter(
            {
                "domain": f"[('{field_id.name}','=',False)]",
                "name": "Inactive",
                "string": f"Inactive {model_name_display_str}",
            }
        )
        lst_field_filter.append(dct_templates_value)
        continue
    # TODO validate code_generator_search_view_sequence is supported
    # if a.code_generator_search_view_sequence >= 0

    if field_id.ttype == "boolean":
        dct_templates_value = E.filter(
            {
                "domain": f"[('{field_id.name}','=',True)]",
                "name": field_id.name,
                "string": field_id.field_description,
            }
        )
        lst_field_filter.append(dct_templates_value)
    else:
        dct_templates_value = E.filter(
            {
                "domain": f"[('{field_id.name}','!=',False)]",
                "name": field_id.name,
                "string": field_id.field_description,
            }
        )
        lst_field_filter.append(dct_templates_value)

lst_item_search = lst_field + lst_field_filter
arch_xml = E.search(
    {
        "string": model_name_display_str,
    },
    *lst_item_search,
)
str_arch = ET.tostring(arch_xml, pretty_print=True)
str_arch = b'<?xml version="1.0"?>\\n' + str_arch
# ir_ui_view_value = {
#     "name": f"{model_name_str}_search",
#     "type": "search",
#     "model": model_name,
#     "arch": str_arch,
#     "m2o_model": model_created.id,
# }
# dct_value_to_create["ir.ui.view"].append(ir_ui_view_value)
view_value = self.env["ir.ui.view"].search(
    [
        ("name", "=", f"{model_name_str}_search"),
        ("type", "=", "search"),
        ("model", "=", model_name),
        # ("arch", "=", str_arch),
        ("m2o_model", "=", model_created.id),
    ]
)
if not view_value:
    view_value = self.env["ir.ui.view"].create(
        {
            "name": f"{model_name_str}_search",
            "type": "search",
            "model": model_name,
            "arch": str_arch,
            "m2o_model": model_created.id,
        }
    )

return view_value""",
                    "name": "_generate_search_views_models",
                    "param": (
                        "self, model_created, model_created_fields, module,"
                        " dct_value_to_create"
                    ),
                    "sequence": 8,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """model_name = model_created.model
model_name_str = model_name.replace(".", "_")
model_name_display_str = model_name_str.replace("_", " ").capitalize()

lst_field_to_remove = ("active",)

has_sequence = False
for field_id in model_created_fields:
    if field_id.code_generator_pivot_view_sequence >= 0:
        has_sequence = True
        break

if not has_sequence:
    lst_order_field_id = [[], [], []]
    # code_generator_pivot_view_sequence all -1, default value
    # Move rec_name in beginning
    # Move one2many at the end
    for field_id in model_created_fields:
        if field_id.name == model_created.rec_name:
            # TODO write this value
            lst_order_field_id[0].append(field_id.id)
            # field_id.code_generator_pivot_view_sequence = 0
        elif field_id.ttype == "one2many":
            lst_order_field_id[2].append(field_id.id)
            # field_id.code_generator_pivot_view_sequence = 2
        else:
            lst_order_field_id[1].append(field_id.id)
            # field_id.code_generator_pivot_view_sequence = 1
    new_lst_order_field_id = (
        lst_order_field_id[0]
        + lst_order_field_id[1]
        + lst_order_field_id[2]
    )
    # TODO this can slow, can we accumulate this data for the end?
    # field_sorted_sequence_0 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[0]
    # )
    # field_sorted_sequence_1 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[1]
    # )
    # field_sorted_sequence_2 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[2]
    # )
    # field_sorted_sequence_0.write(
    #     {"code_generator_form_simple_view_sequence": 0}
    # )
    # field_sorted_sequence_1.write(
    #     {"code_generator_form_simple_view_sequence": 1}
    # )
    # field_sorted_sequence_2.write(
    #     {"code_generator_form_simple_view_sequence": 2}
    # )
    # field_sorted_ids = (
    #     field_sorted_sequence_0
    #     + field_sorted_sequence_1
    #     + field_sorted_sequence_2
    # )
    lst_field_sorted = (
        self.env["ir.model.fields"]
        .browse(new_lst_order_field_id)
        .filtered(
            lambda field: not field.ignore_on_code_generator_writer
            and field.ttype not in ("many2many", "one2many", "binary")
        )
    )
else:
    # Use pivot view sequence, or generic sequence
    lst_field_sorted = model_created_fields.filtered(
        lambda field: not field.ignore_on_code_generator_writer
        and field.ttype not in ("many2many", "one2many", "binary")
    ).sorted(lambda field: field.code_generator_pivot_view_sequence)

# lst_field = [E.field({"name": a.name}) for a in model_created_fields]
lst_field = []
for field_id in lst_field_sorted:
    if field_id.name in lst_field_to_remove:
        continue
    # TODO validate code_generator_pivot_view_sequence is supported
    # if a.code_generator_pivot_view_sequence >= 0

    # TODO detect field_type col, when it's a date?
    if model_created.rec_name == field_id.name:
        field_type = "row"
    elif field_id.ttype in ("integer", "float"):
        field_type = "measure"
    else:
        field_type = "row"

    dct_templates_value = E.field(
        {
            "name": field_id.name,
            "type": field_type,
        }
    )
    lst_field.append(dct_templates_value)

lst_item_pivot = lst_field
arch_xml = E.pivot(
    {
        "string": model_name_display_str,
    },
    *lst_item_pivot,
)
str_arch = ET.tostring(arch_xml, pretty_print=True)
str_arch = b'<?xml version="1.0"?>\\n' + str_arch
# ir_ui_view_value = {
#     "name": f"{model_name_str}_pivot",
#     "type": "pivot",
#     "model": model_name,
#     "arch": str_arch,
#     "m2o_model": model_created.id,
# }
# dct_value_to_create["ir.ui.view"].append(ir_ui_view_value)
view_value = self.env["ir.ui.view"].search(
    [
        ("name", "=", f"{model_name_str}_pivot"),
        ("type", "=", "pivot"),
        ("model", "=", model_name),
        # ("arch", "=", str_arch),
        ("m2o_model", "=", model_created.id),
    ]
)
if not view_value:
    view_value = self.env["ir.ui.view"].create(
        {
            "name": f"{model_name_str}_pivot",
            "type": "pivot",
            "model": model_name,
            "arch": str_arch,
            "m2o_model": model_created.id,
        }
    )

return view_value""",
                    "name": "_generate_pivot_views_models",
                    "param": (
                        "self, model_created, model_created_fields, module,"
                        " dct_value_to_create"
                    ),
                    "sequence": 9,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """model_name = model_created.model
model_name_str = model_name.replace(".", "_")
model_name_display_str = model_name_str.replace("_", " ").capitalize()

lst_field_to_remove = ("active",)

has_sequence = False
for field_id in model_created_fields:
    if field_id.code_generator_calendar_view_sequence >= 0:
        has_sequence = True
        break

if not has_sequence:
    lst_order_field_id = [[], [], []]
    # code_generator_calendar_view_sequence all -1, default value
    # Move rec_name in beginning
    # Move one2many at the end
    for field_id in model_created_fields:
        if field_id.name == model_created.rec_name:
            # TODO write this value
            lst_order_field_id[0].append(field_id.id)
            # field_id.code_generator_calendar_view_sequence = 0
        elif field_id.ttype == "one2many":
            lst_order_field_id[2].append(field_id.id)
            # field_id.code_generator_calendar_view_sequence = 2
        else:
            lst_order_field_id[1].append(field_id.id)
            # field_id.code_generator_calendar_view_sequence = 1
    new_lst_order_field_id = (
        lst_order_field_id[0]
        + lst_order_field_id[1]
        + lst_order_field_id[2]
    )
    # TODO this can slow, can we accumulate this data for the end?
    # field_sorted_sequence_0 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[0]
    # )
    # field_sorted_sequence_1 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[1]
    # )
    # field_sorted_sequence_2 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[2]
    # )
    # field_sorted_sequence_0.write(
    #     {"code_generator_form_simple_view_sequence": 0}
    # )
    # field_sorted_sequence_1.write(
    #     {"code_generator_form_simple_view_sequence": 1}
    # )
    # field_sorted_sequence_2.write(
    #     {"code_generator_form_simple_view_sequence": 2}
    # )
    # field_sorted_ids = (
    #     field_sorted_sequence_0
    #     + field_sorted_sequence_1
    #     + field_sorted_sequence_2
    # )
    lst_field_sorted = (
        self.env["ir.model.fields"]
        .browse(new_lst_order_field_id)
        .filtered(
            lambda field: not field.ignore_on_code_generator_writer
        )
    )
else:
    # Use calendar view sequence, or generic sequence
    lst_field_sorted = model_created_fields.filtered(
        lambda field: not field.ignore_on_code_generator_writer
    ).sorted(lambda field: field.code_generator_calendar_view_sequence)

# lst_field = [E.field({"name": a.name}) for a in model_created_fields]
lst_field = []
date_start = None
for field_id in lst_field_sorted:
    if field_id.name in lst_field_to_remove:
        continue
    # TODO validate code_generator_calendar_view_sequence is supported
    # if a.code_generator_calendar_view_sequence >= 0

    dct_value = {"name": field_id.name}
    if field_id.force_widget:
        dct_value["widget"] = field_id.force_widget

    if field_id.is_date_start_view:
        if date_start:
            _logger.warning(
                f"Double date_start in model {model_name}."
            )
        date_start = field_id

    dct_templates_value = E.field(dct_value)
    lst_field.append(dct_templates_value)

if not date_start:
    _logger.error(
        f"Missing date_start in view calendar for model {model_name}."
    )
    return

lst_item_calendar = lst_field
arch_xml = E.calendar(
    {
        "color": model_created.rec_name,
        "date_start": date_start.name,
        "string": model_name_display_str,
    },
    *lst_item_calendar,
)
str_arch = ET.tostring(arch_xml, pretty_print=True)
str_arch = b'<?xml version="1.0"?>\\n' + str_arch
# ir_ui_view_value = {
#     "name": f"{model_name_str}_calendar",
#     "type": "calendar",
#     "model": model_name,
#     "arch": str_arch,
#     "m2o_model": model_created.id,
# }
# dct_value_to_create["ir.ui.view"].append(ir_ui_view_value)
view_value = self.env["ir.ui.view"].search(
    [
        ("name", "=", f"{model_name_str}_calendar"),
        ("type", "=", "calendar"),
        ("model", "=", model_name),
        # ("arch", "=", str_arch),
        ("m2o_model", "=", model_created.id),
    ]
)
if not view_value:
    view_value = self.env["ir.ui.view"].create(
        {
            "name": f"{model_name_str}_calendar",
            "type": "calendar",
            "model": model_name,
            "arch": str_arch,
            "m2o_model": model_created.id,
        }
    )

return view_value""",
                    "name": "_generate_calendar_views_models",
                    "param": (
                        "self, model_created, model_created_fields, module,"
                        " dct_value_to_create"
                    ),
                    "sequence": 10,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """model_name = model_created.model
model_name_str = model_name.replace(".", "_")
model_name_display_str = model_name_str.replace("_", " ").capitalize()

lst_field_to_remove = ("active",)

has_sequence = False
for field_id in model_created_fields:
    if field_id.code_generator_graph_view_sequence >= 0:
        has_sequence = True
        break

if not has_sequence:
    lst_order_field_id = [[], [], []]
    # code_generator_graph_view_sequence all -1, default value
    # Move rec_name in beginning
    # Move one2many at the end
    for field_id in model_created_fields:
        if field_id.name == model_created.rec_name:
            # TODO write this value
            lst_order_field_id[0].append(field_id.id)
            # field_id.code_generator_graph_view_sequence = 0
        elif field_id.ttype == "one2many":
            lst_order_field_id[2].append(field_id.id)
            # field_id.code_generator_graph_view_sequence = 2
        else:
            lst_order_field_id[1].append(field_id.id)
            # field_id.code_generator_graph_view_sequence = 1
    new_lst_order_field_id = (
        lst_order_field_id[0]
        + lst_order_field_id[1]
        + lst_order_field_id[2]
    )
    # TODO this can slow, can we accumulate this data for the end?
    # field_sorted_sequence_0 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[0]
    # )
    # field_sorted_sequence_1 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[1]
    # )
    # field_sorted_sequence_2 = self.env["ir.model.fields"].browse(
    #     lst_order_field_id[2]
    # )
    # field_sorted_sequence_0.write(
    #     {"code_generator_form_simple_view_sequence": 0}
    # )
    # field_sorted_sequence_1.write(
    #     {"code_generator_form_simple_view_sequence": 1}
    # )
    # field_sorted_sequence_2.write(
    #     {"code_generator_form_simple_view_sequence": 2}
    # )
    # field_sorted_ids = (
    #     field_sorted_sequence_0
    #     + field_sorted_sequence_1
    #     + field_sorted_sequence_2
    # )
    lst_field_sorted = (
        self.env["ir.model.fields"]
        .browse(new_lst_order_field_id)
        .filtered(
            lambda field: not field.ignore_on_code_generator_writer
            and field.ttype not in ("many2many", "one2many")
        )
    )
else:
    # Use graph view sequence, or generic sequence
    lst_field_sorted = model_created_fields.filtered(
        lambda field: not field.ignore_on_code_generator_writer
        and field.ttype not in ("many2many", "one2many")
    ).sorted(lambda field: field.code_generator_graph_view_sequence)

# lst_field = [E.field({"name": a.name}) for a in model_created_fields]
lst_field = []
for field_id in lst_field_sorted:
    if field_id.name in lst_field_to_remove:
        continue
    # TODO validate code_generator_graph_view_sequence is supported
    # if a.code_generator_graph_view_sequence >= 0

    # TODO detect field_type col, when it's a date?
    if model_created.rec_name == field_id.name:
        field_type = "row"
    elif field_id.ttype in ("integer", "float"):
        field_type = "measure"
    else:
        field_type = "row"

    dct_templates_value = E.field(
        {
            "name": field_id.name,
            "type": field_type,
        }
    )
    lst_field.append(dct_templates_value)

lst_item_graph = lst_field
arch_xml = E.graph(
    {
        "string": model_name_display_str,
    },
    *lst_item_graph,
)
str_arch = ET.tostring(arch_xml, pretty_print=True)
str_arch = b'<?xml version="1.0"?>\\n' + str_arch
# ir_ui_view_value = {
#     "name": f"{model_name_str}_graph",
#     "type": "graph",
#     "model": model_name,
#     "arch": str_arch,
#     "m2o_model": model_created.id,
# }
# dct_value_to_create["ir.ui.view"].append(ir_ui_view_value)
view_value = self.env["ir.ui.view"].search(
    [
        ("name", "=", f"{model_name_str}_graph"),
        ("type", "=", "graph"),
        ("model", "=", model_name),
        # ("arch", "=", str_arch),
        ("m2o_model", "=", model_created.id),
    ]
)
if not view_value:
    view_value = self.env["ir.ui.view"].create(
        {
            "name": f"{model_name_str}_graph",
            "type": "graph",
            "model": model_name,
            "arch": str_arch,
            "m2o_model": model_created.id,
        }
    )

return view_value""",
                    "name": "_generate_graph_views_models",
                    "param": (
                        "self, model_created, model_created_fields, module,"
                        " dct_value_to_create"
                    ),
                    "sequence": 11,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """model_name = model_created.model
model_name_str = model_name.replace(".", "_")
model_name_display_str = model_name_str.replace("_", " ").capitalize()

start_date = None
end_date = None
for field_id in model_created_fields:
    if field_id.is_date_start_view and not start_date:
        start_date = field_id
    if field_id.is_date_end_view and not end_date:
        end_date = field_id

if not start_date:
    _logger.warning(
        "Missing start date field, need word start in name."
    )
if not end_date:
    _logger.warning("Missing end date field, need word start in name.")
if not start_date or not end_date:
    return

# lst_item_timeline = lst_field
arch_xml = E.timeline(
    {
        "date_start": start_date.name,
        "date_stop": end_date.name,
        "default_group_by": model_created.rec_name,
        "event_open_popup": "True",
        "string": model_name_display_str,
    }
)
str_arch = ET.tostring(arch_xml, pretty_print=True)
str_arch = b'<?xml version="1.0"?>\\n' + str_arch
# ir_ui_view_value = {
#     "name": f"{model_name_str}_timeline",
#     "type": "timeline",
#     "model": model_name,
#     "arch": str_arch,
#     "m2o_model": model_created.id,
# }
# dct_value_to_create["ir.ui.view"].append(ir_ui_view_value)
view_value = self.env["ir.ui.view"].search(
    [
        ("name", "=", f"{model_name_str}_timeline"),
        ("type", "=", "timeline"),
        ("model", "=", model_name),
        # ("arch", "=", str_arch),
        ("m2o_model", "=", model_created.id),
    ]
)
if not view_value:
    view_value = self.env["ir.ui.view"].create(
        {
            "name": f"{model_name_str}_timeline",
            "type": "timeline",
            "model": model_name,
            "arch": str_arch,
            "m2o_model": model_created.id,
        }
    )

return view_value""",
                    "name": "_generate_timeline_views_models",
                    "param": (
                        "self, model_created, model_created_fields, module,"
                        " dct_value_to_create"
                    ),
                    "sequence": 12,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """model_name = model_created.model
model_name_str = model_name.replace(".", "_")
model_name_display_str = model_name_str.replace("_", " ").capitalize()

if (
    not model_created.diagram_node_object
    or not model_created.diagram_node_xpos_field
    or not model_created.diagram_node_ypos_field
    or not model_created.diagram_arrow_object
    or not model_created.diagram_arrow_src_field
    or not model_created.diagram_arrow_dst_field
):
    _logger.error(
        "Cannot create diagram view, missing field in model, check"
        " diagram_*"
    )
    return

model_node = module.env["ir.model"].search(
    [("model", "=", model_created.diagram_node_object)], limit=1
)
if not model_node:
    _logger.error(
        f"Diagram model {model_created.diagram_node_object} doesn't"
        " exist."
    )
    return
model_arrow = module.env["ir.model"].search(
    [("model", "=", model_created.diagram_arrow_object)], limit=1
)
if not model_arrow:
    _logger.error(
        f"Diagram model {model_created.diagram_arrow_object} doesn't"
        " exist."
    )
    return

lst_field_node = [E.field({"name": model_node.rec_name})]
lst_field_arrow = [
    E.field({"name": model_created.diagram_arrow_src_field}),
    E.field({"name": model_created.diagram_arrow_dst_field}),
    E.field({"name": model_arrow.rec_name}),
]

# Take first
node_form_view = module.env["ir.ui.view"].search(
    [
        ("model", "=", model_created.diagram_node_object),
        ("type", "=", "form"),
    ],
    limit=1,
)
node_xml_id = module.env["ir.model.data"].search(
    [("model", "=", "ir.ui.view"), ("res_id", "=", node_form_view.id)]
)
arrow_form_view = module.env["ir.ui.view"].search(
    [
        ("model", "=", model_created.diagram_arrow_object),
        ("type", "=", "form"),
    ],
    limit=1,
)
arrow_xml_id = module.env["ir.model.data"].search(
    [("model", "=", "ir.ui.view"), ("res_id", "=", arrow_form_view.id)]
)

arch_xml = E.diagram(
    {},
    E.node(
        {
            # "bgcolor":"",
            "form_view_ref": node_xml_id.name,
            "object": model_created.diagram_node_object,
            "shape": "rectangle:True",
            "xpos": model_created.diagram_node_xpos_field,
            "ypos": model_created.diagram_node_ypos_field,
        },
        *lst_field_node,
    ),
    E.arrow(
        {
            "destination": model_created.diagram_arrow_dst_field,
            "form_view_ref": arrow_xml_id.name,
            "label": f"['{model_arrow.rec_name}']",
            "object": model_created.diagram_arrow_object,
            "source": model_created.diagram_arrow_src_field,
        },
        *lst_field_arrow,
    ),
    E.label(
        {
            "for": "",
            "string": (
                "Caution, all modification is live. Diagram model:"
                f" {model_created.model}, node model:"
                f" {model_created.diagram_node_object} and arrow"
                f" model: {model_created.diagram_arrow_object}"
            ),
        }
    ),
)

str_arch = ET.tostring(arch_xml, pretty_print=True)
str_arch = b'<?xml version="1.0"?>\\n' + str_arch
# dct_value_to_create["ir.ui.view"].append(ir_ui_view_value)
view_value = self.env["ir.ui.view"].search(
    [
        ("name", "=", f"{model_name_str}_diagram"),
        ("type", "=", "diagram"),
        ("model", "=", model_name),
        # ("arch", "=", str_arch),
        ("m2o_model", "=", model_created.id),
    ]
)
if not view_value:
    view_value = self.env["ir.ui.view"].create(
        {
            "name": f"{model_name_str}_diagram",
            "type": "diagram",
            "model": model_name,
            "arch": str_arch,
            "m2o_model": model_created.id,
        }
    )

return view_value""",
                    "name": "_generate_diagram_views_models",
                    "param": (
                        "self, model_created, module, dct_value_to_create"
                    ),
                    "sequence": 13,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """button_attributes = {
    "name": item.action_name,
    "type": "object",
}
if item.label:
    button_attributes["string"] = item.label
if item.button_type:
    button_attributes["class"] = item.button_type
if item.icon:
    button_attributes["icon"] = item.icon

# Create method
items = self.env["code.generator.model.code"].search(
    [
        ("name", "=", item.action_name),
        ("m2o_model", "=", model_id),
        ("m2o_module", "=", self.code_generator_id.id),
    ]
)
# TODO get this list from module base
lst_ignore_code = ["toggle_active"]
if not items and item.action_name not in lst_ignore_code:
    value = {
        "code": '''\"""TODO what to run\"""
pass''',
        "name": item.action_name,
        "decorator": "@api.multi",
        "param": "self",
        "m2o_module": self.code_generator_id.id,
        "m2o_model": model_id,
        "is_wip": True,
    }
    self.env["code.generator.model.code"].create(value)
button_attributes = dict(
    sorted(button_attributes.items(), key=lambda kv: kv[0])
)
if lst_child_update:
    return E.button(button_attributes, *lst_child_update)

return E.button(button_attributes)""",
                    "name": "_generate_xml_button",
                    "param": "self, item, model_id, lst_child_update=None",
                    "sequence": 14,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": '''"""

:param item:
:param lst_child: list of item to add more in some context
:param dct_replace: need it to replace html in xml without validation
:return:
"""
dct_item = {"string": "Help"}
if item.colspan > 1:
    dct_item["colspan"] = str(item.colspan)
dct_item = dict(sorted(dct_item.items(), key=lambda kv: kv[0]))
item_xml = E.separator(dct_item)
lst_child.append(item_xml)

uid = str(uuid.uuid1())
dct_replace[uid] = item.label
item_xml = E.div({}, uid)
return item_xml''',
                    "name": "_generate_xml_html_help",
                    "decorator": "@staticmethod",
                    "param": "item, lst_child, dct_replace",
                    "sequence": 15,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """lst_child_update = [] if not lst_child else lst_child
item_xml = None
dct_item = {}
# TODO duplicate code here with function _generate_xml_title_field
if not item.item_type == "html":
    if item.name:
        dct_item["name"] = item.name
    elif item.action_name:
        dct_item["name"] = item.action_name

    if item.t_name:
        dct_item["t-name"] = item.t_name
    if item.t_attf_class:
        dct_item["t-attf-class"] = item.t_attf_class
    if item.t_if:
        dct_item["t-if"] = item.t_if
    if item.title:
        dct_item["title"] = item.title
    if item.aria_label:
        dct_item["aria-label"] = item.aria_label
    if item.role:
        dct_item["role"] = item.role
    if item.type:
        dct_item["type"] = item.type
    if item.widget:
        dct_item["widget"] = item.widget
    if item.label:
        dct_item["string"] = item.label
    if item.domain:
        dct_item["domain"] = item.domain
    if item.context:
        dct_item["context"] = item.context
    if item.class_attr:
        dct_item["class"] = item.class_attr

if item.item_type == "field":
    if item.placeholder:
        dct_item["placeholder"] = item.placeholder
    if item.password:
        dct_item["password"] = "True"
    dct_item = dict(sorted(dct_item.items(), key=lambda kv: kv[0]))
    item_xml = E.field(dct_item)
elif item.item_type == "filter":
    dct_item = dict(sorted(dct_item.items(), key=lambda kv: kv[0]))
    item_xml = E.filter(dct_item)
elif item.item_type == "button":
    return self._generate_xml_button(
        item, model_id, lst_child_update=lst_child_update
    )
elif item.item_type == "html":
    lst_html_child = []
    if item.background_type:
        old_class = dct_item.get("class")
        if old_class and old_class != item.background_type:
            _logger.error(
                "Duplicate class, old class: {old_class},"
                " background_type {item.background_type}"
            )
        dct_item["class"] = item.background_type
        if item.background_type.startswith("bg-warning"):
            lst_html_child.append(E.h3({}, "Warning:"))
        elif item.background_type.startswith("bg-success"):
            lst_html_child.append(E.h3({}, "Success:"))
        elif item.background_type.startswith("bg-info"):
            lst_html_child.append(E.h3({}, "Info:"))
        elif item.background_type.startswith("bg-danger"):
            lst_html_child.append(E.h3({}, "Danger:"))
    lst_html_child.append(item.label)
    dct_item = dict(sorted(dct_item.items(), key=lambda kv: kv[0]))
    item_xml = E.div(dct_item, *lst_html_child)
elif item.item_type == "group":
    if item.label:
        dct_item["string"] = item.label
    if item.attrs:
        dct_item["attrs"] = item.attrs
    dct_item = dict(sorted(dct_item.items(), key=lambda kv: kv[0]))
    item_xml = E.group(dct_item, *lst_child_update)
elif item.item_type == "li":
    dct_item = dict(sorted(dct_item.items(), key=lambda kv: kv[0]))
    item_xml = E.li(dct_item, *lst_child_update)
elif item.item_type == "ul":
    dct_item = dict(sorted(dct_item.items(), key=lambda kv: kv[0]))
    item_xml = E.ul(dct_item, *lst_child_update)
elif item.item_type == "i":
    dct_item = dict(sorted(dct_item.items(), key=lambda kv: kv[0]))
    item_xml = E.i(dct_item, *lst_child_update)
elif item.item_type == "t":
    dct_item = dict(sorted(dct_item.items(), key=lambda kv: kv[0]))
    item_xml = E.t(dct_item, *lst_child_update)
elif item.item_type == "strong":
    dct_item = dict(sorted(dct_item.items(), key=lambda kv: kv[0]))
    item_xml = E.strong(dct_item, *lst_child_update)
elif item.item_type == "xpath":
    if not item.expr:
        _logger.error(
            f"Missing expr for item action_name {item.action_name}"
        )
    elif not item.position:
        _logger.error(
            f"Missing position for item action_name {item.action_name}"
        )
    else:
        dct_item["expr"] = item.expr
        dct_item["position"] = item.position
        dct_item = dict(sorted(dct_item.items(), key=lambda kv: kv[0]))
        item_xml = E.xpath(dct_item, *lst_child_update)
elif item.item_type == "div":
    if item.attrs:
        dct_item["attrs"] = item.attrs
    dct_item = dict(sorted(dct_item.items(), key=lambda kv: kv[0]))
    item_xml = E.div(dct_item, *lst_child_update)
elif item.item_type == "templates":
    if item.attrs:
        dct_item["attrs"] = item.attrs
    dct_item = dict(sorted(dct_item.items(), key=lambda kv: kv[0]))
    item_xml = E.templates(dct_item, *lst_child_update)
else:
    _logger.warning(f"View item '{item.item_type}' is not supported.")
return item_xml""",
                    "name": "_generate_xml_object",
                    "param": "self, item, model_id, lst_child=None",
                    "sequence": 16,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": '''"""

:param item:
:param lst_xml: list of item to add more in some context
:param dct_replace: need it to replace html in xml without validation
:return:
"""
lst_child = sorted(item.child_id, key=lambda a: a.sequence)
lst_item_child = []
if lst_child:
    for item_child_id in lst_child:
        item_child = self._generate_xml_group_div(
            item_child_id, lst_xml, dct_replace, model_id
        )
        if item_child is not None:
            lst_item_child.append(item_child)
        else:
            _logger.warning(
                "Missing item xml group div about view item"
                f" '{item_child_id.item_type}'"
            )
    item_xml = self._generate_xml_object(
        item, model_id, lst_child=lst_item_child
    )
else:
    item_xml = self._generate_xml_object(item, model_id)

if item_xml is None:
    _logger.error(f"Cannot generate view for item {item.action_name}")

return item_xml''',
                    "name": "_generate_xml_group_div",
                    "param": "self, item, lst_xml, dct_replace, model_id",
                    "sequence": 17,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": '''"""

:param item: type odoo.api.code.generator.view.item
:param lst_child: list of item to add more in some context
:param level: 0 is bigger level (H1), >=4 is H5
:return:
"""
if item.edit_only or item.has_label:
    dct_item_label = {"for": item.action_name}
    if item.edit_only:
        dct_item_label["class"] = "oe_edit_only"
    item_label = E.label(dct_item_label)
    lst_child.append(item_label)
dct_item_field = {}
if item.name:
    dct_item_field["name"] = item.name
else:
    dct_item_field["name"] = item.action_name

if item.type:
    dct_item_field["type"] = item.type

if item.is_required:
    dct_item_field["required"] = "1"
if item.is_readonly:
    dct_item_field["readonly"] = "1"
dct_item_field = dict(
    sorted(dct_item_field.items(), key=lambda kv: kv[0])
)
item_field = E.field(dct_item_field)
if level == 0:
    result = E.h1({}, item_field)
elif level == 1:
    result = E.h2({}, item_field)
elif level == 2:
    result = E.h3({}, item_field)
elif level == 3:
    result = E.h4({}, item_field)
else:
    result = E.h5({}, item_field)
return result''',
                    "name": "_generate_xml_title_field",
                    "decorator": "@staticmethod",
                    "param": "item, lst_child, level=0",
                    "sequence": 18,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """view_type = code_generator_view_id.view_type
model_name = code_generator_view_id.m2o_model.model
model_id = code_generator_view_id.m2o_model.id
dct_replace = {}
lst_item_header = []
lst_item_footer = []
lst_item_body = []
lst_item_title = []
for view_item in code_generator_view_id.view_item_ids:
    if view_item.section_type == "body":
        lst_item_body.append(view_item)
    elif view_item.section_type == "header":
        lst_item_header.append(view_item)
    elif view_item.section_type == "footer":
        lst_item_footer.append(view_item)
    elif view_item.section_type == "title":
        lst_item_title.append(view_item)
    else:
        _logger.warning(
            f"View item '{view_item.section_type}' is not supported."
        )

lst_item_form = []
lst_item_form_sheet = []

if lst_item_header:
    lst_item_header = sorted(lst_item_header, key=lambda a: a.sequence)
    lst_child = []
    for item_header in lst_item_header:
        if item_header.item_type == "field":
            item = E.field()
            # TODO field in header
        elif item_header.item_type == "button":
            item = self._generate_xml_button(item_header, model_id)
        else:
            _logger.warning(
                f"Item header type '{item_header.item_type}' is not"
                " supported."
            )
            continue
        lst_child.append(item)
    header_xml = E.header({}, *lst_child)
    lst_item_form.append(header_xml)

if lst_item_title:
    lst_item_title = sorted(lst_item_title, key=lambda a: a.sequence)
    lst_child = []
    i = 0
    for item_title in lst_item_title:
        if item_title.item_type == "field":
            item = self._generate_xml_title_field(
                item_title, lst_child, level=i
            )
        elif item_title.item_type == "button":
            _logger.warning(
                f"Button is not supported in title section."
            )
            continue
        else:
            _logger.warning(
                f"Item title type '{item_title.item_type}' is not"
                " supported."
            )
            continue
        i += 1
        lst_child.append(item)
    title_xml = E.div({"class": "oe_title"}, *lst_child)
    lst_item_form_sheet.append(title_xml)

if lst_item_body:
    lst_item_root_body = [a for a in lst_item_body if not a.parent_id]
    lst_item_root_body = sorted(
        lst_item_root_body, key=lambda a: a.sequence
    )
    for item_body in lst_item_root_body:
        if item_body.is_help:
            item_xml = self._generate_xml_html_help(
                item_body, lst_item_form_sheet, dct_replace
            )
            lst_item_form_sheet.append(item_xml)
        elif item_body.item_type in ("div", "group", "templates"):
            if not item_body.child_id:
                _logger.warning(
                    f"Item type '{item_body.item_type}' missing child."
                )
                continue
            item_xml = self._generate_xml_group_div(
                item_body, lst_item_form_sheet, dct_replace, model_id
            )
            if item_xml is not None:
                lst_item_form_sheet.append(item_xml)
        elif item_body.item_type in ("xpath",):
            # TODO maybe move this in lst_item_xpath with view_item.section_type == 'xpath'
            if not item_body.child_id:
                _logger.warning(f"Item type xpath missing child.")
                continue
            item_xml = self._generate_xml_group_div(
                item_body, lst_item_form_sheet, dct_replace, model_id
            )
            if item_xml is not None:
                lst_item_form_sheet.append(item_xml)
        elif item_body.item_type in ("field", "filter"):
            item_xml = self._generate_xml_object(item_body, model_id)
            if item_xml is not None:
                lst_item_form_sheet.append(item_xml)
        else:
            _logger.warning(f"Unknown type xml {item_body.item_type}")

if lst_item_footer:
    lst_item_footer = sorted(lst_item_footer, key=lambda a: a.sequence)
    lst_child = []
    for item_footer in lst_item_footer:
        if item_footer.item_type == "field":
            item = E.field()
            # TODO field in footer
        elif item_footer.item_type == "button":
            item = self._generate_xml_button(item_footer, model_id)
        else:
            _logger.warning(
                f"Item footer type '{item_footer.item_type}' is not"
                " supported."
            )
            continue
        if item:
            lst_child.append(item)
    footer_xml = E.footer({}, *lst_child)
    lst_item_form.append(footer_xml)

if lst_item_form_sheet:
    if code_generator_view_id.has_body_sheet:
        sheet_xml = E.sheet({}, *lst_item_form_sheet)
        lst_item_form.append(sheet_xml)
    else:
        lst_item_form += lst_item_form_sheet

dct_attr_view = {}
if code_generator_view_id.view_attr_string:
    dct_attr_view["string"] = code_generator_view_id.view_attr_string

if code_generator_view_id.view_attr_class:
    dct_attr_view["class"] = code_generator_view_id.view_attr_class

dct_attr_view = dict(
    sorted(dct_attr_view.items(), key=lambda kv: kv[0])
)
if code_generator_view_id.inherit_view_name:
    if len(lst_item_form) > 1:

        form_xml = E.data(dct_attr_view, *lst_item_form)
    else:
        form_xml = lst_item_form[0]
elif view_type == "form":
    form_xml = E.form(dct_attr_view, *lst_item_form)
elif view_type == "search":
    form_xml = E.search(dct_attr_view, *lst_item_form)
elif view_type == "tree":
    form_xml = E.tree(dct_attr_view, *lst_item_form)
elif view_type == "kanban":
    form_xml = E.kanban(dct_attr_view, *lst_item_form)
elif view_type == "graph":
    form_xml = E.graph(dct_attr_view, *lst_item_form)
elif view_type == "pivot":
    form_xml = E.pivot(dct_attr_view, *lst_item_form)
else:
    _logger.warning(
        f"Unknown xml view_type {view_type}, attribute {dct_attr_view}"
    )
    return

str_arch = ET.tostring(form_xml, pretty_print=True)
str_content = str_arch.decode()

for key, value in dct_replace.items():
    str_content = str_content.replace(key, value)

view_name = (
    code_generator_view_id.view_name
    if code_generator_view_id.view_name
    else f"{model_name.replace('.', '_')}_{view_type}"
)
dct_view_value = {
    "name": view_name,
    "type": view_type,
    "model": model_name,
    "arch": str_content,
    "m2o_model": code_generator_view_id.m2o_model.id,
}
if code_generator_view_id.inherit_view_name:
    dct_view_value["inherit_id"] = self.env.ref(
        code_generator_view_id.inherit_view_name
    ).id
    dct_view_value["is_show_whitelist_write_view"] = True
lst_search = [
    (a, "=", b)
    for a, b in dct_view_value.items()
    if a not in ("m2o_model", "arch")
]
view_value = self.env["ir.ui.view"].search(lst_search)
if not view_value:
    view_value = self.env["ir.ui.view"].create(dct_view_value)
else:
    view_value.m2o_model = code_generator_view_id.m2o_model.id
    # dct_value_to_create["ir.ui.view"].append(ir_ui_view_value)

if code_generator_view_id.id_name:
    ir_model_data_id = self.env["ir.model.data"].search(
        [
            ("name", "=", code_generator_view_id.id_name),
            ("model", "=", "ir.ui.view"),
            (
                "module",
                "=",
                code_generator_view_id.code_generator_id.name,
            ),
        ]
    )
    if ir_model_data_id:
        ir_model_data_id.res_id = view_value.id
    else:
        self.env["ir.model.data"].create(
            {
                "name": code_generator_view_id.id_name,
                "model": "ir.ui.view",
                "module": code_generator_view_id.code_generator_id.name,
                "res_id": view_value.id,
                "noupdate": True,  # If it's False, target record (res_id) will be removed while module update
            }
        )

return view_value""",
                    "name": "_generate_specific_form_views_models",
                    "param": (
                        "self, code_generator_view_id, dct_value_to_create"
                    ),
                    "sequence": 19,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": """if self.disable_generate_access:
    return
# Unique access
# group_id = self.env['res.groups'].search([('name', '=', 'Code Generator / Manager')])
# group_id = self.env['res.groups'].search([('name', '=', 'Internal User')])
# TODO search system lang
lang = "en_US"
group_id = self.env.ref("base.group_user").with_context(lang=lang)
model_name = model_created.model
model_name_str = model_name.replace(".", "_")
name = "%s Access %s" % (model_name_str, group_id.full_name)
# TODO maybe search by permission and model, ignore the name
existing_access = self.env["ir.model.access"].search(
    [
        ("model_id", "=", model_created.id),
        ("group_id", "=", group_id.id),
        ("name", "=", name),
    ]
)
if existing_access:
    return

v = {
    "name": name,
    "model_id": model_created.id,
    "group_id": group_id.id,
    "perm_read": True,
    "perm_create": True,
    "perm_write": True,
    "perm_unlink": True,
}

access_value = self.env["ir.model.access"].create(v)""",
                    "name": "_generate_model_access",
                    "param": "self, model_created",
                    "sequence": 20,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
                {
                    "code": '''if self.disable_generate_menu:
    return

# group_id = self.env['res.groups'].search([('name', '=', 'Code Generator / Manager')])
# group_id = self.env['res.groups'].search([('name', '=', 'Internal User')])
is_generic_menu = not model_created.m2o_module.code_generator_menus_id
group_id = self.env.ref("base.group_user")
model_name = model_created.model
menu_group = model_created.menu_group
menu_parent = model_created.menu_parent
model_name_str = model_name.replace(".", "_")
module_name = module.name
menu_group_id = None
menu_parent_id = None
if module.application and is_generic_menu:
    # Create root if not exist
    if not self.generated_root_menu:
        v = {
            "name": module_name.replace("_", " ").title(),
            "sequence": 20,
            "web_icon": f"code_generator,static/description/icon_new_application.png",
            # 'group_id': group_id.id,
            "m2o_module": module.id,
        }
        self.generated_root_menu = self.env["ir.ui.menu"].create(v)
    if not self.generated_parent_menu:
        v = {
            "name": _("Menu"),
            "sequence": 1,
            "parent_id": self.generated_root_menu.id,
            # 'group_id': group_id.id,
            "m2o_module": module.id,
        }
        self.generated_parent_menu = self.env["ir.ui.menu"].create(v)

# Create list of menu_parent
if not self.lst_parent_generated_menu_name:
    self.lst_parent_generated_menu_name = sorted(
        list(set([a.menu_parent for a in model_ids if a.menu_parent]))
    )

# Create list of menu_group
if not self.lst_group_generated_menu_name:
    self.lst_group_generated_menu_name = sorted(
        list(set([a.menu_group for a in model_ids if a.menu_group]))
    )

# Create menu_parent item
if is_generic_menu and menu_parent:
    menu_parent_id = self.dct_parent_generated_menu.get(menu_parent)
    if menu_parent == "Configuration":
        sequence = 99
    else:
        sequence = (
            self.lst_parent_generated_menu_name.index(menu_parent) + 1
        )

    if not menu_parent_id:
        v = {
            "name": menu_parent,
            "sequence": sequence,
            # 'group_id': group_id.id,
            "m2o_module": module.id,
            "parent_id": self.generated_root_menu.id,
        }

        menu_parent_id = self.env["ir.ui.menu"].create(v)
        self.dct_parent_generated_menu[menu_parent] = menu_parent_id

        # Create id name
        menu_parent_name = (
            f"parent_{unidecode.unidecode(menu_parent).replace(' ','').lower()}"
        )
        self.env["ir.model.data"].create(
            {
                "name": menu_parent_name,
                "model": "ir.ui.menu",
                "module": module.name,
                "res_id": menu_parent_id.id,
                "noupdate": True,
                # If it's False, target record (res_id) will be removed while module update
            }
        )

# Create menu_group item
if is_generic_menu and menu_group:
    menu_group_id = self.dct_group_generated_menu.get(menu_group)
    sequence = self.lst_group_generated_menu_name.index(menu_group)
    if not menu_group_id:
        v = {
            "name": menu_group,
            "sequence": sequence,
            # 'group_id': group_id.id,
            "m2o_module": module.id,
        }
        if menu_parent_id:
            v["parent_id"] = menu_parent_id.id
        elif self.generated_parent_menu:
            v["parent_id"] = self.generated_parent_menu.id
        else:
            v["parent_id"] = self.generated_root_menu.id

        menu_group_id = self.env["ir.ui.menu"].create(v)
        self.dct_group_generated_menu[menu_group] = menu_group_id

        # Create id name
        menu_group_name = (
            f"group_{unidecode.unidecode(menu_group).replace(' ','').lower()}"
        )
        self.env["ir.model.data"].create(
            {
                "name": menu_group_name,
                "model": "ir.ui.menu",
                "module": module.name,
                "res_id": menu_group_id.id,
                "noupdate": True,
                # If it's False, target record (res_id) will be removed while module update
            }
        )

help_str = f"""<p class="o_view_nocontent_empty_folder">
Add a new {model_name_str}
  </p>
  <p>
    Databases whose tables could be imported to Odoo and then be exported into code
  </p>
"""

# TODO change sequence of view mode
# Kanban first by default
if "kanban" in lst_view_generated:
    lst_first_view_generated = ["kanban"]
    lst_second_view_generated = list(set(lst_view_generated[:]))
    lst_second_view_generated.remove("kanban")
else:
    lst_first_view_generated = []
    lst_second_view_generated = list(set(lst_view_generated))

# Special case, cannot support search view type in action_view
try:
    lst_second_view_generated.remove("search")
except:
    pass

view_mode = ",".join(
    lst_first_view_generated
    + sorted(lst_second_view_generated, reverse=True)
)
view_type = (
    "form" if "form" in lst_view_generated else lst_view_generated[0]
)

# Create menu
if module.application and is_generic_menu:
    # Compute menu name
    menu_name = model_name_str
    if "." in model_name:
        application_name, sub_model_name = model_name.split(
            ".", maxsplit=1
        )
        if model_created.menu_label:
            menu_name = model_created.menu_label
        elif (
            not model_created.menu_name_keep_application
            and sub_model_name
            and menu_name.lower().startswith(application_name.lower())
        ):
            menu_name = (
                sub_model_name.capitalize()
                .replace(".", " ")
                .replace("_", " ")
            )
        else:
            menu_name = f"{application_name} {sub_model_name.replace('.', ' ')}".capitalize().replace(
                "_", " "
            )
    else:
        menu_name = model_name
    # Create action
    v = {
        "name": menu_name,
        "res_model": model_name,
        "type": "ir.actions.act_window",
        "view_mode": view_mode,
        "view_type": view_type,
        # 'help': help_str,
        # 'search_view_id': self.search_view_id.id,
        "context": {},
        "m2o_res_model": model_created.id,
    }
    action_id = self.env["ir.actions.act_window"].create(v)

    # TODO check function _get_action_data_name in code_generator_writer.py
    fix_action_id_name = (
        unidecode.unidecode(menu_name)
        .replace(" ", "_")
        .replace("'", "_")
        .replace("-", "_")
        .lower()
    )
    action_id_name = (
        f"{model_name_str}_{fix_action_id_name}_action_window"
    )

    v_ir_model_data = {
        "name": action_id_name,
        "model": "ir.actions.act_window",
        "module": module.name,
        "res_id": action_id.id,
        "noupdate": True,
    }
    self.env["ir.model.data"].create(v_ir_model_data)

    self.nb_sub_menu += 1

    v = {
        "name": menu_name,
        "sequence": self.nb_sub_menu,
        "action": "ir.actions.act_window,%s" % action_id.id,
        # 'group_id': group_id.id,
        "m2o_module": module.id,
    }

    if menu_group_id:
        v["parent_id"] = menu_group_id.id
    elif menu_parent_id:
        v["parent_id"] = menu_parent_id.id
    elif self.generated_parent_menu:
        v["parent_id"] = self.generated_parent_menu.id

    new_menu_id = self.env["ir.ui.menu"].create(v)

    menu_id_name = (
        unidecode.unidecode(menu_name)
        .replace(" ", "_")
        .replace("'", "_")
        .replace("-", "_")
        .lower()
    )

    v_ir_model_data = {
        "name": menu_id_name,
        "model": "ir.ui.menu",
        "module": module.name,
        "res_id": new_menu_id.id,
        "noupdate": True,
    }
    self.env["ir.model.data"].create(v_ir_model_data)
elif not is_generic_menu:
    cg_menu_ids = model_created.m2o_module.code_generator_menus_id
    # TODO check different case, with act_window, without, multiple menu, single menu
    # Sort parent first

    lst_menu_to_sort = [a for a in cg_menu_ids]
    lst_menu = []
    lst_inserted_menu_name = []
    i = -1
    while lst_menu_to_sort:
        i += 1
        lst_added_menu = []
        if len(lst_menu_to_sort) <= i:
            # Re loop
            i = 0
        menu_id = lst_menu_to_sort[i]
        menu_name = menu_id.id_name
        if not menu_id.parent_id_name:
            lst_inserted_menu_name.append(menu_name)
            lst_added_menu.append(menu_id)
        else:
            parent_module_name = None
            if "." in menu_id.parent_id_name:
                (
                    parent_module_name,
                    parent_menu_name,
                ) = menu_id.parent_id_name.split(".")
            else:
                parent_menu_name = menu_id.parent_id_name
            if (
                parent_module_name != module.name
                or parent_menu_name in lst_inserted_menu_name
            ):
                lst_inserted_menu_name.append(menu_name)
                lst_added_menu.append(menu_id)
        for added_menu in lst_added_menu:
            lst_menu.append(added_menu)
            lst_menu_to_sort.remove(added_menu)
            i = -1

    for menu_id in lst_menu:
        action_id = None
        if menu_id.m2o_act_window:
            # Create action
            v = {
                "name": menu_id.m2o_act_window.name,
                "type": "ir.actions.act_window",
                "view_mode": view_mode,
                "view_type": view_type,
                # 'help': help_str,
                # 'search_view_id': self.search_view_id.id,
                "context": {},
                "m2o_res_model": model_created.id,
            }
            if menu_id.m2o_act_window.model_name:
                v["res_model"] = menu_id.m2o_act_window.model_name
            else:
                _logger.warning(
                    "Missing model_name into m2o_act_window"
                    f" '{menu_id.m2o_act_window.name}', force another"
                    f" model name '{model_name}'"
                )
                v["res_model"] = model_name

            lst_action = [
                (a, "=", b)
                for a, b in v.items()
                if a != "m2o_res_model"
            ]
            action_id = self.env["ir.actions.act_window"].search(
                lst_action
            )
            if not action_id:
                action_id = self.env["ir.actions.act_window"].create(v)
            else:
                action_id.m2o_res_model = model_created.id
            if menu_id.m2o_act_window.id_name:
                ir_model_data_id = self.env["ir.model.data"].search(
                    [
                        ("name", "=", menu_id.m2o_act_window.id_name),
                        ("model", "=", "ir.actions.act_window"),
                        (
                            "module",
                            "=",
                            module.name,
                        ),
                    ]
                )
                if ir_model_data_id:
                    ir_model_data_id.res_id = action_id.id
                else:
                    # Write id name
                    self.env["ir.model.data"].create(
                        {
                            "name": menu_id.m2o_act_window.id_name,
                            "model": "ir.actions.act_window",
                            "module": module.name,
                            "res_id": action_id.id,
                            "noupdate": True,
                            # If it's False, target record (res_id) will be removed while module update
                        }
                    )
        elif not menu_id.ignore_act_window:
            # Create action
            v = {
                "name": f"{model_name_str}_action_view",
                "res_model": model_name,
                "type": "ir.actions.act_window",
                "view_mode": view_mode,
                "view_type": view_type,
                # 'help': help_str,
                # 'search_view_id': self.search_view_id.id,
                "context": {},
                "m2o_res_model": model_created.id,
            }
            action_id = self.env["ir.actions.act_window"].create(v)

        v = {
            "name": menu_id.name,
            # 'group_id': group_id.id,
            "m2o_module": module.id,
        }
        if menu_id.ignore_act_window:
            v["ignore_act_window"] = True
        else:
            v["action"] = "ir.actions.act_window,%s" % action_id.id

        v["sequence"] = menu_id.sequence

        if menu_id.web_icon:
            v["web_icon"] = menu_id.web_icon

        if menu_id.parent_id_name:
            # TODO crash when create empty module and template to read this empty module
            try:
                v["parent_id"] = self.env.ref(
                    menu_id.parent_id_name
                ).id
            except Exception:
                _logger.error(
                    f"Cannot find ref {menu_id.parent_id_name} of menu"
                    f" {menu_id.id_name} to associate parent_id."
                )

        new_menu_id = self.env["ir.ui.menu"].create(v)

        ir_model_data_id = self.env["ir.model.data"].search(
            [
                ("name", "=", menu_id.id_name),
                ("model", "=", "ir.ui.menu"),
                (
                    "module",
                    "=",
                    module.name,
                ),
            ]
        )
        if ir_model_data_id:
            ir_model_data_id.res_id = new_menu_id.id
        else:
            v_ir_model_data = {
                "name": menu_id.id_name,
                "model": "ir.ui.menu",
                "module": module.name,
                "res_id": new_menu_id.id,
                "noupdate": True,
            }
            self.env["ir.model.data"].create(v_ir_model_data)''',
                    "name": "_generate_menu",
                    "param": (
                        "self, model_created, module, lst_view_generated,"
                        " model_ids"
                    ),
                    "sequence": 21,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_generate_views_wizard.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Code Generator Ir Model Dependency
        model_model = "code.generator.ir.model.dependency"
        model_name = "code_generator_ir_model_dependency"
        dct_model = {
            "description": "Code Generator ir model Dependency",
        }
        dct_field = {
            "depend_id": {
                "code_generator_sequence": 3,
                "field_description": "Dependency",
                "relation": "ir.model",
                "ttype": "many2one",
            },
            "name": {
                "code_generator_compute": "compute_name",
                "code_generator_sequence": 2,
                "field_description": "Name",
                "ttype": "char",
            },
        }
        model_code_generator_ir_model_dependency = (
            code_generator_id.add_update_model(
                model_model,
                model_name,
                dct_field=dct_field,
                dct_model=dct_model,
            )
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_ir_model_dependency.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """for rec in self:
    if rec.depend_id:
        rec.name = rec.depend_id.model""",
                    "name": "compute_name",
                    "decorator": '@api.depends("depend_id")',
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_ir_model_dependency.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Code Generator Ir Model Fields
        model_model = "code.generator.ir.model.fields"
        model_name = "code_generator_ir_model_fields"
        dct_model = {
            "description": "Code Generator Fields",
        }
        dct_field = {
            "code_generator_compute": {
                "code_generator_sequence": 3,
                "field_description": "Compute Code Generator",
                "help": "Compute method to code_generator_writer.",
                "ttype": "char",
            },
            "default_lambda": {
                "code_generator_sequence": 4,
                "field_description": "Default lambda value",
                "ttype": "char",
            },
            "field_context": {
                "code_generator_sequence": 5,
                "field_description": "Field Context",
                "ttype": "char",
            },
            "filter_field_attribute": {
                "code_generator_sequence": 6,
                "field_description": "Filter Field Attribute",
                "help": (
                    "Separate by ; to enumerate your attribute to filter, like"
                    " a whitelist of attributes field."
                ),
                "ttype": "char",
            },
            "is_show_whitelist_model_inherit": {
                "code_generator_sequence": 7,
                "field_description": "Show in whitelist model inherit",
                "help": (
                    "If a field in model is in whitelist, will be show in"
                    " generated model."
                ),
                "ttype": "boolean",
            },
            "m2o_fields": {
                "code_generator_sequence": 8,
                "field_description": "Fields",
                "relation": "ir.model.fields",
                "ttype": "many2one",
            },
            "m2o_module": {
                "code_generator_sequence": 9,
                "field_description": "Module",
                "help": "Module",
                "relation": "code.generator.module",
                "ttype": "many2one",
            },
            "name": {
                "code_generator_compute": "_change_m2o_fields",
                "code_generator_sequence": 2,
                "field_description": "Name",
                "help": "Name of selected field.",
                "ttype": "char",
            },
            "nomenclature_blacklist": {
                "code_generator_sequence": 10,
                "field_description": "Ignore from nomenclature.",
                "ttype": "boolean",
            },
            "nomenclature_whitelist": {
                "code_generator_sequence": 11,
                "field_description": "Force to nomenclature.",
                "ttype": "boolean",
            },
            "selection": {
                "code_generator_sequence": 12,
                "field_description": "Selection Options",
                "help": (
                    "List of options for a selection field, specified as a"
                    " Python expression defining a list of (key, label) pairs."
                    " For example: [('blue','Blue'),('yellow','Yellow')]"
                ),
                "ttype": "char",
            },
        }
        model_code_generator_ir_model_fields = (
            code_generator_id.add_update_model(
                model_model,
                model_name,
                dct_field=dct_field,
                dct_model=dct_model,
            )
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_ir_model_fields.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """for ir_field in self:
    if ir_field.m2o_fields:
        ir_field.name = ir_field.m2o_fields.name
    else:
        self.name = False""",
                    "name": "_change_m2o_fields",
                    "decorator": '@api.onchange("m2o_fields")',
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_ir_model_fields.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Code Generator Menu
        model_model = "code.generator.menu"
        model_name = "code_generator_menu"
        dct_model = {
            "description": "Code Generator Menu",
        }
        dct_field = {
            "code_generator_id": {
                "code_generator_sequence": 3,
                "field_description": "Code Generator",
                "relation": "code.generator.module",
                "required": True,
                "ttype": "many2one",
            },
            "id_name": {
                "code_generator_sequence": 4,
                "field_description": "Menu id",
                "help": "Specify id name of this menu.",
                "ttype": "char",
            },
            "ignore_act_window": {
                "code_generator_sequence": 5,
                "field_description": "Ignore Act Window",
                "help": "Set True to force no act_window, like a parent menu.",
                "ttype": "boolean",
            },
            "m2o_act_window": {
                "code_generator_sequence": 6,
                "field_description": "Action Windows",
                "help": "Act window to open when click on this menu.",
                "relation": "code.generator.act_window",
                "ttype": "many2one",
            },
            "name": {
                "code_generator_sequence": 2,
                "field_description": "Name",
                "help": "Menu name",
                "ttype": "char",
            },
            "parent_id_name": {
                "code_generator_sequence": 7,
                "field_description": "Menu parent id",
                "help": "Specify id name of parent menu, optional.",
                "ttype": "char",
            },
            "sequence": {
                "code_generator_sequence": 8,
                "field_description": "Sequence",
                "ttype": "integer",
            },
            "web_icon": {
                "code_generator_sequence": 9,
                "field_description": "Web Icon",
                "help": "Icon menu",
                "ttype": "char",
            },
        }
        model_code_generator_menu = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_menu.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Code Generator Model Code
        model_model = "code.generator.model.code"
        model_name = "code_generator_model_code"
        dct_model = {
            "description": "Code to display in model",
        }
        dct_field = {
            "code": {
                "code_generator_sequence": 3,
                "default": """
return""",
                "field_description": "Code of pre_init_hook",
                "ttype": "text",
            },
            "decorator": {
                "code_generator_sequence": 4,
                "field_description": "Decorator",
                "help": "Like @api.model. Use ; for multiple decorator.",
                "ttype": "char",
            },
            "is_templated": {
                "code_generator_sequence": 5,
                "field_description": "Templated",
                "help": "Code for code generator from template.",
                "ttype": "boolean",
            },
            "is_wip": {
                "code_generator_sequence": 6,
                "field_description": "Work in progress",
                "help": "Temporary function to be fill later.",
                "ttype": "boolean",
            },
            "m2o_model": {
                "code_generator_sequence": 7,
                "field_description": "Model",
                "help": "Model",
                "relation": "ir.model",
                "ttype": "many2one",
            },
            "m2o_module": {
                "code_generator_sequence": 8,
                "field_description": "Module",
                "help": "Module",
                "relation": "code.generator.module",
                "ttype": "many2one",
            },
            "name": {
                "code_generator_sequence": 2,
                "field_description": "Method name",
                "help": "Method name",
                "required": True,
                "ttype": "char",
            },
            "param": {
                "code_generator_sequence": 9,
                "field_description": "Param",
                "help": "Like : name,color",
                "ttype": "char",
            },
            "returns": {
                "code_generator_sequence": 10,
                "field_description": "Return type",
                "help": "Annotation to return type value.",
                "ttype": "char",
            },
            "sequence": {
                "code_generator_sequence": 11,
                "field_description": "Sequence",
                "help": "Order of sequence code.",
                "ttype": "integer",
            },
        }
        model_code_generator_model_code = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_model_code.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Code Generator Model Code Import
        model_model = "code.generator.model.code.import"
        model_name = "code_generator_model_code_import"
        dct_model = {
            "description": "Header code to display in model",
        }
        dct_field = {
            "code": {
                "code_generator_sequence": 3,
                "field_description": "Code",
                "help": "Code of import header of python file",
                "ttype": "text",
            },
            "is_templated": {
                "code_generator_sequence": 4,
                "field_description": "Templated",
                "help": "Code for code generator from template.",
                "ttype": "boolean",
            },
            "m2o_model": {
                "code_generator_sequence": 5,
                "field_description": "Model",
                "help": "Model",
                "relation": "ir.model",
                "ttype": "many2one",
            },
            "m2o_module": {
                "code_generator_sequence": 6,
                "field_description": "Module",
                "help": "Module",
                "relation": "code.generator.module",
                "ttype": "many2one",
            },
            "name": {
                "code_generator_sequence": 2,
                "field_description": "Import name",
                "help": "import name",
                "ttype": "char",
            },
            "sequence": {
                "code_generator_sequence": 7,
                "field_description": "Sequence",
                "help": "Order of sequence code.",
                "ttype": "integer",
            },
        }
        model_code_generator_model_code_import = (
            code_generator_id.add_update_model(
                model_model,
                model_name,
                dct_field=dct_field,
                dct_model=dct_model,
            )
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_model_code_import.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Code Generator Module
        model_model = "code.generator.module"
        model_name = "code_generator_module"
        lst_depend_model = ["ir.module.module"]
        dct_model = {
            "description": "Code Generator Module",
        }
        dct_field = {
            "application": {
                "code_generator_form_simple_view_sequence": 22,
                "code_generator_sequence": 4,
                "code_generator_tree_view_sequence": 22,
                "field_description": "Application",
                "ttype": "boolean",
            },
            "author": {
                "code_generator_form_simple_view_sequence": 14,
                "code_generator_sequence": 5,
                "code_generator_tree_view_sequence": 14,
                "field_description": "Author",
                "ttype": "char",
            },
            "category_id": {
                "code_generator_form_simple_view_sequence": 15,
                "code_generator_sequence": 6,
                "code_generator_tree_view_sequence": 15,
                "field_description": "Category",
                "relation": "ir.module.category",
                "ttype": "many2one",
            },
            "contributors": {
                "code_generator_sequence": 10,
                "field_description": "Contributors",
                "ttype": "text",
            },
            "demo": {
                "code_generator_sequence": 11,
                "field_description": "Demo Data",
                "ttype": "boolean",
            },
            "description": {
                "code_generator_sequence": 14,
                "field_description": "Description",
                "ttype": "text",
            },
            "enable_pylint_check": {
                "code_generator_sequence": 15,
                "field_description": "Enable Pylint check",
                "help": "Show pylint result at the end of generation.",
                "ttype": "boolean",
            },
            "enable_sync_code": {
                "code_generator_form_simple_view_sequence": 20,
                "code_generator_sequence": 16,
                "code_generator_tree_view_sequence": 20,
                "field_description": "Enable Sync Code",
                "help": "Will sync with code on drive when generate.",
                "ttype": "boolean",
            },
            "exclude_dependencies_str": {
                "code_generator_sequence": 18,
                "field_description": "Exclude Dependencies Str",
                "help": (
                    "Exclude from list dependencies_id about"
                    " code.generator.module.dependency name separate by ;"
                ),
                "ttype": "char",
            },
            "export_website_optimize_binary_image": {
                "code_generator_sequence": 17,
                "field_description": "Export Website Optimize Binary Image",
                "help": (
                    "Associate with nomenclator export data. Search url"
                    " /web/image/ in website page and remove ir.attachment who"
                    " is not into view. Remove duplicate same attachment,"
                    " image or scss."
                ),
                "ttype": "boolean",
            },
            "icon_child_image": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 20,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Generated icon",
                "ttype": "binary",
            },
            "icon_image": {
                "code_generator_sequence": 21,
                "field_description": "Icon",
                "ttype": "binary",
            },
            "icon_real_image": {
                "code_generator_form_simple_view_sequence": 11,
                "code_generator_sequence": 22,
                "code_generator_tree_view_sequence": 11,
                "field_description": "Replace icon",
                "help": "This will replace icon_image",
                "ttype": "binary",
            },
            "latest_version": {
                "code_generator_sequence": 23,
                "field_description": "Installed Version",
                "ttype": "char",
            },
            "license": {
                "code_generator_form_simple_view_sequence": 18,
                "code_generator_sequence": 24,
                "code_generator_tree_view_sequence": 18,
                "default": "AGPL-3",
                "field_description": "License",
                "selection": (
                    "[('GPL-2', 'GPL Version 2'), ('GPL-2 or any later"
                    " version', 'GPL-2 or later version'), ('GPL-3', 'GPL"
                    " Version 3'), ('GPL-3 or any later version', 'GPL-3 or"
                    " later version'), ('AGPL-3', 'Affero GPL-3'), ('LGPL-3',"
                    " 'LGPL Version 3'), ('Other OSI approved licence', 'Other"
                    " OSI Approved Licence'), ('OEEL-1', 'Odoo Enterprise"
                    " Edition License v1.0'), ('OPL-1', 'Odoo Proprietary"
                    " License v1.0'), ('Other proprietary', 'Other"
                    " Proprietary')]"
                ),
                "ttype": "selection",
            },
            "list_scss_process_hook": {
                "code_generator_sequence": 25,
                "field_description": "List Scss Process Hook",
                "help": (
                    "READONLY, use by computation. Value are separated by ;."
                    " List of xml_id to compute scss in hook when export"
                    " website data with scss modification."
                ),
                "ttype": "char",
            },
            "maintainer": {
                "code_generator_sequence": 26,
                "field_description": "Maintainer",
                "ttype": "char",
            },
            "name": {
                "code_generator_form_simple_view_sequence": 25,
                "code_generator_sequence": 3,
                "code_generator_tree_view_sequence": 25,
                "field_description": "Technical Name",
                "required": True,
                "ttype": "char",
            },
            "nomenclator_only": {
                "code_generator_form_simple_view_sequence": 23,
                "code_generator_sequence": 27,
                "code_generator_tree_view_sequence": 23,
                "field_description": "Only export data",
                "help": "Useful to export data with existing model.",
                "ttype": "boolean",
            },
            "path_sync_code": {
                "code_generator_form_simple_view_sequence": 21,
                "code_generator_sequence": 55,
                "code_generator_tree_view_sequence": 21,
                "default": "_default_path_sync_code",
                "field_description": "Directory",
                "help": (
                    "Path directory where sync the code, will erase directory"
                    " and generate new code."
                ),
                "ttype": "char",
            },
            "published_version": {
                "code_generator_sequence": 44,
                "field_description": "Published Version",
                "ttype": "char",
            },
            "shortdesc": {
                "code_generator_form_simple_view_sequence": 13,
                "code_generator_sequence": 45,
                "code_generator_tree_view_sequence": 13,
                "field_description": "Module Name",
                "required": True,
                "ttype": "char",
            },
            "state": {
                "code_generator_form_simple_view_sequence": 26,
                "code_generator_sequence": 46,
                "code_generator_tree_view_sequence": 12,
                "default": "uninstalled",
                "field_description": "Status",
                "selection": (
                    "[('uninstallable', 'Uninstallable'), ('uninstalled', 'Not"
                    " Installed'), ('installed', 'Installed'), ('to upgrade',"
                    " 'To be upgraded'), ('to remove', 'To be removed'), ('to"
                    " install', 'To be installed')]"
                ),
                "ttype": "selection",
            },
            "summary": {
                "code_generator_form_simple_view_sequence": 16,
                "code_generator_sequence": 47,
                "code_generator_tree_view_sequence": 16,
                "field_description": "Summary",
                "ttype": "char",
            },
            "template_inherit_model_name": {
                "code_generator_sequence": 48,
                "field_description": "Functions models inherit",
                "help": (
                    "Add model from list, separate by ';' and generate"
                    " template."
                ),
                "ttype": "char",
            },
            "template_model_name": {
                "code_generator_sequence": 49,
                "field_description": "Functions models",
                "help": (
                    "Add model from list, separate by ';' and generate"
                    " template."
                ),
                "ttype": "char",
            },
            "template_module_id": {
                "code_generator_compute": "_fill_template_module_id",
                "code_generator_sequence": 50,
                "field_description": "Template module id",
                "help": "Child module to generate.",
                "relation": "ir.module.module",
                "ttype": "many2one",
            },
            "template_module_name": {
                "code_generator_sequence": 51,
                "field_description": "Generated module name",
                "help": (
                    "Can be empty in case of code_generator_demo, else it's"
                    " the module name goal to generate."
                ),
                "ttype": "char",
            },
            "url": {
                "code_generator_sequence": 52,
                "field_description": "URL",
                "ttype": "char",
            },
            "website": {
                "code_generator_sequence": 53,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Website",
                "ttype": "char",
            },
        }
        model_code_generator_module = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """import base64
import logging
import os

import lxml
from docutils.core import publish_string

from odoo import api, fields, models, modules, tools
from odoo.addons.base.models.ir_module import MyWriter

_logger = logging.getLogger(__name__)""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_module.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """sibling = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "TechnoLibre_odoo-code-generator-template",
    )
)
if os.path.isdir(sibling):
    return sibling
# Cannot find sibling template, use this working repo directory instead
return os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)""",
                    "name": "_default_path_sync_code",
                    "decorator": "@api.model",
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_module.id,
                },
                {
                    "code": """for module_id in self:
    if module_id.template_module_name:
        module_id.template_module_id = self.env[
            "ir.module.module"
        ].search([("name", "=", module_id.template_module_name)])""",
                    "name": "_fill_template_module_id",
                    "decorator": (
                        '@api.depends("template_module_name");@api.multi'
                    ),
                    "param": "self",
                    "sequence": 1,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_module.id,
                },
                {
                    "code": """self.add_module_dependency(
    module_name,
    model_dependency="code.generator.module.template.dependency",
)""",
                    "name": "add_module_dependency_template",
                    "decorator": "@api.multi",
                    "param": "self, module_name",
                    "sequence": 2,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_module.id,
                },
                {
                    "code": '''"""

:param module_name: list or string
:param model_dependency: string model name to operate
:return:
"""
for cg in self:
    if type(module_name) is str:
        lst_model_name = [module_name]
    elif type(module_name) is list:
        lst_model_name = module_name
    else:
        _logger.error(
            "Wrong type of model_name in method add_model_inherit:"
            f" {type(module_name)}"
        )
        return

    dependency_ids = self.env["ir.module.module"].search(
        [("name", "in", lst_model_name)]
    )
    for dependency in dependency_ids:
        check_duplicate = self.env[model_dependency].search(
            [
                ("module_id", "=", cg.id),
                ("depend_id", "=", dependency.id),
            ]
        )
        if not check_duplicate:
            value = {
                "module_id": cg.id,
                "depend_id": dependency.id,
                "name": dependency.display_name,
            }
            self.env[model_dependency].create(value)''',
                    "name": "add_module_dependency",
                    "decorator": "@api.multi",
                    "param": (
                        "self, module_name,"
                        " model_dependency='code.generator.module.dependency'"
                    ),
                    "sequence": 3,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_module.id,
                },
                {
                    "code": """for module in self:
    module.o2m_model_access = module.o2m_models.mapped("access_ids")
    module.o2m_model_rules = module.o2m_models.mapped("rule_ids")
    module.o2m_model_constraints = module.o2m_models.mapped(
        "o2m_constraints"
    )
    module.o2m_model_views = module.o2m_models.mapped("view_ids")
    module.o2m_model_act_window = module.o2m_models.mapped(
        "o2m_act_window"
    )
    module.o2m_model_act_server = module.o2m_models.mapped(
        "o2m_server_action"
    )
    module.o2m_model_server_constrains = module.o2m_models.mapped(
        "o2m_server_constrains"
    )
    module.o2m_model_reports = module.o2m_models.mapped("o2m_reports")""",
                    "name": "_get_models_info",
                    "decorator": '@api.depends("o2m_models")',
                    "param": "self",
                    "sequence": 4,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_module.id,
                },
                {
                    "code": """for module in self:
    if module.name and module.description:
        path = modules.get_module_resource(
            module.name, "static/description/index.html"
        )
        if path:
            with tools.file_open(path, "rb") as desc_file:
                doc = desc_file.read()
                html = lxml.html.document_fromstring(doc)
                for element, attribute, link, pos in html.iterlinks():
                    if (
                        element.get("src")
                        and "//" not in element.get("src")
                        and "static/" not in element.get("src")
                    ):
                        element.set(
                            "src",
                            "/%s/static/description/%s"
                            % (module.name, element.get("src")),
                        )
                module.description_html = tools.html_sanitize(
                    lxml.html.tostring(html)
                )
        else:
            overrides = {
                "embed_stylesheet": False,
                "doctitle_xform": False,
                "output_encoding": "unicode",
                "xml_declaration": False,
                "file_insertion_enabled": False,
            }
            output = publish_string(
                source=module.description
                if not module.application and module.description
                else "",
                settings_overrides=overrides,
                writer=MyWriter(),
            )
            module.description_html = tools.html_sanitize(output)""",
                    "name": "_get_desc",
                    "decorator": '@api.depends("name", "description")',
                    "param": "self",
                    "sequence": 5,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_module.id,
                },
                {
                    "code": """for module in self:
    # module.icon_image = ""
    if module.icon:
        path_parts = module.icon.split("/")
        # TODO this is broken ??
        # path = modules.get_module_resource(
        #     path_parts[0], *path_parts[1:]
        # )
        path = modules.get_module_resource(
            path_parts[1], *path_parts[2:]
        )
    else:
        path = modules.module.get_module_icon(module.name)
        path = path[1:]
    if path:
        with tools.file_open(path, "rb") as image_file:
            module.icon_image = base64.b64encode(image_file.read())""",
                    "name": "_get_icon_image",
                    "decorator": '@api.depends("icon")',
                    "param": "self",
                    "sequence": 6,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_module.id,
                },
                {
                    "code": """if dct_field:
    for field_name, field_info in dct_field.items():
        if (
            field_info.get("is_show_whitelist_model_inherit") is None
            and field_info.get("is_hide_blacklist_model_inherit")
            is None
        ):
            field_info["is_show_whitelist_model_inherit"] = True
model_id = self.env["ir.model"].search([("model", "=", model_model)])
if model_name is None:
    model_name = model_model.replace(".", "_")
# Check if exist or create it
if model_id:
    model_id.m2o_module = self.id

    if dct_field:
        for field_name, field_info in dct_field.items():
            if field_info.get("ttype") == "many2many":
                self._check_relation_many2many(model_model, field_info)
            field_id = self.env["ir.model.fields"].search(
                [
                    ("model", "=", model_model),
                    ("name", "=", field_name),
                ]
            )
            if not field_id:
                value_ir_model_fields = {
                    "name": field_name,
                    "model": model_model,
                    "model_id": model_id.id,
                }
                for key in field_info.keys():
                    self._update_dict(
                        key,
                        field_info,
                        value_ir_model_fields,
                    )
                self.env["ir.model.fields"].create(
                    value_ir_model_fields
                )
            else:
                value_ir_model_fields = {
                    "m2o_fields": field_id.id,
                }
                # TODO update all field with getter
                self._update_dict(
                    "filter_field_attribute",
                    field_info,
                    value_ir_model_fields,
                )
                self._update_dict(
                    "code_generator_compute",
                    field_info,
                    value_ir_model_fields,
                )
                self._update_dict(
                    "default_lambda",
                    field_info,
                    value_ir_model_fields,
                )

                self.env["code.generator.ir.model.fields"].create(
                    value_ir_model_fields
                )
else:
    has_field_name = False
    # Update model values
    value = {
        "name": model_name,
        "model": model_model,
        "m2o_module": self.id,
    }
    if dct_model:
        for key in dct_model.keys():
            self._update_dict(
                key,
                dct_model,
                value,
            )
    else:
        dct_model = {}
    rec_name = dct_model.get("rec_name")
    has_already_rec_name = False
    if not rec_name:
        rec_name = "name"
    else:
        has_already_rec_name = True

    # Update fields values
    lst_field_value = []
    if dct_field:
        for field_name, field_info in dct_field.items():
            if field_info.get("ttype") == "many2many":
                self._check_relation_many2many(model_model, field_info)

            if field_name == rec_name:
                has_field_name = True

            field_id = self.env["ir.model.fields"].search(
                [
                    ("model", "=", model_model),
                    ("name", "=", field_name),
                ]
            )
            if not field_id:
                value_field_id = {
                    "name": field_name,
                }
                for key in field_info.keys():
                    self._update_dict(
                        key,
                        field_info,
                        value_field_id,
                    )

                lst_field_value.append((0, 0, value_field_id))
            else:
                _logger.error("What to do with existing field?")

    if lst_field_value:
        value["field_id"] = lst_field_value

    if not has_already_rec_name:
        if has_field_name:
            value["rec_name"] = "name"
        elif not dct_field:
            # TODO this will create x_name field
            # value["rec_name"] = None
            value["rec_name"] = "name"
            # value["field_id"] = {"name": {"name": "name", "ttype": "char"}}
            value["field_id"] = [
                (
                    0,
                    0,
                    {
                        "name": "name",
                        "field_description": "Name",
                        "ttype": "char",
                    },
                )
            ]
        else:
            _logger.error(
                f"Cannot found rec_name for model {model_model}."
            )

    model_id = self.env["ir.model"].create(value)

# Model inherit
if lst_depend_model:
    model_id.add_model_inherit(lst_depend_model)

return model_id""",
                    "name": "add_update_model",
                    "decorator": "@api.model",
                    "param": (
                        "self, model_model, model_name=None, dct_field=None,"
                        " dct_model=None, lst_depend_model=None"
                    ),
                    "sequence": 7,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_module.id,
                },
                {
                    "code": """relation_name = field_value.get("relation")
comodel_name = relation_name.replace(".", "_")
str_model_model = model_model.replace(".", "_")
if not comodel_name:
    _logger.warning(f"Missing relation for field_value {field_value}")
else:
    # Source, file odoo/odoo/addons/base/models/ir_model.py function _custom_many2many_names
    # relation = self.env["ir.model.fields"]._custom_many2many_names(model_name, comodel_name)
    # Execution error will come from file odoo/odoo/fields.py, function check_pg_name
    relation = f"x_{comodel_name}_{str_model_model}_rel"
    if len(relation) > 63:
        _logger.warning(
            "The size is too high, please reduce size of model name"
            f" of '{model_model}' ({len(model_model)}) or"
            f" '{field_value.get('relation')}' ({len(relation_name)}),"
            " automatic relation will be broke, max 63 chars. Result"
            f" ({len(relation)}) '{relation}'"
        )""",
                    "name": "_check_relation_many2many",
                    "param": "self, model_model, field_value",
                    "sequence": 8,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_module.id,
                },
                {
                    "code": """for field_name, field_info in dct_field.items():
    if (
        field_info.get("is_show_whitelist_model_inherit") is None
        and field_info.get("is_hide_blacklist_model_inherit") is None
    ):
        field_info["is_show_whitelist_model_inherit"] = True
model_id = self.env["ir.model"].search([("model", "=", model_model)])
# Check if exist or create it
if model_id:
    model_id.m2o_module = self.id
    for field_name, field_info in dct_field.items():
        field_id = self.env["ir.model.fields"].search(
            [
                ("model", "=", model_model),
                ("name", "=", field_name),
            ]
        )
        if not field_id:
            value_field_one2many = {
                "name": field_name,
                "model": model_model,
                "model_id": model_id.id,
            }

            for key in field_info.keys():
                self._update_dict(
                    key,
                    field_info,
                    value_field_one2many,
                )

            self.env["ir.model.fields"].create(value_field_one2many)
        else:
            if "field_context" in field_info.keys():
                value_ir_model_fields = {
                    "m2o_fields": field_id.id,
                }
                # TODO find missing attribute
                self._update_dict(
                    "field_context",
                    field_info,
                    value_ir_model_fields,
                )
                self.env["code.generator.ir.model.fields"].create(
                    value_ir_model_fields
                )
            # _logger.error("What to do to update a one2many?")
else:
    _logger.error(
        f"The model '{model_model}' is not existing, need to be create"
        " before call add_update_model_one2many from"
        " CodeGeneratorModule."
    )""",
                    "name": "add_update_model_one2many",
                    "decorator": "@api.model",
                    "param": "self, model_model, dct_field",
                    "sequence": 9,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_module.id,
                },
                {
                    "code": """filter_field_attribute = field_info.get(key_name)
if filter_field_attribute:
    value_field_id[key_name] = filter_field_attribute""",
                    "name": "_update_dict",
                    "decorator": "@api.model",
                    "param": "self, key_name, field_info, value_field_id",
                    "sequence": 10,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_module.id,
                },
                {
                    "code": """if "icon" in vals.keys():
    icon_path = vals["icon"]

    if icon_path and os.path.isfile(icon_path):
        with tools.file_open(icon_path, "rb") as image_file:
            vals["icon_image"] = base64.b64encode(image_file.read())
return super(models.Model, self).create(vals)""",
                    "name": "create",
                    "decorator": "@api.model",
                    "param": "self, vals",
                    "sequence": 11,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_module.id,
                },
                {
                    "code": """o2m_models = self.mapped("o2m_models")
if o2m_models:
    o2m_models.mapped("view_ids").unlink()
    o2m_models.unlink()  # I need to delete the created tables
return super(CodeGeneratorModule, self).unlink()""",
                    "name": "unlink",
                    "decorator": "@api.multi",
                    "param": "self",
                    "sequence": 12,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_module.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Generate server action
        # action_server view
        act_server_id = env["ir.actions.server"].search(
            [
                ("name", "=", "Generate code"),
                ("model_id", "=", model_code_generator_module.id),
            ]
        )
        if not act_server_id:
            act_server_id = env["ir.actions.server"].create(
                {
                    "name": "Generate code",
                    "model_id": model_code_generator_module.id,
                    "binding_model_id": model_code_generator_module.id,
                    "state": "code",
                    "code": """
if records:
    action = {"type": "ir.actions.act_url", "target": "self", "url": "/code_generator/%s" % ','.join(records.mapped(lambda r: str(r.id)))}
    """,
                }
            )

            # Add record id name
            env["ir.model.data"].create(
                {
                    "name": "code_generator_module_actionserver",
                    "model": "ir.actions.server",
                    "module": MODULE_NAME,
                    "res_id": act_server_id.id,
                    "noupdate": True,
                }
            )

        # Add/Update Code Generator Module Dependency
        model_model = "code.generator.module.dependency"
        model_name = "code_generator_module_dependency"
        lst_depend_model = ["ir.module.module.dependency"]
        dct_model = {
            "description": "Code Generator Module Dependency",
        }
        dct_field = {
            "depend_id": {
                "code_generator_sequence": 3,
                "field_description": "Dependency",
                "relation": "ir.module.module",
                "ttype": "many2one",
            },
            "module_id": {
                "code_generator_sequence": 4,
                "field_description": "Module",
                "relation": "code.generator.module",
                "ttype": "many2one",
            },
        }
        model_code_generator_module_dependency = (
            code_generator_id.add_update_model(
                model_model,
                model_name,
                dct_field=dct_field,
                dct_model=dct_model,
                lst_depend_model=lst_depend_model,
            )
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_module_dependency.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Code Generator Module External Dependency
        model_model = "code.generator.module.external.dependency"
        model_name = "code_generator_module_external_dependency"
        dct_model = {
            "description": "Code Generator Module External Dependency",
        }
        dct_field = {
            "application_type": {
                "code_generator_sequence": 2,
                "default": "python",
                "field_description": "Application Type",
                "selection": "[('python', 'python'), ('bin', 'bin')]",
                "ttype": "selection",
            },
            "depend": {
                "code_generator_sequence": 3,
                "field_description": "Dependency name",
                "ttype": "char",
            },
            "is_template": {
                "code_generator_sequence": 4,
                "field_description": "Is template",
                "help": "Will be affect template module.",
                "ttype": "boolean",
            },
            "module_id": {
                "code_generator_sequence": 5,
                "field_description": "Module",
                "relation": "code.generator.module",
                "ttype": "many2one",
            },
        }
        model_code_generator_module_external_dependency = (
            code_generator_id.add_update_model(
                model_model,
                model_name,
                dct_field=dct_field,
                dct_model=dct_model,
            )
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_module_external_dependency.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Code Generator Module Template Dependency
        model_model = "code.generator.module.template.dependency"
        model_name = "code_generator_module_template_dependency"
        lst_depend_model = ["ir.module.module.dependency"]
        dct_model = {
            "description": (
                "Code Generator Module Template Dependency, set by"
                " code_generator_template"
            ),
        }
        dct_field = {
            "depend_id": {
                "code_generator_sequence": 3,
                "field_description": "Dependency",
                "relation": "ir.module.module",
                "ttype": "many2one",
            },
            "module_id": {
                "code_generator_sequence": 4,
                "field_description": "Module",
                "relation": "code.generator.module",
                "ttype": "many2one",
            },
        }
        model_code_generator_module_template_dependency = (
            code_generator_id.add_update_model(
                model_model,
                model_name,
                dct_field=dct_field,
                dct_model=dct_model,
                lst_depend_model=lst_depend_model,
            )
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_module_template_dependency.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Code Generator Pyclass
        model_model = "code.generator.pyclass"
        model_name = "code_generator_pyclass"
        dct_model = {
            "description": "Code Generator Python Class",
        }
        dct_field = {
            "module": {
                "code_generator_sequence": 3,
                "field_description": "Class path",
                "help": "Class path",
                "ttype": "char",
            },
            "name": {
                "code_generator_sequence": 2,
                "field_description": "Class name",
                "help": "Class name",
                "required": True,
                "ttype": "char",
            },
        }
        model_code_generator_pyclass = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_pyclass.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Code Generator View
        model_model = "code.generator.view"
        model_name = "code_generator_view"
        dct_model = {
            "description": "Code Generator View",
        }
        dct_field = {
            "code_generator_id": {
                "code_generator_sequence": 2,
                "field_description": "Code Generator",
                "relation": "code.generator.module",
                "required": True,
                "ttype": "many2one",
            },
            "has_body_sheet": {
                "code_generator_sequence": 3,
                "field_description": "Sheet format",
                "help": "Use sheet presentation for body of form view.",
                "ttype": "boolean",
            },
            "id_name": {
                "code_generator_sequence": 4,
                "field_description": "View id",
                "help": "Specify id name of this view.",
                "ttype": "char",
            },
            "inherit_view_name": {
                "code_generator_sequence": 5,
                "field_description": "Inherit View Name",
                "help": (
                    "Set inherit view name, use record id (ir.model.data)."
                ),
                "ttype": "char",
            },
            "m2o_model": {
                "code_generator_sequence": 6,
                "field_description": "Code generator Model",
                "help": "Model related with this report",
                "relation": "ir.model",
                "ttype": "many2one",
            },
            "view_attr_class": {
                "code_generator_sequence": 7,
                "field_description": "Class attribute",
                "ttype": "char",
            },
            "view_attr_string": {
                "code_generator_sequence": 8,
                "field_description": "String attribute",
                "ttype": "char",
            },
            "view_item_ids": {
                "code_generator_sequence": 9,
                "field_description": "View item",
                "help": "Item view to add in this view.",
                "relation": "code.generator.view.item",
                "ttype": "many2many",
            },
            "view_name": {
                "code_generator_sequence": 10,
                "field_description": "View name",
                "ttype": "char",
            },
            "view_type": {
                "code_generator_sequence": 11,
                "default": "form",
                "field_description": "View Type",
                "help": "Choose view type to generate.",
                "selection": (
                    "[('activity', 'Activity'), ('calendar', 'Calendar'),"
                    " ('diagram', 'Diagram'), ('form', 'Form'), ('graph',"
                    " 'Graph'), ('kanban', 'Kanban'), ('pivot', 'Pivot'),"
                    " ('search', 'Search'), ('timeline', 'Timeline'), ('tree',"
                    " 'Tree')]"
                ),
                "ttype": "selection",
            },
        }
        model_code_generator_view = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_view.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Code Generator View Item
        model_model = "code.generator.view.item"
        model_name = "code_generator_view_item"
        dct_model = {
            "description": "Code Generator View Item",
        }
        dct_field = {
            "action_name": {
                "code_generator_sequence": 3,
                "field_description": "Action name",
                "ttype": "char",
            },
            "aria_label": {
                "code_generator_sequence": 4,
                "field_description": "Aria Label",
                "help": "aria-label attribute",
                "ttype": "char",
            },
            "attrs": {
                "code_generator_sequence": 5,
                "field_description": "Attributes",
                "help": (
                    "Specific condition, search attrs for more information."
                ),
                "ttype": "char",
            },
            "background_type": {
                "code_generator_sequence": 6,
                "field_description": "Background Type",
                "help": "Choose background color of HTML.",
                "selection": (
                    "[('', ''), ('bg-success', 'Success'), ('bg-success-full',"
                    " 'Success full'), ('bg-warning', 'Warning'),"
                    " ('bg-warning-full', 'Warning full'), ('bg-info',"
                    " 'Info'), ('bg-info-full', 'Info full'), ('bg-danger',"
                    " 'Danger'), ('bg-danger-full', 'Danger full'),"
                    " ('bg-light', 'Light'), ('bg-dark', 'Dark')]"
                ),
                "ttype": "selection",
            },
            "button_type": {
                "code_generator_sequence": 7,
                "field_description": "Button Type",
                "help": "Choose item type to generate.",
                "selection": (
                    "[('', ''), ('btn-default', 'Default'), ('btn-primary',"
                    " 'Primary'), ('btn-secondary', 'Secondary'), ('btn-link',"
                    " 'Link'), ('btn-success', 'Success'), ('btn-warning',"
                    " 'Warning'), ('btn-danger', 'Danger'), ('oe_highlight',"
                    " 'Highlight'), ('oe_stat_button', 'Statistic')]"
                ),
                "ttype": "selection",
            },
            "class_attr": {
                "code_generator_sequence": 9,
                "field_description": "Class Attr",
                "help": "Update class attribute",
                "ttype": "char",
            },
            "colspan": {
                "code_generator_sequence": 10,
                "default": 1,
                "field_description": "Colspan",
                "help": "Use this to fill more column, check HTML table.",
                "ttype": "integer",
            },
            "context": {
                "code_generator_sequence": 11,
                "field_description": "Context",
                "help": "context attribute",
                "ttype": "char",
            },
            "domain": {
                "code_generator_sequence": 12,
                "field_description": "Domain",
                "help": "domain attribute",
                "ttype": "char",
            },
            "edit_only": {
                "code_generator_sequence": 13,
                "field_description": "Edit only",
                "ttype": "boolean",
            },
            "expr": {
                "code_generator_sequence": 14,
                "field_description": "Expr",
                "help": "Example: //field[@name='name']",
                "ttype": "char",
            },
            "has_label": {
                "code_generator_sequence": 15,
                "field_description": "Labeled",
                "help": "Label for title.",
                "ttype": "boolean",
            },
            "icon": {
                "code_generator_sequence": 16,
                "field_description": "Icon",
                "help": "Example fa-television. Only supported with button.",
                "ttype": "char",
            },
            "is_help": {
                "code_generator_sequence": 17,
                "field_description": "Help",
                "ttype": "boolean",
            },
            "is_invisible": {
                "code_generator_sequence": 18,
                "field_description": "Invisible",
                "ttype": "boolean",
            },
            "is_readonly": {
                "code_generator_sequence": 19,
                "field_description": "Readonly",
                "ttype": "boolean",
            },
            "is_required": {
                "code_generator_sequence": 20,
                "field_description": "Required",
                "ttype": "boolean",
            },
            "item_type": {
                "code_generator_sequence": 21,
                "default": "field",
                "field_description": "Item Type",
                "help": "Choose item type to generate.",
                "selection": (
                    "[('field', 'Field'), ('button', 'Button'), ('html',"
                    " 'HTML'), ('filter', 'Filter'), ('div', 'Division'),"
                    " ('group', 'Group'), ('xpath', 'Xpath'), ('templates',"
                    " 'Templates'), ('t', 'T'), ('ul', 'UL'), ('li', 'LI'),"
                    " ('i', 'I'), ('strong', 'Strong')]"
                ),
                "ttype": "selection",
            },
            "label": {
                "code_generator_sequence": 22,
                "field_description": "Label",
                "ttype": "char",
            },
            "name": {
                "code_generator_sequence": 2,
                "field_description": "Name",
                "help": "name attribute",
                "ttype": "char",
            },
            "parent_id": {
                "code_generator_sequence": 23,
                "field_description": "Parent",
                "relation": "code.generator.view.item",
                "ttype": "many2one",
            },
            "password": {
                "code_generator_sequence": 24,
                "field_description": "Password",
                "help": "Hide character.",
                "ttype": "boolean",
            },
            "placeholder": {
                "code_generator_sequence": 25,
                "field_description": "Placeholder",
                "ttype": "char",
            },
            "position": {
                "code_generator_sequence": 26,
                "field_description": "Position",
                "selection": (
                    "[('inside', 'Inside'), ('replace', 'Replace'), ('after',"
                    " 'After'), ('before', 'Before'), ('attributes',"
                    " 'Attributes'), ('move', 'Move')]"
                ),
                "ttype": "selection",
            },
            "role": {
                "code_generator_sequence": 27,
                "field_description": "Role",
                "help": "role attribute",
                "ttype": "char",
            },
            "section_type": {
                "code_generator_sequence": 28,
                "default": "body",
                "field_description": "Section Type",
                "help": "Choose item type to generate.",
                "selection": (
                    "[('header', 'Header'), ('title', 'Title'), ('body',"
                    " 'Body'), ('footer', 'Footer')]"
                ),
                "ttype": "selection",
            },
            "sequence": {
                "code_generator_sequence": 29,
                "default": 1,
                "field_description": "Sequence",
                "ttype": "integer",
            },
            "t_attf_class": {
                "code_generator_sequence": 30,
                "field_description": "T Attf Class",
                "help": "t-attf-class attribute",
                "ttype": "char",
            },
            "t_if": {
                "code_generator_sequence": 31,
                "field_description": "T If",
                "help": "t-if attribute",
                "ttype": "char",
            },
            "t_name": {
                "code_generator_sequence": 32,
                "field_description": "T Name",
                "help": "t_name attribute",
                "ttype": "char",
            },
            "title": {
                "code_generator_sequence": 33,
                "field_description": "Title",
                "help": "title attribute",
                "ttype": "char",
            },
            "type": {
                "code_generator_sequence": 34,
                "field_description": "Type",
                "help": "Statistique type.",
                "selection": (
                    "[('row', 'Row'), ('col', 'Col'), ('measure', 'Measure')]"
                ),
                "ttype": "selection",
            },
            "widget": {
                "code_generator_sequence": 35,
                "field_description": "Widget",
                "help": "widget attribute",
                "ttype": "char",
            },
        }
        model_code_generator_view_item = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_view_item.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Code Generator Writer
        model_model = "code.generator.writer"
        model_name = "code_generator_writer"
        dct_model = {
            "description": "Code Generator Writer",
        }
        dct_field = {
            "basename": {
                "code_generator_sequence": 2,
                "field_description": "Base name",
                "ttype": "char",
            },
            "code_generator_ids": {
                "code_generator_sequence": 3,
                "field_description": "Code Generator",
                "relation": "code.generator.module",
                "ttype": "many2many",
            },
            "list_path_file": {
                "code_generator_sequence": 4,
                "field_description": "List path file",
                "help": "Value are separated by ;",
                "ttype": "char",
            },
            "rootdir": {
                "code_generator_sequence": 5,
                "field_description": "Root dir",
                "ttype": "char",
            },
        }
        model_code_generator_writer = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """import ast
import base64
import glob
import hashlib
import io
import logging
import os
import shutil
import tempfile
import uuid
from collections import defaultdict

import unidecode
from code_writer import CodeWriter
from lxml import etree as ET
from lxml.builder import E
from PIL import Image

from odoo import api, fields, models
from odoo.models import MAGIC_COLUMNS
from odoo.tools.misc import mute_logger

from ..code_generator_data import CodeGeneratorData
from ..extractor_controller import ExtractorController
from ..extractor_module import ExtractorModule
from ..extractor_view import ExtractorView
from ..python_controller_writer import PythonControllerWriter

_logger = logging.getLogger(__name__)

UNDEFINEDMESSAGE = "Restriction message not yet define."
MAGIC_FIELDS = MAGIC_COLUMNS + [
    "display_name",
    "__last_update",
    "access_url",
    "access_token",
    "access_warning",
]
MODULE_NAME = "code_generator"
BLANK_LINE = [""]
BREAK_LINE_OFF = "\\n"
BREAK_LINE = ["\\n"]
XML_VERSION_HEADER = '<?xml version="1.0" encoding="utf-8"?>' + BREAK_LINE_OFF
XML_VERSION = ['<?xml version="1.0" encoding="utf-8"?>']
XML_VERSION_STR = '<?xml version="1.0"?>\\n'
XML_ODOO_OPENING_TAG = ["<odoo>"]
XML_HEAD = XML_VERSION + XML_ODOO_OPENING_TAG
XML_ODOO_CLOSING_TAG = ["</odoo>"]
FROM_ODOO_IMPORTS = ["from odoo import _, api, models, fields"]
MODEL_HEAD = FROM_ODOO_IMPORTS + BREAK_LINE
FROM_ODOO_IMPORTS_SUPERUSER = [
    "from odoo import _, api, models, fields, SUPERUSER_ID"
]
MODEL_SUPERUSER_HEAD = FROM_ODOO_IMPORTS_SUPERUSER + BREAK_LINE""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_code_generator_writer.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """return word.lower().replace(".", "_")""",
                    "name": "_fmt_underscores",
                    "decorator": "@staticmethod",
                    "param": "word",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """return word.replace(".", "_").title().replace("_", "")""",
                    "name": "_fmt_camel",
                    "decorator": "@staticmethod",
                    "param": "word",
                    "sequence": 1,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """return word.replace(".", " ").title()""",
                    "name": "_fmt_title",
                    "decorator": "@staticmethod",
                    "param": "word",
                    "sequence": 2,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Util function to get a list of a map operation
:param fn:
:param collection:
:return:
"""

return list(map(fn, collection))''',
                    "name": "_get_l_map",
                    "decorator": "@staticmethod",
                    "param": "fn, collection",
                    "sequence": 3,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Util function to get a model class name representation from a model name (code.generator -> CodeGenerator)
:param model:
:return:
"""

result = []
bypoint = model.split(".")
for byp in bypoint:
    result += byp.split("_")
return "".join(self._get_l_map(lambda e: e.capitalize(), result))''',
                    "name": "_get_class_name",
                    "param": "self, model",
                    "sequence": 4,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Util function to replace and get the lower content of a string
:param string:
:return:
"""

v = (
    str(string)
    .lower()
    .replace(replacee, replacer)
    .replace("-", "_")
    .replace(".", "_")
    .replace("'", "_")
    .replace("`", "_")
    .replace("^", "_")
)
new_v = v.strip("_")

while new_v.count("__"):
    new_v = new_v.replace("__", "_")
return unidecode.unidecode(new_v)''',
                    "name": "_lower_replace",
                    "decorator": "@staticmethod",
                    "param": "string, replacee=' ', replacer='_'",
                    "sequence": 5,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Util function to get a model res_id-like representation (code.generator -> code_generator)
:param model_model:
:param replacee:
:return:
"""
return self._lower_replace(model_model, replacee=replacee)''',
                    "name": "_get_model_model",
                    "param": "self, model_model, replacee='.'",
                    "sequence": 6,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Util function to get the Python Classes for inheritance
:param model:
:return:
"""

class_4inherit = (
    "models.TransientModel"
    if model.transient
    else (
        "models.AbstractModel" if model._abstract else "models.Model"
    )
)
if model.m2o_inherit_py_class.name:
    class_4inherit += ", %s" % model.m2o_inherit_py_class.name

return class_4inherit''',
                    "name": "_get_python_class_4inherit",
                    "decorator": "@staticmethod",
                    "param": "model",
                    "sequence": 7,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Util function to get a field class name from a field type (char -> Char, many2one -> Many2one)
:param ttype:
:return:
"""

return f"fields.{self._get_class_name(ttype)}"''',
                    "name": "_get_odoo_ttype_class",
                    "param": "self, ttype",
                    "sequence": 8,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Util function to count the starting spaces of a string
:param compute_line:
:return:
"""

space_counter = 0
for character in compute_line:
    if character.isspace():
        space_counter += 1

    else:
        break

return space_counter''',
                    "name": "_get_starting_spaces",
                    "decorator": "@staticmethod",
                    "param": "compute_line",
                    "sequence": 9,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Util function to truncate (to 64 characters) an xml_id
:param xmlid:
:return:
"""

# if 64 - len(xmlid) < 0:
#     new_xml_id = "%s..." % xmlid[: 61 - len(xmlid)]
#     _logger.warning(
#         f"Slice xml_id {xmlid} to {new_xml_id} because length is upper"
#         " than 63."
#     )
# else:
#     new_xml_id = xmlid
# return new_xml_id
return xmlid''',
                    "name": "_set_limit_4xmlid",
                    "decorator": "@staticmethod",
                    "param": "xmlid",
                    "sequence": 10,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""

:param l_fields:
:return:
"""

counter = 1
prepared = ""
for field in l_fields:
    prepared += "'%s'%s" % (
        field,
        ", " if counter < len(l_fields) else "",
    )
    counter += 1

return prepared''',
                    "name": "_prepare_compute_constrained_fields",
                    "decorator": "@staticmethod",
                    "param": "l_fields",
                    "sequence": 11,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to obtain the model constrains
:param model:
:return:
"""

if model.o2m_server_constrains:

    cw.emit()

    for sconstrain in model.o2m_server_constrains:
        l_constrained = self._get_l_map(
            lambda e: e.strip(), sconstrain.constrained.split(",")
        )

        cw.emit(
            f"@api.constrains({self._prepare_compute_constrained_fields(l_constrained)})"
        )
        cw.emit(f"def _check_{'_'.join(l_constrained)}(self):")

        l_code = sconstrain.txt_code.split("\\n")
        with cw.indent():
            for line in l_code:
                cw.emit(line.rstrip())
        # starting_spaces = 2
        # for line in l_code:
        #     if self._get_starting_spaces(line) == 2:
        #         starting_spaces += 1
        #     l_model_constrains.append('%s%s' % (TAB4 * starting_spaces, line.strip()))
        #     starting_spaces = 2

        cw.emit()

    cw.emit()

constraints_id = None
if model.o2m_constraints:
    # TODO how to use this way? binding model not working
    constraints_id = model.o2m_constraints
elif module.o2m_model_constraints:
    constraints_id = module.o2m_model_constraints

if constraints_id:
    lst_constraint = []
    for constraint in constraints_id:
        constraint_name = constraint.name.replace(
            "%s_" % self._get_model_model(model.model), ""
        )
        constraint_definition = constraint.definition
        constraint_message = (
            constraint.message
            if constraint.message
            else UNDEFINEDMESSAGE
        )

        lst_constraint.append(
            f"('{constraint_name}', '{constraint_definition}',"
            f" '{constraint_message}')"
        )

    cw.emit()
    cw.emit_list(
        lst_constraint, ("[", "]"), before="_sql_constraints = "
    )
    cw.emit()''',
                    "name": "_get_model_constrains",
                    "param": "self, cw, model, module",
                    "sequence": 12,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to set the static descriptions files
:param module:
:param application_icon:
:return:
"""

static_description_icon_path = os.path.join(
    self.code_generator_data.static_description_path, "icon.png"
)
static_description_icon_code_generator_path = os.path.join(
    self.code_generator_data.static_description_path,
    "code_generator_icon.png",
)
# TODO hack to force icon or True
if module.icon_child_image or module.icon_real_image:
    if module.icon_real_image:
        self.code_generator_data.write_file_binary(
            static_description_icon_path,
            base64.b64decode(module.icon_real_image),
        )
    if module.icon_child_image:
        self.code_generator_data.write_file_binary(
            static_description_icon_code_generator_path,
            base64.b64decode(module.icon_child_image),
        )
else:
    # elif module.icon_image:

    # TODO use this when fix loading picture, now temporary disabled and force use icon from menu
    # self.code_generator_data.write_file_binary(static_description_icon_path,
    # base64.b64decode(module.icon_image))
    # TODO temp solution with icon from menu
    icon_path = ""
    if module.icon and os.path.isfile(module.icon):
        with open(module.icon, "rb") as file:
            content = file.read()
        icon_path = module.icon
    else:
        if application_icon:
            icon_path = application_icon[
                application_icon.find(",") + 1 :
            ]
            # icon_path = application_icon.replace(",", "/")
        else:
            icon_path = "static/description/icon_new_application.png"
        icon_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", icon_path)
        )
        with open(icon_path, "rb") as file:
            content = file.read()
    if (
        module.template_module_id
        and module.template_module_id.icon_image
    ):
        if not icon_path:
            _logger.error("Icon path is empty.")
            return ""
        if not os.path.exists(icon_path):
            _logger.error(f"Icon path {icon_path} doesn't exist.")
            return ""
        # It's a template generator
        minimal_size_width = 350
        # Add logo in small corner
        logo = Image.open(
            io.BytesIO(
                base64.b64decode(module.template_module_id.icon_image)
            )
        )
        icon = Image.open(icon_path)
        # Change original size for better quality
        if logo.width < minimal_size_width:
            new_h = int(logo.height / logo.width * minimal_size_width)
            new_w = minimal_size_width
            logo = logo.resize((new_w, new_h), Image.ANTIALIAS)
        ratio = 0.3
        w = int(logo.width * ratio)
        if icon.width != icon.height:
            h = int(logo.height / logo.width * w)
        else:
            h = w
        size = w, h
        icon.thumbnail(size, Image.ANTIALIAS)
        x = logo.width - w
        logo.paste(icon, (x, 0))
        img_byte_arr = io.BytesIO()
        logo.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()

        # image = base64.b64decode(module.template_module_id.icon_image)
        self.code_generator_data.write_file_binary(
            static_description_icon_path, img_byte_arr
        )
        module.icon_real_image = base64.b64encode(img_byte_arr)
        code_generator_image = base64.b64decode(
            module.template_module_id.icon_image
        )
        module.icon_child_image = module.template_module_id.icon_image
        self.code_generator_data.write_file_binary(
            static_description_icon_code_generator_path,
            code_generator_image,
        )
    else:
        self.code_generator_data.write_file_binary(
            static_description_icon_path, content
        )
        module.icon_real_image = base64.b64encode(content)
# else:
#     static_description_icon_path = ""

return static_description_icon_path''',
                    "name": "_set_static_description_file",
                    "param": "self, module, application_icon",
                    "sequence": 13,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Util function to handle the _rec_name / rec_name access
:param record:
:param model:
:return:
"""

return (
    getattr(record, model._rec_name)
    if getattr(record, model._rec_name)
    else getattr(record, model.rec_name)
)''',
                    "name": "_get_from_rec_name",
                    "decorator": "@staticmethod",
                    "param": "record, model",
                    "sequence": 14,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """pass""",
                    "name": "set_module_init_file_extra",
                    "param": "self, module",
                    "sequence": 15,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """module_id = self.env["ir.module.module"].search(
    [("name", "=", module_name), ("state", "=", "installed")]
)
if not module_id:
    return

i18n_path = os.path.join(module_path, "i18n")
data = CodeGeneratorData(module_id, module_path)
data.check_mkdir_and_create(i18n_path, is_file=False)

# Create pot
export = self.env["base.language.export"].create(
    {"format": "po", "modules": [(6, 0, [module_id.id])]}
)

export.act_getfile()
po_file = export.data
data = base64.b64decode(po_file).decode("utf-8")
translation_file = os.path.join(i18n_path, f"{module_name}.pot")

with open(translation_file, "w") as file:
    file.write(data)

# Create po
# TODO get this info from configuration/module
# lst_lang = [
#     ("fr_CA", "fr_CA"),
#     ("fr_FR", "fr"),
#     ("en_US", "en"),
#     ("en_CA", "en_CA"),
# ]
lst_lang = [("fr_CA", "fr_CA")]
for lang_local, lang_ISO in lst_lang:
    translation_file = os.path.join(i18n_path, f"{lang_ISO}.po")

    if not self.env["ir.translation"].search(
        [("lang", "=", lang_local)]
    ):
        with mute_logger("odoo.addons.base.models.ir_translation"):
            self.env["base.language.install"].create(
                {"lang": lang_local, "overwrite": True}
            ).lang_install()
        self.env["base.update.translations"].create(
            {"lang": lang_local}
        ).act_update()

    # Load existing translations
    # translations = self.env["ir.translation"].search([
    #     ('lang', '=', lang),
    #     ('module', '=', module_name)
    # ])

    export = self.env["base.language.export"].create(
        {
            "lang": lang_local,
            "format": "po",
            "modules": [(6, 0, [module_id.id])],
        }
    )
    export.act_getfile()
    po_file = export.data
    data = base64.b64decode(po_file).decode("utf-8").strip() + "\\n"

    # Special replace for lang fr_CA
    if lang_ISO in ["fr_CA", "fr", "en", "en_CA"]:
        data = data.replace(
            '"Plural-Forms: \\\n"',
            '"Plural-Forms: nplurals=2; plural=(n > 1);\\\n"',
        )

    with open(translation_file, "w") as file:
        file.write(data)""",
                    "name": "set_module_translator",
                    "param": "self, module_name, module_path",
                    "sequence": 16,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
This function will create and copy file into template module.
:param module_name:
:param module_path:
:param template_dir:
:param lst_file_extra:
:return:
"""
# TODO bad conception, this method not suppose to be here, move this before generate code
module_id = self.env["ir.module.module"].search(
    [("name", "=", module_name), ("state", "=", "installed")]
)
if not module_id:
    return

template_copied_dir = os.path.join(template_dir, "not_supported_files")

# Copy i18n files
i18n_po_path = os.path.join(module_path, "i18n", "*.po")
i18n_pot_path = os.path.join(module_path, "i18n", "*.pot")
target_i18n_path = os.path.join(template_copied_dir, "i18n")
lst_file = glob.glob(i18n_po_path) + glob.glob(i18n_pot_path)
if lst_file:
    CodeGeneratorData.os_make_dirs(target_i18n_path)
    for file_name in lst_file:
        shutil.copy(file_name, target_i18n_path)

# Copy readme file
readme_file_path = os.path.join(module_path, "README.rst")
target_readme_file_path = os.path.join(template_copied_dir)
shutil.copy(readme_file_path, target_readme_file_path)

# Copy readme dir
readme_dir_path = os.path.join(module_path, "readme")
target_readme_dir_path = os.path.join(template_copied_dir, "readme")
shutil.copytree(readme_dir_path, target_readme_dir_path)

# Copy tests dir
tests_dir_path = os.path.join(module_path, "tests")
target_tests_dir_path = os.path.join(template_copied_dir, "tests")
shutil.copytree(tests_dir_path, target_tests_dir_path)

if lst_file_extra:
    for file_extra in lst_file_extra:
        # Special if existing, mail_message_subtype.xml
        mail_data_xml_path = os.path.join(module_path, file_extra)
        target_mail_data_xml_path = os.path.join(
            template_copied_dir, file_extra
        )
        if os.path.isfile(mail_data_xml_path):
            CodeGeneratorData.check_mkdir_and_create(
                target_mail_data_xml_path
            )
            shutil.copy(mail_data_xml_path, target_mail_data_xml_path)''',
                    "name": "copy_missing_file",
                    "param": (
                        "self, module_name, module_path, template_dir,"
                        " lst_file_extra=None"
                    ),
                    "sequence": 17,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """\"""
Function to set the module manifest file
:param module:
:return:
\"""

lang = "en_US"

cw = CodeWriter()

has_header = False
if module.header_manifest:
    lst_header = module.header_manifest.split("\\n")
    for line in lst_header:
        s_line = line.strip()
        if s_line:
            cw.emit(s_line)
            has_header = True
if has_header:
    cw.emit()

with cw.block(delim=("{", "}")):
    cw.emit(f"'name': '{module.shortdesc}',")

    if module.category_id:
        cw.emit(
            "'category':"
            f" '{module.category_id.with_context(lang=lang).name}',"
        )

    if module.summary and module.summary != "false":
        cw.emit(f"'summary': '{module.summary}',")

    if module.description:
        description = module.description.strip()
        lst_description = description.split("\\n")
        if len(lst_description) == 1:
            cw.emit(f"'description': '{description}',")
        else:
            cw.emit("'description': '''")
            for desc in lst_description:
                cw.emit_raw(desc)
            cw.emit("''',")

    if module.installed_version:
        cw.emit(f"'version': '{module.installed_version}',")

    if module.author:
        author = module.author.strip()
        lst_author = author.split(",")
        if len(lst_author) == 1:
            cw.emit(f"'author': '{author}',")
        else:
            cw.emit(f"'author': (")
            with cw.indent():
                for auth in lst_author[:-1]:
                    s_auth = auth.strip()
                    cw.emit(f"'{s_auth}, '")
            cw.emit(f"'{lst_author[-1].strip()}'),")

    if module.contributors:
        cw.emit(f"'contributors': '{module.contributors}',")

    # if module.maintener:
    #     cw.emit(f"'maintainers': '{module.maintener}',")

    if module.license != "LGPL-3":
        cw.emit(f"'license': '{module.license}',")

    if module.sequence != 100:
        cw.emit(f"'sequence': {module.sequence},")

    if module.website:
        cw.emit(f"'website': '{module.website}',")

    if module.auto_install:
        cw.emit(f"'auto_install': True,")

    if module.demo:
        cw.emit(f"'demo': True,")

    if module.application:
        cw.emit(f"'application': True,")

    if module.dependencies_id:
        lst_depend = module.dependencies_id.mapped(
            lambda did: f"'{did.depend_id.name}'"
        )
        # Remove exclude_dependencies_str
        if module.exclude_dependencies_str:
            lst_exclude_depend = [
                f"'{a}'"
                for a in module.exclude_dependencies_str.split(";")
            ]
            lst_depend = list(
                set(lst_depend) - set(lst_exclude_depend)
            )
        cw.emit_list(
            lst_depend, ("[", "]"), before="'depends': ", after=","
        )

    if module.external_dependencies_id and [
        a for a in module.external_dependencies_id if not a.is_template
    ]:
        with cw.block(
            before="'external_dependencies':",
            delim=("{", "}"),
            after=",",
        ):
            dct_depend = defaultdict(list)
            for depend in module.external_dependencies_id:
                if depend.is_template:
                    continue
                dct_depend[depend.application_type].append(
                    f"'{depend.depend}'"
                )
            for application_type, lst_value in dct_depend.items():
                cw.emit_list(
                    lst_value,
                    ("[", "]"),
                    before=f"'{application_type}': ",
                    after=",",
                )

    lst_data = self._get_l_map(
        lambda dfile: f"'{dfile}'",
        self.code_generator_data.lst_manifest_data_files,
    )
    if lst_data:
        cw.emit_list(
            lst_data, ("[", "]"), before="'data': ", after=","
        )

    cw.emit(f"'installable': True,")

    self.set_manifest_file_extra(cw, module)

manifest_file_path = "__manifest__.py"
self.code_generator_data.write_file_str(
    manifest_file_path, cw.render()
)""",
                    "name": "_set_manifest_file",
                    "param": "self, module",
                    "sequence": 18,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """pass""",
                    "name": "set_manifest_file_extra",
                    "param": "self, cw, module",
                    "sequence": 19,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to obtain the model data from a record
:param record:
:param is_internal: if False, add module name for external reference
:return:
"""

# special trick for some record
xml_id = getattr(record, "xml_id")
if xml_id:
    if is_internal:
        return xml_id.split(".")[1]
    return xml_id

if model:
    record_model = model
else:
    record_model = record.model

ir_model_data = self.env["ir.model.data"].search(
    [
        ("model", "=", record_model),
        ("res_id", "=", record.id),
    ]
)
if not ir_model_data:
    return

if is_internal:
    return ir_model_data[0].name
return f"{ir_model_data[0].module}.{ir_model_data[0].name}"''',
                    "name": "_get_id_view_model_data",
                    "param": "self, record, model=None, is_internal=False",
                    "sequence": 20,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to obtain the model data from a record
:param record:
:param give_a_default:
:param module_name:
:return:
"""

ir_model_data = self.env["ir.model.data"].search(
    [
        # TODO: Opción por valorar
        # ('module', '!=', '__export__'),
        ("model", "=", record._name),
        ("res_id", "=", record.id),
    ]
)

if ir_model_data:
    if module_name and module_name == ir_model_data[0].module:
        result = ir_model_data[0].name
    else:
        result = f"{ir_model_data[0].module}.{ir_model_data[0].name}"
elif give_a_default:
    if force_field_name:
        name_v = getattr(record, force_field_name)
        second = self._lower_replace(name_v)
    elif record._rec_name:
        rec_name_v = getattr(record, record._rec_name)
        if not rec_name_v:
            rec_name_v = uuid.uuid1().int
        second = self._lower_replace(rec_name_v)
    else:
        second = uuid.uuid1().int
    result = self._set_limit_4xmlid(
        f"{self._get_model_model(record._name)}_{second}"
    )
    # Check if name already exist
    model_data_exist = self.env["ir.model.data"].search(
        [("name", "=", result)]
    )
    new_result = result
    i = 0
    while model_data_exist:
        i += 1
        new_result = f"{result}_{i}"
        model_data_exist = self.env["ir.model.data"].search(
            [("name", "=", new_result)]
        )

    self.env["ir.model.data"].create(
        {
            "name": new_result,
            "model": record._name,
            "module": module_name,
            "res_id": record.id,
            "noupdate": True,  # If it's False, target record (res_id) will be removed while module update
        }
    )
    result = new_result
else:
    result = False

# Need to limit to 128 char, else can crash like when loading i18n po and id is too long
if type(result) is str:
    # Remove strange char
    # TODO find another way to remove not alpha numeric char, but accept '_'
    result = (
        result.replace(",", "")
        .replace("'", "")
        .replace('"', "")
        .replace("(", "")
        .replace(")", "")
    )
    # TODO maybe check duplicate
    return result[:120]
return result''',
                    "name": "_get_ir_model_data",
                    "param": (
                        "self, record, give_a_default=False, module_name='',"
                        " force_field_name=None"
                    ),
                    "sequence": 21,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to obtain the res_id-like group name (Code Generator / Manager -> code_generator_manager)
:param group:
:return:
"""

return (
    self._get_ir_model_data(group)
    if self._get_ir_model_data(group)
    else self._lower_replace(group.name.replace(" /", ""))
)''',
                    "name": "_get_group_data_name",
                    "param": "self, group",
                    "sequence": 22,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to obtain the res_id-like model name (code.generator.module -> code_generator_module)
:param model:
:return:
"""

return (
    self._get_ir_model_data(model, module_name=module_name)
    if self._get_ir_model_data(model, module_name=module_name)
    else "model_%s" % self._get_model_model(model.model)
)''',
                    "name": "_get_model_data_name",
                    "param": "self, model, module_name=''",
                    "sequence": 23,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to obtain the res_id-like view name
:param view:
:return:
"""

return (
    self._get_ir_model_data(view)
    if self._get_ir_model_data(view)
    else "%s_%sview" % (self._get_model_model(view.model), view.type)
)''',
                    "name": "_get_view_data_name",
                    "param": "self, view",
                    "sequence": 24,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to obtain the res_id-like action name
:param action:
:param server:
:param creating:
:return:
"""

if not creating and self._get_ir_model_data(
    action, module_name=module.name
):
    action_name = self._get_ir_model_data(
        action, module_name=module.name
    )
    if not module or "." not in action_name:
        return action_name
    lst_action = action_name.split(".")
    if module.name == lst_action[0]:
        # remove internal name
        return lst_action[1]
    # link is external
    return action_name

else:
    model = (
        getattr(action, "res_model")
        if not server
        else getattr(action, "model_id").model
    )
    model_model = self._get_model_model(model)
    action_type = "action_window" if not server else "server_action"

    new_action_name = action.name
    # TODO No need to support limit of 64, why this code?
    # new_action_name = self._set_limit_4xmlid(
    #     "%s" % action.name[: 64 - len(model_model) - len(action_type)]
    # )

    result_name = f"{model_model}_{self._lower_replace(new_action_name)}_{action_type}"

    # if new_action_name != action.name:
    #     _logger.warning(
    #         f"Slice action name {action.name} to"
    #         f" {new_action_name} because length is upper than 63."
    #         f" Result: {result_name}."
    #     )

    return result_name''',
                    "name": "_get_action_data_name",
                    "param": (
                        "self, action, server=False, creating=False,"
                        " module=None"
                    ),
                    "sequence": 25,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to obtain the res_id-like action name
:param action:
:return:
"""
return f"action_{self._lower_replace(action.name)}"''',
                    "name": "_get_action_act_url_name",
                    "param": "self, action",
                    "sequence": 26,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to obtain the res_id-like menu name
:param menu:
:return:
"""

menu_name = self._get_ir_model_data(menu, module_name=module.name)
if menu_name:
    if "." in menu_name:
        module_name, menu_name_short = menu_name.split(".")
        if ignore_module or (
            ignore_module_name and ignore_module_name == module_name
        ):
            return menu_name_short
    return menu_name
return self._lower_replace(menu.name)''',
                    "name": "_get_menu_data_name",
                    "param": (
                        "self, menu, ignore_module=False,"
                        " ignore_module_name=None, module=None"
                    ),
                    "sequence": 27,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to set the module data file
:param module:
:param model:
:param model_model:
:return:
"""

expression_export_data = model.expression_export_data
if not expression_export_data:
    search = []
elif expression_export_data[0] == "[":
    search = ast.literal_eval(expression_export_data)
else:
    search = [ast.literal_eval(expression_export_data)]
# Search with active_test to support when active is False
nomenclador_data = (
    self.env[model.model]
    .sudo()
    .with_context(active_test=False)
    .search(search)
)
if not nomenclador_data:
    return

ignore_name_export_data = model.ignore_name_export_data
if ignore_name_export_data:
    lst_ignore_name_export_data = ignore_name_export_data.strip(
        ";"
    ).split(";")
    if lst_ignore_name_export_data:
        new_nomenclator_data_list = [
            a.id
            for b in lst_ignore_name_export_data
            for a in nomenclador_data
            if not a.name.split("/")[-1].endswith(b.strip())
            and not a.name == b.strip()
        ]
        if len(new_nomenclator_data_list) != len(nomenclador_data):
            nomenclador_data = self.env[model.model].browse(
                new_nomenclator_data_list
            )

lst_data_xml = []
lst_id = []
lst_depend = []
lst_field_id_blacklist = [
    a.m2o_fields.id
    for a in model.m2o_module.o2m_nomenclator_blacklist_fields
]
lst_field_id_whitelist = [
    a.m2o_fields.id
    for a in model.m2o_module.o2m_nomenclator_whitelist_fields
]
lst_record = []
lst_new_data_to_write = []
dct_search_and_replace_in_file = defaultdict(list)
lst_scss_process_hook = []
for record in nomenclador_data:
    add_scss_hook = False
    new_data_to_write = None
    force_field_name_xml_id = None
    f2exports = model.field_id.filtered(
        lambda field: field.name not in MAGIC_FIELDS
    )
    lst_field = []
    lst_end_field = []
    lst_ignore_field_name = []
    for rfield in f2exports:
        # whitelist check
        if (
            lst_field_id_whitelist
            and rfield.id not in lst_field_id_whitelist
        ):
            continue
        # blacklist check
        if rfield.id in lst_field_id_blacklist:
            continue
        if rfield.name in lst_ignore_field_name:
            continue
        record_value = getattr(record, rfield.name)
        child = None
        if record_value or (
            not record_value
            and rfield.ttype == "boolean"
            and rfield.default == "True"
        ):
            delete_node = False
            if rfield.ttype == "many2one":
                ref = self._get_ir_model_data(
                    record_value,
                    give_a_default=True,
                    module_name=module.name,
                )
                if not ref:
                    # This will cause an error at installation
                    _logger.error(
                        "Cannot find reference for field"
                        f" {rfield.name} model {model_model}"
                    )
                    continue
                child = E.field({"name": rfield.name, "ref": ref})

                if "." not in ref:
                    lst_depend.append(ref)

            elif rfield.ttype == "one2many":
                # TODO do we need to export one2many relation data, it's better to export many2one
                # TODO maybe check if many2one is exported or export this one
                continue
                # field_eval = ", ".join(
                #     record_value.mapped(
                #         lambda rvalue: "(4, ref('%s'))"
                #         % self._get_ir_model_data(
                #             rvalue, give_a_default=True, module_name=module.name
                #         )
                #     )
                # )
                # child = E.field(
                #     {"name": rfield.name, "eval": f"[{field_eval}]"}
                # )

            elif rfield.ttype == "many2many":
                # TODO add dependencies id in lst_depend
                field_eval = ", ".join(
                    record_value.mapped(
                        lambda rvalue: "ref(%s)"
                        % self._get_ir_model_data(
                            rvalue,
                            give_a_default=True,
                            module_name=module.name,
                        )
                    )
                )
                child = E.field(
                    {
                        "name": rfield.name,
                        "eval": f"[(6,0, [{field_eval}])]",
                    }
                )

            elif rfield.ttype == "binary":
                add_in_search_and_replace_file = False
                manage_scss = False
                sub_dir = "img"
                # Create file if image, else create binary
                if record.index_content == "image":
                    manage_scss = True
                elif record.mimetype in ["text/css", "text/scss"]:
                    force_field_name_xml_id = "datas_fname"
                    manage_scss = True
                    sub_dir = "scss"
                elif (
                    record.mimetype in ["application/octet-stream"]
                    and ".custom." in record.name
                    and record.name.endswith(".scss")
                ):
                    manage_scss = True
                    add_scss_hook = True
                    add_in_search_and_replace_file = True
                    sub_dir = "scss"
                # Check record.index_content or record.mimetype
                if manage_scss:
                    new_filename = (
                        record.datas_fname
                        if not add_scss_hook
                        else record.name.rsplit("/", maxsplit=1)[1]
                    )
                    url_path_file_module = os.path.join(
                        "static",
                        "src",
                        sub_dir,
                        new_filename,
                    )
                    url_path_file = os.path.join(
                        "/",
                        module.name,
                        "static",
                        "src",
                        sub_dir,
                        new_filename,
                    )
                    child_end = E.field({"name": "type"}, "url")
                    lst_end_field.append(child_end)
                    lst_ignore_field_name.append("type")

                    child_end = E.field({"name": "url"}, url_path_file)
                    lst_end_field.append(child_end)
                    lst_ignore_field_name.append("url")

                    new_data_to_write = [
                        record_value,
                        url_path_file_module,
                    ]
                    # decode_record = base64.b64decode(record_value)
                    # self.code_generator_data.write_file_binary(
                    #     url_path_file_module,
                    #     decode_record,
                    # )
                    if add_in_search_and_replace_file:
                        pattern_str = (
                            '<attribute name="href">%s</attribute>'
                        )
                        str_to_search = pattern_str % record.name
                        str_to_replace = pattern_str % url_path_file
                        dct_search_and_replace_in_file[
                            "data/ir_ui_view.xml"
                        ].append((str_to_search, str_to_replace))
                else:
                    # Transform binary in string and remove b''
                    child = E.field(
                        {"name": rfield.name},
                        str(record_value)[2:-1],
                    )
            elif rfield.ttype == "boolean":
                # Don't show boolean if same value of default
                if str(record_value) != rfield.default:
                    child = E.field(
                        {"name": rfield.name},
                        str(record_value),
                    )
                else:
                    delete_node = True
            elif rfield.related == "view_id.arch" or (
                rfield.name == "arch" and rfield.model == "ir.ui.view"
            ):
                root = ET.fromstring(record_value)
                child = E.field(
                    {"name": rfield.name, "type": "xml"}, root
                )

            else:
                child = E.field(
                    {"name": rfield.name}, str(record_value)
                )

            if not delete_node and child is not None:
                lst_field.append(child)

    # TODO delete this comment, check why no need anymore rec_name
    # rec_name_v = self._get_from_rec_name(record, model)
    # if rec_name_v:
    #     rec_name_v = self._lower_replace(rec_name_v)
    #     id_record = self._set_limit_4xmlid(f"{model_model}_{rec_name_v}")
    # else:
    #     rec_name_v = uuid.uuid1().int
    id_record = self._get_ir_model_data(
        record,
        give_a_default=True,
        module_name=module.name,
        force_field_name=force_field_name_xml_id,
    )
    lst_id.append(id_record)
    lst_total_field = lst_field + lst_end_field
    record_xml = E.record(
        {"id": id_record, "model": model.model}, *lst_total_field
    )
    lst_data_xml.append(record_xml)
    lst_record.append(record)
    lst_new_data_to_write.append(new_data_to_write)

    if add_scss_hook:
        lst_scss_process_hook.append(id_record)

# Do xml update for attachment later
if model_model == "ir_attachment":
    result = ""
else:
    # TODO find when is noupdate and not noupdate
    # <data noupdate="1">
    # xml_no_update = E.data({"noupdate": "1"}, *lst_data_xml)
    # module_file = E.odoo({}, xml_no_update)
    #
    # result = XML_VERSION_HEADER.encode("utf-8") + ET.tostring(
    #     module_file, pretty_print=True
    # )
    # TODO bug some character is missing, check code_generator_demo_website_attachments_data, use this method instead
    result = (
        XML_VERSION_HEADER.encode("utf-8")
        + b"<odoo>\\n"
        + ET.tostring(E.data({"noupdate": "1"}, *lst_data_xml))
        + b"\\n</odoo>\\n"
    )

return {
    model_model: [
        result,
        lst_data_xml,
        lst_id,
        lst_depend,
        lst_record,
        lst_new_data_to_write,
        dct_search_and_replace_in_file,
        lst_scss_process_hook,
    ]
}''',
                    "name": "_set_model_xmldata_file",
                    "param": "self, module, model, model_model",
                    "sequence": 28,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''if "ir_attachment" in dct_result.keys():
    dct_ir_attachment = dct_result.get("ir_attachment")
    lst_scss_process_hook = dct_ir_attachment[7]
    if lst_scss_process_hook:
        str_scss_process_hook = ";".join(lst_scss_process_hook)
        # self.write({"list_scss_process_hook":str_scss_process_hook})
        module.post_init_hook_show = True
        module.list_scss_process_hook = str_scss_process_hook
        module.hook_constant_code = """import logging
import base64
_logger = logging.getLogger(__name__)"""

# filter ir_attachment with ir_ui_view from website export data
if (
    "website_page" not in dct_result.keys()
    or "ir_attachment" not in dct_result.keys()
    or "ir_ui_view" not in dct_result.keys()
):
    return
# lst_attach_image_index_keep = []
dct_replace_view = {}
lst_attachment_id_to_keep = []
lst_attachment_id_check = []
result_view = dct_result.get("ir_ui_view")[0]
lst_view_id = dct_result.get("ir_ui_view")[4]
lst_ele_attach_xml = dct_ir_attachment[1]
lst_attach_xml_id = dct_ir_attachment[2]
lst_attach_id = dct_ir_attachment[4]
lst_new_data_to_write = dct_ir_attachment[5]
dct_associate_duplicate_attach_id = {}  # ref to master
dct_associate_duplicate_attach_id_index = {}  # ref to master
lst_attachment_id_index_has_rename = []

# TODO do algorithme to detect duplicate image reference. To test it, upload 2 same image and add it in html
# Detect duplicate and create association with master
if module.export_website_optimize_binary_image:
    i = -1
    for attach_id in lst_attach_id:
        i += 1
        for i_attach, attach_id_iter in enumerate(lst_attach_id):
            if i_attach == i:
                # same file...
                continue

            if (
                i not in dct_associate_duplicate_attach_id_index.keys()
                and attach_id.datas_fname == attach_id_iter.datas_fname
            ):
                if attach_id.datas == attach_id_iter.datas:
                    dct_associate_duplicate_attach_id[
                        attach_id_iter.id
                    ] = attach_id.id
                    dct_associate_duplicate_attach_id_index[
                        i_attach
                    ] = i
                else:
                    # Support rename for picture, the name is the same, but it's a different picture
                    new_data_to_write = lst_new_data_to_write[i_attach]
                    if (
                        new_data_to_write
                        and attach_id_iter.index_content == "image"
                        and i_attach
                        not in lst_attachment_id_index_has_rename
                    ):
                        (
                            record_value,
                            url_path_file_module,
                        ) = new_data_to_write
                        unique_str = hashlib.md5(
                            str(i_attach).encode("utf-8")
                        ).hexdigest()[:6]

                        new_data_to_write[
                            1
                        ] = self.rename_filename_with_uuid(
                            url_path_file_module, unique_str
                        )

                        element = ET.tostring(
                            lst_ele_attach_xml[i_attach]
                        ).decode("utf-8")
                        new_name = self.rename_filename_with_uuid(
                            attach_id.name, unique_str
                        )
                        new_datas_fname = (
                            self.rename_filename_with_uuid(
                                attach_id.datas_fname, unique_str
                            )
                        )
                        new_element = element.replace(
                            attach_id.name, new_name
                        ).replace(
                            attach_id.datas_fname, new_datas_fname
                        )
                        lst_ele_attach_xml[i_attach] = ET.fromstring(
                            new_element
                        )
                        lst_attachment_id_index_has_rename.append(
                            i_attach
                        )

# Detect /web/image/ in views, change attachment_id.id to his xml_id
for view_id in lst_view_id:
    str_view = view_id.arch
    iter_find = self.findall("/web/image/", str_view)
    lst_find = list(iter_find)
    for index in lst_find:
        preview_char_find = str_view[index - 1]
        if preview_char_find == '"':
            keyword_str = '"'
        elif preview_char_find == ";":
            # extract &quot;
            if index > 6 and str_view[index - 6 : index] == "&quot;":
                keyword_str = "&quot;"
            else:
                _logger.warning(
                    "Cannot extract /web/image/ in view name"
                    f" {view_id.name},"
                    f" ...'{str_view[index-30:index+30]}'..."
                )
                continue
        else:
            _logger.warning(
                "Cannot extract /web/image/ in view name"
                f" {view_id.name},"
                f" ...'{str_view[index-30:index+30]}'..."
            )
            continue
        # TODO this will not work if the filename include the keyword_str, need to detect it
        last_index = view_id.arch.find(keyword_str, index + 1)
        attach_link = view_id.arch[index:last_index]
        if attach_link.count("/") != 4:
            _logger.warning(
                f"Not support attach_link web/image of '{attach_link}'"
            )
            continue
        lst_attach = attach_link.split("/")
        i_attach_id = lst_attach[3]
        if i_attach_id.isdigit():
            i_attach_id = int(i_attach_id)
        else:
            # Support only id
            _logger.warning(f"Ignore attach_link '{attach_link}'")
            continue
        # Ignore processing if already got this information
        if i_attach_id in lst_attachment_id_check:
            continue
        lst_attachment_id_check.append(i_attach_id)
        # Search this picture if exist
        i = -1
        for attach_id in lst_attach_id:
            i += 1
            if attach_id.id == i_attach_id:
                # lst_attach_image_index_keep.append(i)
                break
        else:
            _logger.warning(
                f"Not found attachment for attach_link '{attach_link}'"
                f" into {view_id.name}"
            )
            continue
        if (
            module.export_website_optimize_binary_image
            and i in dct_associate_duplicate_attach_id_index.keys()
        ):
            # change link, to the master
            new_i = dct_associate_duplicate_attach_id_index[i]
            new_i_attach_id = dct_associate_duplicate_attach_id[
                i_attach_id
            ]
        else:
            new_i = i
            new_i_attach_id = i_attach_id

        # Rewrite link
        xml_id_link = f"{module.name}.{lst_attach_xml_id[new_i]}"
        new_lst_attach = lst_attach[:]
        new_lst_attach[3] = xml_id_link
        new_attach_link = "/".join(new_lst_attach)
        dct_replace_view[attach_link] = new_attach_link
        if new_i_attach_id not in lst_attachment_id_to_keep:
            lst_attachment_id_to_keep.append(new_i_attach_id)

# Replace all link
if dct_replace_view:
    str_result_view = result_view.decode("utf-8")
    for attach_link, new_attach_link in dct_replace_view.items():
        str_result_view = str_result_view.replace(
            attach_link, new_attach_link
        )
    dct_result.get("ir_ui_view")[0] = str_result_view.encode("utf-8")

# Remove unused image, missing from /web/image/ link
if module.export_website_optimize_binary_image:
    lst_index_to_delete = []
    i = -1
    for attach_id in lst_attach_id:
        i += 1
        if (
            attach_id.id in lst_attachment_id_to_keep
            or attach_id.index_content != "image"
        ):
            continue
        lst_index_to_delete.append(i)
    # Add slave attachment in the list
    for slave_index in dct_associate_duplicate_attach_id_index:
        if slave_index not in lst_index_to_delete:
            lst_index_to_delete.append(slave_index)
    lst_index_to_delete.sort(reverse=True)
    for index_to_delete in lst_index_to_delete:
        attach_id = lst_attach_id[index_to_delete]
        attach_xml_id = lst_attach_xml_id[index_to_delete]
        _logger.info(
            "Ignore export attachment id"
            f" {attach_id.id} '{attach_id.datas_fname}', xml_id"
            f" '{attach_xml_id}'."
        )
        dct_ir_attachment[1].pop(index_to_delete)
        dct_ir_attachment[2].pop(index_to_delete)
        dct_ir_attachment[4].pop(index_to_delete)
        dct_ir_attachment[5].pop(index_to_delete)''',
                    "name": "_compute_xml_data_file",
                    "param": "self, module, dct_result",
                    "sequence": 29,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""Yields all the positions of
the pattern p in the string s."""
i = s.find(p)
while i != -1:
    yield i
    i = s.find(p, i + 1)''',
                    "name": "findall",
                    "decorator": "@staticmethod",
                    "param": "p, s",
                    "sequence": 30,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """if "." in name:
    lst_new_name = name.rsplit(".", maxsplit=1)
    new_url_path = f"{lst_new_name[0]}_{s_uuid}.{lst_new_name[1]}"
else:
    new_url_path = f"{name}_{s_uuid}"
return new_url_path""",
                    "name": "rename_filename_with_uuid",
                    "decorator": "@staticmethod",
                    "param": "name, s_uuid",
                    "sequence": 31,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """dct_search_and_replace_in_file_global = defaultdict(list)
for model_model, tpl_result in dct_result.items():
    (
        result,
        lst_data_xml,
        lst_id,
        lst_depend,
        lst_record,
        lst_new_data_to_write,
        dct_search_and_replace_in_file,
        lst_scss_process_hook,
    ) = tpl_result
    if dct_search_and_replace_in_file:
        for (
            file_name,
            lst_value,
        ) in dct_search_and_replace_in_file.items():
            dct_search_and_replace_in_file_global[file_name].extend(
                lst_value
            )
for model_model, tpl_result in dct_result.items():
    (
        result,
        lst_data_xml,
        lst_id,
        lst_depend,
        lst_record,
        lst_new_data_to_write,
        dct_search_and_replace_in_file,
        lst_scss_process_hook,
    ) = tpl_result
    if not any(tpl_result):
        # it's empty
        continue
    data_file_path = os.path.join(
        self.code_generator_data.data_path, f"{model_model}.xml"
    )

    for new_data_to_write in lst_new_data_to_write:
        if not new_data_to_write:
            continue
        record_value, url_path_file_module = new_data_to_write
        decode_record = base64.b64decode(record_value)
        self.code_generator_data.write_file_binary(
            url_path_file_module,
            decode_record,
        )

    if not result:
        # Need to recompute the result
        # TODO find when is noupdate and not noupdate
        # <data noupdate="1">
        xml_no_update = E.data({"noupdate": "1"}, *lst_data_xml)
        module_file = E.odoo({}, xml_no_update)

        new_result = XML_VERSION_HEADER.encode("utf-8") + ET.tostring(
            module_file, pretty_print=True
        )
    else:
        new_result = result
    lst_to_replace = dct_search_and_replace_in_file_global.get(
        data_file_path
    )
    if lst_to_replace:
        for str_search, str_replace in lst_to_replace:
            new_result = new_result.replace(
                str_search.encode(), str_replace.encode()
            )

    self.code_generator_data.write_file_binary(
        data_file_path, new_result, data_file=True
    )

    abs_path_file = os.path.join("data", f"{model_model}.xml")

    self.code_generator_data.dct_data_metadata_file[
        abs_path_file
    ] = lst_id
    if lst_depend:
        self.code_generator_data.dct_data_depend[
            abs_path_file
        ] = lst_depend""",
                    "name": "_write_xml_data_file",
                    "param": "self, dct_result",
                    "sequence": 32,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to set the module menus file
:param module:
:return:
"""

application_icon = None
menus = module.with_context({"ir.ui.menu.full_list": True}).o2m_menus
if not menus:
    return ""

# Group by parent_id
lst_menu_root = menus.filtered(lambda x: not x.parent_id).sorted(
    key=lambda x: self._get_menu_data_name(x, module=module).split(
        "."
    )[-1]
)
lst_menu_item = menus.filtered(lambda x: x.parent_id and x.child_id)
lst_menu_last_child = menus.filtered(lambda x: not x.child_id).sorted(
    key=lambda x: self._get_menu_data_name(x, module=module).split(
        "."
    )[-1]
)
nb_root = len(lst_menu_root)
nb_item = len(lst_menu_item)
nb_last_child = len(lst_menu_last_child)
has_add_root = False
has_item = False
has_last_child = False

# Order by id_name
lst_menu = [a for a in lst_menu_root]

# Be sure parent is added
lst_menu_item = [a for a in lst_menu_item]

while lst_menu_item:
    lst_menu_to_order = []
    len_start = len(lst_menu_item)
    for menu_item in lst_menu_item[:]:
        # Remove item and add it
        if menu_item.parent_id in lst_menu:
            lst_menu_item.remove(menu_item)
            lst_menu_to_order.append(menu_item)

    if lst_menu_to_order:
        lst_menu_ordered = sorted(
            lst_menu_to_order,
            key=lambda x: self._get_menu_data_name(
                x, module=module
            ).split(".")[-1],
        )
        for menu_ordered in lst_menu_ordered:
            lst_menu.append(menu_ordered)

    len_end = len(lst_menu_item)
    if len_start == len_end:
        # Find no parent
        for menu_item in lst_menu_item:
            lst_menu.append(menu_item)

# Order by id_name
for menu_child in lst_menu_last_child:
    lst_menu.append(menu_child)

lst_menu_xml = []

for i, menu in enumerate(lst_menu):

    menu_id = self._get_menu_data_name(
        menu, ignore_module=True, module=module
    )
    dct_menu_item = {"id": menu_id}
    if menu.name != menu_id:
        dct_menu_item["name"] = menu.name

    if not menu.ignore_act_window:
        try:
            menu.action
        except Exception as e:
            # missing action on menu
            _logger.error(
                f"Missing action window on menu {menu.name}."
            )
            continue

        if menu.action:
            dct_menu_item["action"] = self._get_action_data_name(
                menu.action, module=module
            )

    if not menu.active:
        dct_menu_item["active"] = "False"

    if len(lst_menu) == 1 and menu.sequence != 10 or len(lst_menu) > 1:
        dct_menu_item["sequence"] = str(menu.sequence)

    if menu.parent_id:
        dct_menu_item["parent"] = self._get_menu_data_name(
            menu.parent_id,
            ignore_module_name=module.name,
            module=module,
        )

    if menu.groups_id:
        dct_menu_item["groups"] = self._get_m2m_groups(menu.groups_id)

    if menu.web_icon:
        # TODO move application_icon in code_generator_data
        application_icon = menu.web_icon
        # ignore actual icon, force a new icon
        new_icon = f"{module.name},static/description/icon.png"
        dct_menu_item["web_icon"] = new_icon
        if new_icon != menu.web_icon:
            _logger.warning(
                f"Difference between menu icon '{menu.web_icon}' and"
                f" new icon '{new_icon}'"
            )

    if not has_add_root and nb_root:
        has_add_root = True
        lst_menu_xml.append(ET.Comment("end line"))
        lst_menu_xml.append(ET.Comment("Root menu"))

    if not has_item and nb_item and i >= nb_root:
        has_item = True
        lst_menu_xml.append(ET.Comment("end line"))
        lst_menu_xml.append(ET.Comment("Sub menu"))

    if not has_last_child and nb_last_child and i >= nb_root + nb_item:
        has_last_child = True
        lst_menu_xml.append(ET.Comment("end line"))
        lst_menu_xml.append(ET.Comment("Child menu"))

    menu_xml = E.menuitem(dct_menu_item)
    lst_menu_xml.append(ET.Comment("end line"))
    lst_menu_xml.append(menu_xml)

lst_menu_xml.append(ET.Comment("end line"))
module_menus_file = E.odoo({}, *lst_menu_xml)
menu_file_path = os.path.join(
    self.code_generator_data.views_path, "menu.xml"
)
result = XML_VERSION_HEADER.encode("utf-8") + ET.tostring(
    module_menus_file, pretty_print=True
)

new_result = result.decode().replace("  <!--end line-->\\n", "\\n")[:-1]

self.code_generator_data.write_file_str(
    menu_file_path, new_result, data_file=True
)

return application_icon''',
                    "name": "_set_module_menus",
                    "param": "self, module",
                    "sequence": 33,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """# return "\\n".join([f"{'    ' * indent}{a}" for a in content.split("\\n")])
str_content = content.rstrip().replace("\\n", f"\\n{'  ' * indent}")
super_content = f"\\n{'  ' * indent}{str_content}"
if is_end:
    super_content += f"\\n{'  ' * 1}"
else:
    super_content += f"\\n{'  ' * (indent - 1)}"
return super_content""",
                    "name": "_setup_xml_indent",
                    "decorator": "@staticmethod",
                    "param": "content, indent=0, is_end=False",
                    "sequence": 34,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """new_content = ""
# Change 2 space for 4 space
for line in content.split("\\n"):
    # count first space
    if line.strip():
        new_content += (
            f'{"  " * (len(line) - len(line.lstrip()))}{line.strip()}\\n'
        )
    else:
        new_content += "\\n"
return new_content""",
                    "name": "_change_xml_2_to_4_spaces",
                    "decorator": "@staticmethod",
                    "param": "content",
                    "sequence": 35,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to set the model xml files
:param module:
:param model:
:param model_model:
:return:
"""

# view_ids = model.view_ids
# TODO model.view_ids not working when add inherit view from wizard... what is different? Force values
view_ids = self.env["ir.ui.view"].search([("model", "=", model.model)])
act_window_ids = self.env["ir.actions.act_window"].search(
    [("res_model", "=", model.model)]
)
server_action_ids = model.o2m_server_action

# Remove all field when in inherit if not in whitelist
is_whitelist = any([a.is_show_whitelist_write_view for a in view_ids])
view_filtered_ids = view_ids.filtered(
    lambda field: field.name not in MAGIC_FIELDS
    and not field.is_hide_blacklist_write_view
    and (
        not is_whitelist
        or (is_whitelist and field.is_show_whitelist_write_view)
    )
)

if not (view_filtered_ids or act_window_ids or server_action_ids):
    return

dct_replace = {}
dct_replace_template = {}
lst_id = []
lst_item_xml = []
lst_item_template = []

#
# Views
#
for view in view_filtered_ids:

    view_type = view.type

    lst_view_type = list(
        dict(
            self.env["code.generator.view"]
            ._fields["view_type"]
            .selection
        ).keys()
    )
    if view_type in lst_view_type:

        str_id_system = self._get_id_view_model_data(
            view, model="ir.ui.view", is_internal=True
        )
        if not str_id_system:
            str_id = f"{model_model}_view_{view_type}"
        else:
            str_id = str_id_system
        if str_id in lst_id:
            count_id = lst_id.count(str_id)
            str_id += str(count_id)
        lst_id.append(str_id)

        self.code_generator_data.add_view_id(view.name, str_id)

        lst_field = []

        if view.name:
            lst_field.append(E.field({"name": "name"}, view.name))

        lst_field.append(E.field({"name": "model"}, view.model))

        if view.key:
            lst_field.append(E.field({"name": "key"}, view.key))

        if view.priority != 16:
            lst_field.append(
                E.field({"name": "priority"}, str(view.priority))
            )

        if view.inherit_id:
            lst_field.append(
                E.field(
                    {
                        "name": "inherit_id",
                        "ref": self._get_view_data_name(
                            view.inherit_id
                        ),
                    }
                )
            )

            if view.mode == "primary":
                lst_field.append(E.field({"name": "mode"}, "primary"))

        if not view.active:
            lst_field.append(
                E.field({"name": "active", "eval": False})
            )

        if view.arch_db:
            uid = str(uuid.uuid1())
            str_arch_db = (
                view.arch_db
                if not view.arch_db.startswith(XML_VERSION_STR)
                else view.arch_db[len(XML_VERSION_STR) :]
            )
            # TODO retransform xml to format correctly
            str_data_begin = "<data>\\n"
            str_data_end = "</data>\\n"
            if str_arch_db.startswith(
                str_data_begin
            ) and str_arch_db.endswith(str_data_end):
                str_arch_db = str_arch_db[
                    len(str_data_begin) : -len(str_data_end)
                ]
            dct_replace[uid] = self._setup_xml_indent(
                str_arch_db, indent=3
            )
            lst_field.append(
                E.field({"name": "arch", "type": "xml"}, uid)
            )

        if view.groups_id:
            lst_field.append(
                self._get_m2m_groups_etree(view.groups_id)
            )

        info = E.record(
            {"id": str_id, "model": "ir.ui.view"}, *lst_field
        )
        lst_item_xml.append(ET.Comment("end line"))
        lst_item_xml.append(info)

    elif view_type == "qweb":
        template_value = {"id": view.key, "name": view.name}
        if view.inherit_id:
            template_value["inherit_id"] = view.inherit_id.key

        uid = str(uuid.uuid1())
        dct_replace_template[uid] = self._setup_xml_indent(
            view.arch, indent=2, is_end=True
        )
        info = E.template(template_value, uid)
        # lst_item_xml.append(ET.Comment("end line"))
        # lst_item_xml.append(info)
        lst_item_template.append(ET.Comment("end line"))
        lst_item_template.append(info)

    else:
        _logger.error(
            f"View type {view_type} of {view.name} not supported."
        )

#
# Action Windows
#
for act_window in act_window_ids:
    # Use descriptive method when contain this attributes, not supported in simplify view
    use_complex_view = bool(
        act_window.groups_id
        or act_window.help
        or act_window.multi
        or not act_window.auto_search
        or act_window.filter
        or act_window.search_view_id
        or act_window.usage
    )

    record_id = self._get_id_view_model_data(
        act_window, model="ir.actions.act_window", is_internal=True
    )
    if not record_id:
        record_id = self._get_action_data_name(
            act_window, creating=True
        )

    has_menu = bool(
        module.with_context({"ir.ui.menu.full_list": True}).o2m_menus
    )
    # TODO if not complex, search if associate with a menu. If the menu is not generated, don't generate is act_window
    if use_complex_view:
        lst_field = []

        if act_window.name:
            lst_field.append(
                E.field({"name": "name"}, act_window.name)
            )

        if act_window.res_model or act_window.m2o_res_model:
            lst_field.append(
                E.field(
                    {"name": "res_model"},
                    act_window.res_model
                    or act_window.m2o_res_model.model,
                )
            )

        if act_window.binding_model_id:
            binding_model = self._get_model_data_name(
                act_window.binding_model_id, module_name=module.name
            )
            lst_field.append(
                E.field(
                    {"name": "binding_model_id", "ref": binding_model}
                )
            )

        if act_window.view_id:
            lst_field.append(
                E.field(
                    {
                        "name": "view_id",
                        "ref": self._get_view_data_name(
                            act_window.view_id
                        ),
                    }
                )
            )

        if act_window.domain != "[]" and act_window.domain:
            lst_field.append(
                E.field({"name": "domain"}, act_window.domain)
            )

        if act_window.context != "{}":
            lst_field.append(
                E.field({"name": "context"}, act_window.context)
            )

        if act_window.src_model or act_window.m2o_src_model:
            lst_field.append(
                E.field(
                    {"name": "src_model"},
                    act_window.src_model
                    or act_window.m2o_src_model.model,
                )
            )

        if act_window.target != "current":
            lst_field.append(
                E.field({"name": "target"}, act_window.target)
            )

        if (
            act_window.view_mode != "tree,form"
            and act_window.view_mode != "form,tree"
        ):
            lst_field.append(
                E.field({"name": "view_mode"}, act_window.view_mode)
            )

        if act_window.view_type != "form":
            lst_field.append(
                E.field({"name": "view_type"}, act_window.view_type)
            )

        if act_window.usage:
            lst_field.append(E.field({"name": "usage", "eval": True}))

        if act_window.limit != 80 and act_window.limit != 0:
            lst_field.append(
                E.field({"name": "limit"}, str(act_window.limit))
            )

        if act_window.search_view_id:
            lst_field.append(
                E.field(
                    {
                        "name": "search_view_id",
                        "ref": self._get_view_data_name(
                            act_window.search_view_id
                        ),
                    }
                )
            )

        if act_window.filter:
            lst_field.append(E.field({"name": "filter", "eval": True}))

        if not act_window.auto_search:
            lst_field.append(
                E.field({"name": "auto_search", "eval": False})
            )

        if act_window.multi:
            lst_field.append(E.field({"name": "multi", "eval": True}))

        if act_window.help:
            lst_field.append(
                E.field(
                    {"name": "name", "type": "html"}, act_window.help
                )
            )

        if act_window.groups_id:
            lst_field.append(
                self._get_m2m_groups_etree(act_window.groups_id)
            )

        info = E.record(
            {"id": record_id, "model": "ir.actions.act_window"},
            *lst_field,
        )
        lst_item_xml.append(ET.Comment("end line"))
        lst_item_xml.append(info)
    elif has_menu:
        dct_act_window = {"id": record_id}

        if act_window.name:
            dct_act_window["name"] = act_window.name

        if act_window.res_model or act_window.m2o_res_model:
            dct_act_window["res_model"] = (
                act_window.res_model or act_window.m2o_res_model.model
            )

        if act_window.binding_model_id:
            # TODO replace ref
            pass

        if act_window.view_id:
            # TODO replace ref
            pass

        if act_window.domain != "[]" and act_window.domain:
            dct_act_window["domain"] = (
                act_window.res_model or act_window.m2o_res_model.model
            )

        if act_window.context != "{}":
            dct_act_window["context"] = act_window.context

        if act_window.src_model or act_window.m2o_src_model:
            dct_act_window["src_model"] = (
                act_window.src_model or act_window.m2o_src_model.model
            )

        if act_window.target != "current":
            dct_act_window["target"] = act_window.target

        if act_window.view_mode != "tree,form":
            dct_act_window["view_mode"] = act_window.view_mode

        if act_window.view_type != "form":
            dct_act_window["view_type"] = act_window.view_type

        if act_window.usage:
            # TODO replace ref
            pass

        if act_window.limit != 80 and act_window.limit != 0:
            dct_act_window["limit"] = str(act_window.limit)

        if act_window.search_view_id:
            # TODO replace ref
            pass

        if act_window.filter:
            # TODO replace ref
            pass

        if not act_window.auto_search:
            # TODO replace ref
            pass

        if act_window.multi:
            # TODO replace ref
            pass

        if act_window.help:
            # TODO how add type html and contents?
            pass

        if act_window.groups_id:
            # TODO check _get_m2m_groups_etree
            pass

        info = E.act_window(dct_act_window)
        lst_item_xml.append(ET.Comment("end line"))
        lst_item_xml.append(info)

#
# Server Actions
#
for server_action in server_action_ids:

    lst_field = [
        E.field({"name": "name"}, server_action.name),
        E.field(
            {
                "name": "model_id",
                "ref": self._get_model_data_name(
                    server_action.model_id, module_name=module.name
                ),
            }
        ),
        E.field(
            {
                "name": "binding_model_id",
                "ref": self._get_model_data_name(
                    model, module_name=module.name
                ),
            }
        ),
    ]

    if server_action.state == "code":
        lst_field.append(E.field({"name": "state"}, "code"))

        lst_field.append(E.field({"name": "code"}, server_action.code))

    else:
        lst_field.append(E.field({"name": "state"}, "multi"))

        if server_action.child_ids:
            child_obj = ", ".join(
                server_action.child_ids.mapped(
                    lambda child: "ref(%s)"
                    % self._get_action_data_name(child, server=True)
                )
            )
            lst_field.append(
                E.field(
                    {
                        "name": "child_ids",
                        "eval": f"[(6,0, [{child_obj}])]",
                    }
                )
            )

    record_id = self._get_id_view_model_data(
        server_action, model="ir.actions.server", is_internal=True
    )
    if not record_id:
        record_id = self._get_action_data_name(
            server_action, server=True, creating=True
        )
    info = E.record(
        {"id": record_id, "model": "ir.actions.server"}, *lst_field
    )
    lst_item_xml.append(ET.Comment("end line"))

    if server_action.comment:
        lst_item_xml.append(
            ET.Comment(text=f" {server_action.comment} ")
        )

    lst_item_xml.append(info)

lst_item_xml.append(ET.Comment("end line"))
root = E.odoo({}, *lst_item_xml)

content = XML_VERSION_HEADER.encode("utf-8") + ET.tostring(
    root, pretty_print=True
)
str_content = content.decode()

str_content = str_content.replace("  <!--end line-->\\n", "\\n")
for key, value in dct_replace.items():
    str_content = str_content.replace(key, value)
str_content = self._change_xml_2_to_4_spaces(str_content)[:-1]

wizards_path = self.code_generator_data.wizards_path
views_path = self.code_generator_data.views_path
xml_file_path = os.path.join(
    wizards_path if model.transient else views_path,
    f"{model_model}.xml",
)
self.code_generator_data.write_file_str(
    xml_file_path, str_content, data_file=True
)

if dct_replace_template:
    root_template = E.odoo({}, *lst_item_template)
    content_template = XML_VERSION_HEADER.encode(
        "utf-8"
    ) + ET.tostring(root_template, pretty_print=True)
    str_content_template = content_template.decode()

    str_content_template = str_content_template.replace(
        "  <!--end line-->\\n", "\\n"
    )
    for key, value in dct_replace_template.items():
        str_content_template = str_content_template.replace(key, value)
    str_content_template = self._change_xml_2_to_4_spaces(
        str_content_template
    )[:-1]

    views_path = self.code_generator_data.views_path
    xml_file_path = os.path.join(
        views_path,
        f"{module.name}_templates.xml",
    )
    self.code_generator_data.write_file_str(
        xml_file_path, str_content_template, data_file=True
    )''',
                    "name": "_set_model_xmlview_file",
                    "param": "self, module, model, model_model",
                    "sequence": 36,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""

:param module:
:param model:
:param model_model:
:return:
"""

if not model.o2m_reports:
    return

l_model_report_file = XML_HEAD + BLANK_LINE

for report in model.o2m_reports:

    l_model_report_file.append(
        '<template id="%s">' % report.report_name
    )

    str_arch_db = (
        report.m2o_template.arch_db
        if not report.m2o_template.arch_db.startswith(XML_VERSION_STR)
        else report.m2o_template.arch_db[len(XML_VERSION_STR) :]
    )
    l_model_report_file.append(
        f'<field name="arch" type="xml">{str_arch_db}</field>'
    )

    l_model_report_file.append("</template>\\n")

    l_model_report_file.append(
        '<record model="ir.actions.report" id="%s_actionreport">'
        % report.report_name
    )

    l_model_report_file.append(
        '<field name="model">%s</field>' % report.model
    )

    l_model_report_file.append(
        '<field name="name">%s</field>' % report.report_name
    )

    l_model_report_file.append(
        '<field name="file">%s</field>' % report.report_name
    )

    l_model_report_file.append(
        '<field name="string">%s</field>' % report.name
    )

    l_model_report_file.append(
        '<field name="report_type">%s</field>' % report.report_type
    )

    if report.print_report_name:
        l_model_report_file.append(
            '<field name="print_report_name">%s</field>'
            % report.print_report_name
        )

    if report.multi:
        l_model_report_file.append(
            '<field name="multi">%s</field>' % report.multi
        )

    if report.attachment_use:
        l_model_report_file.append(
            '<field name="attachment_use">%s</field>'
            % report.attachment_use
        )

    if report.attachment:
        l_model_report_file.append(
            '<field name="attachment">%s</field>' % report.attachment
        )

    if report.binding_model_id:
        l_model_report_file.append(
            '<field name="binding_model_id" ref="%s" />'
            % self._get_model_data_name(
                report.binding_model_id, module_name=module.name
            )
        )

    if report.groups_id:
        l_model_report_file.append(
            self._get_m2m_groups(report.groups_id)
        )

    l_model_report_file.append("</record>")

    l_model_report_file += XML_ODOO_CLOSING_TAG

xmlreport_file_path = os.path.join(
    self.code_generator_data.reports_path, f"{model_model}.xml"
)
self.code_generator_data.write_file_lst_content(
    xmlreport_file_path, l_model_report_file, data_file=True
)''',
                    "name": "_set_model_xmlreport_file",
                    "param": "self, module, model, model_model",
                    "sequence": 37,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''lst_model = []

def recursive_get_inherit_model(actual_model_id):
    """
    actual_model_id is code.generator.ir.model.dependency
    """
    lst_model_id = [a.id for a in lst_model] + model_id.ids
    if actual_model_id.depend_id.id not in lst_model_id:
        new_model_id = actual_model_id.depend_id
        lst_model.append(new_model_id)
        if new_model_id.inherit_model_ids:
            for new_inherit_model_id in new_model_id.inherit_model_ids:
                recursive_get_inherit_model(new_inherit_model_id)

if model_id.inherit_model_ids:
    for inherit_model_id in model_id.inherit_model_ids:
        recursive_get_inherit_model(inherit_model_id)

return lst_model''',
                    "name": "_get_lst_inherit_model",
                    "decorator": "@staticmethod",
                    "param": "model_id",
                    "sequence": 38,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """lst_rec_name_inherit = []
for inherit_model in model.inherit_model_ids:
    model_inherit_id = inherit_model.depend_id
    if model_inherit_id.id != model.id:
        # TODO can remove recursive and use _get_lst_inherit_model to get all rec_name model
        lst_rec_name_inherit.append(
            self._get_rec_name_inherit_model(model_inherit_id)
        )
result_rec_name = None
new_rec_name = self.env[model.model]._rec_name
if new_rec_name and new_rec_name != "name":
    result_rec_name = new_rec_name
elif model.rec_name and model.rec_name != "name":
    result_rec_name = model.rec_name
# Ignore rec_name if same of inherit parent
if lst_rec_name_inherit and result_rec_name:
    if result_rec_name in lst_rec_name_inherit:
        return None
return result_rec_name""",
                    "name": "_get_rec_name_inherit_model",
                    "param": "self, model",
                    "sequence": 39,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to set the model files
:param model:
:param model_model:
:return:
"""

key_special_endline = str(uuid.uuid1())

cw = CodeWriter()

code_ids = model.o2m_codes.filtered(
    lambda x: not x.is_templated
).sorted(key=lambda x: x.sequence)
code_import_ids = model.o2m_code_import.filtered(
    lambda x: not x.is_templated
).sorted(key=lambda x: x.sequence)
if code_import_ids:
    for code in code_import_ids:
        for code_line in code.code.split("\\n"):
            cw.emit(code_line)
else:
    # search api or contextmanager
    # TODO ignore api, because need to search in code
    has_context_manager = False
    lst_import = MODEL_HEAD
    for code_id in code_ids:
        if (
            code_id.decorator
            and "@contextmanager" in code_id.decorator
        ):
            has_context_manager = True
    if has_context_manager:
        lst_import.insert(1, "from contextlib import contextmanager")

    for line in lst_import:
        str_line = line.strip()
        cw.emit(str_line)

    if (
        model.m2o_inherit_py_class.name
        and model.m2o_inherit_py_class.module
    ):
        cw.emit(
            f"from {model.m2o_inherit_py_class.module} import"
            f" {model.m2o_inherit_py_class.name}"
        )

cw.emit()
cw.emit(
    "class"
    f" {self._get_class_name(model.model)}({self._get_python_class_4inherit(model)}):"
)

with cw.indent():
    """
    _name
    _table =
    _description
    _auto = False
    _log_access = False
    _order = ""
    _rec_name = ""
    _foreign_keys = []
    """
    # Force unique inherit
    lst_inherit = sorted(
        list(set([a.depend_id.model for a in model.inherit_model_ids]))
    )

    add_name = False
    if model.model not in lst_inherit:
        add_name = True
        cw.emit(f"_name = '{model.model}'")

    if lst_inherit:
        if len(lst_inherit) == 1:
            str_inherit = f"'{lst_inherit[0]}'"
        else:
            str_inherit_internal = '", "'.join(lst_inherit)
            str_inherit = f'["{str_inherit_internal}"]'
        cw.emit(f"_inherit = {str_inherit}")

    if model.description:
        new_description = model.description.replace("'", "\\'")
        cw.emit(f"_description = '{new_description}'")
    elif not lst_inherit or add_name:
        cw.emit(f"_description = '{model.name}'")
    rec_name = self._get_rec_name_inherit_model(model)
    if rec_name:
        cw.emit(f"_rec_name = '{rec_name}'")

    # TODO _order, _local_fields, _period_number, _inherits, _log_access, _auto, _parent_store
    # TODO _parent_name

    self._get_model_constrains(cw, model, module)

    self._get_model_fields(cw, model, module)

    # code_ids = self.env["code.generator.model.code"].search(
    #     [("m2o_module", "=", module.id)]
    # )

    # Add function
    for code in code_ids:
        cw.emit()
        if code.decorator:
            for line in code.decorator.split(";"):
                if line:
                    cw.emit(line)
        return_v = "" if not code.returns else f" -> {code.returns}"
        cw.emit(f"def {code.name}({code.param}){return_v}:")

        code_traited = code.code.replace("\\\\n", key_special_endline)
        code_traited = code_traited.replace("\\'", "\\\\'")
        code_traited = code_traited.replace("\b", "\\b")
        with cw.indent():
            for code_line in code_traited.split("\\n"):
                if key_special_endline in code_line:
                    code_line = code_line.replace(
                        key_special_endline, "\\\\\n"
                    )
                cw.emit(code_line)

if model.transient:
    pypath = self.code_generator_data.wizards_path
elif model.o2m_reports and self.env[model.model]._abstract:
    pypath = self.code_generator_data.reports_path
else:
    pypath = self.code_generator_data.models_path

model_file_path = os.path.join(pypath, f"{model_model}.py")

self.code_generator_data.write_file_str(model_file_path, cw.render())

return model_file_path''',
                    "name": "_set_model_py_file",
                    "param": "self, module, model, model_model",
                    "sequence": 40,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to set the module security file
:param module:
:param l_model_rules:
:param l_model_csv_access:
:return:
"""
l_model_csv_access.insert(
    0,
    "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink",
)

if module.o2m_groups or l_model_rules:
    l_module_security = ["<data>\\n"]

    for group in module.o2m_groups:

        l_module_security += [
            '<record model="res.groups" id="%s">'
            % self._get_group_data_name(group)
        ]
        l_module_security += [
            '<field name="name">%s</field>' % group.name
        ]

        if group.comment:
            l_module_security += [
                '<field name="comment">%s</field>' % group.comment
            ]

        if group.implied_ids:
            l_module_security += [
                '<field name="implied_ids" eval="[%s]"/>'
                % ", ".join(
                    group.implied_ids.mapped(
                        lambda g: "(4, ref('%s'))"
                        % self._get_group_data_name(g)
                    )
                )
            ]

        l_module_security += ["</record>\\n"]

    l_module_security += l_model_rules

    l_module_security += ["</data>"]

    module_name = module.name.lower().strip()
    security_file_path = os.path.join(
        self.code_generator_data.security_path, f"{module_name}.xml"
    )
    self.code_generator_data.write_file_lst_content(
        security_file_path,
        XML_HEAD + l_module_security + XML_ODOO_CLOSING_TAG,
        data_file=True,
        insert_first=True,
    )

if len(l_model_csv_access) > 1:
    model_access_file_path = os.path.join(
        self.code_generator_data.security_path, "ir.model.access.csv"
    )
    self.code_generator_data.write_file_lst_content(
        model_access_file_path,
        l_model_csv_access,
        data_file=True,
        insert_first=True,
    )''',
                    "name": "_set_module_security",
                    "param": "self, module, l_model_rules, l_model_csv_access",
                    "sequence": 41,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to obtain the model access
:param model:
:return:
"""

l_model_csv_access = []

for access in model.access_ids:
    access_name = access.name

    access_model_data = self.env["ir.model.data"].search(
        [
            ("module", "=", module.name),
            ("model", "=", "ir.model.access"),
            ("res_id", "=", access.id),
        ]
    )

    access_id = (
        access_model_data[0].name
        if access_model_data
        else self._lower_replace(access_name)
    )

    access_model = self._get_model_model(access.model_id.model)

    access_group = (
        self._get_group_data_name(access.group_id)
        if access.group_id
        else ""
    )

    access_read, access_create, access_write, access_unlink = (
        1 if access.perm_read else 0,
        1 if access.perm_create else 0,
        1 if access.perm_write else 0,
        1 if access.perm_unlink else 0,
    )

    l_model_csv_access.append(
        "%s,%s,model_%s,%s,%s,%s,%s,%s"
        % (
            access_id,
            access_name,
            access_model,
            access_group,
            access_read,
            access_create,
            access_write,
            access_unlink,
        )
    )

return l_model_csv_access''',
                    "name": "_get_model_access",
                    "param": "self, module, model",
                    "sequence": 42,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to obtain the model rules
:param model:
:return:
"""

l_model_rules = []

for rule in model.rule_ids:

    if rule.name:
        l_model_rules.append(
            '<record model="ir.rule" id="%s">'
            % self._lower_replace(rule.name)
        )
        l_model_rules.append(
            '<field name="name">%s</field>' % rule.name
        )

    else:
        l_model_rules.append(
            '<record model="ir.rule" id="%s_rrule_%s">'
            % (
                self._get_model_data_name(
                    rule.model_id, module_name=module.name
                ),
                rule.id,
            )
        )

    l_model_rules.append(
        '<field name="model_id" ref="%s"/>'
        % self._get_model_data_name(
            rule.model_id, module_name=module.name
        )
    )

    if rule.domain_force:
        l_model_rules.append(
            '<field name="domain_force">%s</field>' % rule.domain_force
        )

    if not rule.active:
        l_model_rules.append('<field name="active" eval="False" />')

    if rule.groups:
        l_model_rules.append(self._get_m2m_groups(rule.groups))

    if not rule.perm_read:
        l_model_rules.append('<field name="perm_read" eval="False" />')

    if not rule.perm_create:
        l_model_rules.append(
            '<field name="perm_create" eval="False" />'
        )

    if not rule.perm_write:
        l_model_rules.append(
            '<field name="perm_write" eval="False" />'
        )

    if not rule.perm_unlink:
        l_model_rules.append(
            '<field name="perm_unlink" eval="False" />'
        )

    l_model_rules.append("</record>\\n")

return l_model_rules''',
                    "name": "_get_model_rules",
                    "param": "self, module, model",
                    "sequence": 43,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""

:param m2m_groups:
:return:
"""

return '<field name="groups_id" eval="[(6,0, [%s])]" />' % ", ".join(
    m2m_groups.mapped(
        lambda g: "ref(%s)" % self._get_group_data_name(g)
    )
)''',
                    "name": "_get_m2m_groups",
                    "param": "self, m2m_groups",
                    "sequence": 44,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""

:param m2m_groups:
:return:
"""

var = ", ".join(
    m2m_groups.mapped(
        lambda g: "ref(%s)" % self._get_group_data_name(g)
    )
)
return E.field({"name": "groups_id", "eval": f"[(6,0, [{var}])]"})''',
                    "name": "_get_m2m_groups_etree",
                    "param": "self, m2m_groups",
                    "sequence": 45,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """if lst_field_inherit and not dct_field_attr_diff:
    return [], False, None, False
has_endline = False
lst_attribute_to_filter = []
lst_first_field_attribute = []
lst_field_attribute = []
compute = None
lst_last_field_attribute = []
extra_info = (
    self.env[f2export.model]
    .fields_get(f2export.name)
    .get(f2export.name)
)
dct_field_attribute = {}

code_generator_compute = f2export.get_code_generator_compute()
if not code_generator_compute and not f2export.related:
    code_generator_compute = self._get_compute_fct(f2export)

# TODO not optimal to remove attributes, but more easy ;-)
if dct_field_attr_diff:
    for attr_key, lst_value in dct_field_attr_diff.items():
        if attr_key == "default":
            dct_field_attribute[attr_key] = self._get_default(f2export)
        else:
            dct_field_attribute[attr_key] = getattr(f2export, attr_key)
    # Exception for compute
    if "compute" in dct_field_attr_diff.keys():
        new_value_compute = self._get_compute_fct(f2export)
        if not new_value_compute:
            dct_field_attribute["compute"] = None
            if dct_field_attribute.get("store"):
                # no need to store when no compute
                del dct_field_attribute["store"]
            if dct_field_attribute.get("readonly") is False:
                del dct_field_attribute["readonly"]
        else:
            dct_field_attribute["compute"] = new_value_compute
    # Rename attribute
    if "relation" in dct_field_attribute.keys():
        dct_field_attribute["comodel_name"] = dct_field_attribute[
            "relation"
        ]
        del dct_field_attribute["relation"]
    if "field_description" in dct_field_attribute.keys():
        dct_field_attribute["string"] = dct_field_attribute[
            "field_description"
        ]
        del dct_field_attribute["field_description"]
    if "relation_field" in dct_field_attribute.keys():
        dct_field_attribute["inverse_name"] = dct_field_attribute[
            "relation_field"
        ]
        del dct_field_attribute["relation_field"]
    if "relation_table" in dct_field_attribute.keys():
        dct_field_attribute["relation"] = dct_field_attribute[
            "relation_table"
        ]
        del dct_field_attribute["relation_table"]
    if "copied" in dct_field_attribute.keys():
        dct_field_attribute["copy"] = dct_field_attribute["copied"]
        del dct_field_attribute["copied"]
else:
    # TODO use if cannot find information
    # field_selection = self.env[f2export.model].fields_get(f2export.name).get(f2export.name)

    related_field_id = None
    if f2export.related:
        dct_field_attribute["related"] = f2export.related
        # Get related field if, it works like inherit
        (
            related_inside_field,
            related_outside_field,
        ) = f2export.related.split(".")
        # This need to be a many2many
        related_model_name = f2export.model_id.field_id.filtered(
            lambda field: field.name == related_inside_field
        ).relation
        related_outside_field_id = self.env["ir.model.fields"].search(
            [
                ("model", "=", related_model_name),
                ("name", "=", related_inside_field),
            ],
            limit=1,
        )
        if not related_outside_field_id:
            _logger.error(
                "Cannot find related field from field"
                f" '{f2export.name}' and model '{f2export.model}'"
            )
        else:
            # Get is model and search outside field
            related_field_id = (
                related_outside_field_id.model_id.field_id.filtered(
                    lambda field: field.name == related_outside_field
                )
            )

    # Respect sequence in list, order listed by human preference
    if (
        f2export.ttype in ("selection", "reference")
        and not f2export.related
    ):
        # cannot support selection item with related attributes
        str_selection = f2export.get_selection()
        if str_selection:
            dct_field_attribute["selection"] = str_selection

    if f2export.ttype in ["many2one", "one2many", "many2many"]:
        if f2export.relation:
            dct_field_attribute["comodel_name"] = f2export.relation

        if f2export.ttype == "one2many" and f2export.relation_field:
            dct_field_attribute[
                "inverse_name"
            ] = f2export.relation_field

        if f2export.ttype == "many2many":
            # elif f2export.relation_table.startswith("x_"):
            #     # TODO why ignore relation when start name with x_? Is it about x_name?
            #     # A relation who begin with x_ is an automated relation, ignore it
            #     ignored_relation = True
            if (
                f2export.relation_table
                and f"{f2export.model.replace('.', '_')}_id"
                != f2export.column1
                and f"{f2export.relation.replace('.', '_')}_id"
                != f2export.column2
                and f"{f2export.model.replace('.', '_')}_{f2export.relation.replace('.', '_')}"
                != f2export.relation_table
            ):
                dct_field_attribute[
                    "relation"
                ] = f2export.relation_table
                dct_field_attribute["column1"] = f2export.column1
                dct_field_attribute["column2"] = f2export.column2
            elif (
                dct_field_attribute.get("relation") is None
                and f2export.relation_table
                and f2export.relation
                and len(f2export.relation_table) > 63
            ):
                # TODO need to validate it's not exist, the new relation table
                # relation can be empty, the system will generate it, but crash if highter then 63
                new_relation_table = (
                    f"{f2export.name}_{f2export.model.replace('.', '_')}_rel"
                )
                if len(new_relation_table) > 63:
                    # again!
                    lst_split_relation_t = f2export.relation_table[
                        :-4
                    ].split("_")
                    if lst_split_relation_t[0] == "x":
                        lst_split_relation_t = lst_split_relation_t[1:]
                    # Take only first later of each word
                    new_relation_table = (
                        "_".join(
                            [
                                a[0]
                                for a in lst_split_relation_t.split(
                                    "_"
                                )
                            ]
                        )
                        + "_rel"
                    )
                    if len(new_relation_table) > 63:
                        new_relation_table = new_relation_table[
                            :63
                        ].trim("_")
                dct_field_attribute["relation"] = new_relation_table
        domain_info = extra_info.get("domain")
        if f2export.domain and f2export.domain != "[]":
            dct_field_attribute["domain"] = f2export.domain
        elif domain_info and domain_info != "[]":
            dct_field_attribute["domain"] = domain_info

        if (
            f2export.ttype == "many2one"
            and f2export.on_delete
            and f2export.on_delete != "set null"
        ):
            dct_field_attribute["ondelete"] = f2export.on_delete

    if (
        f2export.field_description
        and f2export.name.replace("_", " ").title()
        != f2export.field_description
    ):
        if not (
            related_field_id
            and related_field_id.field_description
            == f2export.field_description
        ):
            dct_field_attribute["string"] = f2export.field_description

    if (
        f2export.ttype == "char" or f2export.ttype == "reference"
    ) and f2export.size != 0:
        dct_field_attribute["size"] = f2export.size

    if f2export.related:
        dct_field_attribute["related"] = f2export.related

    if f2export.readonly and not code_generator_compute:
        # Note that a computed field without an inverse method is readonly by default.
        if not (
            related_field_id
            and related_field_id.readonly == f2export.readonly
        ):
            dct_field_attribute["readonly"] = True

    if f2export.required:
        dct_field_attribute["required"] = True

    if f2export.index:
        dct_field_attribute["index"] = True

    field_context = f2export.get_field_context()
    if field_context:
        # Extract content from string
        try:
            dct_field_context = ast.literal_eval(field_context)
            dct_field_attribute["context"] = dct_field_context
        except Exception as e:
            _logger.error(
                f"Cannot extract dict from context '{field_context}'"
                f" for field '{f2export.name}' in model"
                f" '{f2export.model}'"
            )

    if f2export.track_visibility:
        if f2export.track_visibility in ("onchange", "always"):
            dct_field_attribute[
                "track_visibility"
            ] = f2export.track_visibility
            # TODO is it the good place for this?
            # lst_depend_model = [
            #     "mail.thread",
            #     "mail.activity.mixin",
            # ]
            # f2export.model_id.add_model_inherit(lst_depend_model)
        else:
            _logger.warning(
                "Cannot support track_visibility value"
                f" {f2export.track_visibility}, only support"
                " 'onchange' and 'always'."
            )

    # Get default value
    default_lambda = f2export.get_default_lambda()
    if default_lambda:
        dct_field_attribute["default"] = default_lambda.replace(
            "'", '"'
        )
    else:
        default_value = None
        if f2export.default:
            default_value = f2export.default
        else:
            dct_default_value = self.env[model_name].default_get(
                [f2export.name]
            )
            if dct_default_value:
                default_value = dct_default_value.get(f2export.name)
        if default_value:
            # TODO support default = None
            if f2export.ttype == "boolean" and (
                default_value == "True" or default_value is True
            ):
                dct_field_attribute["default"] = True
            elif f2export.ttype == "boolean" and (
                default_value == "False" or default_value is False
            ):
                # TODO Only if the field inherit, else None it
                dct_field_attribute["default"] = False
            elif f2export.ttype == "integer":
                dct_field_attribute["default"] = int(default_value)
            elif f2export.ttype in (
                "char",
                "selection",
                "text",
                "html",
            ):
                dct_field_attribute["default"] = default_value
            else:
                _logger.warning(
                    f"Not supported default type '{f2export.ttype}',"
                    f" field name '{f2export.name}', model"
                    f" '{f2export.model_id.model}', value"
                    f" '{default_value}'"
                )
                dct_field_attribute["default"] = default_value

    # TODO support states
    if f2export.groups:
        dct_field_attribute["groups"] = f2export.groups.mapped(
            lambda g: self._get_group_data_name(g)
        )

    compute = f2export.compute and f2export.depends

    if code_generator_compute:
        dct_field_attribute["compute"] = code_generator_compute
    elif compute:
        dct_field_attribute["compute"] = f"_compute_{f2export.name}"

    if (
        f2export.ttype == "one2many" or f2export.related or compute
    ) and f2export.copied:
        dct_field_attribute["copy"] = True

    # TODO support oldname

    # TODO support group_operator

    # TODO support inverse

    # TODO support search

    # TODO support store
    if f2export.store and code_generator_compute:
        dct_field_attribute["store"] = True
    elif (
        not f2export.store
        and not code_generator_compute
        and not related_field_id
    ):
        # By default, a computed field is not stored to the database, and is computed on-the-fly.
        dct_field_attribute["store"] = False

    # TODO support compute_sudo

    if f2export.translate:
        dct_field_attribute["translate"] = True

    # TODO not working, but no module need it
    # if not f2export.selectable and f2export.ttype == "one2many":
    #     # Default is True
    #     # Check _reflect_field_params in file odoo/odoo/addons/base/models/ir_model.py
    #     dct_field_attribute["selectable"] = False

    # TODO support digits, check dp.get_precision('Account')

    if f2export.help:
        dct_field_attribute["help"] = f2export.help.replace("\\'", '"')

    # Ignore it, by default it's copy=False
    # elif f2export.ttype != 'one2many' and not f2export.related and not compute and not f2export.copied:
    #     dct_field_attribute["copy"] = False

    if (
        f2export.code_generator_ir_model_fields_ids
        and f2export.code_generator_ir_model_fields_ids.filter_field_attribute
    ):
        # Filter list of attribute
        lst_attribute_to_filter = f2export.code_generator_ir_model_fields_ids.filter_field_attribute.split(
            ";"
        )
        lst_attribute_to_filter = [
            a.strip() for a in lst_attribute_to_filter if a.strip()
        ]

for key, value in dct_field_attribute.items():
    if lst_attribute_to_filter and key not in lst_attribute_to_filter:
        continue
    if type(value) is str:
        # TODO find another solution than removing \\n, this cause error with cw.CodeWriter
        copy_value = value.replace("'", "\\'")
        value = value.replace("\\n", " ").replace("'", "\\'")
        if key == "comodel_name":
            lst_first_field_attribute.append(f"{key}='{value}'")
        elif key == "ondelete":
            lst_last_field_attribute.append(f"{key}='{value}'")
        else:
            if (
                value.startswith("lambda")
                or value.startswith("date")
                or value.startswith("datetime")
            ):
                # Exception for lambda
                lst_field_attribute.append(f"{key}={value}")
            else:
                if "\\n" in copy_value:
                    has_endline = True
                    lst_field_attribute.append(
                        f"{key}='''{copy_value}'''"
                    )
                else:
                    lst_field_attribute.append(f"{key}='{copy_value}'")
    elif type(value) is list:
        # TODO find another solution than removing \\n, this cause error with cw.CodeWriter
        new_value = str(value).replace("\\n", " ")
        lst_field_attribute.append(f"{key}={new_value}")
    else:
        lst_field_attribute.append(f"{key}={value}")

lst_field_attribute = (
    lst_first_field_attribute
    + lst_field_attribute
    + lst_last_field_attribute
)

return lst_field_attribute, has_endline, compute, True""",
                    "name": "_generate_field_from_model",
                    "param": (
                        "self, f2export, model_name, lst_field_inherit,"
                        " dct_field_attr_diff"
                    ),
                    "sequence": 46,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Function to obtain the model fields
:param model:
:return:
"""
# TODO detect if contain code_generator_sequence, else order by name
# TODO some field.modules containts space, this is why it strip each element
# the field.modules is full when the module is installed, check file odoo/odoo/addons/base/models/ir_model.py fct _in_modules
f2exports = model.field_id.filtered(
    lambda field: field.name not in MAGIC_FIELDS
    and (
        module.name in [a.strip() for a in field.modules.split(",")]
        or not field.modules
    )
).sorted(key=lambda r: r.code_generator_sequence)

lst_inherit_model = self._get_lst_inherit_model(model)

if model.inherit_model_ids:
    is_whitelist = any(
        [a.is_show_whitelist_model_inherit_call() for a in f2exports]
    )
    if is_whitelist:
        f2exports = f2exports.filtered(
            lambda field: field.name not in MAGIC_FIELDS
            and not field.is_hide_blacklist_model_inherit
            and (
                not is_whitelist
                or (
                    is_whitelist
                    and field.is_show_whitelist_model_inherit_call()
                )
            )
        )
    # else:
    #     father_ids = self.env["ir.model"].browse(
    #         [a.depend_id.id for a in model.inherit_model_ids]
    #     )
    #     set_unique_field = set()
    #     for father_id in father_ids:
    #         fatherfieldnames = father_id.field_id.filtered(
    #             lambda field: field.name not in MAGIC_FIELDS
    #         ).mapped("name")
    #         set_unique_field.update(fatherfieldnames)
    #     f2exports = f2exports.filtered(
    #         lambda field: field.name not in list(set_unique_field)
    #     )

# Force field name first
field_rec_name = model.get_rec_name()
if not field_rec_name:
    field_rec_name = "name"
lst_field_rec_name = f2exports.filtered(
    lambda field: field.name == field_rec_name
)
if lst_field_rec_name:
    lst_field_not_name = f2exports.filtered(
        lambda field: field.name != field_rec_name
    )
    lst_id = lst_field_rec_name.ids + lst_field_not_name.ids
    f2exports = self.env["ir.model.fields"].browse(lst_id)

lst_field_to_write = []
for f2export in f2exports:
    lst_field_inherit = [
        b
        for a in lst_inherit_model
        for b in a.field_id
        if b.name == f2export.name
    ]
    # TODO update this list
    # Documentation to understand how attributes work, check file odoo/odoo/addons/base/models/ir_model.py function _instanciate_attrs
    lst_attribute_check_diff = [
        "readonly",
        "required",
        "field_description",  # String
        "relation_field",  # inverse_name
        "relation",  # comodel_name
        "relation_table",  # relation
        # "default",
        "help",
        # "context",
        "compute",
        "domain",
        "store",
    ]
    dct_field_attr_diff = defaultdict(list)
    # TODO éviter d'écraser une valeur pour le multi héritage
    for field_inherit in lst_field_inherit:
        for attr_name in lst_attribute_check_diff:
            try:
                actual_value = getattr(f2export, attr_name)
            except Exception as e:
                print(e)
            inherit_value = getattr(field_inherit, attr_name)
            if actual_value != inherit_value:
                dct_field_attr_diff[attr_name].append(inherit_value)
        self._find_field_computed(
            dct_field_attr_diff, f2export, field_inherit
        )
        self._find_field_default(
            dct_field_attr_diff, f2export, field_inherit
        )
    (
        lst_field_attribute,
        has_endline,
        compute,
        do_generate,
    ) = self._generate_field_from_model(
        f2export, model.model, lst_field_inherit, dct_field_attr_diff
    )
    if do_generate:
        lst_field_to_write.append(
            (lst_field_attribute, f2export, has_endline, compute)
        )

for (
    lst_field_attribute,
    f2export,
    has_endline,
    compute,
) in lst_field_to_write:
    cw.emit()
    if not has_endline:
        cw.emit_list(
            lst_field_attribute,
            ("(", ")"),
            before=(
                f"{f2export.name} ="
                f" {self._get_odoo_ttype_class(f2export.ttype)}"
            ),
        )
    else:
        cw.emit(
            f"{f2export.name} ="
            f" {self._get_odoo_ttype_class(f2export.ttype)}("
        )
        with cw.indent():
            for item in lst_field_attribute:
                if "\\n" in item:
                    lst_item = item.split("\\n")
                    cw.emit(f"{lst_item[0]}")
                    i_last = len(lst_item) - 2
                    for i, inter_item in enumerate(lst_item[1:]):
                        if i == i_last:
                            cw.emit_raw(f"{inter_item},\\n")
                        else:
                            cw.emit_raw(f"{inter_item}\\n")
                else:
                    cw.emit(f"{item},")
        cw.emit(")")

    if compute:
        cw.emit()
        l_depends = self._get_l_map(
            lambda e: e.strip(), f2export.depends.split(",")
        )

        cw.emit(
            f"@api.depends({self._prepare_compute_constrained_fields(l_depends)})"
        )
        cw.emit(f"def _compute_{f2export.name}(self):")

        l_compute = f2export.compute.split("\\n")
        # starting_spaces = 2
        # for line in l_compute:
        #     if self._get_starting_spaces(line) == 2:
        #         starting_spaces += 1
        #     l_model_fields.append('%s%s' % (TAB4 * starting_spaces, line.strip()))
        for line in l_compute:
            with cw.indent():
                cw.emit(line.rstrip())''',
                    "name": "_get_model_fields",
                    "param": "self, cw, model, module",
                    "sequence": 47,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """model_name = field_id.model
lst_field = [
    a
    for a in self.env[model_name]._field_computed.keys()
    if a.name == field_id.name
]
if lst_field:
    field_relation = lst_field[0]
    return field_relation.compute
return False""",
                    "name": "_get_compute_fct",
                    "param": "self, field_id",
                    "sequence": 48,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """default_value = field_id.get_default_lambda()
if not default_value:
    default_value = self.env[field_id.model].default_get(
        [field_id.name]
    )
    if default_value:
        default_value = default_value.get(field_id.name)
if not default_value:
    default_value = False
return default_value""",
                    "name": "_get_default",
                    "param": "self, field_id",
                    "sequence": 49,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """inherit_compute = self._get_compute_fct(field_inherit)
actual_compute = self._get_compute_fct(f2export)
if inherit_compute and not actual_compute:
    dct_field_attr_diff["compute"] = inherit_compute""",
                    "name": "_find_field_computed",
                    "param": (
                        "self, dct_field_attr_diff, f2export, field_inherit"
                    ),
                    "sequence": 50,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """inherit_default = self._get_default(field_inherit)
actual_default = self._get_default(f2export)
if inherit_default != actual_default:
    dct_field_attr_diff["default"] = inherit_default""",
                    "name": "_find_field_default",
                    "param": (
                        "self, dct_field_attr_diff, f2export, field_inherit"
                    ),
                    "sequence": 51,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": '''"""
Create log of code generator writer
:return:
"""
new_list = []
for vals in vals_list:
    new_list.append(self.generate_writer(vals))

return super(CodeGeneratorWriter, self).create(new_list)''',
                    "name": "create",
                    "decorator": "@api.model_create_multi",
                    "param": "self, vals_list",
                    "sequence": 52,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """l_model_csv_access = []
l_model_rules = []
dct_model_model_xmldata = {}

module.view_file_sync = {}
module.module_file_sync = {}

if module.template_model_name or module.template_inherit_model_name:
    i = -1
    lst_model = f"{module.template_model_name};{module.template_inherit_model_name}".strip(
        ";"
    ).split(
        ";"
    )
    for model in lst_model:
        i += 1
        model = model.strip()
        if model:
            module.view_file_sync[model] = ExtractorView(
                module, model, i
            )
            module.module_file_sync[model] = ExtractorModule(
                module, model, module.view_file_sync[model]
            )
            # TODO no need to keep memory
            ExtractorController(
                module, model, module.module_file_sync[model]
            )

for model in module.o2m_models:

    model_model = self._get_model_model(model.model)

    if not module.nomenclator_only:
        # Wizard
        self._set_model_py_file(module, model, model_model)
        self._set_model_xmlview_file(module, model, model_model)

        # Report
        self._set_model_xmlreport_file(module, model, model_model)

    parameters = self.env["ir.config_parameter"].sudo()
    s_data2export = parameters.get_param(
        "code_generator.s_data2export", default="nomenclator"
    )
    if s_data2export != "nomenclator" or (
        s_data2export == "nomenclator" and model.nomenclator
    ):
        dct_result_xmldata = self._set_model_xmldata_file(
            module, model, model_model
        )
        if dct_result_xmldata:
            dct_model_model_xmldata.update(dct_result_xmldata)

    if not module.nomenclator_only:
        l_model_csv_access += self._get_model_access(module, model)

        l_model_rules += self._get_model_rules(module, model)

l_model_csv_access = sorted(
    list(set(l_model_csv_access)),
    key=lambda x: x,
)
self._compute_xml_data_file(module, dct_model_model_xmldata)
self._write_xml_data_file(dct_model_model_xmldata)

if not module.nomenclator_only:
    application_icon = self._set_module_menus(module)

    self.set_xml_data_file(module)

    self.set_xml_views_file(module)

    self.set_module_python_file(module)

    self.set_module_css_file(module)

    self._set_module_security(
        module, l_model_rules, l_model_csv_access
    )

    self._set_static_description_file(module, application_icon)

    # TODO info Moved in template module
    # self.set_module_translator(module)

python_controller_writer.generate()

self.set_extra_get_lst_file_generate(module)

self.code_generator_data.reorder_manifest_data_files()

self._set_manifest_file(module)

self.set_module_init_file_extra(module)

self.code_generator_data.generate_python_init_file(module)

self.code_generator_data.auto_format()
if module.enable_pylint_check:
    # self.code_generator_data.flake8_check()
    self.code_generator_data.pylint_check()""",
                    "name": "get_lst_file_generate",
                    "param": "self, module, python_controller_writer",
                    "sequence": 53,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """pass""",
                    "name": "set_xml_data_file",
                    "param": "self, module",
                    "sequence": 54,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """pass""",
                    "name": "set_xml_views_file",
                    "param": "self, module",
                    "sequence": 55,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """pass""",
                    "name": "set_module_css_file",
                    "param": "self, module",
                    "sequence": 56,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """pass""",
                    "name": "set_module_python_file",
                    "param": "self, module",
                    "sequence": 57,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """pass""",
                    "name": "set_extra_get_lst_file_generate",
                    "param": "self, module",
                    "sequence": 58,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """pass""",
                    "name": "write_extra_pre_init_hook",
                    "param": "self, module, cw",
                    "sequence": 59,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """if module.list_scss_process_hook:
    lst_scss_process_hook = [
        a.strip() for a in module.list_scss_process_hook.split(";")
    ]
    for scss_process_hook in lst_scss_process_hook:
        cw.emit(f'xml_id = "{scss_process_hook}"')
        cw.emit("update_datas_ir_attachment_from_xmlid(env, xml_id)")
    cw.emit()""",
                    "name": "write_extra_post_init_hook",
                    "param": "self, module, cw",
                    "sequence": 60,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """pass""",
                    "name": "write_extra_uninstall_hook",
                    "param": "self, module, cw",
                    "sequence": 61,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """if module.list_scss_process_hook:
    cw.emit("def update_datas_ir_attachment_from_xmlid(env, xml_id):")
    with cw.indent():
        cw.emit(
            "dir_path ="
            " os.path.normpath(os.path.join(os.path.dirname(__file__),"
            ' ".."))'
        )
        cw.emit(
            'ir_attach_id_name = env["ir.model.data"].search([("name",'
            ' "=", xml_id)])'
        )
        cw.emit("if not ir_attach_id_name:")
        with cw.indent():
            cw.emit(
                '_logger.warning(f"Cannot find ir.attachment id'
                " '{xml_id}'\")"
            )
            cw.emit("return")
        cw.emit(
            "ir_attach_id ="
            ' env["ir.attachment"].browse(ir_attach_id_name.res_id)'
        )
        cw.emit("file_path = dir_path + ir_attach_id.url")
        cw.emit("if not os.path.isfile(file_path):")
        with cw.indent():
            cw.emit(
                "_logger.warning(f\"File not exist '{file_path}'\")"
            )
            cw.emit("return")
        cw.emit(
            'datas = base64.b64encode(open(file_path, "rb").read())'
        )
        cw.emit('ir_attach_id.write({"datas": datas})')""",
                    "name": "write_extra_extra_function_hook",
                    "param": "self, module, cw",
                    "sequence": 62,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """modules = self.env["code.generator.module"].browse(
    vals.get("code_generator_ids")
)

# path = tempfile.gettempdir()
path = tempfile.mkdtemp()
_logger.info(f"Temporary path for code generator: {path}")
morethanone = len(modules.ids) > 1
if morethanone:
    # TODO validate it's working
    path += "/modules"
    CodeGeneratorData.os_make_dirs(path)

# TODO is it necessary? os.chdir into sync_code to be back to normal
# os.chdir(path=path)

basename = (
    "modules" if morethanone else modules[0].name.lower().strip()
)
vals["basename"] = basename
rootdir = (
    path
    if morethanone
    else path + "/" + modules[0].name.lower().strip()
)
vals["rootdir"] = rootdir

for module in modules:
    # TODO refactor this to share variable in another class,
    #  like that, self.code_generator_data will be associate to a class of generation of module
    self.code_generator_data = CodeGeneratorData(module, path)
    python_controller_writer = PythonControllerWriter(
        module, self.code_generator_data
    )
    self.get_lst_file_generate(module, python_controller_writer)

    if module.enable_sync_code:
        self.code_generator_data.sync_code(
            module.path_sync_code, module.name
        )

vals["list_path_file"] = ";".join(
    self.code_generator_data.lst_path_file
)

return vals""",
                    "name": "generate_writer",
                    "decorator": "@api.multi",
                    "param": "self, vals",
                    "sequence": 63,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
                {
                    "code": """return self.list_path_file.split(";")""",
                    "name": "get_list_path_file",
                    "param": "self",
                    "sequence": 64,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_code_generator_writer.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Ir Model Server Constrain
        model_model = "ir.model.server_constrain"
        model_name = "ir_model_server_constrain"
        dct_model = {
            "description": "Code Generator Model Server Constrains",
            "rec_name": "constrained",
        }
        dct_field = {
            "constrained": {
                "code_generator_sequence": 3,
                "field_description": "Constrained",
                "help": "Constrained fields, ej: name, age",
                "required": True,
                "ttype": "char",
            },
            "m2o_ir_model": {
                "code_generator_sequence": 4,
                "domain": [("transient", "=", False)],
                "field_description": "Code generator Model",
                "help": "Model that will hold this server constrain",
                "relation": "ir.model",
                "required": True,
                "ttype": "many2one",
            },
            "txt_code": {
                "code_generator_sequence": 5,
                "field_description": "Code",
                "help": "Code to execute",
                "required": True,
                "ttype": "text",
            },
        }
        model_ir_model_server_constrain = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": '''import re

from odoo import _, api, fields, models, modules, tools
from odoo.addons.base.models.ir_model import SAFE_EVAL_BASE
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval

CONSTRAINEDLS = _(
    "The field Constrained lists the fields that the server constrain will"
    " check. It is a comma-separated list of field names, like name, size."
)
SERVERCONSTRAIN = _("%s Server constrain ")
SYNTAXERRORMSG = _("There is a syntax error in your %scode definition.")

SAFE_EVAL_BASE["re"] = re
SAFE_EVAL_BASE["ValidationError"] = ValidationError

SAFE_EVAL_4FUNCTION = SAFE_EVAL_BASE
SAFE_EVAL_4FUNCTION["api"] = api
SAFE_EVAL_4FUNCTION["models"] = models
SAFE_EVAL_4FUNCTION["fields"] = fields
SAFE_EVAL_4FUNCTION["_"] = _
PREDEFINEDVARS = _(
    "You specified a non predefined variable. The predefined variables are"
    " self, datetime, dateutil, time, re, ValidationError and the ones"
    " accessible through self, like self.env."
)


def common_4constrains(el_self, code, message=SYNTAXERRORMSG):
    """

    :param el_self:
    :param code:
    :param message:
    :return:
    """

    try:
        safe_eval(code, SAFE_EVAL_4FUNCTION, {"self": el_self}, mode="exec")

    except ValueError:
        raise ValidationError(PREDEFINEDVARS)

    except SyntaxError:
        raise ValidationError(message)''',
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ir_model_server_constrain.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """if self.constrained:
    splitted = self.constrained.split(",")
    if list(
        filter(
            lambda e: e.strip()
            not in self.env[self.m2o_ir_model.model]._fields.keys(),
            splitted,
        )
    ):
        raise ValidationError(CONSTRAINEDLS)""",
                    "name": "_check_constrained",
                    "decorator": '@api.onchange("constrained");@api.constrains("constrained")',
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model_server_constrain.id,
                },
                {
                    "code": """if self.txt_code:
    constrain_detail = SERVERCONSTRAIN % self.constrained
    common_4constrains(
        self.env[self.m2o_ir_model.model],
        self.txt_code,
        SYNTAXERRORMSG % constrain_detail,
    )""",
                    "name": "_check_txt_code",
                    "decorator": (
                        '@api.onchange("txt_code");@api.constrains("txt_code")'
                    ),
                    "param": "self",
                    "sequence": 1,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model_server_constrain.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Ir Actions Act Url
        model_model = "ir.actions.act_url"
        model_name = "ir_actions_act_url"
        lst_depend_model = ["ir.actions.act_url"]
        dct_field = {
            "m2o_code_generator": {
                "code_generator_sequence": 1,
                "field_description": "Code Generator",
                "help": "Code Generator relation",
                "is_show_whitelist_model_inherit": True,
                "relation": "code.generator.module",
                "ttype": "many2one",
            },
        }
        model_ir_actions_act_url = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ir_actions_act_url.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Ir Actions Act Window
        model_model = "ir.actions.act_window"
        model_name = "ir_actions_act_window"
        lst_depend_model = ["ir.actions.act_window"]
        dct_field = {
            "m2o_res_model": {
                "code_generator_sequence": 1,
                "field_description": "Res Model",
                "help": "Res Model",
                "is_show_whitelist_model_inherit": True,
                "relation": "ir.model",
                "ttype": "many2one",
            },
            "m2o_src_model": {
                "code_generator_sequence": 2,
                "field_description": "Src Model",
                "help": "Src Model",
                "is_show_whitelist_model_inherit": True,
                "relation": "ir.model",
                "ttype": "many2one",
            },
        }
        model_ir_actions_act_window = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ir_actions_act_window.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """if self.m2o_res_model:
    return dict(value=dict(res_model=self.m2o_res_model.model))""",
                    "name": "_onchange_m2o_res_model",
                    "decorator": '@api.onchange("m2o_res_model")',
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_actions_act_window.id,
                },
                {
                    "code": """if self.m2o_src_model:
    return dict(value=dict(src_model=self.m2o_src_model.model))""",
                    "name": "_onchange_m2o_src_model",
                    "decorator": '@api.onchange("m2o_src_model")',
                    "param": "self",
                    "sequence": 1,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_actions_act_window.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Ir Actions Report
        model_model = "ir.actions.report"
        model_name = "ir_actions_report"
        lst_depend_model = ["ir.actions.report"]
        dct_field = {
            "m2o_model": {
                "code_generator_compute": "_compute_m2os",
                "code_generator_sequence": 1,
                "field_description": "Code generator Model",
                "help": "Model related with this report",
                "is_show_whitelist_model_inherit": True,
                "relation": "ir.model",
                "store": True,
                "ttype": "many2one",
            },
            "m2o_template": {
                "code_generator_compute": "_compute_m2os",
                "code_generator_sequence": 2,
                "field_description": "Template",
                "help": "Template related with this report",
                "is_show_whitelist_model_inherit": True,
                "relation": "ir.ui.view",
                "ttype": "many2one",
            },
        }
        model_ir_actions_report = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ir_actions_report.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """for report in self:
    searched = self.env["ir.model"].search(
        [("model", "=", report.model.strip())]
    )
    if searched:
        report.m2o_model = searched[0].id

    stripped = report.report_name.strip()
    splitted = stripped.split(".")
    searched = self.env["ir.ui.view"].search(
        [
            ("type", "=", "qweb"),
            ("name", "=", splitted[len(splitted) - 1]),
        ]
    )
    if searched:
        report.m2o_template = searched[0].id""",
                    "name": "_compute_m2os",
                    "decorator": '@api.depends("model", "report_name")',
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_actions_report.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Ir Actions Server
        model_model = "ir.actions.server"
        model_name = "ir_actions_server"
        lst_depend_model = ["ir.actions.server"]
        dct_field = {
            "comment": {
                "code_generator_sequence": 1,
                "field_description": "Comment",
                "help": "Hint about this record.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
        }
        model_ir_actions_server = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ir_actions_server.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """if self.model_id.m2o_module and (
    self.state == "code" or self.state == "multi"
):
    result = dict()

    if self.state == "code":
        result.update(
            dict(
                value=dict(code="raise Warning('Not implemented yet')")
            )
        )

    if not self.binding_model_id:
        result.update(
            dict(
                warning=dict(
                    title="Contextual action",
                    message=(
                        "Remember to create the contextual action..."
                    ),
                )
            )
        )

    return result

elif self.model_id and self.state == "code":
    return dict(value=dict(code=self.DEFAULT_PYTHON_CODE))""",
                    "name": "_onchange_model_id_state",
                    "decorator": '@api.onchange("model_id", "state")',
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_actions_server.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Ir Actions Todo
        model_model = "ir.actions.todo"
        model_name = "ir_actions_todo"
        lst_depend_model = ["ir.actions.todo"]
        dct_field = {
            "m2o_code_generator": {
                "code_generator_sequence": 1,
                "field_description": "Code Generator",
                "help": "Code Generator relation",
                "is_show_whitelist_model_inherit": True,
                "relation": "code.generator.module",
                "ttype": "many2one",
            },
        }
        model_ir_actions_todo = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ir_actions_todo.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Ir Model
        model_model = "ir.model"
        model_name = "ir_model"
        lst_depend_model = ["ir.model"]
        dct_field = {
            "description": {
                "code_generator_sequence": 1,
                "field_description": "Description",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "diagram_arrow_dst_field": {
                "code_generator_sequence": 2,
                "field_description": "Diagram Arrow Dst Field",
                "help": "Diagram arrow field name for destination.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "diagram_arrow_form_view_ref": {
                "code_generator_sequence": 3,
                "field_description": "Diagram Arrow Form View Ref",
                "help": (
                    "Diagram arrow field, reference view xml id. If empty,"
                    " will take default form."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "diagram_arrow_label": {
                "code_generator_sequence": 4,
                "default": "['name']",
                "field_description": "Diagram Arrow Label",
                "help": "Diagram label, data to show when draw a line.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "diagram_arrow_object": {
                "code_generator_sequence": 5,
                "field_description": "Diagram Arrow Object",
                "help": "Diagram arrow model name for arrow.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "diagram_arrow_src_field": {
                "code_generator_sequence": 6,
                "field_description": "Diagram Arrow Src Field",
                "help": "Diagram arrow field name for source.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "diagram_label_string": {
                "code_generator_sequence": 7,
                "field_description": "Diagram Label String",
                "help": "Sentence to show at top of diagram.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "diagram_node_form_view_ref": {
                "code_generator_sequence": 8,
                "field_description": "Diagram Node Form View Ref",
                "help": (
                    "Diagram node field, reference view xml id. If empty, will"
                    " take default form."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "diagram_node_object": {
                "code_generator_sequence": 9,
                "field_description": "Diagram Node Object",
                "help": "Diagram model name for node.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "diagram_node_shape_field": {
                "code_generator_sequence": 10,
                "default": "rectangle:True",
                "field_description": "Diagram Node Shape Field",
                "help": "Diagram node field shape.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "diagram_node_xpos_field": {
                "code_generator_sequence": 11,
                "field_description": "Diagram Node Xpos Field",
                "help": "Diagram node field name for xpos.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "diagram_node_ypos_field": {
                "code_generator_sequence": 12,
                "field_description": "Diagram Node Ypos Field",
                "help": "Diagram node field name for ypos.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "enable_activity": {
                "code_generator_sequence": 13,
                "field_description": "Enable Activity",
                "help": (
                    "Will add chatter and activity to this model in form view."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "expression_export_data": {
                "code_generator_sequence": 14,
                "field_description": "Expression Export Data",
                "help": (
                    "Set an expression to apply filter when exporting data."
                    ' example ("website_id", "in", [1,2]). Keep it empty to'
                    " export all data."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "ignore_name_export_data": {
                "code_generator_sequence": 15,
                "field_description": "Ignore Name Export Data",
                "help": "List of ignore file_name separate by ;",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "inherit_model_ids": {
                "code_generator_form_simple_view_sequence": 15,
                "code_generator_sequence": 16,
                "field_description": "Inherit ir Model",
                "help": "Inherit Model",
                "is_show_whitelist_model_inherit": True,
                "relation": "code.generator.ir.model.dependency",
                "ttype": "many2many",
            },
            "m2o_inherit_py_class": {
                "code_generator_form_simple_view_sequence": 14,
                "code_generator_sequence": 17,
                "field_description": "Python Class",
                "help": "Python Class",
                "is_show_whitelist_model_inherit": True,
                "relation": "code.generator.pyclass",
                "ttype": "many2one",
            },
            "m2o_module": {
                "code_generator_form_simple_view_sequence": 13,
                "code_generator_sequence": 18,
                "field_description": "Module",
                "help": "Module",
                "is_show_whitelist_model_inherit": True,
                "relation": "code.generator.module",
                "ttype": "many2one",
            },
            "menu_group": {
                "code_generator_sequence": 19,
                "field_description": "Menu Group",
                "help": (
                    "If not empty, will create a group of element in menu when"
                    " auto-generate."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "menu_label": {
                "code_generator_sequence": 20,
                "field_description": "Menu Label",
                "help": "Force label menu to use this value.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "menu_name_keep_application": {
                "code_generator_sequence": 21,
                "field_description": "Menu Name Keep Application",
                "help": (
                    "When generate menu name, do we keep application name in"
                    " item name?"
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "menu_parent": {
                "code_generator_sequence": 22,
                "field_description": "Menu Parent",
                "help": (
                    "If not empty, will create a new root menu of element in"
                    " menu when auto-generate."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "nomenclator": {
                "code_generator_form_simple_view_sequence": 16,
                "code_generator_sequence": 23,
                "field_description": "Nomenclator?",
                "help": "Set this if you want this model as a nomenclator",
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "rec_name": {
                "code_generator_form_simple_view_sequence": 12,
                "code_generator_sequence": 31,
                "default": "name",
                "field_description": "Rec Name",
                "help": (
                    "Will be the field name to use when show the generic name."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
        }
        model_ir_model = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """import importlib
import logging

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError
from odoo.models import MAGIC_COLUMNS

_logger = logging.getLogger(__name__)

MAGIC_FIELDS = MAGIC_COLUMNS + [
    "display_name",
    "__last_update",
    "access_url",
    "access_token",
    "access_warning",
]""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ir_model.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """if self.m2o_module:

    name4filter = "x_name"
    name4newfield = "name"

else:

    name4filter = "xname"
    name4newfield = "x_name"

remain = self.field_id.filtered(
    lambda field: field.name != name4filter
)

return dict(
    value=dict(
        field_id=[
            (6, False, remain.ids),
            (
                0,
                False,
                dict(
                    name=name4newfield,
                    field_description="Name",
                    ttype="char",
                ),
            ),
        ]
    )
)""",
                    "name": "_onchange_m2o_module",
                    "decorator": '@api.onchange("m2o_module")',
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model.id,
                },
                {
                    "code": """for model in self:
    if model.state == "manual":
        if not model.m2o_module and not model.model.startswith("x_"):
            raise ValidationError(
                _("The model name must start with 'x_'.")
            )
    if not models.check_object_name(model.model):
        raise ValidationError(
            _(
                "The model name %s can only contain lowercase"
                " characters, digits, underscores and dots."
            )
            % model.model
        )""",
                    "name": "_check_model_name",
                    "decorator": '@api.constrains("model")',
                    "param": "self",
                    "sequence": 1,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model.id,
                },
                {
                    "code": """return self.rec_name if self.rec_name else self._rec_name""",
                    "name": "get_rec_name",
                    "param": "self",
                    "sequence": 2,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model.id,
                },
                {
                    "code": '''"""

:param model_name: list or string
:return:
"""
lst_model_id = []
if type(model_name) is str:
    lst_model_name = [model_name]
elif type(model_name) is list:
    lst_model_name = model_name
elif isinstance(model_name, models.Model):
    lst_model_name = []
    lst_model_id = model_name
else:
    _logger.error(
        "Wrong type of model_name in method add_model_inherit:"
        f" {type(model_name)}"
    )
    return
for ir_model in self:
    inherit_model = None
    if lst_model_id:
        for check_inherit_model in lst_model_id:
            if check_inherit_model.id not in [
                a.depend_id.id for a in ir_model.inherit_model_ids
            ]:
                if not inherit_model:
                    inherit_model = check_inherit_model
                else:
                    inherit_model += check_inherit_model
    else:
        for model_name in lst_model_name:
            check_inherit_model = self.env["ir.model"].search(
                [("model", "=", model_name)]
            )
            if check_inherit_model.id not in [
                a.depend_id.id for a in ir_model.inherit_model_ids
            ]:
                if not inherit_model:
                    inherit_model = check_inherit_model
                else:
                    inherit_model += check_inherit_model

    if not inherit_model:
        return

    lst_create = [{"depend_id": a.id} for a in inherit_model]
    depend_ids = self.env["code.generator.ir.model.dependency"].create(
        lst_create
    )
    ir_model.inherit_model_ids = depend_ids.ids

    # Add missing field
    actual_field_list = set(ir_model.field_id.mapped("name"))
    lst_dct_field = []
    for ir_model_id in inherit_model:
        diff_list = list(
            set(ir_model_id.field_id.mapped("name")).difference(
                actual_field_list
            )
        )
        lst_new_field = [
            a for a in ir_model_id.field_id if a.name in diff_list
        ]
        for new_field_id in lst_new_field:
            # TODO support ttype selection, who extract this information?
            if new_field_id.ttype == "selection":
                continue
            value_field_backup_format = {
                "name": new_field_id.name,
                "model": ir_model.model,
                "field_description": new_field_id.field_description,
                "ttype": new_field_id.ttype,
                "model_id": ir_model.id,
                "ignore_on_code_generator_writer": True,
            }
            tpl_relation = ("many2one", "many2many", "one2many")
            tpl_relation_field = ("many2many", "one2many")
            if new_field_id.ttype in tpl_relation:
                value_field_backup_format[
                    "relation"
                ] = new_field_id.relation

            if (
                new_field_id.ttype in tpl_relation_field
                and new_field_id.relation_field
            ):
                value_field_backup_format[
                    "relation_field"
                ] = new_field_id.relation_field

            lst_dct_field.append(value_field_backup_format)
    if lst_dct_field:
        self.env["ir.model.fields"].create(lst_dct_field)''',
                    "name": "add_model_inherit",
                    "decorator": "@api.multi",
                    "param": "self, model_name",
                    "sequence": 3,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model.id,
                },
                {
                    "code": """for inherit_model_id in self.inherit_model_ids:
    # if inherit_model_id.ir_model_ids.ids == self.ids:
    #     return True
    if inherit_model_id.depend_id.id in self.ids:
        return True
return False""",
                    "name": "has_same_model_in_inherit_model",
                    "decorator": "@api.model",
                    "param": "self",
                    "sequence": 4,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model.id,
                },
                {
                    "code": """custommodelclass = super(IrModel, self)._instanciate(model_data)

try:
    if "rec_name" in model_data and model_data["rec_name"]:
        # TODO this was commented because it caused stack overflow when running with pydev
        # model_fields = self.field_id.search([('model_id', '=', model_data['id'])]). \
        #     filtered(lambda f: f.name not in MAGIC_FIELDS)
        #
        # if model_fields and not model_fields.filtered(lambda f: f.name == model_data['rec_name']):
        #     raise ValidationError(_('The Record Label value must exist within the model fields name.'))

        custommodelclass._rec_name = model_data["rec_name"]

    if (
        "inherit_model_ids" in model_data
        and model_data["inherit_model_ids"]
    ):
        lst_inherit = [
            a.depend_id.model for a in model_data["inherit_model_ids"]
        ]
        if lst_inherit:
            if len(lst_inherit) == 1:
                custommodelclass._inherit = lst_inherit[0]
            else:
                custommodelclass._inherit = lst_inherit

    if (
        "m2o_inherit_py_class" in model_data
        and model_data["m2o_inherit_py_class"]
    ):

        try:
            py_class = self.env["code.generator.pyclass"].browse(
                model_data["m2o_inherit_py_class"]
            )
            m2o_inherit_py_class_module = importlib.import_module(
                py_class.module
            )
            m2o_inherit_py_class = getattr(
                m2o_inherit_py_class_module, py_class.name
            )

            class CustomModelInheritedPyClass(
                custommodelclass, m2o_inherit_py_class
            ):
                pass

            return CustomModelInheritedPyClass

        except AttributeError:
            pass

except RecursionError:
    pass

return custommodelclass""",
                    "name": "_instanciate",
                    "decorator": "@api.model",
                    "param": "self, model_data",
                    "sequence": 5,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Ir Model Constraint
        model_model = "ir.model.constraint"
        model_name = "ir_model_constraint"
        lst_depend_model = ["ir.model.constraint"]
        dct_field = {
            "code_generator_id": {
                "code_generator_sequence": 1,
                "field_description": "Code Generator",
                "is_show_whitelist_model_inherit": True,
                "relation": "code.generator.module",
                "ttype": "many2one",
            },
            "message": {
                "code_generator_sequence": 2,
                "field_description": "Message",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "model_state": {
                "code_generator_sequence": 3,
                "field_description": "Type",
                "is_show_whitelist_model_inherit": True,
                "selection": (
                    "[('manual', 'Custom Object'), ('base', 'Base Object')]"
                ),
                "ttype": "selection",
            },
            "module": {
                "code_generator_sequence": 4,
                "default_lambda": (
                    "lambda self:"
                    " self.env['ir.module.module'].search([('name', '=',"
                    " 'base')])[    0].id"
                ),
                "field_description": "Module",
                "is_show_whitelist_model_inherit": True,
                "relation": "ir.module.module",
                "required": True,
                "ttype": "many2one",
            },
        }
        model_ir_model_constraint = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": '''import logging
import re

from psycopg2._psycopg import ProgrammingError

from odoo import _, api, fields, models, tools
from odoo.exceptions import MissingError, ValidationError

_logger = logging.getLogger(__name__)

CONSCREATEUNABLE = _("Unable to create the constraint.")
CONSDELETECREATEUNABLE = _(
    "Since you modify the sql constraint definition we must delete it and"
    " create a new one, and we were unable to do it."
)
CONSMODIFYUNABLE = _("Unable to modify the constraint.")
CONSDELETEUNABLE = _("Unable to delete the constraint.")


def sql_constraint(el_self, constraints):
    cr = el_self._cr
    foreign_key_re = re.compile(r"\s*foreign\s+key\\b.*", re.I)

    def process(key, definition):
        conname = "%s_%s" % (el_self._table, key)
        current_definition = tools.constraint_definition(
            cr, el_self._table, conname
        )
        if not current_definition:
            # constraint does not exists
            return add_constraint(cr, el_self._table, conname, definition)
        elif current_definition != definition:
            # constraint exists but its definition may have changed
            drop_constraint(cr, el_self._table, conname)
            return add_constraint(cr, el_self._table, conname, definition)

        else:
            return True

    result = False
    for sql_key, sql_definition, _ in constraints:
        if foreign_key_re.match(sql_definition):
            el_self.pool.post_init(process, sql_key, sql_definition)
        else:
            result = process(sql_key, sql_definition)

        if not result:
            break

    return result


def add_constraint(cr, tablename, constraintname, definition):
    """Add a constraint on the given table."""
    query1 = 'ALTER TABLE "{}" ADD CONSTRAINT "{}" {}'.format(
        tablename, constraintname, definition
    )
    query2 = 'COMMENT ON CONSTRAINT "{}" ON "{}" IS %s'.format(
        constraintname, tablename
    )
    try:
        with cr.savepoint():
            cr.execute(query1)
            cr.execute(query2, (definition,))
            _logger.debug(
                "Table %r: added constraint %r as %s",
                tablename,
                constraintname,
                definition,
            )
            return True
    except Exception:
        msg = (
            "Table %r: unable to add constraint %r!\\nIf you want to have it,"
            " you should update the records and execute manually:\\n%s"
        )
        _logger.warning(msg, tablename, constraintname, query1, exc_info=True)
        return False


def drop_constraint(cr, tablename, constraintname):
    """drop the given constraint."""
    try:
        with cr.savepoint():
            cr.execute(
                'ALTER TABLE "{}" DROP CONSTRAINT "{}"'.format(
                    tablename, constraintname
                )
            )
            _logger.debug(
                "Table %r: dropped constraint %r", tablename, constraintname
            )
            return True
    except ProgrammingError as proerror:
        return proerror.pgerror.count("does not exist") or False

    except Exception:
        _logger.warning(
            "Table %r: unable to drop constraint %r!",
            tablename,
            constraintname,
        )
        return False''',
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ir_model_constraint.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """imcs = super(IrModelConstraint, self).create(vals_list)

for imc in imcs:
    m_target = self.env[imc.model.model]
    t_constrain = (imc.name, imc.definition, imc.message)
    if not sql_constraint(
        m_target, m_target._sql_constraints + [t_constrain]
    ):
        raise ValidationError(CONSCREATEUNABLE)

return imcs""",
                    "name": "create",
                    "decorator": "@api.model_create_multi",
                    "param": "self, vals_list",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model_constraint.id,
                },
                {
                    "code": """if "definition" in vals:
    for imc in self:
        tablename = self.env[imc.model.model]._table
        if not drop_constraint(
            self._cr, tablename, "%s_%s" % (tablename, imc.name)
        ):
            raise ValidationError(CONSDELETECREATEUNABLE)

result = super(IrModelConstraint, self).write(vals)

for imc in self:
    m_target = self.env[imc.model.model]
    t_constrain = (imc.name, imc.definition, imc.message)
    if not sql_constraint(m_target, [t_constrain]):
        raise ValidationError(CONSMODIFYUNABLE)

return result""",
                    "name": "write",
                    "decorator": "@api.multi",
                    "param": "self, vals",
                    "sequence": 1,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model_constraint.id,
                },
                {
                    "code": """for imc in self:
    try:
        tablename = self.env[imc.model.model]._table
        if not drop_constraint(
            self._cr, tablename, "%s_%s" % (tablename, imc.name)
        ):
            raise ValidationError(CONSDELETEUNABLE)

    except MissingError:
        _logger.warning(
            "The registry entry associated with %s no longer exists"
            % imc.model.model
        )

return super(IrModelConstraint, self).unlink()""",
                    "name": "unlink",
                    "decorator": "@api.multi",
                    "param": "self",
                    "sequence": 2,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model_constraint.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Ir Model Fields
        model_model = "ir.model.fields"
        model_name = "ir_model_fields"
        lst_depend_model = ["ir.model.fields"]
        dct_field = {
            "code_generator_calendar_view_sequence": {
                "code_generator_sequence": 1,
                "field_description": "calendar view sequence",
                "help": (
                    "Sequence to write this field in calendar view from Code"
                    " Generator."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "integer",
            },
            "code_generator_compute": {
                "code_generator_sequence": 2,
                "field_description": "Compute Code Generator",
                "help": "Compute method to code_generator_writer.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "code_generator_form_simple_view_sequence": {
                "code_generator_sequence": 3,
                "field_description": "Form simple view sequence",
                "help": (
                    "Sequence to write this field in form simple view from"
                    " Code Generator."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "integer",
            },
            "code_generator_graph_view_sequence": {
                "code_generator_sequence": 4,
                "field_description": "graph view sequence",
                "help": (
                    "Sequence to write this field in graph view from Code"
                    " Generator."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "integer",
            },
            "code_generator_kanban_view_sequence": {
                "code_generator_sequence": 6,
                "field_description": "Kanban view sequence",
                "help": (
                    "Sequence to write this field in kanban view from Code"
                    " Generator."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "integer",
            },
            "code_generator_pivot_view_sequence": {
                "code_generator_sequence": 7,
                "field_description": "pivot view sequence",
                "help": (
                    "Sequence to write this field in pivot view from Code"
                    " Generator."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "integer",
            },
            "code_generator_search_sequence": {
                "code_generator_sequence": 8,
                "field_description": "Search sequence",
                "help": (
                    "Sequence to write this field in search from Code"
                    " Generator."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "integer",
            },
            "code_generator_search_view_sequence": {
                "code_generator_sequence": 9,
                "field_description": "search view sequence",
                "help": (
                    "Sequence to write this field in search view from Code"
                    " Generator."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "integer",
            },
            "code_generator_sequence": {
                "code_generator_sequence": 10,
                "field_description": "Sequence Code Generator",
                "help": "Sequence to write this field from Code Generator.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "integer",
            },
            "code_generator_tree_view_sequence": {
                "code_generator_sequence": 11,
                "field_description": "Tree view sequence",
                "help": (
                    "Sequence to write this field in tree view from Code"
                    " Generator."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "integer",
            },
            "default": {
                "code_generator_sequence": 12,
                "field_description": "Default value",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "default_lambda": {
                "code_generator_sequence": 13,
                "field_description": "Default lambda value",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "field_context": {
                "code_generator_sequence": 14,
                "field_description": "Field Context",
                "is_show_whitelist_model_inherit": True,
                "ttype": "char",
            },
            "force_widget": {
                "code_generator_sequence": 15,
                "field_description": "Force widget",
                "help": "Use this widget for this field when create views.",
                "is_show_whitelist_model_inherit": True,
                "selection": (
                    "[('barcode_handler', 'Barcode handler'), ('handle',"
                    " 'Handle'), ('float_with_uom', 'Float with uom'),"
                    " ('timesheet_uom', 'Timesheet uom'), ('radio', 'Radio'),"
                    " ('priority', 'Priority'), ('mail_thread', 'Mail"
                    " thread'), ('mail_activity', 'Mail activity'),"
                    " ('mail_followers', 'Mail followers'), ('phone',"
                    " 'Phone'), ('statinfo', 'Statinfo'), ('statusbar',"
                    " 'Statusbar'), ('many2many', 'Many2many'),"
                    " ('many2many_tags', 'Many2many tags'),"
                    " ('many2many_tags_email', 'Many2many tags email'),"
                    " ('many2many_checkboxes', 'Many2many checkboxes'),"
                    " ('many2many_binary', 'Many2many binary'), ('monetary',"
                    " 'Monetary'), ('selection', 'Selection'), ('url', 'Url'),"
                    " ('boolean_button', 'Boolean button'), ('boolean_toggle',"
                    " 'Boolean toggle'), ('toggle_button', 'Toggle button'),"
                    " ('state_selection', 'State selection'),"
                    " ('kanban_state_selection', 'Kanban state selection'),"
                    " ('kanban_activity', 'Kanban activity'),"
                    " ('tier_validation', 'Tier validation'), ('binary_size',"
                    " 'Binary size'), ('binary_preview', 'Binary preview'),"
                    " ('char_domain', 'Char domain'), ('domain', 'Domain'),"
                    " ('file_actions', 'File actions'), ('color', 'Color'),"
                    " ('copy_binary', 'Copy binary'), ('share_char', 'Share"
                    " char'), ('share_text', 'Share text'), ('share_binary',"
                    " 'Share binary'), ('selection_badge', 'Selection badge'),"
                    " ('link_button', 'Link button'), ('image', 'Image'),"
                    " ('contact', 'Contact'), ('float_time', 'Float time'),"
                    " ('image-url', 'Image-url'), ('html', 'Html'), ('email',"
                    " 'Email'), ('website_button', 'Website button'),"
                    " ('one2many', 'One2many'), ('one2many_list', 'One2many"
                    " list'), ('gauge', 'Gauge'), ('label_selection', 'Label"
                    " selection'), ('percentpie', 'Percentpie'),"
                    " ('progressbar', 'Progressbar'), ('mrp_time_counter',"
                    " 'Mrp time counter'), ('qty_available', 'Qty available'),"
                    " ('ace', 'Ace'), ('pdf_viewer', 'Pdf viewer'),"
                    " ('path_names', 'Path names'), ('path_json', 'Path"
                    " json'), ('date', 'Date'), ('color_index', 'Color"
                    " index'), ('google_partner_address', 'Google partner"
                    " address'), ('google_marker_picker', 'Google marker"
                    " picker'), ('spread_line_widget', 'Spread line widget'),"
                    " ('geo_edit_map', 'Geo edit map'), ('dynamic_dropdown',"
                    " 'Dynamic dropdown'), ('section_and_note_one2many',"
                    " 'Section and note one2many'), ('section_and_note_text',"
                    " 'Section and note text'), ('reference', 'Reference'),"
                    " ('x2many_2d_matrix', 'X2many 2d matrix'),"
                    " ('numeric_step', 'Numeric step'), ('BVEEditor',"
                    " 'Bveeditor'), ('er_diagram_image', 'Er diagram image'),"
                    " ('u2f_scan', 'U2f scan'), ('password', 'Password'),"
                    " ('open_tab', 'Open tab'), ('signature', 'Signature'),"
                    " ('upgrade_boolean', 'Upgrade boolean'),"
                    " ('many2manyattendee', 'Many2manyattendee'),"
                    " ('res_partner_many2one', 'Res partner many2one'),"
                    " ('hr_org_chart', 'Hr org chart'), ('CopyClipboardText',"
                    " 'Copyclipboardtext'), ('CopyClipboardChar',"
                    " 'Copyclipboardchar'), ('bullet_state', 'Bullet state'),"
                    " ('pad', 'Pad'), ('field_partner_autocomplete', 'Field"
                    " partner autocomplete'), ('html_frame', 'Html frame'),"
                    " ('task_workflow', 'Task workflow'),"
                    " ('document_page_reference', 'Document page reference'),"
                    " ('mis_report_widget', 'Mis report widget'), ('kpi',"
                    " 'Kpi'), ('action_barcode_handler', 'Action barcode"
                    " handler'), ('mail_failed_message', 'Mail failed"
                    " message'), ('mermaid', 'Mermaid'), ('payment',"
                    " 'Payment'), ('previous_order', 'Previous order')]"
                ),
                "ttype": "selection",
            },
            "ignore_on_code_generator_writer": {
                "code_generator_sequence": 16,
                "field_description": "Ignore On Code Generator Writer",
                "help": "Enable this to ignore it when write code.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_date_end_view": {
                "code_generator_sequence": 17,
                "field_description": "Show end date view",
                "help": "View timeline only, end field.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_date_start_view": {
                "code_generator_sequence": 18,
                "field_description": "Show start date view",
                "help": "View timeline only, start field.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_hide_blacklist_calendar_view": {
                "code_generator_sequence": 19,
                "field_description": "Hide in blacklist calendar view",
                "help": (
                    "Hide from view when field is blacklisted. View calendar"
                    " only."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_hide_blacklist_form_view": {
                "code_generator_sequence": 20,
                "field_description": "Hide in blacklist form view",
                "help": (
                    "Hide from view when field is blacklisted. View form only."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_hide_blacklist_graph_view": {
                "code_generator_sequence": 21,
                "field_description": "Hide in blacklist graph view",
                "help": (
                    "Hide from view when field is blacklisted. View graph"
                    " only."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_hide_blacklist_kanban_view": {
                "code_generator_sequence": 22,
                "field_description": "Hide in blacklist kanban view",
                "help": (
                    "Hide from view when field is blacklisted. View kanban"
                    " only."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_hide_blacklist_list_view": {
                "code_generator_sequence": 23,
                "field_description": "Hide in blacklist list view",
                "help": (
                    "Hide from view when field is blacklisted. View list only."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_hide_blacklist_model_inherit": {
                "code_generator_sequence": 24,
                "field_description": "Hide in blacklist model inherit",
                "help": "Hide from model inherit when field is blacklisted.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_hide_blacklist_pivot_view": {
                "code_generator_sequence": 25,
                "field_description": "Hide in blacklist pivot view",
                "help": (
                    "Hide from view when field is blacklisted. View pivot"
                    " only."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_hide_blacklist_search_view": {
                "code_generator_sequence": 26,
                "field_description": "Hide in blacklist search view",
                "help": (
                    "Hide from view when field is blacklisted. View search"
                    " only."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_show_whitelist_calendar_view": {
                "code_generator_sequence": 27,
                "field_description": "Show in whitelist calendar view",
                "help": (
                    "If a field in model is in whitelist, all is not will be"
                    " hide. View calendar only."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_show_whitelist_form_view": {
                "code_generator_sequence": 28,
                "field_description": "Show in whitelist form view",
                "help": (
                    "If a field in model is in whitelist, all is not will be"
                    " hide. View form only."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_show_whitelist_graph_view": {
                "code_generator_sequence": 29,
                "field_description": "Show in whitelist graph view",
                "help": (
                    "If a field in model is in whitelist, all is not will be"
                    " hide. View graph only."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_show_whitelist_kanban_view": {
                "code_generator_sequence": 30,
                "field_description": "Show in whitelist kanban view",
                "help": (
                    "If a field in model is in whitelist, all is not will be"
                    " hide. View kanban only."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_show_whitelist_list_view": {
                "code_generator_sequence": 31,
                "field_description": "Show in whitelist list view",
                "help": (
                    "If a field in model is in whitelist, all is not will be"
                    " hide. View list only."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_show_whitelist_model_inherit": {
                "code_generator_sequence": 32,
                "field_description": "Show in whitelist model inherit",
                "help": (
                    "If a field in model is in whitelist, will be show in"
                    " generated model."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_show_whitelist_pivot_view": {
                "code_generator_sequence": 33,
                "field_description": "Show in whitelist pivot view",
                "help": (
                    "If a field in model is in whitelist, all is not will be"
                    " hide. View pivot only."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_show_whitelist_search_view": {
                "code_generator_sequence": 34,
                "field_description": "Show in whitelist search view",
                "help": (
                    "If a field in model is in whitelist, all is not will be"
                    " hide. View search only."
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
        }
        model_ir_model_fields = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """import ast
import inspect
import logging
import types

import astor

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

FORCE_WIDGET_TYPES = [
    ("barcode_handler", "Barcode handler"),
    ("handle", "Handle"),
    ("float_with_uom", "Float with uom"),
    ("timesheet_uom", "Timesheet uom"),
    ("radio", "Radio"),
    ("priority", "Priority"),
    ("mail_thread", "Mail thread"),
    ("mail_activity", "Mail activity"),
    ("mail_followers", "Mail followers"),
    ("phone", "Phone"),
    ("statinfo", "Statinfo"),
    ("statusbar", "Statusbar"),
    ("many2many", "Many2many"),
    ("many2many_tags", "Many2many tags"),
    ("many2many_tags_email", "Many2many tags email"),
    ("many2many_checkboxes", "Many2many checkboxes"),
    ("many2many_binary", "Many2many binary"),
    ("monetary", "Monetary"),
    ("selection", "Selection"),
    ("url", "Url"),
    ("boolean_button", "Boolean button"),
    ("boolean_toggle", "Boolean toggle"),
    ("toggle_button", "Toggle button"),
    ("state_selection", "State selection"),
    ("kanban_state_selection", "Kanban state selection"),
    ("kanban_activity", "Kanban activity"),
    ("tier_validation", "Tier validation"),
    ("binary_size", "Binary size"),
    ("binary_preview", "Binary preview"),
    ("char_domain", "Char domain"),
    ("domain", "Domain"),
    ("file_actions", "File actions"),
    ("color", "Color"),
    ("copy_binary", "Copy binary"),
    ("share_char", "Share char"),
    ("share_text", "Share text"),
    ("share_binary", "Share binary"),
    ("selection_badge", "Selection badge"),
    ("link_button", "Link button"),
    ("image", "Image"),
    ("contact", "Contact"),
    ("float_time", "Float time"),
    ("image-url", "Image-url"),
    ("html", "Html"),
    ("email", "Email"),
    ("website_button", "Website button"),
    ("one2many", "One2many"),
    ("one2many_list", "One2many list"),
    ("gauge", "Gauge"),
    ("label_selection", "Label selection"),
    ("percentpie", "Percentpie"),
    ("progressbar", "Progressbar"),
    ("mrp_time_counter", "Mrp time counter"),
    ("qty_available", "Qty available"),
    ("ace", "Ace"),
    ("pdf_viewer", "Pdf viewer"),
    ("path_names", "Path names"),
    ("path_json", "Path json"),
    ("date", "Date"),
    ("color_index", "Color index"),
    ("google_partner_address", "Google partner address"),
    ("google_marker_picker", "Google marker picker"),
    ("spread_line_widget", "Spread line widget"),
    ("geo_edit_map", "Geo edit map"),
    ("dynamic_dropdown", "Dynamic dropdown"),
    ("section_and_note_one2many", "Section and note one2many"),
    ("section_and_note_text", "Section and note text"),
    ("reference", "Reference"),
    ("x2many_2d_matrix", "X2many 2d matrix"),
    ("numeric_step", "Numeric step"),
    ("BVEEditor", "Bveeditor"),
    ("er_diagram_image", "Er diagram image"),
    ("u2f_scan", "U2f scan"),
    ("password", "Password"),
    ("open_tab", "Open tab"),
    ("signature", "Signature"),
    ("upgrade_boolean", "Upgrade boolean"),
    ("many2manyattendee", "Many2manyattendee"),
    ("res_partner_many2one", "Res partner many2one"),
    ("hr_org_chart", "Hr org chart"),
    ("CopyClipboardText", "Copyclipboardtext"),
    ("CopyClipboardChar", "Copyclipboardchar"),
    ("bullet_state", "Bullet state"),
    ("pad", "Pad"),
    ("field_partner_autocomplete", "Field partner autocomplete"),
    ("html_frame", "Html frame"),
    ("task_workflow", "Task workflow"),
    ("document_page_reference", "Document page reference"),
    ("mis_report_widget", "Mis report widget"),
    ("kpi", "Kpi"),
    ("action_barcode_handler", "Action barcode handler"),
    ("mail_failed_message", "Mail failed message"),
    ("mermaid", "Mermaid"),
    ("payment", "Payment"),
    ("previous_order", "Previous order"),
]""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ir_model_fields.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """for field in self:
    if field.state == "manual":
        if (
            not field.model_id.m2o_module
            and not field.name.startswith("x_")
        ):
            raise ValidationError(
                _(
                    "Custom fields must have a name that starts with"
                    " 'x_' !"
                )
            )
    try:
        models.check_pg_name(field.name)
    except ValidationError:
        msg = _(
            "Field names can only contain characters, digits and"
            " underscores (up to 63)."
        )
        raise ValidationError(msg)""",
                    "name": "_check_name",
                    "decorator": '@api.constrains("name", "state")',
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model_fields.id,
                },
                {
                    "code": """if self.code_generator_ir_model_fields_ids:
    return (
        self.code_generator_ir_model_fields_ids.is_show_whitelist_model_inherit
    )
return self.is_show_whitelist_model_inherit""",
                    "name": "is_show_whitelist_model_inherit_call",
                    "decorator": "@api.model",
                    "param": "self",
                    "sequence": 1,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model_fields.id,
                },
                {
                    "code": """if self.code_generator_ir_model_fields_ids:
    return self.code_generator_ir_model_fields_ids.default_lambda
return self.default_lambda""",
                    "name": "get_default_lambda",
                    "decorator": "@api.model",
                    "param": "self",
                    "sequence": 2,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model_fields.id,
                },
                {
                    "code": """if self.code_generator_ir_model_fields_ids:
    return self.code_generator_ir_model_fields_ids.field_context
return self.field_context""",
                    "name": "get_field_context",
                    "decorator": "@api.model",
                    "param": "self",
                    "sequence": 3,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model_fields.id,
                },
                {
                    "code": """if self.code_generator_ir_model_fields_ids:
    if len(self.code_generator_ir_model_fields_ids) > 1:
        # Check if multiple field before crash without message
        lst_model = set(
            [
                a.m2o_fields.model
                for a in self.code_generator_ir_model_fields_ids
            ]
        )
        lst_field = [
            a.name for a in self.code_generator_ir_model_fields_ids
        ]
        raise Exception(
            f"Cannot compute multiple field. In model {lst_model},"
            f" List of field: {lst_field}"
        )
    else:
        return (
            self.code_generator_ir_model_fields_ids.code_generator_compute
        )
return self.code_generator_compute""",
                    "name": "get_code_generator_compute",
                    "decorator": "@api.model",
                    "param": "self",
                    "sequence": 4,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model_fields.id,
                },
                {
                    "code": """return_value = []

if self.ttype not in ("reference", "selection"):
    return

if self.selection and self.selection != "[]":
    try:
        # Transform string in list
        lst_selection = ast.literal_eval(self.selection)
        # lst_selection = [f"'{a}'" for a in lst_selection]
        return_value = lst_selection
    except Exception as e:
        _logger.error(
            f"The selection of field {self.name} is not a"
            f" list: '{self.selection}'."
        )
elif (
    self.code_generator_ir_model_fields_ids
    and self.code_generator_ir_model_fields_ids.selection
    and self.code_generator_ir_model_fields_ids.selection != "[()]"
):
    try:
        # Transform string in list
        lst_selection = ast.literal_eval(
            self.code_generator_ir_model_fields_ids.selection
        )
        return_value = lst_selection
    except Exception as e:
        _logger.error(
            f"The selection of field {self.name} is not a"
            f" list: '{self.selection}'."
        )
if not return_value:
    return_value = self.env[self.model]._fields[self.name].selection
    if isinstance(return_value, types.FunctionType):
        source_code = (
            inspect.getsource(return_value).strip().strip(",")
        )
        selection_equal_str = "selection="
        # Clean variable assignment if exist
        pos = source_code.find(" = fields.Selection(")
        if pos > 0:
            source_code = source_code[pos + 3 :].strip()
            return_value = self._extract_lambda_in_selection(
                source_code
            )
        elif selection_equal_str in source_code:
            return_value = source_code[
                source_code.find(selection_equal_str)
                + len(selection_equal_str) :
            ]
return return_value""",
                    "name": "get_selection",
                    "decorator": "@api.model",
                    "param": "self",
                    "sequence": 5,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model_fields.id,
                },
                {
                    "code": """tree = ast.parse(source_code)

class LambdaVisitor(ast.NodeVisitor):
    def __init__(self):
        _new_source = None

    def visit_Lambda(self, node):
        self._new_source = astor.to_source(node).strip()
        if self._new_source[0] == "(" and self._new_source[-1] == ")":
            self._new_source = self._new_source[1:-1]

    def get_result(self):
        return self._new_source

visitor = LambdaVisitor()
visitor.visit(tree)
return visitor.get_result()""",
                    "name": "_extract_lambda_in_selection",
                    "param": "self, source_code",
                    "sequence": 6,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model_fields.id,
                },
                {
                    "code": """model_data = None
if "model_id" in vals:
    model_data = self.env["ir.model"].browse(vals["model_id"])
    vals["model"] = model_data.model
if vals.get("ttype") == "selection":
    if not vals.get("selection"):
        raise UserError(
            _(
                "For selection fields, the Selection Options must be"
                " given!"
            )
        )
    self._check_selection(vals["selection"])

res = super(models.Model, self).create(vals)

if vals.get("state", "manual") == "manual":

    check_relation = True
    if vals.get("relation") and vals.get("model_id") and model_data:
        check_relation = not model_data.m2o_module

    if (
        vals.get("relation")
        and not self.env["ir.model"].search(
            [("model", "=", vals["relation"])]
        )
        and check_relation
    ):
        raise UserError(
            _("Model %s does not exist!") % vals["relation"]
        )

    if vals.get("ttype") == "one2many":
        # TODO check relation exist, but some times, it's created later to respect many2one order
        # if not self.env[""].search(
        #     [
        #         ("model_id", "=", vals["relation"]),
        #         ("name", "=", vals["relation_field"]),
        #         ("ttype", "=", "many2one"),
        #     ]
        # ):
        #     raise UserError(
        #         _("Many2one %s on model %s does not exist!")
        #         % (vals["relation_field"], vals["relation"])
        #     )
        pass

    self.clear_caches()  # for _existing_field_data()

    if vals["model"] in self.pool:
        # setup models; this re-initializes model in registry
        self.pool.setup_models(self._cr)
        # update database schema of model and its descendant models
        descendants = self.pool.descendants(
            [vals["model"]], "_inherits"
        )
        self.pool.init_models(
            self._cr,
            descendants,
            dict(self._context, update_custom_fields=True),
        )

return res""",
                    "name": "create",
                    "decorator": "@api.model",
                    "param": "self, vals",
                    "sequence": 7,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_model_fields.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Ir Module Module
        model_model = "ir.module.module"
        model_name = "ir_module_module"
        lst_depend_model = ["ir.module.module"]
        dct_model = {
            "description": "Code Generator Module",
        }
        dct_field = {
            "header_manifest": {
                "code_generator_sequence": 1,
                "field_description": "Header",
                "help": "Header comment in __manifest__.py file.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "text",
            },
        }
        model_ir_module_module = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """import base64
import logging
import os

import lxml
from docutils.core import publish_string

from odoo import api, fields, models, modules, tools
from odoo.addons.base.models.ir_module import MyWriter

_logger = logging.getLogger(__name__)""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ir_module_module.id,
            }
            env["code.generator.model.code.import"].create(value)

            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ir_module_module.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """sibling = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "TechnoLibre_odoo-code-generator-template",
    )
)
if os.path.isdir(sibling):
    return sibling
# Cannot find sibling template, use this working repo directory instead
return os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)""",
                    "name": "_default_path_sync_code",
                    "decorator": "@api.model",
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_module_module.id,
                },
                {
                    "code": """for module_id in self:
    if module_id.template_module_name:
        module_id.template_module_id = self.env[
            "ir.module.module"
        ].search([("name", "=", module_id.template_module_name)])""",
                    "name": "_fill_template_module_id",
                    "decorator": (
                        '@api.depends("template_module_name");@api.multi'
                    ),
                    "param": "self",
                    "sequence": 1,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_module_module.id,
                },
                {
                    "code": """self.add_module_dependency(
    module_name,
    model_dependency="code.generator.module.template.dependency",
)""",
                    "name": "add_module_dependency_template",
                    "decorator": "@api.multi",
                    "param": "self, module_name",
                    "sequence": 2,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_module_module.id,
                },
                {
                    "code": '''"""

:param module_name: list or string
:param model_dependency: string model name to operate
:return:
"""
for cg in self:
    if type(module_name) is str:
        lst_model_name = [module_name]
    elif type(module_name) is list:
        lst_model_name = module_name
    else:
        _logger.error(
            "Wrong type of model_name in method add_model_inherit:"
            f" {type(module_name)}"
        )
        return

    dependency_ids = self.env["ir.module.module"].search(
        [("name", "in", lst_model_name)]
    )
    for dependency in dependency_ids:
        check_duplicate = self.env[model_dependency].search(
            [
                ("module_id", "=", cg.id),
                ("depend_id", "=", dependency.id),
            ]
        )
        if not check_duplicate:
            value = {
                "module_id": cg.id,
                "depend_id": dependency.id,
                "name": dependency.display_name,
            }
            self.env[model_dependency].create(value)''',
                    "name": "add_module_dependency",
                    "decorator": "@api.multi",
                    "param": (
                        "self, module_name,"
                        " model_dependency='code.generator.module.dependency'"
                    ),
                    "sequence": 3,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_module_module.id,
                },
                {
                    "code": """for module in self:
    module.o2m_model_access = module.o2m_models.mapped("access_ids")
    module.o2m_model_rules = module.o2m_models.mapped("rule_ids")
    module.o2m_model_constraints = module.o2m_models.mapped(
        "o2m_constraints"
    )
    module.o2m_model_views = module.o2m_models.mapped("view_ids")
    module.o2m_model_act_window = module.o2m_models.mapped(
        "o2m_act_window"
    )
    module.o2m_model_act_server = module.o2m_models.mapped(
        "o2m_server_action"
    )
    module.o2m_model_server_constrains = module.o2m_models.mapped(
        "o2m_server_constrains"
    )
    module.o2m_model_reports = module.o2m_models.mapped("o2m_reports")""",
                    "name": "_get_models_info",
                    "decorator": '@api.depends("o2m_models")',
                    "param": "self",
                    "sequence": 4,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_module_module.id,
                },
                {
                    "code": """for module in self:
    if module.name and module.description:
        path = modules.get_module_resource(
            module.name, "static/description/index.html"
        )
        if path:
            with tools.file_open(path, "rb") as desc_file:
                doc = desc_file.read()
                html = lxml.html.document_fromstring(doc)
                for element, attribute, link, pos in html.iterlinks():
                    if (
                        element.get("src")
                        and "//" not in element.get("src")
                        and "static/" not in element.get("src")
                    ):
                        element.set(
                            "src",
                            "/%s/static/description/%s"
                            % (module.name, element.get("src")),
                        )
                module.description_html = tools.html_sanitize(
                    lxml.html.tostring(html)
                )
        else:
            overrides = {
                "embed_stylesheet": False,
                "doctitle_xform": False,
                "output_encoding": "unicode",
                "xml_declaration": False,
                "file_insertion_enabled": False,
            }
            output = publish_string(
                source=module.description
                if not module.application and module.description
                else "",
                settings_overrides=overrides,
                writer=MyWriter(),
            )
            module.description_html = tools.html_sanitize(output)""",
                    "name": "_get_desc",
                    "decorator": '@api.depends("name", "description")',
                    "param": "self",
                    "sequence": 5,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_module_module.id,
                },
                {
                    "code": """for module in self:
    # module.icon_image = ""
    if module.icon:
        path_parts = module.icon.split("/")
        # TODO this is broken ??
        # path = modules.get_module_resource(
        #     path_parts[0], *path_parts[1:]
        # )
        path = modules.get_module_resource(
            path_parts[1], *path_parts[2:]
        )
    else:
        path = modules.module.get_module_icon(module.name)
        path = path[1:]
    if path:
        with tools.file_open(path, "rb") as image_file:
            module.icon_image = base64.b64encode(image_file.read())""",
                    "name": "_get_icon_image",
                    "decorator": '@api.depends("icon")',
                    "param": "self",
                    "sequence": 6,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_module_module.id,
                },
                {
                    "code": """if dct_field:
    for field_name, field_info in dct_field.items():
        if (
            field_info.get("is_show_whitelist_model_inherit") is None
            and field_info.get("is_hide_blacklist_model_inherit")
            is None
        ):
            field_info["is_show_whitelist_model_inherit"] = True
model_id = self.env["ir.model"].search([("model", "=", model_model)])
if model_name is None:
    model_name = model_model.replace(".", "_")
# Check if exist or create it
if model_id:
    model_id.m2o_module = self.id

    if dct_field:
        for field_name, field_info in dct_field.items():
            if field_info.get("ttype") == "many2many":
                self._check_relation_many2many(model_model, field_info)
            field_id = self.env["ir.model.fields"].search(
                [
                    ("model", "=", model_model),
                    ("name", "=", field_name),
                ]
            )
            if not field_id:
                value_ir_model_fields = {
                    "name": field_name,
                    "model": model_model,
                    "model_id": model_id.id,
                }
                for key in field_info.keys():
                    self._update_dict(
                        key,
                        field_info,
                        value_ir_model_fields,
                    )
                self.env["ir.model.fields"].create(
                    value_ir_model_fields
                )
            else:
                value_ir_model_fields = {
                    "m2o_fields": field_id.id,
                }
                # TODO update all field with getter
                self._update_dict(
                    "filter_field_attribute",
                    field_info,
                    value_ir_model_fields,
                )
                self._update_dict(
                    "code_generator_compute",
                    field_info,
                    value_ir_model_fields,
                )
                self._update_dict(
                    "default_lambda",
                    field_info,
                    value_ir_model_fields,
                )

                self.env["code.generator.ir.model.fields"].create(
                    value_ir_model_fields
                )
else:
    has_field_name = False
    # Update model values
    value = {
        "name": model_name,
        "model": model_model,
        "m2o_module": self.id,
    }
    if dct_model:
        for key in dct_model.keys():
            self._update_dict(
                key,
                dct_model,
                value,
            )
    else:
        dct_model = {}
    rec_name = dct_model.get("rec_name")
    has_already_rec_name = False
    if not rec_name:
        rec_name = "name"
    else:
        has_already_rec_name = True

    # Update fields values
    lst_field_value = []
    if dct_field:
        for field_name, field_info in dct_field.items():
            if field_info.get("ttype") == "many2many":
                self._check_relation_many2many(model_model, field_info)

            if field_name == rec_name:
                has_field_name = True

            field_id = self.env["ir.model.fields"].search(
                [
                    ("model", "=", model_model),
                    ("name", "=", field_name),
                ]
            )
            if not field_id:
                value_field_id = {
                    "name": field_name,
                }
                for key in field_info.keys():
                    self._update_dict(
                        key,
                        field_info,
                        value_field_id,
                    )

                lst_field_value.append((0, 0, value_field_id))
            else:
                _logger.error("What to do with existing field?")

    if lst_field_value:
        value["field_id"] = lst_field_value

    if not has_already_rec_name:
        if has_field_name:
            value["rec_name"] = "name"
        elif not dct_field:
            # TODO this will create x_name field
            # value["rec_name"] = None
            value["rec_name"] = "name"
            # value["field_id"] = {"name": {"name": "name", "ttype": "char"}}
            value["field_id"] = [
                (
                    0,
                    0,
                    {
                        "name": "name",
                        "field_description": "Name",
                        "ttype": "char",
                    },
                )
            ]
        else:
            _logger.error(
                f"Cannot found rec_name for model {model_model}."
            )

    model_id = self.env["ir.model"].create(value)

# Model inherit
if lst_depend_model:
    model_id.add_model_inherit(lst_depend_model)

return model_id""",
                    "name": "add_update_model",
                    "decorator": "@api.model",
                    "param": (
                        "self, model_model, model_name=None, dct_field=None,"
                        " dct_model=None, lst_depend_model=None"
                    ),
                    "sequence": 7,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_module_module.id,
                },
                {
                    "code": """relation_name = field_value.get("relation")
comodel_name = relation_name.replace(".", "_")
str_model_model = model_model.replace(".", "_")
if not comodel_name:
    _logger.warning(f"Missing relation for field_value {field_value}")
else:
    # Source, file odoo/odoo/addons/base/models/ir_model.py function _custom_many2many_names
    # relation = self.env["ir.model.fields"]._custom_many2many_names(model_name, comodel_name)
    # Execution error will come from file odoo/odoo/fields.py, function check_pg_name
    relation = f"x_{comodel_name}_{str_model_model}_rel"
    if len(relation) > 63:
        _logger.warning(
            "The size is too high, please reduce size of model name"
            f" of '{model_model}' ({len(model_model)}) or"
            f" '{field_value.get('relation')}' ({len(relation_name)}),"
            " automatic relation will be broke, max 63 chars. Result"
            f" ({len(relation)}) '{relation}'"
        )""",
                    "name": "_check_relation_many2many",
                    "param": "self, model_model, field_value",
                    "sequence": 8,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_module_module.id,
                },
                {
                    "code": """for field_name, field_info in dct_field.items():
    if (
        field_info.get("is_show_whitelist_model_inherit") is None
        and field_info.get("is_hide_blacklist_model_inherit") is None
    ):
        field_info["is_show_whitelist_model_inherit"] = True
model_id = self.env["ir.model"].search([("model", "=", model_model)])
# Check if exist or create it
if model_id:
    model_id.m2o_module = self.id
    for field_name, field_info in dct_field.items():
        field_id = self.env["ir.model.fields"].search(
            [
                ("model", "=", model_model),
                ("name", "=", field_name),
            ]
        )
        if not field_id:
            value_field_one2many = {
                "name": field_name,
                "model": model_model,
                "model_id": model_id.id,
            }

            for key in field_info.keys():
                self._update_dict(
                    key,
                    field_info,
                    value_field_one2many,
                )

            self.env["ir.model.fields"].create(value_field_one2many)
        else:
            if "field_context" in field_info.keys():
                value_ir_model_fields = {
                    "m2o_fields": field_id.id,
                }
                # TODO find missing attribute
                self._update_dict(
                    "field_context",
                    field_info,
                    value_ir_model_fields,
                )
                self.env["code.generator.ir.model.fields"].create(
                    value_ir_model_fields
                )
            # _logger.error("What to do to update a one2many?")
else:
    _logger.error(
        f"The model '{model_model}' is not existing, need to be create"
        " before call add_update_model_one2many from"
        " CodeGeneratorModule."
    )""",
                    "name": "add_update_model_one2many",
                    "decorator": "@api.model",
                    "param": "self, model_model, dct_field",
                    "sequence": 9,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_module_module.id,
                },
                {
                    "code": """filter_field_attribute = field_info.get(key_name)
if filter_field_attribute:
    value_field_id[key_name] = filter_field_attribute""",
                    "name": "_update_dict",
                    "decorator": "@api.model",
                    "param": "self, key_name, field_info, value_field_id",
                    "sequence": 10,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_module_module.id,
                },
                {
                    "code": """if "icon" in vals.keys():
    icon_path = vals["icon"]

    if icon_path and os.path.isfile(icon_path):
        with tools.file_open(icon_path, "rb") as image_file:
            vals["icon_image"] = base64.b64encode(image_file.read())
return super(models.Model, self).create(vals)""",
                    "name": "create",
                    "decorator": "@api.model",
                    "param": "self, vals",
                    "sequence": 11,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_module_module.id,
                },
                {
                    "code": """o2m_models = self.mapped("o2m_models")
if o2m_models:
    o2m_models.mapped("view_ids").unlink()
    o2m_models.unlink()  # I need to delete the created tables
return super(CodeGeneratorModule, self).unlink()""",
                    "name": "unlink",
                    "decorator": "@api.multi",
                    "param": "self",
                    "sequence": 12,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ir_module_module.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Generate server action
        # action_server view
        act_server_id = env["ir.actions.server"].search(
            [
                ("name", "=", "Install Modules"),
                ("model_id", "=", model_ir_module_module.id),
            ]
        )
        if not act_server_id:
            act_server_id = env["ir.actions.server"].create(
                {
                    "name": "Install Modules",
                    "model_id": model_ir_module_module.id,
                    "binding_model_id": model_ir_module_module.id,
                    "state": "code",
                    "code": "records.button_immediate_install()",
                }
            )

        # Add/Update Ir Module Module Dependency
        model_model = "ir.module.module.dependency"
        model_name = "ir_module_module_dependency"
        lst_depend_model = ["ir.module.module.dependency"]
        dct_model = {
            "description": "Code Generator Module Dependency",
        }
        dct_field = {
            "depend_id": {
                "code_generator_sequence": 3,
                "field_description": "Dependency",
                "is_show_whitelist_model_inherit": True,
                "relation": "ir.module.module",
                "ttype": "many2one",
            },
            "module_id": {
                "code_generator_sequence": 4,
                "field_description": "Module",
                "is_show_whitelist_model_inherit": True,
                "relation": "ir.module.module",
                "ttype": "many2one",
            },
        }
        model_ir_module_module_dependency = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ir_module_module_dependency.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Ir Ui Menu
        model_model = "ir.ui.menu"
        model_name = "ir_ui_menu"
        lst_depend_model = ["ir.ui.menu"]
        dct_field = {
            "ignore_act_window": {
                "code_generator_sequence": 1,
                "field_description": "Ignore Act Window",
                "help": "Set True to force no act_window, like a parent menu.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "m2o_module": {
                "code_generator_sequence": 2,
                "field_description": "Module",
                "help": "Module",
                "is_show_whitelist_model_inherit": True,
                "relation": "code.generator.module",
                "ttype": "many2one",
            },
        }
        model_ir_ui_menu = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ir_ui_menu.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Ir Ui View
        model_model = "ir.ui.view"
        model_name = "ir_ui_view"
        lst_depend_model = ["ir.ui.view"]
        dct_field = {
            "is_hide_blacklist_write_view": {
                "code_generator_sequence": 1,
                "field_description": (
                    "Hide in blacklist when writing code view"
                ),
                "help": "Hide from view when field is blacklisted.",
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "is_show_whitelist_write_view": {
                "code_generator_sequence": 2,
                "field_description": (
                    "Show in whitelist when writing code view"
                ),
                "help": (
                    "If a field in model is in whitelist, all is not will be"
                    " hide. "
                ),
                "is_show_whitelist_model_inherit": True,
                "ttype": "boolean",
            },
            "m2o_model": {
                "code_generator_sequence": 3,
                "field_description": "Code generator Model",
                "help": "Model",
                "is_show_whitelist_model_inherit": True,
                "relation": "ir.model",
                "ttype": "many2one",
            },
        }
        model_ir_ui_view = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import api, fields, models, modules, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ir_ui_view.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Res Config Settings
        model_model = "res.config.settings"
        model_name = "res_config_settings"
        lst_depend_model = ["res.config.settings"]
        dct_field = {
            "s_data2export": {
                "code_generator_sequence": 1,
                "default": "nomenclator",
                "field_description": "Model data to export",
                "help": "Model data to export",
                "is_show_whitelist_model_inherit": True,
                "selection": (
                    "[('nonomenclator', 'Include the data of all of the"
                    " selected models to export.'), ('nomenclator', 'Include"
                    " the data of the selected models to export set it as"
                    " nomenclator.')]"
                ),
                "ttype": "selection",
            },
        }
        model_res_config_settings = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import fields, models""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_res_config_settings.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Res Groups
        model_model = "res.groups"
        model_name = "res_groups"
        lst_depend_model = ["res.groups"]
        dct_field = {
            "m2o_module": {
                "code_generator_sequence": 1,
                "field_description": "Module",
                "help": "Module",
                "is_show_whitelist_model_inherit": True,
                "relation": "code.generator.module",
                "ttype": "many2one",
            },
        }
        model_res_groups = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            lst_depend_model=lst_depend_model,
        )

        # Added one2many field, many2one need to be create before add one2many
        model_model = "code.generator.ir.model.dependency"
        dct_field = {
            "ir_model_ids": {
                "field_description": "Ir model",
                "ttype": "one2many",
                "help": "Origin model with dependency",
                "code_generator_sequence": 4,
                "relation": "ir.model",
            },
        }
        code_generator_id.add_update_model_one2many(model_model, dct_field)

        model_model = "code.generator.module"
        dct_field = {
            "code_generator_act_window_id": {
                "field_description": "Code Generator Act Window",
                "ttype": "one2many",
                "code_generator_sequence": 7,
                "relation": "code.generator.act_window",
                "relation_field": "code_generator_id",
            },
            "code_generator_menus_id": {
                "field_description": "Code Generator Menus",
                "ttype": "one2many",
                "code_generator_sequence": 8,
                "relation": "code.generator.menu",
                "relation_field": "code_generator_id",
            },
            "code_generator_views_id": {
                "field_description": "Code Generator Views",
                "ttype": "one2many",
                "code_generator_sequence": 9,
                "relation": "code.generator.view",
                "relation_field": "code_generator_id",
            },
            "dependencies_id": {
                "field_description": "Dependencies module",
                "ttype": "one2many",
                "code_generator_sequence": 12,
                "code_generator_form_simple_view_sequence": 24,
                "code_generator_tree_view_sequence": 24,
                "relation": "code.generator.module.dependency",
                "relation_field": "module_id",
            },
            "dependencies_template_id": {
                "field_description": "Dependencies template module",
                "ttype": "one2many",
                "code_generator_sequence": 13,
                "relation": "code.generator.module.template.dependency",
                "relation_field": "module_id",
            },
            "external_dependencies_id": {
                "field_description": "External Dependencies",
                "ttype": "one2many",
                "code_generator_sequence": 19,
                "relation": "code.generator.module.external.dependency",
                "relation_field": "module_id",
            },
            "o2m_codes": {
                "field_description": "O2M Codes",
                "ttype": "one2many",
                "code_generator_sequence": 28,
                "relation": "code.generator.model.code",
                "relation_field": "m2o_module",
            },
            "o2m_groups": {
                "field_description": "O2M Groups",
                "ttype": "one2many",
                "code_generator_sequence": 29,
                "code_generator_form_simple_view_sequence": 27,
                "code_generator_tree_view_sequence": 27,
                "relation": "res.groups",
                "relation_field": "m2o_module",
            },
            "o2m_menus": {
                "field_description": "O2M Menus",
                "ttype": "one2many",
                "code_generator_sequence": 30,
                "code_generator_form_simple_view_sequence": 42,
                "code_generator_tree_view_sequence": 42,
                "field_context": "{'ir.ui.menu.full_list': True}",
                "relation": "ir.ui.menu",
                "relation_field": "m2o_module",
            },
            "o2m_model_access": {
                "field_description": "O2M Model Access",
                "ttype": "one2many",
                "code_generator_sequence": 31,
                "code_generator_form_simple_view_sequence": 31,
                "code_generator_tree_view_sequence": 31,
                "code_generator_compute": "_get_models_info",
                "relation": "ir.model.access",
            },
            "o2m_model_act_server": {
                "field_description": "O2M Model Act Server",
                "ttype": "one2many",
                "code_generator_sequence": 32,
                "code_generator_form_simple_view_sequence": 41,
                "code_generator_tree_view_sequence": 41,
                "code_generator_compute": "_get_models_info",
                "relation": "ir.actions.server",
            },
            "o2m_model_act_todo": {
                "field_description": "O2M Model Act Todo",
                "ttype": "one2many",
                "code_generator_sequence": 33,
                "relation": "ir.actions.todo",
                "relation_field": "m2o_code_generator",
            },
            "o2m_model_act_url": {
                "field_description": "O2M Model Act Url",
                "ttype": "one2many",
                "code_generator_sequence": 34,
                "relation": "ir.actions.act_url",
                "relation_field": "m2o_code_generator",
            },
            "o2m_model_act_window": {
                "field_description": "O2M Model Act Window",
                "ttype": "one2many",
                "code_generator_sequence": 35,
                "code_generator_form_simple_view_sequence": 40,
                "code_generator_tree_view_sequence": 40,
                "code_generator_compute": "_get_models_info",
                "relation": "ir.actions.act_window",
            },
            "o2m_model_constraints": {
                "field_description": "O2M Model Constraints",
                "ttype": "one2many",
                "code_generator_sequence": 36,
                "code_generator_form_simple_view_sequence": 33,
                "code_generator_tree_view_sequence": 33,
                "relation": "ir.model.constraint",
                "relation_field": "code_generator_id",
            },
            "o2m_model_reports": {
                "field_description": "O2M Model Reports",
                "ttype": "one2many",
                "code_generator_sequence": 37,
                "code_generator_form_simple_view_sequence": 43,
                "code_generator_tree_view_sequence": 43,
                "code_generator_compute": "_get_models_info",
                "relation": "ir.actions.report",
            },
            "o2m_model_rules": {
                "field_description": "O2M Model Rules",
                "ttype": "one2many",
                "code_generator_sequence": 38,
                "code_generator_form_simple_view_sequence": 32,
                "code_generator_tree_view_sequence": 32,
                "code_generator_compute": "_get_models_info",
                "relation": "ir.rule",
            },
            "o2m_model_server_constrains": {
                "field_description": "O2M Model Server Constrains",
                "ttype": "one2many",
                "code_generator_sequence": 39,
                "code_generator_form_simple_view_sequence": 34,
                "code_generator_tree_view_sequence": 34,
                "code_generator_compute": "_get_models_info",
                "relation": "ir.model.server_constrain",
            },
            "o2m_model_views": {
                "field_description": "O2M Model Views",
                "ttype": "one2many",
                "code_generator_sequence": 40,
                "code_generator_form_simple_view_sequence": 39,
                "code_generator_tree_view_sequence": 39,
                "code_generator_compute": "_get_models_info",
                "relation": "ir.ui.view",
            },
            "o2m_models": {
                "field_description": "O2M Models",
                "ttype": "one2many",
                "code_generator_sequence": 41,
                "code_generator_form_simple_view_sequence": 28,
                "code_generator_tree_view_sequence": 28,
                "relation": "ir.model",
                "relation_field": "m2o_module",
            },
            "o2m_nomenclator_blacklist_fields": {
                "field_description": "O2M Nomenclator Blacklist Fields",
                "ttype": "one2many",
                "domain": [("nomenclature_blacklist", "=", True)],
                "code_generator_sequence": 42,
                "code_generator_form_simple_view_sequence": 30,
                "code_generator_tree_view_sequence": 30,
                "relation": "code.generator.ir.model.fields",
                "relation_field": "m2o_module",
            },
            "o2m_nomenclator_whitelist_fields": {
                "field_description": "O2M Nomenclator Whitelist Fields",
                "ttype": "one2many",
                "domain": [("nomenclature_whitelist", "=", True)],
                "code_generator_sequence": 43,
                "code_generator_form_simple_view_sequence": 29,
                "code_generator_tree_view_sequence": 29,
                "relation": "code.generator.ir.model.fields",
                "relation_field": "m2o_module",
            },
        }
        code_generator_id.add_update_model_one2many(model_model, dct_field)

        model_model = "code.generator.view.item"
        dct_field = {
            "child_id": {
                "field_description": "Child",
                "ttype": "one2many",
                "code_generator_sequence": 8,
                "relation": "code.generator.view.item",
                "relation_field": "parent_id",
            },
        }
        code_generator_id.add_update_model_one2many(model_model, dct_field)

        model_model = "ir.model"
        dct_field = {
            "o2m_act_window": {
                "is_show_whitelist_model_inherit": True,
                "field_description": "Act window",
                "ttype": "one2many",
                "code_generator_sequence": 24,
                "relation": "ir.actions.act_window",
                "relation_field": "m2o_res_model",
            },
            "o2m_code_import": {
                "is_show_whitelist_model_inherit": True,
                "field_description": "Codes import",
                "ttype": "one2many",
                "code_generator_sequence": 25,
                "relation": "code.generator.model.code.import",
                "relation_field": "m2o_model",
            },
            "o2m_codes": {
                "is_show_whitelist_model_inherit": True,
                "field_description": "Codes",
                "ttype": "one2many",
                "code_generator_sequence": 26,
                "relation": "code.generator.model.code",
                "relation_field": "m2o_model",
            },
            "o2m_constraints": {
                "is_show_whitelist_model_inherit": True,
                "field_description": "Constraints",
                "ttype": "one2many",
                "domain": [("type", "=", "u"), ("message", "!=", None)],
                "code_generator_sequence": 27,
                "relation": "ir.model.constraint",
                "relation_field": "model",
            },
            "o2m_reports": {
                "is_show_whitelist_model_inherit": True,
                "field_description": "Reports",
                "ttype": "one2many",
                "help": "Reports associated with this model",
                "code_generator_sequence": 28,
                "relation": "ir.actions.report",
                "relation_field": "m2o_model",
            },
            "o2m_server_action": {
                "is_show_whitelist_model_inherit": True,
                "field_description": "Server action",
                "ttype": "one2many",
                "domain": [
                    ("binding_type", "=", "action"),
                    "|",
                    ("state", "=", "code"),
                    ("state", "=", "multi"),
                    ("usage", "=", "ir_actions_server"),
                ],
                "code_generator_sequence": 29,
                "relation": "ir.actions.server",
                "relation_field": "model_id",
            },
            "o2m_server_constrains": {
                "is_show_whitelist_model_inherit": True,
                "field_description": "Server Constrains",
                "ttype": "one2many",
                "help": "Server Constrains attach to this model",
                "code_generator_sequence": 30,
                "code_generator_form_simple_view_sequence": 17,
                "relation": "ir.model.server_constrain",
                "relation_field": "m2o_ir_model",
            },
        }
        code_generator_id.add_update_model_one2many(model_model, dct_field)

        model_model = "ir.model.fields"
        dct_field = {
            "code_generator_ir_model_fields_ids": {
                "is_show_whitelist_model_inherit": True,
                "field_description": "Code Generator Ir Model Fields",
                "ttype": "one2many",
                "help": (
                    "Link to update field when generate, because it cannot"
                    " update ir.model.fields in runtime"
                ),
                "code_generator_sequence": 5,
                "relation": "code.generator.ir.model.fields",
                "relation_field": "m2o_fields",
            },
        }
        code_generator_id.add_update_model_one2many(model_model, dct_field)

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import fields, models""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_res_groups.id,
            }
            env["code.generator.model.code.import"].create(value)

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
