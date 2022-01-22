import base64
import logging

import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class DemoMariadbSqlExample1Controller(http.Controller):
    @http.route(
        "/new/organization_arrondissement",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_arrondissement(self, **kw):
        default_nom = (
            http.request.env["organization.arrondissement"]
            .default_get(["nom"])
            .get("nom")
        )
        ville = http.request.env["organization.ville"].search([])
        default_ville = (
            http.request.env["organization.arrondissement"]
            .default_get(["ville"])
            .get("ville")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_arrondissement",
            {
                "ville": ville,
                "page_name": "create_organization_arrondissement",
                "default_nom": default_nom,
                "default_ville": default_ville,
            },
        )

    @http.route(
        "/submitted/organization_arrondissement",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_arrondissement(self, **kw):
        vals = {}

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        if kw.get("ville") and kw.get("ville").isdigit():
            vals["ville"] = int(kw.get("ville"))

        new_organization_arrondissement = (
            request.env["organization.arrondissement"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_arrondissement/{new_organization_arrondissement.id}"
        )

    @http.route(
        "/new/organization_commentaire", type="http", auth="user", website=True
    )
    def create_new_organization_commentaire(self, **kw):
        default_autre_commentaire = (
            http.request.env["organization.commentaire"]
            .default_get(["autre_commentaire"])
            .get("autre_commentaire")
        )
        default_autre_situation = (
            http.request.env["organization.commentaire"]
            .default_get(["autre_situation"])
            .get("autre_situation")
        )
        confidentiel = (
            http.request.env["organization.commentaire"]
            ._fields["confidentiel"]
            .selection
        )
        default_confidentiel = (
            http.request.env["organization.commentaire"]
            .default_get(["confidentiel"])
            .get("confidentiel")
        )
        default_consulter_organization = (
            http.request.env["organization.commentaire"]
            .default_get(["consulter_organization"])
            .get("consulter_organization")
        )
        default_consulter_reseau = (
            http.request.env["organization.commentaire"]
            .default_get(["consulter_reseau"])
            .get("consulter_reseau")
        )
        default_date_incident = (
            http.request.env["organization.commentaire"]
            .default_get(["date_incident"])
            .get("date_incident")
        )
        default_date_mise_a_jour = (
            http.request.env["organization.commentaire"]
            .default_get(["date_mise_a_jour"])
            .get("date_mise_a_jour")
        )
        default_datetime_creation = (
            http.request.env["organization.commentaire"]
            .default_get(["datetime_creation"])
            .get("datetime_creation")
        )
        degre_satisfaction = (
            http.request.env["organization.commentaire"]
            ._fields["degre_satisfaction"]
            .selection
        )
        default_degre_satisfaction = (
            http.request.env["organization.commentaire"]
            .default_get(["degre_satisfaction"])
            .get("degre_satisfaction")
        )
        demande_service_id = http.request.env[
            "organization.demande.service"
        ].search([("active", "=", True)])
        default_demande_service_id = (
            http.request.env["organization.commentaire"]
            .default_get(["demande_service_id"])
            .get("demande_service_id")
        )
        default_demarche = (
            http.request.env["organization.commentaire"]
            .default_get(["demarche"])
            .get("demarche")
        )
        membre_source = http.request.env["organization.membre"].search(
            [("active", "=", True)]
        )
        default_membre_source = (
            http.request.env["organization.commentaire"]
            .default_get(["membre_source"])
            .get("membre_source")
        )
        membre_viser = http.request.env["organization.membre"].search(
            [("active", "=", True)]
        )
        default_membre_viser = (
            http.request.env["organization.commentaire"]
            .default_get(["membre_viser"])
            .get("membre_viser")
        )
        default_nom_comite = (
            http.request.env["organization.commentaire"]
            .default_get(["nom_comite"])
            .get("nom_comite")
        )
        default_nom_complet = (
            http.request.env["organization.commentaire"]
            .default_get(["nom_complet"])
            .get("nom_complet")
        )
        default_note_administrative = (
            http.request.env["organization.commentaire"]
            .default_get(["note_administrative"])
            .get("note_administrative")
        )
        default_number = (
            http.request.env["organization.commentaire"]
            .default_get(["number"])
            .get("number")
        )
        offre_service_id = http.request.env[
            "organization.offre.service"
        ].search([("active", "=", True)])
        default_offre_service_id = (
            http.request.env["organization.commentaire"]
            .default_get(["offre_service_id"])
            .get("offre_service_id")
        )
        point_service = http.request.env["organization.point.service"].search(
            []
        )
        default_point_service = (
            http.request.env["organization.commentaire"]
            .default_get(["point_service"])
            .get("point_service")
        )
        default_resumer_situation = (
            http.request.env["organization.commentaire"]
            .default_get(["resumer_situation"])
            .get("resumer_situation")
        )
        situation_impliquant = (
            http.request.env["organization.commentaire"]
            ._fields["situation_impliquant"]
            .selection
        )
        default_situation_impliquant = (
            http.request.env["organization.commentaire"]
            .default_get(["situation_impliquant"])
            .get("situation_impliquant")
        )
        default_solution_pour_regler = (
            http.request.env["organization.commentaire"]
            .default_get(["solution_pour_regler"])
            .get("solution_pour_regler")
        )
        type_offre = (
            http.request.env["organization.commentaire"]
            ._fields["type_offre"]
            .selection
        )
        default_type_offre = (
            http.request.env["organization.commentaire"]
            .default_get(["type_offre"])
            .get("type_offre")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_commentaire",
            {
                "confidentiel": confidentiel,
                "degre_satisfaction": degre_satisfaction,
                "demande_service_id": demande_service_id,
                "membre_source": membre_source,
                "membre_viser": membre_viser,
                "offre_service_id": offre_service_id,
                "point_service": point_service,
                "situation_impliquant": situation_impliquant,
                "type_offre": type_offre,
                "page_name": "create_organization_commentaire",
                "default_autre_commentaire": default_autre_commentaire,
                "default_autre_situation": default_autre_situation,
                "default_confidentiel": default_confidentiel,
                "default_consulter_organization": default_consulter_organization,
                "default_consulter_reseau": default_consulter_reseau,
                "default_date_incident": default_date_incident,
                "default_date_mise_a_jour": default_date_mise_a_jour,
                "default_datetime_creation": default_datetime_creation,
                "default_degre_satisfaction": default_degre_satisfaction,
                "default_demande_service_id": default_demande_service_id,
                "default_demarche": default_demarche,
                "default_membre_source": default_membre_source,
                "default_membre_viser": default_membre_viser,
                "default_nom_comite": default_nom_comite,
                "default_nom_complet": default_nom_complet,
                "default_note_administrative": default_note_administrative,
                "default_number": default_number,
                "default_offre_service_id": default_offre_service_id,
                "default_point_service": default_point_service,
                "default_resumer_situation": default_resumer_situation,
                "default_situation_impliquant": default_situation_impliquant,
                "default_solution_pour_regler": default_solution_pour_regler,
                "default_type_offre": default_type_offre,
            },
        )

    @http.route(
        "/submitted/organization_commentaire",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_commentaire(self, **kw):
        vals = {}

        if kw.get("autre_commentaire"):
            vals["autre_commentaire"] = kw.get("autre_commentaire")

        if kw.get("autre_situation"):
            vals["autre_situation"] = kw.get("autre_situation")

        default_consulter_organization = (
            http.request.env["organization.commentaire"]
            .default_get(["consulter_organization"])
            .get("consulter_organization")
        )
        if kw.get("consulter_organization"):
            vals["consulter_organization"] = (
                kw.get("consulter_organization") == "True"
            )
        elif default_consulter_organization:
            vals["consulter_organization"] = False

        default_consulter_reseau = (
            http.request.env["organization.commentaire"]
            .default_get(["consulter_reseau"])
            .get("consulter_reseau")
        )
        if kw.get("consulter_reseau"):
            vals["consulter_reseau"] = kw.get("consulter_reseau") == "True"
        elif default_consulter_reseau:
            vals["consulter_reseau"] = False

        if kw.get("date_incident"):
            vals["date_incident"] = kw.get("date_incident")

        if kw.get("date_mise_a_jour"):
            vals["date_mise_a_jour"] = kw.get("date_mise_a_jour")

        if kw.get("datetime_creation"):
            vals["datetime_creation"] = kw.get("datetime_creation")

        if (
            kw.get("demande_service_id")
            and kw.get("demande_service_id").isdigit()
        ):
            vals["demande_service_id"] = int(kw.get("demande_service_id"))

        if kw.get("demarche"):
            vals["demarche"] = kw.get("demarche")

        if kw.get("membre_source") and kw.get("membre_source").isdigit():
            vals["membre_source"] = int(kw.get("membre_source"))

        if kw.get("membre_viser") and kw.get("membre_viser").isdigit():
            vals["membre_viser"] = int(kw.get("membre_viser"))

        if kw.get("nom_comite"):
            vals["nom_comite"] = kw.get("nom_comite")

        if kw.get("nom_complet"):
            vals["nom_complet"] = kw.get("nom_complet")

        if kw.get("note_administrative"):
            vals["note_administrative"] = kw.get("note_administrative")

        if kw.get("number"):
            number_value = kw.get("number")
            if number_value.isdigit():
                vals["number"] = int(number_value)

        if kw.get("offre_service_id") and kw.get("offre_service_id").isdigit():
            vals["offre_service_id"] = int(kw.get("offre_service_id"))

        if kw.get("point_service") and kw.get("point_service").isdigit():
            vals["point_service"] = int(kw.get("point_service"))

        if kw.get("resumer_situation"):
            vals["resumer_situation"] = kw.get("resumer_situation")

        if kw.get("solution_pour_regler"):
            vals["solution_pour_regler"] = kw.get("solution_pour_regler")

        new_organization_commentaire = (
            request.env["organization.commentaire"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_commentaire/{new_organization_commentaire.id}"
        )

    @http.route(
        "/new/organization_demande_adhesion",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_demande_adhesion(self, **kw):
        default_active = (
            http.request.env["organization.demande.adhesion"]
            .default_get(["active"])
            .get("active")
        )
        default_courriel = (
            http.request.env["organization.demande.adhesion"]
            .default_get(["courriel"])
            .get("courriel")
        )
        default_date_mise_a_jour = (
            http.request.env["organization.demande.adhesion"]
            .default_get(["date_mise_a_jour"])
            .get("date_mise_a_jour")
        )
        default_en_attente = (
            http.request.env["organization.demande.adhesion"]
            .default_get(["en_attente"])
            .get("en_attente")
        )
        default_nom = (
            http.request.env["organization.demande.adhesion"]
            .default_get(["nom"])
            .get("nom")
        )
        default_nom_complet = (
            http.request.env["organization.demande.adhesion"]
            .default_get(["nom_complet"])
            .get("nom_complet")
        )
        organization = http.request.env["organization.organization"].search(
            [("active", "=", True)]
        )
        default_organization = (
            http.request.env["organization.demande.adhesion"]
            .default_get(["organization"])
            .get("organization")
        )
        default_poste = (
            http.request.env["organization.demande.adhesion"]
            .default_get(["poste"])
            .get("poste")
        )
        default_prenom = (
            http.request.env["organization.demande.adhesion"]
            .default_get(["prenom"])
            .get("prenom")
        )
        default_telephone = (
            http.request.env["organization.demande.adhesion"]
            .default_get(["telephone"])
            .get("telephone")
        )
        default_transferer = (
            http.request.env["organization.demande.adhesion"]
            .default_get(["transferer"])
            .get("transferer")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_demande_adhesion",
            {
                "organization": organization,
                "page_name": "create_organization_demande_adhesion",
                "default_active": default_active,
                "default_courriel": default_courriel,
                "default_date_mise_a_jour": default_date_mise_a_jour,
                "default_en_attente": default_en_attente,
                "default_nom": default_nom,
                "default_nom_complet": default_nom_complet,
                "default_organization": default_organization,
                "default_poste": default_poste,
                "default_prenom": default_prenom,
                "default_telephone": default_telephone,
                "default_transferer": default_transferer,
            },
        )

    @http.route(
        "/submitted/organization_demande_adhesion",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_demande_adhesion(self, **kw):
        vals = {}

        default_active = (
            http.request.env["organization.demande.adhesion"]
            .default_get(["active"])
            .get("active")
        )
        if kw.get("active"):
            vals["active"] = kw.get("active") == "True"
        elif default_active:
            vals["active"] = False

        if kw.get("courriel"):
            vals["courriel"] = kw.get("courriel")

        if kw.get("date_mise_a_jour"):
            vals["date_mise_a_jour"] = kw.get("date_mise_a_jour")

        default_en_attente = (
            http.request.env["organization.demande.adhesion"]
            .default_get(["en_attente"])
            .get("en_attente")
        )
        if kw.get("en_attente"):
            vals["en_attente"] = kw.get("en_attente") == "True"
        elif default_en_attente:
            vals["en_attente"] = False

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        if kw.get("nom_complet"):
            vals["nom_complet"] = kw.get("nom_complet")

        if kw.get("organization") and kw.get("organization").isdigit():
            vals["organization"] = int(kw.get("organization"))

        if kw.get("poste"):
            vals["poste"] = kw.get("poste")

        if kw.get("prenom"):
            vals["prenom"] = kw.get("prenom")

        if kw.get("telephone"):
            vals["telephone"] = kw.get("telephone")

        default_transferer = (
            http.request.env["organization.demande.adhesion"]
            .default_get(["transferer"])
            .get("transferer")
        )
        if kw.get("transferer"):
            vals["transferer"] = kw.get("transferer") == "True"
        elif default_transferer:
            vals["transferer"] = False

        new_organization_demande_adhesion = (
            request.env["organization.demande.adhesion"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_demande_adhesion/{new_organization_demande_adhesion.id}"
        )

    @http.route(
        "/new/organization_demande_service",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_demande_service(self, **kw):
        default_active = (
            http.request.env["organization.demande.service"]
            .default_get(["active"])
            .get("active")
        )
        default_approuver = (
            http.request.env["organization.demande.service"]
            .default_get(["approuver"])
            .get("approuver")
        )
        default_date_debut = (
            http.request.env["organization.demande.service"]
            .default_get(["date_debut"])
            .get("date_debut")
        )
        default_date_fin = (
            http.request.env["organization.demande.service"]
            .default_get(["date_fin"])
            .get("date_fin")
        )
        default_description = (
            http.request.env["organization.demande.service"]
            .default_get(["description"])
            .get("description")
        )
        membre = http.request.env["organization.membre"].search(
            [("active", "=", True)]
        )
        default_membre = (
            http.request.env["organization.demande.service"]
            .default_get(["membre"])
            .get("membre")
        )
        organization = http.request.env["organization.organization"].search(
            [("active", "=", True)]
        )
        default_organization = (
            http.request.env["organization.demande.service"]
            .default_get(["organization"])
            .get("organization")
        )
        default_titre = (
            http.request.env["organization.demande.service"]
            .default_get(["titre"])
            .get("titre")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_demande_service",
            {
                "membre": membre,
                "organization": organization,
                "page_name": "create_organization_demande_service",
                "default_active": default_active,
                "default_approuver": default_approuver,
                "default_date_debut": default_date_debut,
                "default_date_fin": default_date_fin,
                "default_description": default_description,
                "default_membre": default_membre,
                "default_organization": default_organization,
                "default_titre": default_titre,
            },
        )

    @http.route(
        "/submitted/organization_demande_service",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_demande_service(self, **kw):
        vals = {}

        default_active = (
            http.request.env["organization.demande.service"]
            .default_get(["active"])
            .get("active")
        )
        if kw.get("active"):
            vals["active"] = kw.get("active") == "True"
        elif default_active:
            vals["active"] = False

        default_approuver = (
            http.request.env["organization.demande.service"]
            .default_get(["approuver"])
            .get("approuver")
        )
        if kw.get("approuver"):
            vals["approuver"] = kw.get("approuver") == "True"
        elif default_approuver:
            vals["approuver"] = False

        if kw.get("date_debut"):
            vals["date_debut"] = kw.get("date_debut")

        if kw.get("date_fin"):
            vals["date_fin"] = kw.get("date_fin")

        if kw.get("description"):
            vals["description"] = kw.get("description")

        if kw.get("membre") and kw.get("membre").isdigit():
            vals["membre"] = int(kw.get("membre"))

        if kw.get("organization") and kw.get("organization").isdigit():
            vals["organization"] = int(kw.get("organization"))

        if kw.get("titre"):
            vals["titre"] = kw.get("titre")

        new_organization_demande_service = (
            request.env["organization.demande.service"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_demande_service/{new_organization_demande_service.id}"
        )

    @http.route(
        "/new/organization_droits_admin",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_droits_admin(self, **kw):
        default_consulter_etat_compte = (
            http.request.env["organization.droits.admin"]
            .default_get(["consulter_etat_compte"])
            .get("consulter_etat_compte")
        )
        default_consulter_profil = (
            http.request.env["organization.droits.admin"]
            .default_get(["consulter_profil"])
            .get("consulter_profil")
        )
        default_gestion_dmd = (
            http.request.env["organization.droits.admin"]
            .default_get(["gestion_dmd"])
            .get("gestion_dmd")
        )
        default_gestion_fichier = (
            http.request.env["organization.droits.admin"]
            .default_get(["gestion_fichier"])
            .get("gestion_fichier")
        )
        default_gestion_offre = (
            http.request.env["organization.droits.admin"]
            .default_get(["gestion_offre"])
            .get("gestion_offre")
        )
        default_gestion_offre_service = (
            http.request.env["organization.droits.admin"]
            .default_get(["gestion_offre_service"])
            .get("gestion_offre_service")
        )
        default_gestion_profil = (
            http.request.env["organization.droits.admin"]
            .default_get(["gestion_profil"])
            .get("gestion_profil")
        )
        default_gestion_type_service = (
            http.request.env["organization.droits.admin"]
            .default_get(["gestion_type_service"])
            .get("gestion_type_service")
        )
        default_groupe_achat = (
            http.request.env["organization.droits.admin"]
            .default_get(["groupe_achat"])
            .get("groupe_achat")
        )
        membre = http.request.env["organization.membre"].search(
            [("active", "=", True)]
        )
        default_membre = (
            http.request.env["organization.droits.admin"]
            .default_get(["membre"])
            .get("membre")
        )
        default_nom_complet = (
            http.request.env["organization.droits.admin"]
            .default_get(["nom_complet"])
            .get("nom_complet")
        )
        default_saisie_echange = (
            http.request.env["organization.droits.admin"]
            .default_get(["saisie_echange"])
            .get("saisie_echange")
        )
        default_validation = (
            http.request.env["organization.droits.admin"]
            .default_get(["validation"])
            .get("validation")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_droits_admin",
            {
                "membre": membre,
                "page_name": "create_organization_droits_admin",
                "default_consulter_etat_compte": default_consulter_etat_compte,
                "default_consulter_profil": default_consulter_profil,
                "default_gestion_dmd": default_gestion_dmd,
                "default_gestion_fichier": default_gestion_fichier,
                "default_gestion_offre": default_gestion_offre,
                "default_gestion_offre_service": default_gestion_offre_service,
                "default_gestion_profil": default_gestion_profil,
                "default_gestion_type_service": default_gestion_type_service,
                "default_groupe_achat": default_groupe_achat,
                "default_membre": default_membre,
                "default_nom_complet": default_nom_complet,
                "default_saisie_echange": default_saisie_echange,
                "default_validation": default_validation,
            },
        )

    @http.route(
        "/submitted/organization_droits_admin",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_droits_admin(self, **kw):
        vals = {}

        default_consulter_etat_compte = (
            http.request.env["organization.droits.admin"]
            .default_get(["consulter_etat_compte"])
            .get("consulter_etat_compte")
        )
        if kw.get("consulter_etat_compte"):
            vals["consulter_etat_compte"] = (
                kw.get("consulter_etat_compte") == "True"
            )
        elif default_consulter_etat_compte:
            vals["consulter_etat_compte"] = False

        default_consulter_profil = (
            http.request.env["organization.droits.admin"]
            .default_get(["consulter_profil"])
            .get("consulter_profil")
        )
        if kw.get("consulter_profil"):
            vals["consulter_profil"] = kw.get("consulter_profil") == "True"
        elif default_consulter_profil:
            vals["consulter_profil"] = False

        default_gestion_dmd = (
            http.request.env["organization.droits.admin"]
            .default_get(["gestion_dmd"])
            .get("gestion_dmd")
        )
        if kw.get("gestion_dmd"):
            vals["gestion_dmd"] = kw.get("gestion_dmd") == "True"
        elif default_gestion_dmd:
            vals["gestion_dmd"] = False

        default_gestion_fichier = (
            http.request.env["organization.droits.admin"]
            .default_get(["gestion_fichier"])
            .get("gestion_fichier")
        )
        if kw.get("gestion_fichier"):
            vals["gestion_fichier"] = kw.get("gestion_fichier") == "True"
        elif default_gestion_fichier:
            vals["gestion_fichier"] = False

        default_gestion_offre = (
            http.request.env["organization.droits.admin"]
            .default_get(["gestion_offre"])
            .get("gestion_offre")
        )
        if kw.get("gestion_offre"):
            vals["gestion_offre"] = kw.get("gestion_offre") == "True"
        elif default_gestion_offre:
            vals["gestion_offre"] = False

        default_gestion_offre_service = (
            http.request.env["organization.droits.admin"]
            .default_get(["gestion_offre_service"])
            .get("gestion_offre_service")
        )
        if kw.get("gestion_offre_service"):
            vals["gestion_offre_service"] = (
                kw.get("gestion_offre_service") == "True"
            )
        elif default_gestion_offre_service:
            vals["gestion_offre_service"] = False

        default_gestion_profil = (
            http.request.env["organization.droits.admin"]
            .default_get(["gestion_profil"])
            .get("gestion_profil")
        )
        if kw.get("gestion_profil"):
            vals["gestion_profil"] = kw.get("gestion_profil") == "True"
        elif default_gestion_profil:
            vals["gestion_profil"] = False

        default_gestion_type_service = (
            http.request.env["organization.droits.admin"]
            .default_get(["gestion_type_service"])
            .get("gestion_type_service")
        )
        if kw.get("gestion_type_service"):
            vals["gestion_type_service"] = (
                kw.get("gestion_type_service") == "True"
            )
        elif default_gestion_type_service:
            vals["gestion_type_service"] = False

        default_groupe_achat = (
            http.request.env["organization.droits.admin"]
            .default_get(["groupe_achat"])
            .get("groupe_achat")
        )
        if kw.get("groupe_achat"):
            vals["groupe_achat"] = kw.get("groupe_achat") == "True"
        elif default_groupe_achat:
            vals["groupe_achat"] = False

        if kw.get("membre") and kw.get("membre").isdigit():
            vals["membre"] = int(kw.get("membre"))

        if kw.get("nom_complet"):
            vals["nom_complet"] = kw.get("nom_complet")

        default_saisie_echange = (
            http.request.env["organization.droits.admin"]
            .default_get(["saisie_echange"])
            .get("saisie_echange")
        )
        if kw.get("saisie_echange"):
            vals["saisie_echange"] = kw.get("saisie_echange") == "True"
        elif default_saisie_echange:
            vals["saisie_echange"] = False

        default_validation = (
            http.request.env["organization.droits.admin"]
            .default_get(["validation"])
            .get("validation")
        )
        if kw.get("validation"):
            vals["validation"] = kw.get("validation") == "True"
        elif default_validation:
            vals["validation"] = False

        new_organization_droits_admin = (
            request.env["organization.droits.admin"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_droits_admin/{new_organization_droits_admin.id}"
        )

    @http.route(
        "/new/organization_echange_service",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_echange_service(self, **kw):
        default_commentaire = (
            http.request.env["organization.echange.service"]
            .default_get(["commentaire"])
            .get("commentaire")
        )
        default_date_echange = (
            http.request.env["organization.echange.service"]
            .default_get(["date_echange"])
            .get("date_echange")
        )
        demande_service = http.request.env[
            "organization.demande.service"
        ].search([("active", "=", True)])
        default_demande_service = (
            http.request.env["organization.echange.service"]
            .default_get(["demande_service"])
            .get("demande_service")
        )
        membre_acheteur = http.request.env["organization.membre"].search(
            [("active", "=", True)]
        )
        default_membre_acheteur = (
            http.request.env["organization.echange.service"]
            .default_get(["membre_acheteur"])
            .get("membre_acheteur")
        )
        membre_vendeur = http.request.env["organization.membre"].search(
            [("active", "=", True)]
        )
        default_membre_vendeur = (
            http.request.env["organization.echange.service"]
            .default_get(["membre_vendeur"])
            .get("membre_vendeur")
        )
        default_nb_heure = (
            http.request.env["organization.echange.service"]
            .default_get(["nb_heure"])
            .get("nb_heure")
        )
        default_nom_complet = (
            http.request.env["organization.echange.service"]
            .default_get(["nom_complet"])
            .get("nom_complet")
        )
        offre_service = http.request.env["organization.offre.service"].search(
            [("active", "=", True)]
        )
        default_offre_service = (
            http.request.env["organization.echange.service"]
            .default_get(["offre_service"])
            .get("offre_service")
        )
        point_service = http.request.env["organization.point.service"].search(
            []
        )
        default_point_service = (
            http.request.env["organization.echange.service"]
            .default_get(["point_service"])
            .get("point_service")
        )
        default_remarque = (
            http.request.env["organization.echange.service"]
            .default_get(["remarque"])
            .get("remarque")
        )
        type_echange = (
            http.request.env["organization.echange.service"]
            ._fields["type_echange"]
            .selection
        )
        default_type_echange = (
            http.request.env["organization.echange.service"]
            .default_get(["type_echange"])
            .get("type_echange")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_echange_service",
            {
                "demande_service": demande_service,
                "membre_acheteur": membre_acheteur,
                "membre_vendeur": membre_vendeur,
                "offre_service": offre_service,
                "point_service": point_service,
                "type_echange": type_echange,
                "page_name": "create_organization_echange_service",
                "default_commentaire": default_commentaire,
                "default_date_echange": default_date_echange,
                "default_demande_service": default_demande_service,
                "default_membre_acheteur": default_membre_acheteur,
                "default_membre_vendeur": default_membre_vendeur,
                "default_nb_heure": default_nb_heure,
                "default_nom_complet": default_nom_complet,
                "default_offre_service": default_offre_service,
                "default_point_service": default_point_service,
                "default_remarque": default_remarque,
                "default_type_echange": default_type_echange,
            },
        )

    @http.route(
        "/submitted/organization_echange_service",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_echange_service(self, **kw):
        vals = {}

        if kw.get("commentaire"):
            vals["commentaire"] = kw.get("commentaire")

        if kw.get("date_echange"):
            vals["date_echange"] = kw.get("date_echange")

        if kw.get("demande_service") and kw.get("demande_service").isdigit():
            vals["demande_service"] = int(kw.get("demande_service"))

        if kw.get("membre_acheteur") and kw.get("membre_acheteur").isdigit():
            vals["membre_acheteur"] = int(kw.get("membre_acheteur"))

        if kw.get("membre_vendeur") and kw.get("membre_vendeur").isdigit():
            vals["membre_vendeur"] = int(kw.get("membre_vendeur"))

        if kw.get("nb_heure"):
            nb_heure_value = kw.get("nb_heure")
            tpl_time_nb_heure = nb_heure_value.split(":")
            if len(tpl_time_nb_heure) == 1:
                if tpl_time_nb_heure[0].isdigit():
                    vals["nb_heure"] = int(tpl_time_nb_heure[0])
            elif len(tpl_time_nb_heure) == 2:
                if (
                    tpl_time_nb_heure[0].isdigit()
                    and tpl_time_nb_heure[1].isdigit()
                ):
                    vals["nb_heure"] = (
                        int(tpl_time_nb_heure[0])
                        + int(tpl_time_nb_heure[1]) / 60.0
                    )

        if kw.get("nom_complet"):
            vals["nom_complet"] = kw.get("nom_complet")

        if kw.get("offre_service") and kw.get("offre_service").isdigit():
            vals["offre_service"] = int(kw.get("offre_service"))

        if kw.get("point_service") and kw.get("point_service").isdigit():
            vals["point_service"] = int(kw.get("point_service"))

        if kw.get("remarque"):
            vals["remarque"] = kw.get("remarque")

        new_organization_echange_service = (
            request.env["organization.echange.service"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_echange_service/{new_organization_echange_service.id}"
        )

    @http.route(
        "/new/organization_fichier", type="http", auth="user", website=True
    )
    def create_new_organization_fichier(self, **kw):
        default_date_mise_a_jour = (
            http.request.env["organization.fichier"]
            .default_get(["date_mise_a_jour"])
            .get("date_mise_a_jour")
        )
        default_nom = (
            http.request.env["organization.fichier"]
            .default_get(["nom"])
            .get("nom")
        )
        organization = http.request.env["organization.organization"].search(
            [("active", "=", True)]
        )
        default_organization = (
            http.request.env["organization.fichier"]
            .default_get(["organization"])
            .get("organization")
        )
        default_si_admin = (
            http.request.env["organization.fichier"]
            .default_get(["si_admin"])
            .get("si_admin")
        )
        default_si_disponible = (
            http.request.env["organization.fichier"]
            .default_get(["si_disponible"])
            .get("si_disponible")
        )
        default_si_organization_local_seulement = (
            http.request.env["organization.fichier"]
            .default_get(["si_organization_local_seulement"])
            .get("si_organization_local_seulement")
        )
        type_fichier = http.request.env["organization.type.fichier"].search([])
        default_type_fichier = (
            http.request.env["organization.fichier"]
            .default_get(["type_fichier"])
            .get("type_fichier")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_fichier",
            {
                "organization": organization,
                "type_fichier": type_fichier,
                "page_name": "create_organization_fichier",
                "default_date_mise_a_jour": default_date_mise_a_jour,
                "default_nom": default_nom,
                "default_organization": default_organization,
                "default_si_admin": default_si_admin,
                "default_si_disponible": default_si_disponible,
                "default_si_organization_local_seulement": default_si_organization_local_seulement,
                "default_type_fichier": default_type_fichier,
            },
        )

    @http.route(
        "/submitted/organization_fichier",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_fichier(self, **kw):
        vals = {}

        if kw.get("date_mise_a_jour"):
            vals["date_mise_a_jour"] = kw.get("date_mise_a_jour")

        if kw.get("fichier"):
            lst_file_fichier = request.httprequest.files.getlist("fichier")
            if lst_file_fichier:
                vals["fichier"] = base64.b64encode(lst_file_fichier[-1].read())

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        if kw.get("organization") and kw.get("organization").isdigit():
            vals["organization"] = int(kw.get("organization"))

        default_si_admin = (
            http.request.env["organization.fichier"]
            .default_get(["si_admin"])
            .get("si_admin")
        )
        if kw.get("si_admin"):
            vals["si_admin"] = kw.get("si_admin") == "True"
        elif default_si_admin:
            vals["si_admin"] = False

        default_si_disponible = (
            http.request.env["organization.fichier"]
            .default_get(["si_disponible"])
            .get("si_disponible")
        )
        if kw.get("si_disponible"):
            vals["si_disponible"] = kw.get("si_disponible") == "True"
        elif default_si_disponible:
            vals["si_disponible"] = False

        default_si_organization_local_seulement = (
            http.request.env["organization.fichier"]
            .default_get(["si_organization_local_seulement"])
            .get("si_organization_local_seulement")
        )
        if kw.get("si_organization_local_seulement"):
            vals["si_organization_local_seulement"] = (
                kw.get("si_organization_local_seulement") == "True"
            )
        elif default_si_organization_local_seulement:
            vals["si_organization_local_seulement"] = False

        if kw.get("type_fichier") and kw.get("type_fichier").isdigit():
            vals["type_fichier"] = int(kw.get("type_fichier"))

        new_organization_fichier = (
            request.env["organization.fichier"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_fichier/{new_organization_fichier.id}"
        )

    @http.route(
        "/new/organization_membre", type="http", auth="user", website=True
    )
    def create_new_organization_membre(self, **kw):
        default_achat_regrouper = (
            http.request.env["organization.membre"]
            .default_get(["achat_regrouper"])
            .get("achat_regrouper")
        )
        default_active = (
            http.request.env["organization.membre"]
            .default_get(["active"])
            .get("active")
        )
        default_adresse = (
            http.request.env["organization.membre"]
            .default_get(["adresse"])
            .get("adresse")
        )
        default_annee_naissance = (
            http.request.env["organization.membre"]
            .default_get(["annee_naissance"])
            .get("annee_naissance")
        )
        arrondissement = http.request.env[
            "organization.arrondissement"
        ].search([])
        default_arrondissement = (
            http.request.env["organization.membre"]
            .default_get(["arrondissement"])
            .get("arrondissement")
        )
        default_bottin_courriel = (
            http.request.env["organization.membre"]
            .default_get(["bottin_courriel"])
            .get("bottin_courriel")
        )
        default_bottin_tel = (
            http.request.env["organization.membre"]
            .default_get(["bottin_tel"])
            .get("bottin_tel")
        )
        default_codepostal = (
            http.request.env["organization.membre"]
            .default_get(["codepostal"])
            .get("codepostal")
        )
        default_courriel = (
            http.request.env["organization.membre"]
            .default_get(["courriel"])
            .get("courriel")
        )
        default_date_adhesion = (
            http.request.env["organization.membre"]
            .default_get(["date_adhesion"])
            .get("date_adhesion")
        )
        default_date_mise_a_jour = (
            http.request.env["organization.membre"]
            .default_get(["date_mise_a_jour"])
            .get("date_mise_a_jour")
        )
        default_description_membre = (
            http.request.env["organization.membre"]
            .default_get(["description_membre"])
            .get("description_membre")
        )
        default_est_un_point_service = (
            http.request.env["organization.membre"]
            .default_get(["est_un_point_service"])
            .get("est_un_point_service")
        )
        default_membre_ca = (
            http.request.env["organization.membre"]
            .default_get(["membre_ca"])
            .get("membre_ca")
        )
        default_membre_conjoint = (
            http.request.env["organization.membre"]
            .default_get(["membre_conjoint"])
            .get("membre_conjoint")
        )
        default_membre_conjoint_id = (
            http.request.env["organization.membre"]
            .default_get(["membre_conjoint_id"])
            .get("membre_conjoint_id")
        )
        default_membre_principal = (
            http.request.env["organization.membre"]
            .default_get(["membre_principal"])
            .get("membre_principal")
        )
        default_memo = (
            http.request.env["organization.membre"]
            .default_get(["memo"])
            .get("memo")
        )
        default_nom = (
            http.request.env["organization.membre"]
            .default_get(["nom"])
            .get("nom")
        )
        default_nom_complet = (
            http.request.env["organization.membre"]
            .default_get(["nom_complet"])
            .get("nom_complet")
        )
        default_nom_utilisateur = (
            http.request.env["organization.membre"]
            .default_get(["nom_utilisateur"])
            .get("nom_utilisateur")
        )
        occupation = http.request.env["organization.occupation"].search([])
        default_occupation = (
            http.request.env["organization.membre"]
            .default_get(["occupation"])
            .get("occupation")
        )
        organization = http.request.env["organization.organization"].search(
            [("active", "=", True)]
        )
        default_organization = (
            http.request.env["organization.membre"]
            .default_get(["organization"])
            .get("organization")
        )
        origine = http.request.env["organization.origine"].search([])
        default_origine = (
            http.request.env["organization.membre"]
            .default_get(["origine"])
            .get("origine")
        )
        default_part_social_paye = (
            http.request.env["organization.membre"]
            .default_get(["part_social_paye"])
            .get("part_social_paye")
        )
        default_pas_communication = (
            http.request.env["organization.membre"]
            .default_get(["pas_communication"])
            .get("pas_communication")
        )
        point_service = http.request.env["organization.point.service"].search(
            []
        )
        default_point_service = (
            http.request.env["organization.membre"]
            .default_get(["point_service"])
            .get("point_service")
        )
        default_prenom = (
            http.request.env["organization.membre"]
            .default_get(["prenom"])
            .get("prenom")
        )
        default_pret_actif = (
            http.request.env["organization.membre"]
            .default_get(["pret_actif"])
            .get("pret_actif")
        )
        default_profil_approuver = (
            http.request.env["organization.membre"]
            .default_get(["profil_approuver"])
            .get("profil_approuver")
        )
        provenance = http.request.env["organization.provenance"].search([])
        default_provenance = (
            http.request.env["organization.membre"]
            .default_get(["provenance"])
            .get("provenance")
        )
        quartier = http.request.env["organization.quartier"].search([])
        default_quartier = (
            http.request.env["organization.membre"]
            .default_get(["quartier"])
            .get("quartier")
        )
        default_recevoir_courriel_groupe = (
            http.request.env["organization.membre"]
            .default_get(["recevoir_courriel_groupe"])
            .get("recevoir_courriel_groupe")
        )
        region = http.request.env["organization.region"].search([])
        default_region = (
            http.request.env["organization.membre"]
            .default_get(["region"])
            .get("region")
        )
        revenu_familial = http.request.env[
            "organization.revenu.familial"
        ].search([])
        default_revenu_familial = (
            http.request.env["organization.membre"]
            .default_get(["revenu_familial"])
            .get("revenu_familial")
        )
        sexe = (
            http.request.env["organization.membre"]._fields["sexe"].selection
        )
        default_sexe = (
            http.request.env["organization.membre"]
            .default_get(["sexe"])
            .get("sexe")
        )
        situation_maison = http.request.env[
            "organization.situation.maison"
        ].search([])
        default_situation_maison = (
            http.request.env["organization.membre"]
            .default_get(["situation_maison"])
            .get("situation_maison")
        )
        default_telephone_1 = (
            http.request.env["organization.membre"]
            .default_get(["telephone_1"])
            .get("telephone_1")
        )
        default_telephone_2 = (
            http.request.env["organization.membre"]
            .default_get(["telephone_2"])
            .get("telephone_2")
        )
        default_telephone_3 = (
            http.request.env["organization.membre"]
            .default_get(["telephone_3"])
            .get("telephone_3")
        )
        default_telephone_poste_1 = (
            http.request.env["organization.membre"]
            .default_get(["telephone_poste_1"])
            .get("telephone_poste_1")
        )
        default_telephone_poste_2 = (
            http.request.env["organization.membre"]
            .default_get(["telephone_poste_2"])
            .get("telephone_poste_2")
        )
        default_telephone_poste_3 = (
            http.request.env["organization.membre"]
            .default_get(["telephone_poste_3"])
            .get("telephone_poste_3")
        )
        telephone_type_1 = http.request.env[
            "organization.type.telephone"
        ].search([])
        default_telephone_type_1 = (
            http.request.env["organization.membre"]
            .default_get(["telephone_type_1"])
            .get("telephone_type_1")
        )
        telephone_type_2 = http.request.env[
            "organization.type.telephone"
        ].search([])
        default_telephone_type_2 = (
            http.request.env["organization.membre"]
            .default_get(["telephone_type_2"])
            .get("telephone_type_2")
        )
        telephone_type_3 = http.request.env[
            "organization.type.telephone"
        ].search([])
        default_telephone_type_3 = (
            http.request.env["organization.membre"]
            .default_get(["telephone_type_3"])
            .get("telephone_type_3")
        )
        transfert_organization = http.request.env[
            "organization.organization"
        ].search([("active", "=", True)])
        default_transfert_organization = (
            http.request.env["organization.membre"]
            .default_get(["transfert_organization"])
            .get("transfert_organization")
        )
        type_communication = http.request.env[
            "organization.type.communication"
        ].search([])
        default_type_communication = (
            http.request.env["organization.membre"]
            .default_get(["type_communication"])
            .get("type_communication")
        )
        ville = http.request.env["organization.ville"].search([])
        default_ville = (
            http.request.env["organization.membre"]
            .default_get(["ville"])
            .get("ville")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_membre",
            {
                "arrondissement": arrondissement,
                "occupation": occupation,
                "organization": organization,
                "origine": origine,
                "point_service": point_service,
                "provenance": provenance,
                "quartier": quartier,
                "region": region,
                "revenu_familial": revenu_familial,
                "sexe": sexe,
                "situation_maison": situation_maison,
                "telephone_type_1": telephone_type_1,
                "telephone_type_2": telephone_type_2,
                "telephone_type_3": telephone_type_3,
                "transfert_organization": transfert_organization,
                "type_communication": type_communication,
                "ville": ville,
                "page_name": "create_organization_membre",
                "default_achat_regrouper": default_achat_regrouper,
                "default_active": default_active,
                "default_adresse": default_adresse,
                "default_annee_naissance": default_annee_naissance,
                "default_arrondissement": default_arrondissement,
                "default_bottin_courriel": default_bottin_courriel,
                "default_bottin_tel": default_bottin_tel,
                "default_codepostal": default_codepostal,
                "default_courriel": default_courriel,
                "default_date_adhesion": default_date_adhesion,
                "default_date_mise_a_jour": default_date_mise_a_jour,
                "default_description_membre": default_description_membre,
                "default_est_un_point_service": default_est_un_point_service,
                "default_membre_ca": default_membre_ca,
                "default_membre_conjoint": default_membre_conjoint,
                "default_membre_conjoint_id": default_membre_conjoint_id,
                "default_membre_principal": default_membre_principal,
                "default_memo": default_memo,
                "default_nom": default_nom,
                "default_nom_complet": default_nom_complet,
                "default_nom_utilisateur": default_nom_utilisateur,
                "default_occupation": default_occupation,
                "default_organization": default_organization,
                "default_origine": default_origine,
                "default_part_social_paye": default_part_social_paye,
                "default_pas_communication": default_pas_communication,
                "default_point_service": default_point_service,
                "default_prenom": default_prenom,
                "default_pret_actif": default_pret_actif,
                "default_profil_approuver": default_profil_approuver,
                "default_provenance": default_provenance,
                "default_quartier": default_quartier,
                "default_recevoir_courriel_groupe": default_recevoir_courriel_groupe,
                "default_region": default_region,
                "default_revenu_familial": default_revenu_familial,
                "default_sexe": default_sexe,
                "default_situation_maison": default_situation_maison,
                "default_telephone_1": default_telephone_1,
                "default_telephone_2": default_telephone_2,
                "default_telephone_3": default_telephone_3,
                "default_telephone_poste_1": default_telephone_poste_1,
                "default_telephone_poste_2": default_telephone_poste_2,
                "default_telephone_poste_3": default_telephone_poste_3,
                "default_telephone_type_1": default_telephone_type_1,
                "default_telephone_type_2": default_telephone_type_2,
                "default_telephone_type_3": default_telephone_type_3,
                "default_transfert_organization": default_transfert_organization,
                "default_type_communication": default_type_communication,
                "default_ville": default_ville,
            },
        )

    @http.route(
        "/submitted/organization_membre",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_membre(self, **kw):
        vals = {}

        default_achat_regrouper = (
            http.request.env["organization.membre"]
            .default_get(["achat_regrouper"])
            .get("achat_regrouper")
        )
        if kw.get("achat_regrouper"):
            vals["achat_regrouper"] = kw.get("achat_regrouper") == "True"
        elif default_achat_regrouper:
            vals["achat_regrouper"] = False

        default_active = (
            http.request.env["organization.membre"]
            .default_get(["active"])
            .get("active")
        )
        if kw.get("active"):
            vals["active"] = kw.get("active") == "True"
        elif default_active:
            vals["active"] = False

        if kw.get("adresse"):
            vals["adresse"] = kw.get("adresse")

        if kw.get("annee_naissance"):
            annee_naissance_value = kw.get("annee_naissance")
            if annee_naissance_value.isdigit():
                vals["annee_naissance"] = int(annee_naissance_value)

        if kw.get("arrondissement") and kw.get("arrondissement").isdigit():
            vals["arrondissement"] = int(kw.get("arrondissement"))

        default_bottin_courriel = (
            http.request.env["organization.membre"]
            .default_get(["bottin_courriel"])
            .get("bottin_courriel")
        )
        if kw.get("bottin_courriel"):
            vals["bottin_courriel"] = kw.get("bottin_courriel") == "True"
        elif default_bottin_courriel:
            vals["bottin_courriel"] = False

        default_bottin_tel = (
            http.request.env["organization.membre"]
            .default_get(["bottin_tel"])
            .get("bottin_tel")
        )
        if kw.get("bottin_tel"):
            vals["bottin_tel"] = kw.get("bottin_tel") == "True"
        elif default_bottin_tel:
            vals["bottin_tel"] = False

        if kw.get("codepostal"):
            vals["codepostal"] = kw.get("codepostal")

        if kw.get("courriel"):
            vals["courriel"] = kw.get("courriel")

        if kw.get("date_adhesion"):
            vals["date_adhesion"] = kw.get("date_adhesion")

        if kw.get("date_mise_a_jour"):
            vals["date_mise_a_jour"] = kw.get("date_mise_a_jour")

        default_description_membre = (
            http.request.env["organization.membre"]
            .default_get(["description_membre"])
            .get("description_membre")
        )
        if kw.get("description_membre"):
            vals["description_membre"] = kw.get("description_membre") == "True"
        elif default_description_membre:
            vals["description_membre"] = False

        default_est_un_point_service = (
            http.request.env["organization.membre"]
            .default_get(["est_un_point_service"])
            .get("est_un_point_service")
        )
        if kw.get("est_un_point_service"):
            vals["est_un_point_service"] = (
                kw.get("est_un_point_service") == "True"
            )
        elif default_est_un_point_service:
            vals["est_un_point_service"] = False

        default_membre_ca = (
            http.request.env["organization.membre"]
            .default_get(["membre_ca"])
            .get("membre_ca")
        )
        if kw.get("membre_ca"):
            vals["membre_ca"] = kw.get("membre_ca") == "True"
        elif default_membre_ca:
            vals["membre_ca"] = False

        default_membre_conjoint = (
            http.request.env["organization.membre"]
            .default_get(["membre_conjoint"])
            .get("membre_conjoint")
        )
        if kw.get("membre_conjoint"):
            vals["membre_conjoint"] = kw.get("membre_conjoint") == "True"
        elif default_membre_conjoint:
            vals["membre_conjoint"] = False

        if kw.get("membre_conjoint_id"):
            membre_conjoint_id_value = kw.get("membre_conjoint_id")
            if membre_conjoint_id_value.isdigit():
                vals["membre_conjoint_id"] = int(membre_conjoint_id_value)

        default_membre_principal = (
            http.request.env["organization.membre"]
            .default_get(["membre_principal"])
            .get("membre_principal")
        )
        if kw.get("membre_principal"):
            vals["membre_principal"] = kw.get("membre_principal") == "True"
        elif default_membre_principal:
            vals["membre_principal"] = False

        if kw.get("memo"):
            vals["memo"] = kw.get("memo")

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        if kw.get("nom_complet"):
            vals["nom_complet"] = kw.get("nom_complet")

        if kw.get("nom_utilisateur"):
            vals["nom_utilisateur"] = kw.get("nom_utilisateur")

        if kw.get("occupation") and kw.get("occupation").isdigit():
            vals["occupation"] = int(kw.get("occupation"))

        if kw.get("organization") and kw.get("organization").isdigit():
            vals["organization"] = int(kw.get("organization"))

        if kw.get("origine") and kw.get("origine").isdigit():
            vals["origine"] = int(kw.get("origine"))

        default_part_social_paye = (
            http.request.env["organization.membre"]
            .default_get(["part_social_paye"])
            .get("part_social_paye")
        )
        if kw.get("part_social_paye"):
            vals["part_social_paye"] = kw.get("part_social_paye") == "True"
        elif default_part_social_paye:
            vals["part_social_paye"] = False

        default_pas_communication = (
            http.request.env["organization.membre"]
            .default_get(["pas_communication"])
            .get("pas_communication")
        )
        if kw.get("pas_communication"):
            vals["pas_communication"] = kw.get("pas_communication") == "True"
        elif default_pas_communication:
            vals["pas_communication"] = False

        if kw.get("point_service") and kw.get("point_service").isdigit():
            vals["point_service"] = int(kw.get("point_service"))

        if kw.get("prenom"):
            vals["prenom"] = kw.get("prenom")

        default_pret_actif = (
            http.request.env["organization.membre"]
            .default_get(["pret_actif"])
            .get("pret_actif")
        )
        if kw.get("pret_actif"):
            vals["pret_actif"] = kw.get("pret_actif") == "True"
        elif default_pret_actif:
            vals["pret_actif"] = False

        default_profil_approuver = (
            http.request.env["organization.membre"]
            .default_get(["profil_approuver"])
            .get("profil_approuver")
        )
        if kw.get("profil_approuver"):
            vals["profil_approuver"] = kw.get("profil_approuver") == "True"
        elif default_profil_approuver:
            vals["profil_approuver"] = False

        if kw.get("provenance") and kw.get("provenance").isdigit():
            vals["provenance"] = int(kw.get("provenance"))

        if kw.get("quartier") and kw.get("quartier").isdigit():
            vals["quartier"] = int(kw.get("quartier"))

        default_recevoir_courriel_groupe = (
            http.request.env["organization.membre"]
            .default_get(["recevoir_courriel_groupe"])
            .get("recevoir_courriel_groupe")
        )
        if kw.get("recevoir_courriel_groupe"):
            vals["recevoir_courriel_groupe"] = (
                kw.get("recevoir_courriel_groupe") == "True"
            )
        elif default_recevoir_courriel_groupe:
            vals["recevoir_courriel_groupe"] = False

        if kw.get("region") and kw.get("region").isdigit():
            vals["region"] = int(kw.get("region"))

        if kw.get("revenu_familial") and kw.get("revenu_familial").isdigit():
            vals["revenu_familial"] = int(kw.get("revenu_familial"))

        if kw.get("situation_maison") and kw.get("situation_maison").isdigit():
            vals["situation_maison"] = int(kw.get("situation_maison"))

        if kw.get("telephone_1"):
            vals["telephone_1"] = kw.get("telephone_1")

        if kw.get("telephone_2"):
            vals["telephone_2"] = kw.get("telephone_2")

        if kw.get("telephone_3"):
            vals["telephone_3"] = kw.get("telephone_3")

        if kw.get("telephone_poste_1"):
            vals["telephone_poste_1"] = kw.get("telephone_poste_1")

        if kw.get("telephone_poste_2"):
            vals["telephone_poste_2"] = kw.get("telephone_poste_2")

        if kw.get("telephone_poste_3"):
            vals["telephone_poste_3"] = kw.get("telephone_poste_3")

        if kw.get("telephone_type_1") and kw.get("telephone_type_1").isdigit():
            vals["telephone_type_1"] = int(kw.get("telephone_type_1"))

        if kw.get("telephone_type_2") and kw.get("telephone_type_2").isdigit():
            vals["telephone_type_2"] = int(kw.get("telephone_type_2"))

        if kw.get("telephone_type_3") and kw.get("telephone_type_3").isdigit():
            vals["telephone_type_3"] = int(kw.get("telephone_type_3"))

        if (
            kw.get("transfert_organization")
            and kw.get("transfert_organization").isdigit()
        ):
            vals["transfert_organization"] = int(
                kw.get("transfert_organization")
            )

        if (
            kw.get("type_communication")
            and kw.get("type_communication").isdigit()
        ):
            vals["type_communication"] = int(kw.get("type_communication"))

        if kw.get("ville") and kw.get("ville").isdigit():
            vals["ville"] = int(kw.get("ville"))

        new_organization_membre = (
            request.env["organization.membre"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_membre/{new_organization_membre.id}"
        )

    @http.route(
        "/new/organization_occupation", type="http", auth="user", website=True
    )
    def create_new_organization_occupation(self, **kw):
        default_nom = (
            http.request.env["organization.occupation"]
            .default_get(["nom"])
            .get("nom")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_occupation",
            {
                "page_name": "create_organization_occupation",
                "default_nom": default_nom,
            },
        )

    @http.route(
        "/submitted/organization_occupation",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_occupation(self, **kw):
        vals = {}

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        new_organization_occupation = (
            request.env["organization.occupation"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_occupation/{new_organization_occupation.id}"
        )

    @http.route(
        "/new/organization_offre_service",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_offre_service(self, **kw):
        default_accompli = (
            http.request.env["organization.offre.service"]
            .default_get(["accompli"])
            .get("accompli")
        )
        default_active = (
            http.request.env["organization.offre.service"]
            .default_get(["active"])
            .get("active")
        )
        default_approuve = (
            http.request.env["organization.offre.service"]
            .default_get(["approuve"])
            .get("approuve")
        )
        default_condition = (
            http.request.env["organization.offre.service"]
            .default_get(["condition"])
            .get("condition")
        )
        default_condition_autre = (
            http.request.env["organization.offre.service"]
            .default_get(["condition_autre"])
            .get("condition_autre")
        )
        default_date_affichage = (
            http.request.env["organization.offre.service"]
            .default_get(["date_affichage"])
            .get("date_affichage")
        )
        default_date_debut = (
            http.request.env["organization.offre.service"]
            .default_get(["date_debut"])
            .get("date_debut")
        )
        default_date_fin = (
            http.request.env["organization.offre.service"]
            .default_get(["date_fin"])
            .get("date_fin")
        )
        default_date_mise_a_jour = (
            http.request.env["organization.offre.service"]
            .default_get(["date_mise_a_jour"])
            .get("date_mise_a_jour")
        )
        default_description = (
            http.request.env["organization.offre.service"]
            .default_get(["description"])
            .get("description")
        )
        default_disponibilite = (
            http.request.env["organization.offre.service"]
            .default_get(["disponibilite"])
            .get("disponibilite")
        )
        membre = http.request.env["organization.membre"].search(
            [("active", "=", True)]
        )
        default_membre = (
            http.request.env["organization.offre.service"]
            .default_get(["membre"])
            .get("membre")
        )
        default_nb_consultation = (
            http.request.env["organization.offre.service"]
            .default_get(["nb_consultation"])
            .get("nb_consultation")
        )
        default_nom_offre_special = (
            http.request.env["organization.offre.service"]
            .default_get(["nom_offre_special"])
            .get("nom_offre_special")
        )
        default_offre_special = (
            http.request.env["organization.offre.service"]
            .default_get(["offre_special"])
            .get("offre_special")
        )
        organization = http.request.env["organization.organization"].search(
            [("active", "=", True)]
        )
        default_organization = (
            http.request.env["organization.offre.service"]
            .default_get(["organization"])
            .get("organization")
        )
        default_tarif = (
            http.request.env["organization.offre.service"]
            .default_get(["tarif"])
            .get("tarif")
        )
        type_service_id = http.request.env["organization.type.service"].search(
            [("active", "=", True)]
        )
        default_type_service_id = (
            http.request.env["organization.offre.service"]
            .default_get(["type_service_id"])
            .get("type_service_id")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_offre_service",
            {
                "membre": membre,
                "organization": organization,
                "type_service_id": type_service_id,
                "page_name": "create_organization_offre_service",
                "default_accompli": default_accompli,
                "default_active": default_active,
                "default_approuve": default_approuve,
                "default_condition": default_condition,
                "default_condition_autre": default_condition_autre,
                "default_date_affichage": default_date_affichage,
                "default_date_debut": default_date_debut,
                "default_date_fin": default_date_fin,
                "default_date_mise_a_jour": default_date_mise_a_jour,
                "default_description": default_description,
                "default_disponibilite": default_disponibilite,
                "default_membre": default_membre,
                "default_nb_consultation": default_nb_consultation,
                "default_nom_offre_special": default_nom_offre_special,
                "default_offre_special": default_offre_special,
                "default_organization": default_organization,
                "default_tarif": default_tarif,
                "default_type_service_id": default_type_service_id,
            },
        )

    @http.route(
        "/submitted/organization_offre_service",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_offre_service(self, **kw):
        vals = {}

        default_accompli = (
            http.request.env["organization.offre.service"]
            .default_get(["accompli"])
            .get("accompli")
        )
        if kw.get("accompli"):
            vals["accompli"] = kw.get("accompli") == "True"
        elif default_accompli:
            vals["accompli"] = False

        default_active = (
            http.request.env["organization.offre.service"]
            .default_get(["active"])
            .get("active")
        )
        if kw.get("active"):
            vals["active"] = kw.get("active") == "True"
        elif default_active:
            vals["active"] = False

        default_approuve = (
            http.request.env["organization.offre.service"]
            .default_get(["approuve"])
            .get("approuve")
        )
        if kw.get("approuve"):
            vals["approuve"] = kw.get("approuve") == "True"
        elif default_approuve:
            vals["approuve"] = False

        if kw.get("condition"):
            vals["condition"] = kw.get("condition")

        if kw.get("condition_autre"):
            vals["condition_autre"] = kw.get("condition_autre")

        if kw.get("date_affichage"):
            vals["date_affichage"] = kw.get("date_affichage")

        if kw.get("date_debut"):
            vals["date_debut"] = kw.get("date_debut")

        if kw.get("date_fin"):
            vals["date_fin"] = kw.get("date_fin")

        if kw.get("date_mise_a_jour"):
            vals["date_mise_a_jour"] = kw.get("date_mise_a_jour")

        if kw.get("description"):
            vals["description"] = kw.get("description")

        if kw.get("disponibilite"):
            vals["disponibilite"] = kw.get("disponibilite")

        if kw.get("membre") and kw.get("membre").isdigit():
            vals["membre"] = int(kw.get("membre"))

        if kw.get("nb_consultation"):
            nb_consultation_value = kw.get("nb_consultation")
            if nb_consultation_value.isdigit():
                vals["nb_consultation"] = int(nb_consultation_value)

        if kw.get("nom_offre_special"):
            vals["nom_offre_special"] = kw.get("nom_offre_special")

        default_offre_special = (
            http.request.env["organization.offre.service"]
            .default_get(["offre_special"])
            .get("offre_special")
        )
        if kw.get("offre_special"):
            vals["offre_special"] = kw.get("offre_special") == "True"
        elif default_offre_special:
            vals["offre_special"] = False

        if kw.get("organization") and kw.get("organization").isdigit():
            vals["organization"] = int(kw.get("organization"))

        if kw.get("tarif"):
            vals["tarif"] = kw.get("tarif")

        if kw.get("type_service_id") and kw.get("type_service_id").isdigit():
            vals["type_service_id"] = int(kw.get("type_service_id"))

        new_organization_offre_service = (
            request.env["organization.offre.service"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_offre_service/{new_organization_offre_service.id}"
        )

    @http.route(
        "/new/organization_organization",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_organization(self, **kw):
        default_active = (
            http.request.env["organization.organization"]
            .default_get(["active"])
            .get("active")
        )
        default_adresse = (
            http.request.env["organization.organization"]
            .default_get(["adresse"])
            .get("adresse")
        )
        arrondissement = http.request.env[
            "organization.arrondissement"
        ].search([])
        default_arrondissement = (
            http.request.env["organization.organization"]
            .default_get(["arrondissement"])
            .get("arrondissement")
        )
        default_code_postal = (
            http.request.env["organization.organization"]
            .default_get(["code_postal"])
            .get("code_postal")
        )
        default_courriel = (
            http.request.env["organization.organization"]
            .default_get(["courriel"])
            .get("courriel")
        )
        default_date_mise_a_jour = (
            http.request.env["organization.organization"]
            .default_get(["date_mise_a_jour"])
            .get("date_mise_a_jour")
        )
        default_grp_achat_administrateur = (
            http.request.env["organization.organization"]
            .default_get(["grp_achat_administrateur"])
            .get("grp_achat_administrateur")
        )
        default_grp_achat_membre = (
            http.request.env["organization.organization"]
            .default_get(["grp_achat_membre"])
            .get("grp_achat_membre")
        )
        default_message_accueil = (
            http.request.env["organization.organization"]
            .default_get(["message_accueil"])
            .get("message_accueil")
        )
        default_message_grp_achat = (
            http.request.env["organization.organization"]
            .default_get(["message_grp_achat"])
            .get("message_grp_achat")
        )
        default_nom = (
            http.request.env["organization.organization"]
            .default_get(["nom"])
            .get("nom")
        )
        region = http.request.env["organization.region"].search([])
        default_region = (
            http.request.env["organization.organization"]
            .default_get(["region"])
            .get("region")
        )
        default_telecopieur = (
            http.request.env["organization.organization"]
            .default_get(["telecopieur"])
            .get("telecopieur")
        )
        default_telephone = (
            http.request.env["organization.organization"]
            .default_get(["telephone"])
            .get("telephone")
        )
        default_url_public = (
            http.request.env["organization.organization"]
            .default_get(["url_public"])
            .get("url_public")
        )
        default_url_transactionnel = (
            http.request.env["organization.organization"]
            .default_get(["url_transactionnel"])
            .get("url_transactionnel")
        )
        ville = http.request.env["organization.ville"].search([])
        default_ville = (
            http.request.env["organization.organization"]
            .default_get(["ville"])
            .get("ville")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_organization",
            {
                "arrondissement": arrondissement,
                "region": region,
                "ville": ville,
                "page_name": "create_organization_organization",
                "default_active": default_active,
                "default_adresse": default_adresse,
                "default_arrondissement": default_arrondissement,
                "default_code_postal": default_code_postal,
                "default_courriel": default_courriel,
                "default_date_mise_a_jour": default_date_mise_a_jour,
                "default_grp_achat_administrateur": default_grp_achat_administrateur,
                "default_grp_achat_membre": default_grp_achat_membre,
                "default_message_accueil": default_message_accueil,
                "default_message_grp_achat": default_message_grp_achat,
                "default_nom": default_nom,
                "default_region": default_region,
                "default_telecopieur": default_telecopieur,
                "default_telephone": default_telephone,
                "default_url_public": default_url_public,
                "default_url_transactionnel": default_url_transactionnel,
                "default_ville": default_ville,
            },
        )

    @http.route(
        "/submitted/organization_organization",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_organization(self, **kw):
        vals = {}

        default_active = (
            http.request.env["organization.organization"]
            .default_get(["active"])
            .get("active")
        )
        if kw.get("active"):
            vals["active"] = kw.get("active") == "True"
        elif default_active:
            vals["active"] = False

        if kw.get("adresse"):
            vals["adresse"] = kw.get("adresse")

        if kw.get("arrondissement") and kw.get("arrondissement").isdigit():
            vals["arrondissement"] = int(kw.get("arrondissement"))

        if kw.get("code_postal"):
            vals["code_postal"] = kw.get("code_postal")

        if kw.get("courriel"):
            vals["courriel"] = kw.get("courriel")

        if kw.get("date_mise_a_jour"):
            vals["date_mise_a_jour"] = kw.get("date_mise_a_jour")

        default_grp_achat_administrateur = (
            http.request.env["organization.organization"]
            .default_get(["grp_achat_administrateur"])
            .get("grp_achat_administrateur")
        )
        if kw.get("grp_achat_administrateur"):
            vals["grp_achat_administrateur"] = (
                kw.get("grp_achat_administrateur") == "True"
            )
        elif default_grp_achat_administrateur:
            vals["grp_achat_administrateur"] = False

        default_grp_achat_membre = (
            http.request.env["organization.organization"]
            .default_get(["grp_achat_membre"])
            .get("grp_achat_membre")
        )
        if kw.get("grp_achat_membre"):
            vals["grp_achat_membre"] = kw.get("grp_achat_membre") == "True"
        elif default_grp_achat_membre:
            vals["grp_achat_membre"] = False

        if kw.get("logo"):
            lst_file_logo = request.httprequest.files.getlist("logo")
            if lst_file_logo:
                vals["logo"] = base64.b64encode(lst_file_logo[-1].read())

        if kw.get("message_accueil"):
            vals["message_accueil"] = kw.get("message_accueil")

        if kw.get("message_grp_achat"):
            vals["message_grp_achat"] = kw.get("message_grp_achat")

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        if kw.get("region") and kw.get("region").isdigit():
            vals["region"] = int(kw.get("region"))

        if kw.get("telecopieur"):
            vals["telecopieur"] = kw.get("telecopieur")

        if kw.get("telephone"):
            vals["telephone"] = kw.get("telephone")

        if kw.get("url_public"):
            vals["url_public"] = kw.get("url_public")

        if kw.get("url_transactionnel"):
            vals["url_transactionnel"] = kw.get("url_transactionnel")

        if kw.get("ville") and kw.get("ville").isdigit():
            vals["ville"] = int(kw.get("ville"))

        new_organization_organization = (
            request.env["organization.organization"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_organization/{new_organization_organization.id}"
        )

    @http.route(
        "/new/organization_origine", type="http", auth="user", website=True
    )
    def create_new_organization_origine(self, **kw):
        default_nom = (
            http.request.env["organization.origine"]
            .default_get(["nom"])
            .get("nom")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_origine",
            {
                "page_name": "create_organization_origine",
                "default_nom": default_nom,
            },
        )

    @http.route(
        "/submitted/organization_origine",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_origine(self, **kw):
        vals = {}

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        new_organization_origine = (
            request.env["organization.origine"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_origine/{new_organization_origine.id}"
        )

    @http.route(
        "/new/organization_point_service",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_point_service(self, **kw):
        default_date_mise_a_jour = (
            http.request.env["organization.point.service"]
            .default_get(["date_mise_a_jour"])
            .get("date_mise_a_jour")
        )
        default_nom = (
            http.request.env["organization.point.service"]
            .default_get(["nom"])
            .get("nom")
        )
        organization = http.request.env["organization.organization"].search(
            [("active", "=", True)]
        )
        default_organization = (
            http.request.env["organization.point.service"]
            .default_get(["organization"])
            .get("organization")
        )
        default_sequence = (
            http.request.env["organization.point.service"]
            .default_get(["sequence"])
            .get("sequence")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_point_service",
            {
                "organization": organization,
                "page_name": "create_organization_point_service",
                "default_date_mise_a_jour": default_date_mise_a_jour,
                "default_nom": default_nom,
                "default_organization": default_organization,
                "default_sequence": default_sequence,
            },
        )

    @http.route(
        "/submitted/organization_point_service",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_point_service(self, **kw):
        vals = {}

        if kw.get("date_mise_a_jour"):
            vals["date_mise_a_jour"] = kw.get("date_mise_a_jour")

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        if kw.get("organization") and kw.get("organization").isdigit():
            vals["organization"] = int(kw.get("organization"))

        if kw.get("sequence"):
            sequence_value = kw.get("sequence")
            if sequence_value.isdigit():
                vals["sequence"] = int(sequence_value)

        new_organization_point_service = (
            request.env["organization.point.service"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_point_service/{new_organization_point_service.id}"
        )

    @http.route(
        "/new/organization_provenance", type="http", auth="user", website=True
    )
    def create_new_organization_provenance(self, **kw):
        default_nom = (
            http.request.env["organization.provenance"]
            .default_get(["nom"])
            .get("nom")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_provenance",
            {
                "page_name": "create_organization_provenance",
                "default_nom": default_nom,
            },
        )

    @http.route(
        "/submitted/organization_provenance",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_provenance(self, **kw):
        vals = {}

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        new_organization_provenance = (
            request.env["organization.provenance"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_provenance/{new_organization_provenance.id}"
        )

    @http.route(
        "/new/organization_quartier", type="http", auth="user", website=True
    )
    def create_new_organization_quartier(self, **kw):
        arrondissement = http.request.env[
            "organization.arrondissement"
        ].search([])
        default_arrondissement = (
            http.request.env["organization.quartier"]
            .default_get(["arrondissement"])
            .get("arrondissement")
        )
        default_nom = (
            http.request.env["organization.quartier"]
            .default_get(["nom"])
            .get("nom")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_quartier",
            {
                "arrondissement": arrondissement,
                "page_name": "create_organization_quartier",
                "default_arrondissement": default_arrondissement,
                "default_nom": default_nom,
            },
        )

    @http.route(
        "/submitted/organization_quartier",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_quartier(self, **kw):
        vals = {}

        if kw.get("arrondissement") and kw.get("arrondissement").isdigit():
            vals["arrondissement"] = int(kw.get("arrondissement"))

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        new_organization_quartier = (
            request.env["organization.quartier"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_quartier/{new_organization_quartier.id}"
        )

    @http.route(
        "/new/organization_region", type="http", auth="user", website=True
    )
    def create_new_organization_region(self, **kw):
        default_code = (
            http.request.env["organization.region"]
            .default_get(["code"])
            .get("code")
        )
        default_nom = (
            http.request.env["organization.region"]
            .default_get(["nom"])
            .get("nom")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_region",
            {
                "page_name": "create_organization_region",
                "default_code": default_code,
                "default_nom": default_nom,
            },
        )

    @http.route(
        "/submitted/organization_region",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_region(self, **kw):
        vals = {}

        if kw.get("code"):
            code_value = kw.get("code")
            if code_value.isdigit():
                vals["code"] = int(code_value)

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        new_organization_region = (
            request.env["organization.region"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_region/{new_organization_region.id}"
        )

    @http.route(
        "/new/organization_revenu_familial",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_revenu_familial(self, **kw):
        default_nom = (
            http.request.env["organization.revenu.familial"]
            .default_get(["nom"])
            .get("nom")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_revenu_familial",
            {
                "page_name": "create_organization_revenu_familial",
                "default_nom": default_nom,
            },
        )

    @http.route(
        "/submitted/organization_revenu_familial",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_revenu_familial(self, **kw):
        vals = {}

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        new_organization_revenu_familial = (
            request.env["organization.revenu.familial"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_revenu_familial/{new_organization_revenu_familial.id}"
        )

    @http.route(
        "/new/organization_situation_maison",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_situation_maison(self, **kw):
        default_nom = (
            http.request.env["organization.situation.maison"]
            .default_get(["nom"])
            .get("nom")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_situation_maison",
            {
                "page_name": "create_organization_situation_maison",
                "default_nom": default_nom,
            },
        )

    @http.route(
        "/submitted/organization_situation_maison",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_situation_maison(self, **kw):
        vals = {}

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        new_organization_situation_maison = (
            request.env["organization.situation.maison"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_situation_maison/{new_organization_situation_maison.id}"
        )

    @http.route(
        "/new/organization_type_communication",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_type_communication(self, **kw):
        default_nom = (
            http.request.env["organization.type.communication"]
            .default_get(["nom"])
            .get("nom")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_type_communication",
            {
                "page_name": "create_organization_type_communication",
                "default_nom": default_nom,
            },
        )

    @http.route(
        "/submitted/organization_type_communication",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_type_communication(self, **kw):
        vals = {}

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        new_organization_type_communication = (
            request.env["organization.type.communication"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_type_communication/{new_organization_type_communication.id}"
        )

    @http.route(
        "/new/organization_type_compte", type="http", auth="user", website=True
    )
    def create_new_organization_type_compte(self, **kw):
        default_admin = (
            http.request.env["organization.type.compte"]
            .default_get(["admin"])
            .get("admin")
        )
        default_admin_chef = (
            http.request.env["organization.type.compte"]
            .default_get(["admin_chef"])
            .get("admin_chef")
        )
        default_admin_ord_point_service = (
            http.request.env["organization.type.compte"]
            .default_get(["admin_ord_point_service"])
            .get("admin_ord_point_service")
        )
        default_admin_point_service = (
            http.request.env["organization.type.compte"]
            .default_get(["admin_point_service"])
            .get("admin_point_service")
        )
        membre = http.request.env["organization.membre"].search(
            [("active", "=", True)]
        )
        default_membre = (
            http.request.env["organization.type.compte"]
            .default_get(["membre"])
            .get("membre")
        )
        default_nom_complet = (
            http.request.env["organization.type.compte"]
            .default_get(["nom_complet"])
            .get("nom_complet")
        )
        default_organizateur_simple = (
            http.request.env["organization.type.compte"]
            .default_get(["organizateur_simple"])
            .get("organizateur_simple")
        )
        default_reseau = (
            http.request.env["organization.type.compte"]
            .default_get(["reseau"])
            .get("reseau")
        )
        default_spip = (
            http.request.env["organization.type.compte"]
            .default_get(["spip"])
            .get("spip")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_type_compte",
            {
                "membre": membre,
                "page_name": "create_organization_type_compte",
                "default_admin": default_admin,
                "default_admin_chef": default_admin_chef,
                "default_admin_ord_point_service": default_admin_ord_point_service,
                "default_admin_point_service": default_admin_point_service,
                "default_membre": default_membre,
                "default_nom_complet": default_nom_complet,
                "default_organizateur_simple": default_organizateur_simple,
                "default_reseau": default_reseau,
                "default_spip": default_spip,
            },
        )

    @http.route(
        "/submitted/organization_type_compte",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_type_compte(self, **kw):
        vals = {}

        default_admin = (
            http.request.env["organization.type.compte"]
            .default_get(["admin"])
            .get("admin")
        )
        if kw.get("admin"):
            vals["admin"] = kw.get("admin") == "True"
        elif default_admin:
            vals["admin"] = False

        default_admin_chef = (
            http.request.env["organization.type.compte"]
            .default_get(["admin_chef"])
            .get("admin_chef")
        )
        if kw.get("admin_chef"):
            vals["admin_chef"] = kw.get("admin_chef") == "True"
        elif default_admin_chef:
            vals["admin_chef"] = False

        default_admin_ord_point_service = (
            http.request.env["organization.type.compte"]
            .default_get(["admin_ord_point_service"])
            .get("admin_ord_point_service")
        )
        if kw.get("admin_ord_point_service"):
            vals["admin_ord_point_service"] = (
                kw.get("admin_ord_point_service") == "True"
            )
        elif default_admin_ord_point_service:
            vals["admin_ord_point_service"] = False

        default_admin_point_service = (
            http.request.env["organization.type.compte"]
            .default_get(["admin_point_service"])
            .get("admin_point_service")
        )
        if kw.get("admin_point_service"):
            vals["admin_point_service"] = (
                kw.get("admin_point_service") == "True"
            )
        elif default_admin_point_service:
            vals["admin_point_service"] = False

        if kw.get("membre") and kw.get("membre").isdigit():
            vals["membre"] = int(kw.get("membre"))

        if kw.get("nom_complet"):
            vals["nom_complet"] = kw.get("nom_complet")

        default_organizateur_simple = (
            http.request.env["organization.type.compte"]
            .default_get(["organizateur_simple"])
            .get("organizateur_simple")
        )
        if kw.get("organizateur_simple"):
            vals["organizateur_simple"] = (
                kw.get("organizateur_simple") == "True"
            )
        elif default_organizateur_simple:
            vals["organizateur_simple"] = False

        default_reseau = (
            http.request.env["organization.type.compte"]
            .default_get(["reseau"])
            .get("reseau")
        )
        if kw.get("reseau"):
            vals["reseau"] = kw.get("reseau") == "True"
        elif default_reseau:
            vals["reseau"] = False

        default_spip = (
            http.request.env["organization.type.compte"]
            .default_get(["spip"])
            .get("spip")
        )
        if kw.get("spip"):
            vals["spip"] = kw.get("spip") == "True"
        elif default_spip:
            vals["spip"] = False

        new_organization_type_compte = (
            request.env["organization.type.compte"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_type_compte/{new_organization_type_compte.id}"
        )

    @http.route(
        "/new/organization_type_fichier",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_type_fichier(self, **kw):
        default_date_mise_a_jour = (
            http.request.env["organization.type.fichier"]
            .default_get(["date_mise_a_jour"])
            .get("date_mise_a_jour")
        )
        default_nom = (
            http.request.env["organization.type.fichier"]
            .default_get(["nom"])
            .get("nom")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_type_fichier",
            {
                "page_name": "create_organization_type_fichier",
                "default_date_mise_a_jour": default_date_mise_a_jour,
                "default_nom": default_nom,
            },
        )

    @http.route(
        "/submitted/organization_type_fichier",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_type_fichier(self, **kw):
        vals = {}

        if kw.get("date_mise_a_jour"):
            vals["date_mise_a_jour"] = kw.get("date_mise_a_jour")

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        new_organization_type_fichier = (
            request.env["organization.type.fichier"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_type_fichier/{new_organization_type_fichier.id}"
        )

    @http.route(
        "/new/organization_type_service",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_type_service(self, **kw):
        default_active = (
            http.request.env["organization.type.service"]
            .default_get(["active"])
            .get("active")
        )
        default_approuve = (
            http.request.env["organization.type.service"]
            .default_get(["approuve"])
            .get("approuve")
        )
        default_description = (
            http.request.env["organization.type.service"]
            .default_get(["description"])
            .get("description")
        )
        default_identifiant = (
            http.request.env["organization.type.service"]
            .default_get(["identifiant"])
            .get("identifiant")
        )
        default_nom = (
            http.request.env["organization.type.service"]
            .default_get(["nom"])
            .get("nom")
        )
        default_nom_complet = (
            http.request.env["organization.type.service"]
            .default_get(["nom_complet"])
            .get("nom_complet")
        )
        default_numero = (
            http.request.env["organization.type.service"]
            .default_get(["numero"])
            .get("numero")
        )
        sous_categorie_id = http.request.env[
            "organization.type.service.sous.categorie"
        ].search([("active", "=", True)])
        default_sous_categorie_id = (
            http.request.env["organization.type.service"]
            .default_get(["sous_categorie_id"])
            .get("sous_categorie_id")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_type_service",
            {
                "sous_categorie_id": sous_categorie_id,
                "page_name": "create_organization_type_service",
                "default_active": default_active,
                "default_approuve": default_approuve,
                "default_description": default_description,
                "default_identifiant": default_identifiant,
                "default_nom": default_nom,
                "default_nom_complet": default_nom_complet,
                "default_numero": default_numero,
                "default_sous_categorie_id": default_sous_categorie_id,
            },
        )

    @http.route(
        "/submitted/organization_type_service",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_type_service(self, **kw):
        vals = {}

        default_active = (
            http.request.env["organization.type.service"]
            .default_get(["active"])
            .get("active")
        )
        if kw.get("active"):
            vals["active"] = kw.get("active") == "True"
        elif default_active:
            vals["active"] = False

        default_approuve = (
            http.request.env["organization.type.service"]
            .default_get(["approuve"])
            .get("approuve")
        )
        if kw.get("approuve"):
            vals["approuve"] = kw.get("approuve") == "True"
        elif default_approuve:
            vals["approuve"] = False

        if kw.get("description"):
            vals["description"] = kw.get("description")

        if kw.get("identifiant"):
            vals["identifiant"] = kw.get("identifiant")

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        if kw.get("nom_complet"):
            vals["nom_complet"] = kw.get("nom_complet")

        if kw.get("numero"):
            numero_value = kw.get("numero")
            if numero_value.isdigit():
                vals["numero"] = int(numero_value)

        if (
            kw.get("sous_categorie_id")
            and kw.get("sous_categorie_id").isdigit()
        ):
            vals["sous_categorie_id"] = int(kw.get("sous_categorie_id"))

        new_organization_type_service = (
            request.env["organization.type.service"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_type_service/{new_organization_type_service.id}"
        )

    @http.route(
        "/new/organization_type_service_categorie",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_type_service_categorie(self, **kw):
        default_active = (
            http.request.env["organization.type.service.categorie"]
            .default_get(["active"])
            .get("active")
        )
        default_approuve = (
            http.request.env["organization.type.service.categorie"]
            .default_get(["approuve"])
            .get("approuve")
        )
        default_nocategorie = (
            http.request.env["organization.type.service.categorie"]
            .default_get(["nocategorie"])
            .get("nocategorie")
        )
        default_nom = (
            http.request.env["organization.type.service.categorie"]
            .default_get(["nom"])
            .get("nom")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_type_service_categorie",
            {
                "page_name": "create_organization_type_service_categorie",
                "default_active": default_active,
                "default_approuve": default_approuve,
                "default_nocategorie": default_nocategorie,
                "default_nom": default_nom,
            },
        )

    @http.route(
        "/submitted/organization_type_service_categorie",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_type_service_categorie(self, **kw):
        vals = {}

        default_active = (
            http.request.env["organization.type.service.categorie"]
            .default_get(["active"])
            .get("active")
        )
        if kw.get("active"):
            vals["active"] = kw.get("active") == "True"
        elif default_active:
            vals["active"] = False

        default_approuve = (
            http.request.env["organization.type.service.categorie"]
            .default_get(["approuve"])
            .get("approuve")
        )
        if kw.get("approuve"):
            vals["approuve"] = kw.get("approuve") == "True"
        elif default_approuve:
            vals["approuve"] = False

        if kw.get("nocategorie"):
            nocategorie_value = kw.get("nocategorie")
            if nocategorie_value.isdigit():
                vals["nocategorie"] = int(nocategorie_value)

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        new_organization_type_service_categorie = (
            request.env["organization.type.service.categorie"]
            .sudo()
            .create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_type_service_categorie/{new_organization_type_service_categorie.id}"
        )

    @http.route(
        "/new/organization_type_service_sous_categorie",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_type_service_sous_categorie(self, **kw):
        default_active = (
            http.request.env["organization.type.service.sous.categorie"]
            .default_get(["active"])
            .get("active")
        )
        default_approuver = (
            http.request.env["organization.type.service.sous.categorie"]
            .default_get(["approuver"])
            .get("approuver")
        )
        categorie = http.request.env[
            "organization.type.service.categorie"
        ].search([("active", "=", True)])
        default_categorie = (
            http.request.env["organization.type.service.sous.categorie"]
            .default_get(["categorie"])
            .get("categorie")
        )
        default_nom = (
            http.request.env["organization.type.service.sous.categorie"]
            .default_get(["nom"])
            .get("nom")
        )
        default_sous_categorie_service = (
            http.request.env["organization.type.service.sous.categorie"]
            .default_get(["sous_categorie_service"])
            .get("sous_categorie_service")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_type_service_sous_categorie",
            {
                "categorie": categorie,
                "page_name": "create_organization_type_service_sous_categorie",
                "default_active": default_active,
                "default_approuver": default_approuver,
                "default_categorie": default_categorie,
                "default_nom": default_nom,
                "default_sous_categorie_service": default_sous_categorie_service,
            },
        )

    @http.route(
        "/submitted/organization_type_service_sous_categorie",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_type_service_sous_categorie(self, **kw):
        vals = {}

        default_active = (
            http.request.env["organization.type.service.sous.categorie"]
            .default_get(["active"])
            .get("active")
        )
        if kw.get("active"):
            vals["active"] = kw.get("active") == "True"
        elif default_active:
            vals["active"] = False

        default_approuver = (
            http.request.env["organization.type.service.sous.categorie"]
            .default_get(["approuver"])
            .get("approuver")
        )
        if kw.get("approuver"):
            vals["approuver"] = kw.get("approuver") == "True"
        elif default_approuver:
            vals["approuver"] = False

        if kw.get("categorie") and kw.get("categorie").isdigit():
            vals["categorie"] = int(kw.get("categorie"))

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        if kw.get("sous_categorie_service"):
            vals["sous_categorie_service"] = kw.get("sous_categorie_service")

        new_organization_type_service_sous_categorie = (
            request.env["organization.type.service.sous.categorie"]
            .sudo()
            .create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_type_service_sous_categorie/{new_organization_type_service_sous_categorie.id}"
        )

    @http.route(
        "/new/organization_type_telephone",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_organization_type_telephone(self, **kw):
        default_nom = (
            http.request.env["organization.type.telephone"]
            .default_get(["nom"])
            .get("nom")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_type_telephone",
            {
                "page_name": "create_organization_type_telephone",
                "default_nom": default_nom,
            },
        )

    @http.route(
        "/submitted/organization_type_telephone",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_type_telephone(self, **kw):
        vals = {}

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        new_organization_type_telephone = (
            request.env["organization.type.telephone"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_type_telephone/{new_organization_type_telephone.id}"
        )

    @http.route(
        "/new/organization_ville", type="http", auth="user", website=True
    )
    def create_new_organization_ville(self, **kw):
        default_code = (
            http.request.env["organization.ville"]
            .default_get(["code"])
            .get("code")
        )
        default_nom = (
            http.request.env["organization.ville"]
            .default_get(["nom"])
            .get("nom")
        )
        region = http.request.env["organization.region"].search([])
        default_region = (
            http.request.env["organization.ville"]
            .default_get(["region"])
            .get("region")
        )
        return http.request.render(
            "demo_mariadb_sql_example_1.portal_create_organization_ville",
            {
                "region": region,
                "page_name": "create_organization_ville",
                "default_code": default_code,
                "default_nom": default_nom,
                "default_region": default_region,
            },
        )

    @http.route(
        "/submitted/organization_ville",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_organization_ville(self, **kw):
        vals = {}

        if kw.get("code"):
            code_value = kw.get("code")
            if code_value.isdigit():
                vals["code"] = int(code_value)

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        if kw.get("region") and kw.get("region").isdigit():
            vals["region"] = int(kw.get("region"))

        new_organization_ville = (
            request.env["organization.ville"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/organization_ville/{new_organization_ville.id}"
        )
