from odoo import _, api, fields, models


class OrganizationDroitsAdmin(models.Model):
    _name = "organization.droits.admin"
    _inherit = "portal.mixin"
    _description = "Organization Droits Admin"
    _rec_name = "nom_complet"

    nom_complet = fields.Char(
        string="Nom complet",
        compute="_compute_nom_complet",
        store=True,
    )

    consulter_etat_compte = fields.Boolean(string="Consulter état de compte")

    consulter_profil = fields.Boolean(string="Consulter profil")

    gestion_dmd = fields.Boolean(string="Gestion demande de services")

    gestion_fichier = fields.Boolean(string="Gestion fichier")

    gestion_offre = fields.Boolean(string="Gestion offre")

    gestion_offre_service = fields.Boolean(string="Gestion offre de services")

    gestion_profil = fields.Boolean(string="Gestion profil")

    gestion_type_service = fields.Boolean(string="Gestion type de services")

    groupe_achat = fields.Boolean(string="Groupe d'achat")

    membre = fields.Many2one(comodel_name="organization.membre")

    saisie_echange = fields.Boolean(string="Saisie échange")

    validation = fields.Boolean()

    def _compute_access_url(self):
        super(OrganizationDroitsAdmin, self)._compute_access_url()
        for organization_droits_admin in self:
            organization_droits_admin.access_url = (
                "/my/organization_droits_admin/%s"
                % organization_droits_admin.id
            )

    @api.depends("membre")
    def _compute_nom_complet(self):
        for rec in self:
            if rec.membre:
                rec.nom_complet = rec.membre.nom_complet
            else:
                rec.nom_complet = False
