from odoo import _, api, fields, models


class OrganizationTypeCommunication(models.Model):
    _name = "organization.type.communication"
    _inherit = "portal.mixin"
    _description = "Organization Type Communication"
    _rec_name = "nom"

    nom = fields.Char(string="Typecommunication")

    membre = fields.One2many(
        comodel_name="organization.membre",
        inverse_name="type_communication",
        help="Membre relation",
    )

    def _compute_access_url(self):
        super(OrganizationTypeCommunication, self)._compute_access_url()
        for organization_type_communication in self:
            organization_type_communication.access_url = (
                "/my/organization_type_communication/%s"
                % organization_type_communication.id
            )
