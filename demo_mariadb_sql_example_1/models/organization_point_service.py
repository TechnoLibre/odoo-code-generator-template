from odoo import _, api, fields, models


class OrganizationPointService(models.Model):
    _name = "organization.point.service"
    _inherit = "portal.mixin"
    _description = "Organization Point Service"
    _rec_name = "nom"

    nom = fields.Char(help="Nom du point de service")

    commentaire = fields.One2many(
        comodel_name="organization.commentaire",
        inverse_name="point_service",
        help="Commentaire relation",
    )

    date_mise_a_jour = fields.Datetime(
        string="Dernière mise à jour",
        help="Date de la dernière mise à jour",
    )

    membre = fields.One2many(
        comodel_name="organization.membre",
        inverse_name="point_service",
        help="Membre relation",
    )

    organization = fields.Many2one(
        comodel_name="organization.organization",
        required=True,
    )

    sequence = fields.Integer(
        string="Séquence",
        help="Séquence d'affichage",
    )

    def _compute_access_url(self):
        super(OrganizationPointService, self)._compute_access_url()
        for organization_point_service in self:
            organization_point_service.access_url = (
                "/my/organization_point_service/%s"
                % organization_point_service.id
            )
