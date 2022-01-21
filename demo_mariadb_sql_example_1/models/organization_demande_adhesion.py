from odoo import _, api, fields, models


class OrganizationDemandeAdhesion(models.Model):
    _name = "organization.demande.adhesion"
    _inherit = "portal.mixin"
    _description = "Organization Demande Adhesion"
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
            "Lorsque non actif, cet demande d'adhésion n'est plus en fonction,"
            " mais demeure accessible."
        ),
    )

    courriel = fields.Char()

    date_mise_a_jour = fields.Datetime(
        string="Dernière mise à jour",
        help="Date de la dernière mise à jour",
    )

    en_attente = fields.Boolean(
        string="En attente",
        default=True,
    )

    nom = fields.Char()

    organization = fields.Many2one(
        comodel_name="organization.organization",
        required=True,
    )

    poste = fields.Char()

    prenom = fields.Char(string="Prénom")

    telephone = fields.Char(string="Téléphone")

    transferer = fields.Boolean(string="Transféré")

    def _compute_access_url(self):
        super(OrganizationDemandeAdhesion, self)._compute_access_url()
        for organization_demande_adhesion in self:
            organization_demande_adhesion.access_url = (
                "/my/organization_demande_adhesion/%s"
                % organization_demande_adhesion.id
            )

    @api.depends("nom", "prenom")
    def _compute_nom_complet(self):
        for rec in self:
            if rec.nom and rec.prenom:
                rec.nom_complet = f"{rec.prenom} {rec.nom}"
            elif rec.nom:
                rec.nom_complet = f"{rec.nom}"
            elif rec.prenom:
                rec.nom_complet = f"{rec.prenom}"
            else:
                rec.nom_complet = False
