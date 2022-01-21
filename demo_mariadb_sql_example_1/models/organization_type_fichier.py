from odoo import _, api, fields, models


class OrganizationTypeFichier(models.Model):
    _name = "organization.type.fichier"
    _inherit = "portal.mixin"
    _description = "Organization Type Fichier"
    _rec_name = "nom"

    nom = fields.Char()

    date_mise_a_jour = fields.Datetime(
        string="Dernière mise à jour",
        required=True,
        help="Date de la dernière mise à jour",
    )

    fichier = fields.One2many(
        comodel_name="organization.fichier",
        inverse_name="type_fichier",
        help="Fichier relation",
    )

    def _compute_access_url(self):
        super(OrganizationTypeFichier, self)._compute_access_url()
        for organization_type_fichier in self:
            organization_type_fichier.access_url = (
                "/my/organization_type_fichier/%s"
                % organization_type_fichier.id
            )
