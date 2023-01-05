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

    @http.route(
        [
            "/demo_website_multiple_snippet/demo_model_portal/<int:demo_model_portal>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def get_page_demo_model_portal(self, demo_model_portal=None):
        env = request.env(context=dict(request.env.context))

        demo_model_portal_cls = env["demo.model.portal"]
        if demo_model_portal:
            demo_model_portal_id = (
                demo_model_portal_cls.sudo().browse(demo_model_portal).exists()
            )
        else:
            demo_model_portal_id = None
        dct_value = {"demo_model_portal_id": demo_model_portal_id}

        # Render page
        return request.render(
            "demo_website_multiple_snippet.demo_model_portal_unit_list_item_structure_generic",
            dct_value,
        )

    @http.route(
        ["/demo_website_multiple_snippet/demo_model_portal_list"],
        type="json",
        auth="public",
        website=True,
    )
    def get_demo_model_portal_list(self):
        env = request.env(context=dict(request.env.context))

        demo_model_portal_cls = env["demo.model.portal"]
        demo_model_portal_ids = (
            demo_model_portal_cls.sudo()
            .search([], order="create_date desc", limit=3)
            .ids
        )
        demo_model_portal_s = demo_model_portal_cls.sudo().browse(
            demo_model_portal_ids
        )

        lst_time_diff = []
        timedate_now = datetime.now()
        # fr_CA not exist
        # check .venv/lib/python3.7/site-packages/humanize/locale/
        _t = humanize.i18n.activate("fr_FR")
        for demo_model_portal_id in demo_model_portal_s:
            diff_time = timedate_now - demo_model_portal_id.create_date
            str_diff_time = humanize.naturaltime(diff_time).capitalize() + "."
            lst_time_diff.append(str_diff_time)
        humanize.i18n.deactivate()

        dct_value = {
            "demo_model_portal_s": demo_model_portal_s,
            "lst_time": lst_time_diff,
        }

        # Render page
        return request.env["ir.ui.view"].render_template(
            "demo_website_multiple_snippet.demo_model_portal_list_list_item_structure_generic",
            dct_value,
        )

    @http.route(
        [
            "/demo_website_multiple_snippet/demo_model_portal/<int:double_portal_demo_model_portal>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def get_page_double_portal_demo_model_portal(
        self, double_portal_demo_model_portal=None
    ):
        env = request.env(context=dict(request.env.context))

        demo_model_portal_cls = env["demo.model.portal"]
        if double_portal_demo_model_portal:
            demo_model_portal_id = (
                demo_model_portal_cls.sudo()
                .browse(double_portal_demo_model_portal)
                .exists()
            )
        else:
            demo_model_portal_id = None
        dct_value = {"demo_model_portal_id": demo_model_portal_id}

        # Render page
        return request.render(
            "demo_website_multiple_snippet.demo_model_portal_unit_list_item_structure_double",
            dct_value,
        )

    @http.route(
        [
            "/demo_website_multiple_snippet/demo_model_2_portal/<int:double_portal_demo_model_2_portal>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def get_page_double_portal_demo_model_2_portal(
        self, double_portal_demo_model_2_portal=None
    ):
        env = request.env(context=dict(request.env.context))

        demo_model_2_portal_cls = env["demo.model_2.portal"]
        if double_portal_demo_model_2_portal:
            demo_model_2_portal_id = (
                demo_model_2_portal_cls.sudo()
                .browse(double_portal_demo_model_2_portal)
                .exists()
            )
        else:
            demo_model_2_portal_id = None
        dct_value = {"demo_model_2_portal_id": demo_model_2_portal_id}

        # Render page
        return request.render(
            "demo_website_multiple_snippet.demo_model_2_portal_unit_list_item_structure_double",
            dct_value,
        )

    @http.route(
        [
            "/demo_website_multiple_snippet/demo_model_3_portal_diagram/<int:double_portal_demo_model_3_portal_diagram>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def get_page_double_portal_demo_model_3_portal_diagram(
        self, double_portal_demo_model_3_portal_diagram=None
    ):
        env = request.env(context=dict(request.env.context))

        demo_model_3_portal_diagram_cls = env["demo.model_3.portal.diagram"]
        if double_portal_demo_model_3_portal_diagram:
            demo_model_3_portal_diagram_id = (
                demo_model_3_portal_diagram_cls.sudo()
                .browse(double_portal_demo_model_3_portal_diagram)
                .exists()
            )
        else:
            demo_model_3_portal_diagram_id = None
        dct_value = {
            "demo_model_3_portal_diagram_id": demo_model_3_portal_diagram_id
        }

        # Render page
        return request.render(
            "demo_website_multiple_snippet.demo_model_3_portal_diagram_unit_list_item_structure_double",
            dct_value,
        )

    @http.route(
        ["/demo_website_multiple_snippet/double_portal_list"],
        type="json",
        auth="public",
        website=True,
    )
    def get_double_portal_list(self):
        env = request.env(context=dict(request.env.context))

        demo_model_portal_cls = env["demo.model.portal"]
        demo_model_portal_ids = (
            demo_model_portal_cls.sudo()
            .search([], order="create_date desc", limit=3)
            .ids
        )
        double_portal_demo_model_portal_s = (
            demo_model_portal_cls.sudo().browse(demo_model_portal_ids)
        )

        demo_model_2_portal_cls = env["demo.model_2.portal"]
        demo_model_2_portal_ids = (
            demo_model_2_portal_cls.sudo()
            .search([], order="create_date desc", limit=3)
            .ids
        )
        double_portal_demo_model_2_portal_s = (
            demo_model_2_portal_cls.sudo().browse(demo_model_2_portal_ids)
        )

        demo_model_3_portal_diagram_cls = env["demo.model_3.portal.diagram"]
        demo_model_3_portal_diagram_ids = (
            demo_model_3_portal_diagram_cls.sudo()
            .search([], order="create_date desc", limit=3)
            .ids
        )
        double_portal_demo_model_3_portal_diagram_s = (
            demo_model_3_portal_diagram_cls.sudo().browse(
                demo_model_3_portal_diagram_ids
            )
        )

        lst_time_diff_demo_model_portal = []
        lst_time_diff_demo_model_2_portal = []
        lst_time_diff_demo_model_3_portal_diagram = []
        timedate_now = datetime.now()
        # fr_CA not exist
        # check .venv/lib/python3.7/site-packages/humanize/locale/
        _t = humanize.i18n.activate("fr_FR")
        for demo_model_portal_id in double_portal_demo_model_portal_s:
            diff_time = timedate_now - demo_model_portal_id.create_date
            str_diff_time = humanize.naturaltime(diff_time).capitalize() + "."
            lst_time_diff_demo_model_portal.append(str_diff_time)
        for demo_model_2_portal_id in double_portal_demo_model_2_portal_s:
            diff_time = timedate_now - demo_model_2_portal_id.create_date
            str_diff_time = humanize.naturaltime(diff_time).capitalize() + "."
            lst_time_diff_demo_model_2_portal.append(str_diff_time)
        for (
            demo_model_3_portal_diagram_id
        ) in double_portal_demo_model_3_portal_diagram_s:
            diff_time = (
                timedate_now - demo_model_3_portal_diagram_id.create_date
            )
            str_diff_time = humanize.naturaltime(diff_time).capitalize() + "."
            lst_time_diff_demo_model_3_portal_diagram.append(str_diff_time)
        humanize.i18n.deactivate()

        dct_value = {
            "double_portal_demo_model_portal_s": double_portal_demo_model_portal_s,
            "lst_time_demo_model_portal": lst_time_diff_demo_model_portal,
            "double_portal_demo_model_2_portal_s": double_portal_demo_model_2_portal_s,
            "lst_time_demo_model_2_portal": lst_time_diff_demo_model_2_portal,
            "double_portal_demo_model_3_portal_diagram_s": double_portal_demo_model_3_portal_diagram_s,
            "lst_time_demo_model_3_portal_diagram": lst_time_diff_demo_model_3_portal_diagram,
        }

        # Render page
        return request.env["ir.ui.view"].render_template(
            "demo_website_multiple_snippet.demo_model_portal_and_demo_model_2_portal_and_demo_model_3_portal_diagram_list_list_item_structure_double",
            dct_value,
        )

    @http.route(
        ["/demo_website_multiple_snippet/demo_model_portal/<int:dp_dmp>"],
        type="http",
        auth="public",
        website=True,
    )
    def get_page_dp_dmp(self, dp_dmp=None):
        env = request.env(context=dict(request.env.context))

        demo_model_portal_cls = env["demo.model.portal"]
        if dp_dmp:
            demo_model_portal_id = (
                demo_model_portal_cls.sudo().browse(dp_dmp).exists()
            )
        else:
            demo_model_portal_id = None
        dct_value = {"demo_model_portal_id": demo_model_portal_id}

        # Render page
        return request.render(
            "demo_website_multiple_snippet.demo_model_portal_unit_list_item_structure_double_short",
            dct_value,
        )

    @http.route(
        ["/demo_website_multiple_snippet/demo_model_2_portal/<int:dp_dm2p>"],
        type="http",
        auth="public",
        website=True,
    )
    def get_page_dp_dm2p(self, dp_dm2p=None):
        env = request.env(context=dict(request.env.context))

        demo_model_2_portal_cls = env["demo.model_2.portal"]
        if dp_dm2p:
            demo_model_2_portal_id = (
                demo_model_2_portal_cls.sudo().browse(dp_dm2p).exists()
            )
        else:
            demo_model_2_portal_id = None
        dct_value = {"demo_model_2_portal_id": demo_model_2_portal_id}

        # Render page
        return request.render(
            "demo_website_multiple_snippet.demo_model_2_portal_unit_list_item_structure_double_short",
            dct_value,
        )

    @http.route(
        [
            "/demo_website_multiple_snippet/demo_model_3_portal_diagram/<int:dp_dm3pd>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def get_page_dp_dm3pd(self, dp_dm3pd=None):
        env = request.env(context=dict(request.env.context))

        demo_model_3_portal_diagram_cls = env["demo.model_3.portal.diagram"]
        if dp_dm3pd:
            demo_model_3_portal_diagram_id = (
                demo_model_3_portal_diagram_cls.sudo()
                .browse(dp_dm3pd)
                .exists()
            )
        else:
            demo_model_3_portal_diagram_id = None
        dct_value = {
            "demo_model_3_portal_diagram_id": demo_model_3_portal_diagram_id
        }

        # Render page
        return request.render(
            "demo_website_multiple_snippet.demo_model_3_portal_diagram_unit_list_item_structure_double_short",
            dct_value,
        )

    @http.route(
        [
            "/demo_website_multiple_snippet/dp_dmp_demo_model_portal_and_dp_dm2p_demo_model_2_portal_and_dp_dm3pd_demo_model_3_portal_diagram_list"
        ],
        type="json",
        auth="public",
        website=True,
    )
    def get_dp_dmp_demo_model_portal_and_dp_dm2p_demo_model_2_portal_and_dp_dm3pd_demo_model_3_portal_diagram_list(
        self,
    ):
        env = request.env(context=dict(request.env.context))

        demo_model_portal_cls = env["demo.model.portal"]
        demo_model_portal_ids = (
            demo_model_portal_cls.sudo()
            .search([], order="create_date desc", limit=3)
            .ids
        )
        dp_dmps = demo_model_portal_cls.sudo().browse(demo_model_portal_ids)

        demo_model_2_portal_cls = env["demo.model_2.portal"]
        demo_model_2_portal_ids = (
            demo_model_2_portal_cls.sudo()
            .search([], order="create_date desc", limit=3)
            .ids
        )
        dp_dm2ps = demo_model_2_portal_cls.sudo().browse(
            demo_model_2_portal_ids
        )

        demo_model_3_portal_diagram_cls = env["demo.model_3.portal.diagram"]
        demo_model_3_portal_diagram_ids = (
            demo_model_3_portal_diagram_cls.sudo()
            .search([], order="create_date desc", limit=3)
            .ids
        )
        dp_dm3pds = demo_model_3_portal_diagram_cls.sudo().browse(
            demo_model_3_portal_diagram_ids
        )

        lst_time_diff_dp_dmp = []
        lst_time_diff_dp_dm2p = []
        lst_time_diff_dp_dm3pd = []
        timedate_now = datetime.now()
        # fr_CA not exist
        # check .venv/lib/python3.7/site-packages/humanize/locale/
        _t = humanize.i18n.activate("fr_FR")
        for demo_model_portal_id in dp_dmps:
            diff_time = timedate_now - demo_model_portal_id.create_date
            str_diff_time = humanize.naturaltime(diff_time).capitalize() + "."
            lst_time_diff_dp_dmp.append(str_diff_time)
        for demo_model_2_portal_id in dp_dm2ps:
            diff_time = timedate_now - demo_model_2_portal_id.create_date
            str_diff_time = humanize.naturaltime(diff_time).capitalize() + "."
            lst_time_diff_dp_dm2p.append(str_diff_time)
        for demo_model_3_portal_diagram_id in dp_dm3pds:
            diff_time = (
                timedate_now - demo_model_3_portal_diagram_id.create_date
            )
            str_diff_time = humanize.naturaltime(diff_time).capitalize() + "."
            lst_time_diff_dp_dm3pd.append(str_diff_time)
        humanize.i18n.deactivate()

        dct_value = {
            "dp_dmps": dp_dmps,
            "lst_time_dp_dmp": lst_time_diff_dp_dmp,
            "dp_dm2ps": dp_dm2ps,
            "lst_time_dp_dm2p": lst_time_diff_dp_dm2p,
            "dp_dm3pds": dp_dm3pds,
            "lst_time_dp_dm3pd": lst_time_diff_dp_dm3pd,
        }

        # Render page
        return request.env["ir.ui.view"].render_template(
            "demo_website_multiple_snippet.demo_model_portal_and_demo_model_2_portal_and_demo_model_3_portal_diagram_list_list_item_structure_double_short",
            dct_value,
        )
