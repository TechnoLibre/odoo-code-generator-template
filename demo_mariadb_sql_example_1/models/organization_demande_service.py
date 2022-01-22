from odoo import _, api, fields, models


class OrganizationDemandeService(models.Model):
    _name = "organization.demande.service"
    _inherit = "portal.mixin"
    _description = "Organization Demande Service"
    _rec_name = "titre"

    titre = fields.Char()

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Lorsque non actif, cet demande de services n'est plus en"
            " fonction, mais demeure accessible."
        ),
    )

    approuver = fields.Boolean(
        string="Approuvé",
        help="Permet d'approuver cette demande de service.",
    )

    commentaire = fields.One2many(
        comodel_name="organization.commentaire",
        inverse_name="demande_service_id",
        help="Commentaire relation",
    )

    date_debut = fields.Date(string="Date début")

    date_fin = fields.Date(string="Date fin")

    description = fields.Char()

    membre = fields.Many2one(comodel_name="organization.membre")

    organization = fields.Many2one(comodel_name="organization.organization")

    def _compute_access_url(self):
        super(OrganizationDemandeService, self)._compute_access_url()
        for organization_demande_service in self:
            organization_demande_service.access_url = (
                "/my/organization_demande_service/%s"
                % organization_demande_service.id
            )
