from odoo import _, api, fields, models


class OrganizationQuartier(models.Model):
    _name = "organization.quartier"
    _inherit = "portal.mixin"
    _description = "Organization Quartier"
    _rec_name = "nom"

    nom = fields.Char(
        string="Nom du quartier",
        help="Nom du quartier",
    )

    arrondissement = fields.Many2one(
        comodel_name="organization.arrondissement",
        required=True,
        help="Arrondissement associé au quartier",
    )

    membre = fields.One2many(
        comodel_name="organization.membre",
        inverse_name="quartier",
        help="Membre relation",
    )

    def _compute_access_url(self):
        super(OrganizationQuartier, self)._compute_access_url()
        for organization_quartier in self:
            organization_quartier.access_url = (
                "/my/organization_quartier/%s" % organization_quartier.id
            )
