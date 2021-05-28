from odoo import _, api, models, fields


class DemoWebsiteLeafletMapFeature(models.Model):
    _name = "demo.website_leaflet.map.feature"
    _description = "Map Feature"

    active = fields.Boolean(default=True)

    category_id = fields.Many2one(
        string="Category",
        comodel_name="demo.website_leaflet.category",
        ondelete="restrict",
    )

    geo_line = fields.GeoLine()

    geo_point = fields.GeoPoint()

    geo_polygon = fields.GeoPolygon()

    html_text = fields.Html(string="Popup text")

    name = fields.Char(required=True)

    open_popup = fields.Boolean(string="Popup opened on map")

    type = fields.Selection(
        selection=[
            ("geo_point", "Geo Point"),
            ("geo_line", "Geo Line"),
            ("geo_polygon", "Geo Polygon"),
        ],
        required=True,
        default="point",
    )
