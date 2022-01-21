from odoo import _, api, fields, models


class OrganizationTypeService(models.Model):
    _name = "organization.type.service"
    _inherit = "portal.mixin"
    _description = "Type de services des Organizations"
    _rec_name = "nom_complet"

    nom_complet = fields.Char(
        string="Nom complet",
        compute="_compute_nom_complet",
        store=True,
    )

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Lorsque non actif, ce type de service n'est plus en fonction,"
            " mais demeure accessible."
        ),
    )

    approuve = fields.Boolean(
        string="Approuvé",
        help="Permet d'approuver ce type de services.",
    )

    description = fields.Char(help="Description du type de services")

    identifiant = fields.Char(
        compute="_compute_identifiant",
        store=True,
    )

    nom = fields.Char(help="Nom du type de services")

    numero = fields.Integer(
        string="Numéro",
        help="Numéro du type de services",
    )

    sous_categorie_id = fields.Many2one(
        comodel_name="organization.type.service.sous.categorie",
        string="Sous-catégorie",
        help="Sous-catégorie de services",
    )

    def _compute_access_url(self):
        super(OrganizationTypeService, self)._compute_access_url()
        for organization_type_service in self:
            organization_type_service.access_url = (
                "/my/organization_type_service/%s"
                % organization_type_service.id
            )

    @api.depends("sous_categorie_id", "sous_categorie_id.categorie", "numero")
    def _compute_identifiant(self):
        for rec in self:
            value = ""
            if rec.sous_categorie_id and rec.sous_categorie_id.categorie:
                value += str(rec.sous_categorie_id.categorie.nocategorie)
            if value and rec.sous_categorie_id:
                value += "-"
            if rec.sous_categorie_id:
                value += rec.sous_categorie_id.sous_categorie_service
            if rec.sous_categorie_id and rec.numero:
                value += "-"
            if rec.numero:
                value += str(rec.numero)
            rec.identifiant = value

    @api.depends("nom", "identifiant")
    def _compute_nom_complet(self):
        for rec in self:
            value = ""
            if rec.identifiant:
                value += rec.identifiant
            if rec.identifiant and rec.nom:
                value += " - "
            if rec.nom:
                value += rec.nom
            rec.nom_complet = value
