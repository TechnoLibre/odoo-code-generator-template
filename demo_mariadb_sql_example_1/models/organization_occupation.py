from odoo import _, api, fields, models


class OrganizationOccupation(models.Model):
    _name = "organization.occupation"
    _inherit = "portal.mixin"
    _description = "Organization Occupation"
    _rec_name = "nom"

    nom = fields.Char(string="Occupation")

    membre = fields.One2many(
        comodel_name="organization.membre",
        inverse_name="occupation",
        help="Membre relation",
    )

    def _compute_access_url(self):
        super(OrganizationOccupation, self)._compute_access_url()
        for organization_occupation in self:
            organization_occupation.access_url = (
                "/my/organization_occupation/%s" % organization_occupation.id
            )
