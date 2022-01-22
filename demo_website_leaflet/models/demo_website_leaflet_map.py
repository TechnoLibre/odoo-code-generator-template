from odoo import _, api, fields, models


class DemoWebsiteLeafletMap(models.Model):
    _name = "demo.website_leaflet.map"
    _description = "Map"

    name = fields.Char(required=True)

    active = fields.Boolean(default=True)

    category_id = fields.Many2one(
        comodel_name="demo.website_leaflet.category",
        string="Category",
        ondelete="restrict",
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
    )

    description = fields.Char()

    feature_id = fields.Many2many(
        comodel_name="demo.website_leaflet.map.feature",
        string="Features",
    )
