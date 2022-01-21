from odoo import _, api, fields, models


class OrganizationRegion(models.Model):
    _name = "organization.region"
    _inherit = "portal.mixin"
    _description = "Organization Region"
    _rec_name = "nom"

    nom = fields.Char()

    code = fields.Integer(
        string="Code de région",
        required=True,
        help="Code de la région administrative",
    )

    membre = fields.One2many(
        comodel_name="organization.membre",
        inverse_name="region",
        help="Membre relation",
    )

    organization = fields.One2many(
        comodel_name="organization.organization",
        inverse_name="region",
        help="Organization relation",
    )

    ville = fields.One2many(
        comodel_name="organization.ville",
        inverse_name="region",
        help="Ville relation",
    )

    def _compute_access_url(self):
        super(OrganizationRegion, self)._compute_access_url()
        for organization_region in self:
            organization_region.access_url = (
                "/my/organization_region/%s" % organization_region.id
            )
