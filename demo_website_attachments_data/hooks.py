import base64
import logging
import os

from odoo import SUPERUSER_ID, _, api, fields, models

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Remove all website pages before installing data

        website_page_ids = env["website.page"].search([])
        website_menu_ids = env["website.menu"].search([])
        # TODO website doesn't support multi
        # website_page_ids.website_id = None
        # TODO replace by :
        for website_page in website_page_ids:
            website_page.website_id = None
        for website_menu in website_menu_ids:
            website_menu.website_id = None


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        xml_id = "ir_attachment_/website/static/src/scss/options/colors/user_theme_color_palette_custom_web_assets_common_scss"
        update_datas_ir_attachment_from_xmlid(env, xml_id)
        xml_id = "ir_attachment_/website/static/src/scss/options/colors/user_color_palette_custom_web_assets_common_scss"
        update_datas_ir_attachment_from_xmlid(env, xml_id)
        xml_id = "ir_attachment_/web/static/src/scss/bootstrap_overridden_frontend_custom_web_assets_frontend_scss"
        update_datas_ir_attachment_from_xmlid(env, xml_id)


def update_datas_ir_attachment_from_xmlid(env, xml_id):
    dir_path = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
    ir_attach_id_name = env["ir.model.data"].search([("name", "=", xml_id)])
    if not ir_attach_id_name:
        _logger.warning(f"Cannot find ir.attachment id '{xml_id}'")
        return
    ir_attach_id = env["ir.attachment"].browse(ir_attach_id_name.res_id)
    file_path = dir_path + ir_attach_id.url
    if not os.path.isfile(file_path):
        _logger.warning(f"File not exist '{file_path}'")
        return
    datas = base64.b64encode(open(file_path, "rb").read())
    ir_attach_id.write({"datas": datas})
