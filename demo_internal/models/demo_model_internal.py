from odoo import _, api, fields, models


class DemoModelInternal(models.Model):
    _name = "demo.model.internal"
    _inherit = ["mail.activity.mixin", "mail.thread"]
    _description = "demo_model_internal"

    name = fields.Char()

    # Banana demo
    banana = fields.Boolean(string="Banana demo")

    date_end = fields.Datetime(string="Date end")

    date_start = fields.Datetime(string="Date start")

    empty = fields.Text()
    # End of DemoModelInternal
