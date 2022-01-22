from odoo import _, api, fields, models


class OrganizationTypeServiceCategorie(models.Model):
    _name = "organization.type.service.categorie"
    _inherit = "portal.mixin"
    _description = "Les catégories de types de services des Organizations"
    _rec_name = "nom"

    nom = fields.Char(help="Le nom de la catégorie des services")

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Lorsque non actif, cette catégorie n'est plus en fonction, mais"
            " demeure accessible."
        ),
    )

    approuve = fields.Boolean(
        string="Approuvé",
        help="Permet d'approuver cette catégorie.",
    )

    nocategorie = fields.Integer(required=True)

    type_service_sous_categorie = fields.One2many(
        comodel_name="organization.type.service.sous.categorie",
        inverse_name="categorie",
        help="Type Service Sous Categorie relation",
    )

    def _compute_access_url(self):
        super(OrganizationTypeServiceCategorie, self)._compute_access_url()
        for organization_type_service_categorie in self:
            organization_type_service_categorie.access_url = (
                "/my/organization_type_service_categorie/%s"
                % organization_type_service_categorie.id
            )
