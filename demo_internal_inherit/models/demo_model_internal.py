from odoo import _, api, fields, models


class DemoModelInternal(models.Model):
    _inherit = "demo.model.internal"

    feature_text = fields.Char(string="Feature demo")
