from odoo import _, api, fields, models


class OrganizationVille(models.Model):
    _name = "organization.ville"
    _inherit = "portal.mixin"
    _description = "Organization Ville"
    _rec_name = "nom"

    nom = fields.Char()

    arrondissement = fields.One2many(
        comodel_name="organization.arrondissement",
        inverse_name="ville",
        help="Arrondissement relation",
    )

    code = fields.Integer(
        required=True,
        help="Code de la ville",
    )

    membre = fields.One2many(
        comodel_name="organization.membre",
        inverse_name="ville",
        help="Membre relation",
    )

    organization = fields.One2many(
        comodel_name="organization.organization",
        inverse_name="ville",
        help="Organization relation",
    )

    region = fields.Many2one(
        comodel_name="organization.region",
        string="Région",
    )

    def _compute_access_url(self):
        super(OrganizationVille, self)._compute_access_url()
        for organization_ville in self:
            organization_ville.access_url = (
                "/my/organization_ville/%s" % organization_ville.id
            )
