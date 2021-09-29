from odoo import _, api, fields, models


class DemoModel2Internal(models.Model):
    _name = "demo.model_2.internal"
    _description = "demo_model_2_internal"

    name = fields.Char()

    model_1 = fields.Many2one(comodel_name="demo.model.internal")
