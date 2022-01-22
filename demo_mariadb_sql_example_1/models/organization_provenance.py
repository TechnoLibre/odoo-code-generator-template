from odoo import _, api, fields, models


class OrganizationProvenance(models.Model):
    _name = "organization.provenance"
    _inherit = "portal.mixin"
    _description = "Organization Provenance"
    _rec_name = "nom"

    nom = fields.Char(string="Provenance")

    membre = fields.One2many(
        comodel_name="organization.membre",
        inverse_name="provenance",
        help="Membre relation",
    )

    def _compute_access_url(self):
        super(OrganizationProvenance, self)._compute_access_url()
        for organization_provenance in self:
            organization_provenance.access_url = (
                "/my/organization_provenance/%s" % organization_provenance.id
            )
