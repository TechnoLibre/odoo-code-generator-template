from odoo import _, api, fields, models


class DemoModel2Internal(models.Model):
    _name = "demo.model_2.internal"
    _description = "demo_model_2_internal"

    name = fields.Char()

    # Model_2 contain model_1
    # Only 1 time
    model_1 = fields.Many2one(comodel_name="demo.model.internal")
