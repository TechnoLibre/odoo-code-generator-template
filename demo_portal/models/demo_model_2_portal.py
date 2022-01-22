from odoo import _, api, fields, models


class DemoModel2Portal(models.Model):
    _name = "demo.model_2.portal"
    _inherit = ["mail.activity.mixin", "mail.thread", "portal.mixin"]
    _description = "demo_model_2_portal"

    name = fields.Char(track_visibility="onchange")

    demo_many2one_dst = fields.Many2one(
        comodel_name="demo.model.portal",
        string="Many2one dst",
    )

    demo_many2one_src = fields.Many2one(
        comodel_name="demo.model.portal",
        string="Many2one src",
    )

    diagram_id = fields.Many2one(
        comodel_name="demo.model_3.portal.diagram",
        string="Diagram",
    )

    def _compute_access_url(self):
        super(DemoModel2Portal, self)._compute_access_url()
        for demo_model_2_portal in self:
            demo_model_2_portal.access_url = (
                "/my/demo_model_2_portal/%s" % demo_model_2_portal.id
            )
