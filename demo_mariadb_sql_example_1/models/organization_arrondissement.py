from odoo import _, api, fields, models


class OrganizationArrondissement(models.Model):
    _name = "organization.arrondissement"
    _inherit = "portal.mixin"
    _description = "Ensemble des arrondissement des Organizations"
    _rec_name = "nom"

    nom = fields.Char()

    membre = fields.One2many(
        comodel_name="organization.membre",
        inverse_name="arrondissement",
        help="Membre relation",
    )

    ville = fields.Many2one(comodel_name="organization.ville")

    def _compute_access_url(self):
        super(OrganizationArrondissement, self)._compute_access_url()
        for organization_arrondissement in self:
            organization_arrondissement.access_url = (
                "/my/organization_arrondissement/%s"
                % organization_arrondissement.id
            )
