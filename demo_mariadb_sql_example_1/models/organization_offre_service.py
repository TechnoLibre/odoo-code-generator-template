from odoo import _, api, fields, models


class OrganizationOffreService(models.Model):
    _name = "organization.offre.service"
    _inherit = "portal.mixin"
    _description = "Organization Offre Service"
    _rec_name = "description"

    description = fields.Char()

    accompli = fields.Boolean(
        string="Accomplie",
        help="Cette offre de service est réalisée.",
    )

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Lorsque non actif, cet offre de services n'est plus en fonction,"
            " mais demeure accessible."
        ),
    )

    approuve = fields.Boolean(
        string="Approuvé",
        help="Permet d'approuver ce type de services.",
    )

    condition = fields.Char(
        string="Conditions",
        help="Conditions inhérentes à l'offre",
    )

    condition_autre = fields.Char(
        string="Condition autres",
        help="Autres conditions à informer",
    )

    date_affichage = fields.Date(string="Date d'affichage")

    date_debut = fields.Date(
        string="Date de début",
        help="Date à partir de laquelle l'offre est valide.",
    )

    date_fin = fields.Date(
        string="Date de fin",
        help="Date jusqu'à laquelle l'offre est valide.",
    )

    date_mise_a_jour = fields.Datetime(
        string="Dernière mise à jour",
        required=True,
        help="Date de la dernière mise à jour",
    )

    disponibilite = fields.Char(string="Disponibilité")

    membre = fields.Many2one(
        comodel_name="organization.membre",
        help="Membre qui offre le service",
    )

    nb_consultation = fields.Integer(string="Nombre de consultations")

    nom_offre_special = fields.Char(
        string="Nom de l'offre spéciale",
        help="Nom ou brève description de l'offre spéciale",
    )

    offre_special = fields.Boolean(string="Offre spéciale")

    organization = fields.Many2one(
        comodel_name="organization.organization",
        help="Organization associée",
    )

    tarif = fields.Char()

    type_service_id = fields.Many2one(
        comodel_name="organization.type.service",
        string="Type de services",
    )

    def _compute_access_url(self):
        super(OrganizationOffreService, self)._compute_access_url()
        for organization_offre_service in self:
            organization_offre_service.access_url = (
                "/my/organization_offre_service/%s"
                % organization_offre_service.id
            )
