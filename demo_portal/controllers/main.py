import base64
import logging

import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class DemoPortalController(http.Controller):
    @http.route(
        ["/demo_portal/get_last_item"],
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
        "/new/demo_model_2_portal", type="http", auth="user", website=True
    )
    def create_new_demo_model_2_portal(self, **kw):
        name = http.request.env.user.name
        demo_many2one_dst = http.request.env["demo.model.portal"].search([])
        default_demo_many2one_dst = (
            http.request.env["demo.model_2.portal"]
            .default_get(["demo_many2one_dst"])
            .get("demo_many2one_dst")
        )
        demo_many2one_src = http.request.env["demo.model.portal"].search([])
        default_demo_many2one_src = (
            http.request.env["demo.model_2.portal"]
            .default_get(["demo_many2one_src"])
            .get("demo_many2one_src")
        )
        diagram_id = http.request.env["demo.model_3.portal.diagram"].search([])
        default_diagram_id = (
            http.request.env["demo.model_2.portal"]
            .default_get(["diagram_id"])
            .get("diagram_id")
        )
        return http.request.render(
            "demo_portal.portal_create_demo_model_2_portal",
            {
                "name": name,
                "demo_many2one_dst": demo_many2one_dst,
                "demo_many2one_src": demo_many2one_src,
                "diagram_id": diagram_id,
                "page_name": "create_demo_model_2_portal",
                "default_demo_many2one_dst": default_demo_many2one_dst,
                "default_demo_many2one_src": default_demo_many2one_src,
                "default_diagram_id": default_diagram_id,
            },
        )

    @http.route(
        "/submitted/demo_model_2_portal",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_demo_model_2_portal(self, **kw):
        vals = {}

        if kw.get("name"):
            vals["name"] = kw.get("name")

        if (
            kw.get("demo_many2one_dst")
            and kw.get("demo_many2one_dst").isdigit()
        ):
            vals["demo_many2one_dst"] = int(kw.get("demo_many2one_dst"))

        if (
            kw.get("demo_many2one_src")
            and kw.get("demo_many2one_src").isdigit()
        ):
            vals["demo_many2one_src"] = int(kw.get("demo_many2one_src"))

        if kw.get("diagram_id") and kw.get("diagram_id").isdigit():
            vals["diagram_id"] = int(kw.get("diagram_id"))

        new_demo_model_2_portal = (
            request.env["demo.model_2.portal"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/demo_model_2_portal/{new_demo_model_2_portal.id}"
        )

    @http.route(
        "/new/demo_model_3_portal_diagram",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_demo_model_3_portal_diagram(self, **kw):
        name = http.request.env.user.name
        return http.request.render(
            "demo_portal.portal_create_demo_model_3_portal_diagram",
            {"name": name, "page_name": "create_demo_model_3_portal_diagram"},
        )

    @http.route(
        "/submitted/demo_model_3_portal_diagram",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_demo_model_3_portal_diagram(self, **kw):
        vals = {}

        if kw.get("name"):
            vals["name"] = kw.get("name")

        new_demo_model_3_portal_diagram = (
            request.env["demo.model_3.portal.diagram"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/demo_model_3_portal_diagram/{new_demo_model_3_portal_diagram.id}"
        )

    @http.route(
        "/new/demo_model_portal", type="http", auth="user", website=True
    )
    def create_new_demo_model_portal(self, **kw):
        name = http.request.env.user.name
        default_demo_boolean = (
            http.request.env["demo.model.portal"]
            .default_get(["demo_boolean"])
            .get("demo_boolean")
        )
        default_demo_char = (
            http.request.env["demo.model.portal"]
            .default_get(["demo_char"])
            .get("demo_char")
        )
        default_demo_date = (
            http.request.env["demo.model.portal"]
            .default_get(["demo_date"])
            .get("demo_date")
        )
        default_demo_date_time = (
            http.request.env["demo.model.portal"]
            .default_get(["demo_date_time"])
            .get("demo_date_time")
        )
        default_demo_external_link = (
            http.request.env["demo.model.portal"]
            .default_get(["demo_external_link"])
            .get("demo_external_link")
        )
        default_demo_float = (
            http.request.env["demo.model.portal"]
            .default_get(["demo_float"])
            .get("demo_float")
        )
        default_demo_float_time = (
            http.request.env["demo.model.portal"]
            .default_get(["demo_float_time"])
            .get("demo_float_time")
        )
        default_demo_html = (
            http.request.env["demo.model.portal"]
            .default_get(["demo_html"])
            .get("demo_html")
        )
        default_demo_integer = (
            http.request.env["demo.model.portal"]
            .default_get(["demo_integer"])
            .get("demo_integer")
        )
        demo_many2many = http.request.env["demo.model_2.portal"].search([])
        lst_default_demo_many2many = (
            http.request.env["demo.model.portal"]
            .default_get(["demo_many2many"])
            .get("demo_many2many")
        )
        if lst_default_demo_many2many:
            default_demo_many2many = lst_default_demo_many2many[0][2]
        else:
            default_demo_many2many = []
        demo_selection = (
            http.request.env["demo.model.portal"]
            ._fields["demo_selection"]
            .selection
        )
        default_demo_selection = (
            http.request.env["demo.model.portal"]
            .default_get(["demo_selection"])
            .get("demo_selection")
        )
        default_demo_text = (
            http.request.env["demo.model.portal"]
            .default_get(["demo_text"])
            .get("demo_text")
        )
        diagram_id = http.request.env["demo.model_3.portal.diagram"].search([])
        default_diagram_id = (
            http.request.env["demo.model.portal"]
            .default_get(["diagram_id"])
            .get("diagram_id")
        )
        default_xpos = (
            http.request.env["demo.model.portal"]
            .default_get(["xpos"])
            .get("xpos")
        )
        default_ypos = (
            http.request.env["demo.model.portal"]
            .default_get(["ypos"])
            .get("ypos")
        )
        return http.request.render(
            "demo_portal.portal_create_demo_model_portal",
            {
                "name": name,
                "demo_many2many": demo_many2many,
                "demo_selection": demo_selection,
                "diagram_id": diagram_id,
                "page_name": "create_demo_model_portal",
                "default_demo_boolean": default_demo_boolean,
                "default_demo_char": default_demo_char,
                "default_demo_date": default_demo_date,
                "default_demo_date_time": default_demo_date_time,
                "default_demo_external_link": default_demo_external_link,
                "default_demo_float": default_demo_float,
                "default_demo_float_time": default_demo_float_time,
                "default_demo_html": default_demo_html,
                "default_demo_integer": default_demo_integer,
                "default_demo_many2many": default_demo_many2many,
                "default_demo_selection": default_demo_selection,
                "default_demo_text": default_demo_text,
                "default_diagram_id": default_diagram_id,
                "default_xpos": default_xpos,
                "default_ypos": default_ypos,
            },
        )

    @http.route(
        "/submitted/demo_model_portal",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_demo_model_portal(self, **kw):
        vals = {}

        if kw.get("name"):
            vals["name"] = kw.get("name")

        if kw.get("demo_binary"):
            lst_file_demo_binary = request.httprequest.files.getlist(
                "demo_binary"
            )
            if lst_file_demo_binary:
                vals["demo_binary"] = base64.b64encode(
                    lst_file_demo_binary[-1].read()
                )

        if kw.get("demo_binary_image"):
            lst_file_demo_binary_image = request.httprequest.files.getlist(
                "demo_binary_image"
            )
            if lst_file_demo_binary_image:
                vals["demo_binary_image"] = base64.b64encode(
                    lst_file_demo_binary_image[-1].read()
                )

        default_demo_boolean = (
            http.request.env["demo.model.portal"]
            .default_get(["demo_boolean"])
            .get("demo_boolean")
        )
        if kw.get("demo_boolean"):
            vals["demo_boolean"] = kw.get("demo_boolean") == "True"
        elif default_demo_boolean:
            vals["demo_boolean"] = False

        if kw.get("demo_char"):
            vals["demo_char"] = kw.get("demo_char")

        if kw.get("demo_date"):
            vals["demo_date"] = kw.get("demo_date")

        if kw.get("demo_date_time"):
            vals["demo_date_time"] = kw.get("demo_date_time")

        if kw.get("demo_external_link"):
            vals["demo_external_link"] = kw.get("demo_external_link")

        if kw.get("demo_float"):
            demo_float_value = kw.get("demo_float")
            if demo_float_value.replace(".", "", 1).isdigit():
                vals["demo_float"] = float(demo_float_value)

        if kw.get("demo_float_time"):
            demo_float_time_value = kw.get("demo_float_time")
            tpl_time_demo_float_time = demo_float_time_value.split(":")
            if len(tpl_time_demo_float_time) == 1:
                if tpl_time_demo_float_time[0].isdigit():
                    vals["demo_float_time"] = int(tpl_time_demo_float_time[0])
            elif len(tpl_time_demo_float_time) == 2:
                if (
                    tpl_time_demo_float_time[0].isdigit()
                    and tpl_time_demo_float_time[1].isdigit()
                ):
                    vals["demo_float_time"] = (
                        int(tpl_time_demo_float_time[0])
                        + int(tpl_time_demo_float_time[1]) / 60.0
                    )

        if kw.get("demo_html"):
            vals["demo_html"] = kw.get("demo_html")

        if kw.get("demo_integer"):
            demo_integer_value = kw.get("demo_integer")
            if demo_integer_value.isdigit():
                vals["demo_integer"] = int(demo_integer_value)

        if kw.get("demo_many2many"):
            lst_value_demo_many2many = [
                (4, int(a))
                for a in request.httprequest.form.getlist("demo_many2many")
            ]
            vals["demo_many2many"] = lst_value_demo_many2many

        if kw.get("demo_selection"):
            vals["demo_selection"] = kw.get("demo_selection")

        if kw.get("demo_text"):
            vals["demo_text"] = kw.get("demo_text")

        if kw.get("diagram_id") and kw.get("diagram_id").isdigit():
            vals["diagram_id"] = int(kw.get("diagram_id"))

        if kw.get("xpos"):
            xpos_value = kw.get("xpos")
            if xpos_value.isdigit():
                vals["xpos"] = int(xpos_value)

        if kw.get("ypos"):
            ypos_value = kw.get("ypos")
            if ypos_value.isdigit():
                vals["ypos"] = int(ypos_value)

        new_demo_model_portal = (
            request.env["demo.model.portal"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/demo_model_portal/{new_demo_model_portal.id}"
        )
