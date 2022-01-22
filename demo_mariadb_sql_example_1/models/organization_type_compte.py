from odoo import _, api, fields, models


class OrganizationTypeCompte(models.Model):
    _name = "organization.type.compte"
    _inherit = "portal.mixin"
    _description = "Organization Type Compte"
    _rec_name = "nom_complet"

    nom_complet = fields.Char(
        string="Nom complet",
        compute="_compute_nom_complet",
        store=True,
    )

    admin = fields.Boolean()

    admin_chef = fields.Boolean(string="Admin chef")

    admin_ord_point_service = fields.Boolean(
        string="Administrateur ordinaire point service"
    )

    admin_point_service = fields.Boolean(string="Administrateur point service")

    membre = fields.Many2one(comodel_name="organization.membre")

    organizateur_simple = fields.Boolean(string="Organizateur simple")

    reseau = fields.Boolean(string="Réseau")

    spip = fields.Boolean()

    def _compute_access_url(self):
        super(OrganizationTypeCompte, self)._compute_access_url()
        for organization_type_compte in self:
            organization_type_compte.access_url = (
                "/my/organization_type_compte/%s" % organization_type_compte.id
            )

    @api.depends("membre")
    def _compute_nom_complet(self):
        for rec in self:
            value = ""
            if rec.membre:
                value += rec.membre.nom_complet
            if not value:
                value = False
            rec.nom_complet = value
