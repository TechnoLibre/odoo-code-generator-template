from odoo import _, api, fields, models


class OrganizationOrigine(models.Model):
    _name = "organization.origine"
    _inherit = "portal.mixin"
    _description = "Organization Origine"
    _rec_name = "nom"

    nom = fields.Char(string="Origine")

    membre = fields.One2many(
        comodel_name="organization.membre",
        inverse_name="origine",
        help="Membre relation",
    )

    def _compute_access_url(self):
        super(OrganizationOrigine, self)._compute_access_url()
        for organization_origine in self:
            organization_origine.access_url = (
                "/my/organization_origine/%s" % organization_origine.id
            )
