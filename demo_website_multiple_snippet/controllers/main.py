from datetime import datetime

import humanize

from odoo import http
from odoo.http import request


class DemoWebsiteMultipleSnippetController(http.Controller):
    @http.route(
        ["/demo_website_multiple_snippet/helloworld"],
        type="json",
        auth="public",
        website=True,
        methods=["POST", "GET"],
        csrf=False,
    )
    def hello_world(self):
        return {"hello": "Hello World!"}

    @http.route(
        ["/demo_website_multiple_snippet/get_last_item"],
        type="json",
        auth="public",
        website=True,
        methods=["POST", "GET"],
        csrf=False,
    )
    def get_last_item(self):
        data_id = http.request.env["demo.model.portal"].search(
            [], order="create_date desc", limit=1
        )
        dct_value = {}
        if data_id:
            dct_value["demo_boolean"] = data_id.demo_boolean
            dct_value["demo_char"] = data_id.demo_char
            dct_value["demo_date"] = data_id.demo_date
            dct_value["demo_date_time"] = data_id.demo_date_time
            dct_value["demo_external_link"] = data_id.demo_external_link
            dct_value["demo_float"] = data_id.demo_float
            dct_value["demo_float_time"] = data_id.demo_float_time
            dct_value["demo_html"] = data_id.demo_html
            dct_value["demo_integer"] = data_id.demo_integer
            dct_value["demo_text"] = data_id.demo_text
            dct_value["name"] = data_id.name
            dct_value["xpos"] = data_id.xpos
            dct_value["ypos"] = data_id.ypos
        return dct_value

    @http.route(
        ["/demo_website_multiple_snippet/portal_time/<int:portal_time>"],
        type="http",
        auth="public",
        website=True,
    )
    def get_page_portal_time(self, portal_time=None):
        env = request.env(context=dict(request.env.context))

        demo_model_portal_cls = env["demo.model.portal"]
        if portal_time:
            demo_model_portal_id = (
                demo_model_portal_cls.sudo().browse(portal_time).exists()
            )
        else:
            demo_model_portal_id = None
        dct_value = {"demo_model_portal_id": demo_model_portal_id}

        # Render page
        return request.render(
            "demo_website_multiple_snippet.demo_model_portal_unit_list_show_time_item_structure",
            dct_value,
        )

    @http.route(
        ["/demo_website_multiple_snippet/portal_time_list"],
        type="json",
        auth="public",
        website=True,
    )
    def get_portal_time_list(self):
        env = request.env(context=dict(request.env.context))

        demo_model_portal_cls = env["demo.model.portal"]
        demo_model_portal_ids = (
            demo_model_portal_cls.sudo()
            .search([], order="create_date desc", limit=3)
            .ids
        )
        portal_times = demo_model_portal_cls.sudo().browse(
            demo_model_portal_ids
        )

        lst_time_diff = []
        timedate_now = datetime.now()
        # fr_CA not exist
        # check .venv/lib/python3.7/site-packages/humanize/locale/
        _t = humanize.i18n.activate("fr_FR")
        for demo_model_portal_id in portal_times:
            diff_time = timedate_now - demo_model_portal_id.create_date
            str_diff_time = humanize.naturaltime(diff_time).capitalize() + "."
            lst_time_diff.append(str_diff_time)
        humanize.i18n.deactivate()

        dct_value = {"portal_times": portal_times, "lst_time": lst_time_diff}

        # Render page
        return request.env["ir.ui.view"].render_template(
            "demo_website_multiple_snippet.demo_model_portal_list_list_show_time_item_structure",
            dct_value,
        )

    @http.route(
        ["/demo_website_multiple_snippet/portal/<int:portal>"],
        type="http",
        auth="public",
        website=True,
    )
    def get_page_portal(self, portal=None):
        env = request.env(context=dict(request.env.context))

        demo_model_portal_cls = env["demo.model.portal"]
        if portal:
            demo_model_portal_id = (
                demo_model_portal_cls.sudo().browse(portal).exists()
            )
        else:
            demo_model_portal_id = None
        dct_value = {"demo_model_portal_id": demo_model_portal_id}

        # Render page
        return request.render(
            "demo_website_multiple_snippet.demo_model_portal_unit_list_item_structure",
            dct_value,
        )

    @http.route(
        ["/demo_website_multiple_snippet/portal_list"],
        type="json",
        auth="public",
        website=True,
    )
    def get_portal_list(self):
        env = request.env(context=dict(request.env.context))

        demo_model_portal_cls = env["demo.model.portal"]
        demo_model_portal_ids = (
            demo_model_portal_cls.sudo()
            .search([], order="create_date desc", limit=3)
            .ids
        )
        portals = demo_model_portal_cls.sudo().browse(demo_model_portal_ids)

        dct_value = {"portals": portals}

        # Render page
        return request.env["ir.ui.view"].render_template(
            "demo_website_multiple_snippet.demo_model_portal_list_list_item_structure",
            dct_value,
        )
