from odoo import _, api, fields, models


class OrganizationRevenuFamilial(models.Model):
    _name = "organization.revenu.familial"
    _inherit = "portal.mixin"
    _description = "Organization Revenu Familial"
    _rec_name = "nom"

    nom = fields.Char(string="Revenu")

    membre = fields.One2many(
        comodel_name="organization.membre",
        inverse_name="revenu_familial",
        help="Membre relation",
    )

    def _compute_access_url(self):
        super(OrganizationRevenuFamilial, self)._compute_access_url()
        for organization_revenu_familial in self:
            organization_revenu_familial.access_url = (
                "/my/organization_revenu_familial/%s"
                % organization_revenu_familial.id
            )
