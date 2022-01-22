from odoo import _, api, fields, models


class OrganizationSituationMaison(models.Model):
    _name = "organization.situation.maison"
    _inherit = "portal.mixin"
    _description = "Organization Situation Maison"
    _rec_name = "nom"

    nom = fields.Char(string="Situation")

    membre = fields.One2many(
        comodel_name="organization.membre",
        inverse_name="situation_maison",
        help="Membre relation",
    )

    def _compute_access_url(self):
        super(OrganizationSituationMaison, self)._compute_access_url()
        for organization_situation_maison in self:
            organization_situation_maison.access_url = (
                "/my/organization_situation_maison/%s"
                % organization_situation_maison.id
            )
