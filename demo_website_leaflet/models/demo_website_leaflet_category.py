from odoo import _, api, fields, models


class DemoWebsiteLeafletCategory(models.Model):
    _name = "demo.website_leaflet.category"
    _description = "Map Feature Category"

    name = fields.Char(required=True)

    active = fields.Boolean(default=True)

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
    )

    description = fields.Char()

    parent = fields.Many2one(
        comodel_name="demo.website_leaflet.category",
        ondelete="restrict",
    )
