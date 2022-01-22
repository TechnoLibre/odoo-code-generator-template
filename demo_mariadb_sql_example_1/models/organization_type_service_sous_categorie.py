from odoo import _, api, fields, models


class OrganizationTypeServiceSousCategorie(models.Model):
    _name = "organization.type.service.sous.categorie"
    _inherit = "portal.mixin"
    _description = "Type de services sous-catégorie"
    _rec_name = "nom"

    nom = fields.Char()

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Lorsque non actif, cette sous-catégorie n'est plus en fonction,"
            " mais demeure accessible."
        ),
    )

    approuver = fields.Boolean(
        string="Approuvé",
        help="Permet d'approuver cette sous-catégorie.",
    )

    categorie = fields.Many2one(
        comodel_name="organization.type.service.categorie",
        string="Catégorie",
        required=True,
    )

    sous_categorie_service = fields.Char(
        string="Sous-catégorie",
        required=True,
    )

    type_service = fields.One2many(
        comodel_name="organization.type.service",
        inverse_name="sous_categorie_id",
        help="Type Service relation",
    )

    def _compute_access_url(self):
        super(OrganizationTypeServiceSousCategorie, self)._compute_access_url()
        for organization_type_service_sous_categorie in self:
            organization_type_service_sous_categorie.access_url = (
                "/my/organization_type_service_sous_categorie/%s"
                % organization_type_service_sous_categorie.id
            )
