from odoo import _, api, fields, models


class OrganizationOrganization(models.Model):
    _name = "organization.organization"
    _inherit = "portal.mixin"
    _description = (
        "Gestion des entitées Organization, contient les informations et les"
        " messages d'une Organization."
    )
    _rec_name = "nom"

    nom = fields.Char(
        required=True,
        help="Nom de l'Organization",
    )

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Lorsque non actif, cette organization n'est plus en fonction,"
            " mais demeure accessible."
        ),
    )

    adresse = fields.Char(help="Adresse de l'Organization")

    arrondissement = fields.Many2one(
        comodel_name="organization.arrondissement",
        help="Nom de l'Arrondissement qui contient l'Organization.",
    )

    code_postal = fields.Char(
        string="Code postal",
        help="Code postal de l'Organization",
    )

    courriel = fields.Char(
        string="Adresse courriel",
        help="Adresse courriel pour joindre l'Organization.",
    )

    date_mise_a_jour = fields.Datetime(
        string="Dernière mise à jour",
        help="Date de la dernière mise à jour",
    )

    grp_achat_administrateur = fields.Boolean(
        string="Groupe d'achats des administrateurs",
        help=(
            "Permet de rendre accessible les achats pour les administrateurs."
        ),
    )

    grp_achat_membre = fields.Boolean(
        string="Groupe d'achats membre",
        help="Rend accessible les achats pour les Organizateurs.",
    )

    logo = fields.Binary(help="Logo de l'Organization")

    membre = fields.One2many(
        comodel_name="organization.membre",
        inverse_name="organization",
        help="Membre relation",
    )

    message_accueil = fields.Html(
        string="Message d'accueil",
        help="Message à afficher pour accueillir les membres.",
    )

    message_grp_achat = fields.Html(
        string="Message groupe d'achats",
        help="Message à afficher pour les groupes d'achats.",
    )

    region = fields.Many2one(
        comodel_name="organization.region",
        string="Région administrative",
        help="Nom de la région administrative de l'Organization",
    )

    telecopieur = fields.Char(
        string="Télécopieur",
        help="Numéro de télécopieur pour joindre l'Organization.",
    )

    telephone = fields.Char(
        string="Téléphone",
        help="Numéro de téléphone pour joindre l'Organization.",
    )

    url_public = fields.Char(
        string="Lien du site web publique",
        help="Lien du site web publique de l'Organization",
    )

    url_transactionnel = fields.Char(
        string="Lien du site web transactionnel",
        help="Lien du site web transactionnel de l'Organization",
    )

    ville = fields.Many2one(
        comodel_name="organization.ville",
        help="Nom de la ville de l'Organization",
    )

    def _compute_access_url(self):
        super(OrganizationOrganization, self)._compute_access_url()
        for organization_organization in self:
            organization_organization.access_url = (
                "/my/organization_organization/%s"
                % organization_organization.id
            )
