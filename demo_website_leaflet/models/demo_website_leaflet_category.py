from odoo import _, api, models, fields


class DemoWebsiteLeafletCategory(models.Model):
    _name = "demo.website_leaflet.category"
    _description = "Map Feature Category"

    active = fields.Boolean(default=True)

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
    )

    description = fields.Char()

    name = fields.Char(required=True)

    parent = fields.Many2one(
        comodel_name="demo.website_leaflet.category",
        ondelete="restrict",
    )
