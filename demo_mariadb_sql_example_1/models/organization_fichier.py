from odoo import _, api, fields, models


class OrganizationFichier(models.Model):
    _name = "organization.fichier"
    _inherit = "portal.mixin"
    _description = "Organization Fichier"
    _rec_name = "nom"

    nom = fields.Char(required=True)

    date_mise_a_jour = fields.Datetime(
        string="Dernière mise à jour",
        help="Date de la dernière mise à jour",
    )

    fichier = fields.Binary(required=True)

    organization = fields.Many2one(
        comodel_name="organization.organization",
        required=True,
    )

    si_admin = fields.Boolean(string="Admin")

    si_disponible = fields.Boolean(string="Disponible")

    si_organization_local_seulement = fields.Boolean(
        string="Organization local seulement"
    )

    type_fichier = fields.Many2one(
        comodel_name="organization.type.fichier",
        string="Type fichier",
        required=True,
    )

    def _compute_access_url(self):
        super(OrganizationFichier, self)._compute_access_url()
        for organization_fichier in self:
            organization_fichier.access_url = (
                "/my/organization_fichier/%s" % organization_fichier.id
            )
