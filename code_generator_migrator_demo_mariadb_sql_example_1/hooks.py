import logging
import os
import time

from odoo import SUPERUSER_ID, _, api, fields, models

_logger = logging.getLogger(__name__)

MODULE_NAME = "demo_mariadb_sql_example_1"
# SECRET_PASSWORD = ""


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # The path of the actual file
        path_module_generate = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        short_name = MODULE_NAME.replace("_", " ").title()

        # Add code generator
        categ_id = env["ir.module.category"].search(
            [("name", "=", "Uncategorized")]
        )
        value = {
            "shortdesc": short_name,
            "name": MODULE_NAME,
            "license": "AGPL-3",
            "category_id": categ_id.id,
            "summary": "",
            "author": "TechnoLibre",
            "website": "",
            "application": True,
            "enable_sync_code": True,
            "path_sync_code": path_module_generate,
            # "icon": os.path.join(
            #     os.path.basename(os.path.dirname(os.path.dirname(__file__))),
            #     "static",
            #     "description",
            #     "code_generator_icon.png",
            # ),
        }

        # TODO HUMAN: enable your functionality to generate
        value["enable_sync_template"] = False
        value["ignore_fields"] = ""
        value["post_init_hook_show"] = False
        value["uninstall_hook_show"] = False
        value["post_init_hook_feature_code_generator"] = False
        value["uninstall_hook_feature_code_generator"] = False

        value["hook_constant_code"] = f'MODULE_NAME = "{MODULE_NAME}"'

        code_generator_id = env["code.generator.module"].create(value)

        # Database
        value_db = {
            "m2o_dbtype": env.ref(
                "code_generator_db_servers.code_generator_db_type_mysql"
            ).id,
            "database": "mariadb_sql_example_1",
            "host": "localhost",
            "port": 3306,
            "user": "organization",
            "password": "organization",
            "schema": "public",
            "accept_primary_key": True,
            # TODO option to create application pear first prefix or use in model name (si on prend tbl ou non)
        }
        code_generator_db_server_id = env["code.generator.db"].create(value_db)

        # Local variable to add update information
        db_table = env["code.generator.db.table"]
        db_column = env["code.generator.db.column"]

        # Modification of field before migration

        before_time = time.process_time()

        # tbl_organization
        db_table.update_table(
            "tbl_organization",
            new_model_name="organization.organization",
            new_rec_name="nom",
            new_description=(
                "Gestion des entitées Organization, contient les informations"
                " et les messages d'une Organization."
            ),
            # nomenclator=True,
            menu_group="Organization",
            menu_parent="Organization",
        )
        db_column.update_column(
            "tbl_organization",
            "noorganization",
            delete=True,
        )
        db_column.update_column(
            "tbl_organization",
            "noregion",
            new_field_name="region",
            new_description="Région administrative",
            new_required=False,
            new_help="Nom de la région administrative de l'Organization",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_organization",
            "noville",
            new_field_name="ville",
            new_description="Ville",
            new_required=False,
            new_help="Nom de la ville de l'Organization",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_organization",
            "noarrondissement",
            new_field_name="arrondissement",
            new_description="Arrondissement",
            new_help="Nom de l'Arrondissement qui contient l'Organization.",
        )
        db_column.update_column(
            "tbl_organization",
            "nocartier",
            # new_field_name="cartier",
            # new_description="Cartier",
            delete=True,
        )
        db_column.update_column(
            "tbl_organization",
            "nom",
            new_required=True,
            new_help="Nom de l'Organization",
        )
        db_column.update_column(
            "tbl_organization",
            "nomcomplet",
            # new_field_name="nom_complet",
            # new_description="Nom complet",
            delete=True,
        )
        db_column.update_column(
            "tbl_organization",
            "adresseorganization",
            new_field_name="adresse",
            new_description="Adresse",
            new_help="Adresse de l'Organization",
        )
        db_column.update_column(
            "tbl_organization",
            "codepostalorganization",
            new_field_name="code_postal",
            new_description="Code postal",
            new_help="Code postal de l'Organization",
        )
        db_column.update_column(
            "tbl_organization",
            "telorganization",
            new_field_name="telephone",
            new_description="Téléphone",
            new_help="Numéro de téléphone pour joindre l'Organization.",
        )
        db_column.update_column(
            "tbl_organization",
            "telecopieurorganization",
            new_field_name="telecopieur",
            new_description="Télécopieur",
            new_help="Numéro de télécopieur pour joindre l'Organization.",
        )
        db_column.update_column(
            "tbl_organization",
            "courrielorganization",
            new_field_name="courriel",
            new_description="Adresse courriel",
            new_help="Adresse courriel pour joindre l'Organization.",
        )
        db_column.update_column(
            "tbl_organization",
            "messagegrpachat",
            new_field_name="message_grp_achat",
            new_description="Message groupe d'achats",
            new_type="html",
            new_help="Message à afficher pour les groupes d'achats.",
            is_hide_blacklist_list_view=True,
        )
        db_column.update_column(
            "tbl_organization",
            "messageaccueil",
            new_field_name="message_accueil",
            new_description="Message d'accueil",
            new_type="html",
            new_help="Message à afficher pour accueillir les membres.",
            is_hide_blacklist_list_view=True,
        )
        db_column.update_column(
            "tbl_organization",
            "url_public_organization",
            new_field_name="url_public",
            new_description="Lien du site web publique",
            new_help="Lien du site web publique de l'Organization",
            force_widget="link_button",
        )
        db_column.update_column(
            "tbl_organization",
            "url_transac_organization",
            new_field_name="url_transactionnel",
            new_description="Lien du site web transactionnel",
            force_widget="link_button",
            new_help="Lien du site web transactionnel de l'Organization",
        )
        db_column.update_column(
            "tbl_organization",
            "url_logoorganization",
            new_field_name="logo",
            new_description="Logo",
            new_type="binary",
            force_widget="image",
            path_binary="/organization_canada/Intranet/images/logo",
            new_help="Logo de l'Organization",
        )
        db_column.update_column(
            "tbl_organization",
            "grpachat_admin",
            new_field_name="grp_achat_administrateur",
            new_description="Groupe d'achats des administrateurs",
            new_type="boolean",
            new_help=(
                "Permet de rendre accessible les achats pour les"
                " administrateurs."
            ),
        )
        db_column.update_column(
            "tbl_organization",
            "grpachat_organizateur",
            new_field_name="grp_achat_membre",
            new_description="Groupe d'achats membre",
            new_type="boolean",
            new_help="Rend accessible les achats pour les Organizateurs.",
        )
        db_column.update_column(
            "tbl_organization",
            "nonvisible",
            new_required=False,
            new_type="boolean",
            new_field_name="active",
            new_description="Actif",
            new_default_value="True",
            force_widget="boolean_button",
            new_help=(
                "Lorsque non actif, cette organization n'est plus en fonction,"
                " mais demeure accessible."
            ),
            compute_data_function="""not active""",
        )
        db_column.update_column(
            "tbl_organization",
            "datemaj_organization",
            new_field_name="date_mise_a_jour",
            new_description="Dernière mise à jour",
            new_help="Date de la dernière mise à jour",
        )

        # tbl_achat_ponctuel
        db_table.update_table(
            "tbl_achat_ponctuel",
            delete=True,
            # new_model_name="organization.achat.ponctuel",
            # new_description="Gestion des achats ponctuels"
            # new_rec_name="nom",
        )

        # tbl_achat_ponctuel_produit
        db_table.update_table(
            "tbl_achat_ponctuel_produit",
            delete=True,
            # new_model_name="organization.achat.ponctuel.produit",
            # new_description="Liaisons des achats ponctuels aux produits des fournisseurs."
            # new_rec_name="nom",
        )

        # tbl_arrondissement
        db_table.update_table(
            "tbl_arrondissement",
            new_model_name="organization.arrondissement",
            new_description="Ensemble des arrondissement des Organizations",
            new_rec_name="nom",
            nomenclator=True,
            menu_group="Location",
            menu_parent="Configuration",
        )
        db_column.update_column(
            "tbl_arrondissement",
            "noarrondissement",
            delete=True,
        )
        db_column.update_column(
            "tbl_arrondissement",
            "noville",
            new_field_name="ville",
            new_description="Ville",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_arrondissement",
            "arrondissement",
            new_field_name="nom",
            new_description="Nom",
        )

        # tbl_cartier
        db_table.update_table(
            "tbl_cartier",
            new_model_name="organization.quartier",
            new_rec_name="nom",
            nomenclator=True,
            menu_group="Location",
            menu_parent="Configuration",
        )
        db_column.update_column(
            "tbl_cartier",
            "nocartier",
            delete=True,
        )
        db_column.update_column(
            "tbl_cartier",
            "noarrondissement",
            new_field_name="arrondissement",
            new_description="Arrondissement",
            new_help="Arrondissement associé au quartier",
        )
        db_column.update_column(
            "tbl_cartier",
            "cartier",
            new_field_name="nom",
            new_description="Nom du quartier",
            new_help="Nom du quartier",
        )

        # tbl_categorie
        db_table.update_table(
            "tbl_categorie",
            new_model_name="organization.type.service.categorie",
            new_description=(
                "Les catégories de types de services des Organizations"
            ),
            new_rec_name="nom",
            nomenclator=True,
            menu_group="Catégorie de services",
            menu_label="Catégorie de services",
            menu_parent="Service",
        )
        db_column.update_column(
            "tbl_categorie",
            "nocategorie",
            # delete=True,
        )
        db_column.update_column(
            "tbl_categorie",
            "titrecategorie",
            new_field_name="nom",
            new_description="Nom",
            new_help="Le nom de la catégorie des services",
            compute_data_function="""nom.replace("&#8217;", "'").strip()""",
        )
        db_column.update_column(
            "tbl_categorie",
            "supprimer",
            new_field_name="active",
            new_description="Actif",
            new_type="boolean",
            new_default_value="True",
            force_widget="boolean_button",
            new_help=(
                "Lorsque non actif, cette catégorie n'est plus en fonction,"
                " mais demeure accessible."
            ),
            compute_data_function="""not active""",
        )
        db_column.update_column(
            "tbl_categorie",
            "approuver",
            new_field_name="approuve",
            new_description="Approuvé",
            new_type="boolean",
            new_help="Permet d'approuver cette catégorie.",
        )

        # tbl_categorie_sous_categorie
        db_table.update_table(
            "tbl_categorie_sous_categorie",
            new_model_name="organization.type.service",
            new_rec_name="nom",
            new_description="Type de services des Organizations",
            nomenclator=True,
            menu_group="Catégorie de services",
            menu_parent="Service",
            menu_label="Type de services",
        )
        db_column.update_column(
            "tbl_categorie_sous_categorie",
            "nosouscategorieid",
            new_field_name="sous_categorie_id",
            new_description="Sous-catégorie",
            new_help="Sous-catégorie de services",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_categorie_sous_categorie",
            "nocategoriesouscategorie",
            delete=True,
        )
        db_column.update_column(
            "tbl_categorie_sous_categorie",
            "nosouscategorie",
            delete=True,
        )
        db_column.update_column(
            "tbl_categorie_sous_categorie",
            "nocategorie",
            delete=True,
        )
        db_column.update_column(
            "tbl_categorie_sous_categorie",
            "titreoffre",
            new_field_name="nom",
            new_description="Nom",
            new_help="Nom du type de services",
        )
        db_column.update_column(
            "tbl_categorie_sous_categorie",
            "supprimer",
            new_field_name="active",
            new_description="Actif",
            new_type="boolean",
            new_default_value="True",
            force_widget="boolean_button",
            new_help=(
                "Lorsque non actif, ce type de service n'est plus en fonction,"
                " mais demeure accessible."
            ),
            compute_data_function="""not active""",
        )
        db_column.update_column(
            "tbl_categorie_sous_categorie",
            "approuver",
            new_field_name="approuve",
            new_description="Approuvé",
            new_type="boolean",
            new_help="Permet d'approuver ce type de services.",
        )
        db_column.update_column(
            "tbl_categorie_sous_categorie",
            "description",
            new_help="Description du type de services",
            compute_data_function="""description.replace("&#8217;", "'").strip()""",
        )
        db_column.update_column(
            "tbl_categorie_sous_categorie",
            "nooffre",
            new_field_name="numero",
            new_description="Numéro",
            new_help="Numéro du type de services"
            # TODO mettre invisible
            # TODO mettre numéro_complet
        )

        # tbl_commande
        db_table.update_table(
            "tbl_commande",
            delete=True,
            # new_model_name="organization.commande",
        )

        # tbl_commande_membre
        db_table.update_table(
            "tbl_commande_membre",
            delete=True,
            # new_rec_name="description",
            # new_model_name="organization.commande.membre",
        )

        # tbl_commande_membre_produit
        db_table.update_table(
            "tbl_commande_membre_produit",
            delete=True,
            # new_rec_name="description",
            # new_model_name="organization.commande.membre.produit",
        )

        # tbl_commentaire
        db_table.update_table(
            "tbl_commentaire",
            # new_rec_name="description",
            new_model_name="organization.commentaire",
            new_description=(
                "Les commentaires des membres envers d'autres membres sur des"
                " services et demandes"
            ),
            menu_group="Service",
            menu_parent="Service",
        )
        db_column.update_column(
            "tbl_commentaire",
            "nocommentaire",
            new_field_name="number",
            new_description="# de commentaire",
            # delete=True,
        )
        db_column.update_column(
            "tbl_commentaire",
            "nopointservice",
            new_field_name="point_service",
            new_description="Point de services",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_commentaire",
            "nomembresource",
            new_field_name="membre_source",
            new_description="Membre source",
            new_help="Membre duquel provient le commentaire",
            add_one2many=True,
            one2many_description="Commentaire membre source",
        )
        db_column.update_column(
            "tbl_commentaire",
            "nomembreviser",
            new_field_name="membre_viser",
            new_description="Membre visé",
            new_help="Membre visé par le commentaire",
            add_one2many=True,
            one2many_description="Commentaire membre visé",
        )
        db_column.update_column(
            "tbl_commentaire",
            "nooffreservicemembre",
            new_field_name="offre_service_id",
            new_description="Offre de services",
            new_help="L'offre de services qui est visée par ce commentaire.",
        )
        db_column.update_column(
            "tbl_commentaire",
            "nodemandeservice",
            new_field_name="demande_service_id",
            new_description="Demande de services",
            new_help=(
                "La demande de services qui est visée par ce commentaire."
            ),
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_commentaire",
            "dateheureajout",
            new_field_name="datetime_creation",
            new_description="Date et heure de création",
        )
        db_column.update_column(
            "tbl_commentaire",
            "situation_impliquant",
            new_help="Choisir un type de groupes visé par ce commentaire.",
            new_type="selection",
            selection_migration_start_at=1,
            new_selection=(
                "[('organizateur', 'UnE ou des OrganizateurEs'),"
                "('comite', 'Un comité'),"
                "('employe', 'UnE employéE'),"
                "('autre', 'Autre')]"
            ),
        )
        db_column.update_column(
            "tbl_commentaire",
            "nomemployer",
            delete=True,
        )
        db_column.update_column(
            "tbl_commentaire",
            "nomcomite",
            new_field_name="nom_comite",
            new_description="Nom du comité",
        )
        db_column.update_column(
            "tbl_commentaire",
            "autresituation",
            new_field_name="autre_situation",
            new_description="Autre situation",
        )
        db_column.update_column(
            "tbl_commentaire",
            "satisfactioninsatisfaction",
            new_field_name="degre_satisfaction",
            new_description="Degré de satisfaction",
            new_type="selection",
            selection_migration_start_at=1,
            new_selection=(
                "[('satisfait', 'Grand satisfaction'),"
                "('insatisfait', 'Insatisfaction')]"
            ),
        )
        db_column.update_column(
            "tbl_commentaire",
            "dateincident",
            new_field_name="date_incident",
            new_description="Date de l'indicent",
        )
        db_column.update_column(
            "tbl_commentaire",
            "typeoffre",
            new_field_name="type_offre",
            new_description="Type de l'offre",
            new_type="selection",
            new_selection=(
                "[('aucun', 'Aucun'),"
                "('offre_ordinaire', 'Offre ordinaire'),"
                "('offre_special', 'Offre spéciale'),"
                "('demande', 'Demande'),"
                "('ponctuel', 'Ponctuel')"
                "]"
            ),
        )
        db_column.update_column(
            "tbl_commentaire",
            "resumersituation",
            new_field_name="resumer_situation",
            new_description="Résumé de la situation",
        )
        db_column.update_column(
            "tbl_commentaire",
            "demarche",
            new_description="Démarche",
            new_help="Démarche entreprise avant de faire le commentaire",
        )
        db_column.update_column(
            "tbl_commentaire",
            "solutionpourregler",
            new_field_name="solution_pour_regler",
            new_description="Solution pour régler la situation",
            new_help=(
                "Indiquer quels seraient la meilleur solution, selon vous,"
                " pour régler la situation."
            ),
        )
        db_column.update_column(
            "tbl_commentaire",
            "autrecommentaire",
            new_field_name="autre_commentaire",
            new_description="Autres commentaires",
        )
        db_column.update_column(
            "tbl_commentaire",
            "siconfidentiel",
            new_field_name="confidentiel",
            new_description="Confidentialité",
            new_type="selection",
            new_selection="""[("non_autorise", 
            "Non-autorisé - Je demande à L'Organization de ne pas divulguer mon identité lors de ses démarches auprès des personnes concernées par la situation."),
            ("autorise", "Autorisé - J'autorise l'Organization à divulguer mon identité lors de ses démarches auprès des personnes concernées par la situation.")]""",
        )
        db_column.update_column(
            "tbl_commentaire",
            "noteadministrative",
            new_field_name="note_administrative",
            new_description="Note administrative",
            new_help=(
                "Suivi du commentaire, visible par le Réseau et les"
                " administrateurs-chefs seulement."
            ),
            # TODO write only by reseau + admin
        )
        db_column.update_column(
            "tbl_commentaire",
            "consulterorganization",
            new_field_name="consulter_organization",
            new_description="Consulté par une Organization",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_commentaire",
            "consulterreseau",
            new_field_name="consulter_reseau",
            new_description="Consulté par le Réseau",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_commentaire",
            "datemaj_commentaire",
            new_field_name="date_mise_a_jour",
            new_description="Dernière mise à jour",
            new_help="Date de la dernière mise à jour",
        )

        # tbl_demande_service
        db_table.update_table(
            "tbl_demande_service",
            new_rec_name="titre",
            new_model_name="organization.demande.service",
            menu_group="Service",
            menu_parent="Service",
            menu_label="Demande de services",
        )
        db_column.update_column(
            "tbl_demande_service",
            "nodemandeservice",
            delete=True,
        )
        db_column.update_column(
            "tbl_demande_service",
            "nomembre",
            new_field_name="membre",
            new_description="Membre",
        )
        db_column.update_column(
            "tbl_demande_service",
            "noorganization",
            new_field_name="organization",
            new_description="Organization",
        )
        db_column.update_column(
            "tbl_demande_service",
            "titredemande",
            new_field_name="titre",
            new_description="Titre",
        )
        db_column.update_column(
            "tbl_demande_service",
            "description",
        )
        db_column.update_column(
            "tbl_demande_service",
            "approuve",
            new_field_name="approuver",
            new_description="Approuvé",
            new_type="boolean",
            new_help="Permet d'approuver cette demande de service.",
        )
        db_column.update_column(
            "tbl_demande_service",
            "supprimer",
            new_field_name="active",
            new_description="Actif",
            new_type="boolean",
            new_default_value="True",
            force_widget="boolean_button",
            new_help=(
                "Lorsque non actif, cet demande de services n'est plus en"
                " fonction, mais demeure accessible."
            ),
            compute_data_function="""not active""",
        )
        db_column.update_column(
            "tbl_demande_service",
            "transmit",
            ignore_field=True,
        )
        db_column.update_column(
            "tbl_demande_service",
            "datedebut",
            new_field_name="date_debut",
            new_description="Date début",
        )
        db_column.update_column(
            "tbl_demande_service",
            "datefin",
            new_field_name="date_fin",
            new_description="Date fin",
        )

        # tbl_dmd_adhesion
        db_table.update_table(
            "tbl_dmd_adhesion",
            # new_rec_name="description",
            new_model_name="organization.demande.adhesion",
            menu_group="Membre",
            menu_parent="Organization",
            menu_label="Demande d'adhésion",
        )
        db_column.update_column(
            "tbl_dmd_adhesion",
            "nodmdadhesion",
            delete=True,
        )
        db_column.update_column(
            "tbl_dmd_adhesion",
            "noorganization",
            new_field_name="organization",
            new_description="Organization",
        )
        db_column.update_column(
            "tbl_dmd_adhesion",
            "nom",
            is_hide_blacklist_list_view=True,
        )
        db_column.update_column(
            "tbl_dmd_adhesion",
            "prenom",
            new_description="Prénom",
            is_hide_blacklist_list_view=True,
        )
        db_column.update_column(
            "tbl_dmd_adhesion",
            "telephone",
            new_description="Téléphone",
        )
        db_column.update_column(
            "tbl_dmd_adhesion",
            "courriel",
        )
        db_column.update_column(
            "tbl_dmd_adhesion",
            "supprimer",
            new_field_name="active",
            new_description="Actif",
            new_type="boolean",
            new_default_value="True",
            force_widget="boolean_button",
            new_help=(
                "Lorsque non actif, cet demande d'adhésion n'est plus en"
                " fonction, mais demeure accessible."
            ),
            compute_data_function="""not active""",
        )
        db_column.update_column(
            "tbl_dmd_adhesion",
            "transferer",
            new_description="Transféré",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_dmd_adhesion",
            "enattente",
            new_field_name="en_attente",
            new_description="En attente",
            new_type="boolean",
            new_default_value="True",
        )
        db_column.update_column(
            "tbl_dmd_adhesion",
            "datemaj",
            new_field_name="date_mise_a_jour",
            new_description="Dernière mise à jour",
            new_help="Date de la dernière mise à jour",
        )
        db_column.update_column(
            "tbl_dmd_adhesion",
            "poste",
        )

        # tbl_droits_admin
        db_table.update_table(
            "tbl_droits_admin",
            # new_rec_name="description",
            new_model_name="organization.droits.admin",
            menu_group="Configuration",
            menu_parent="Configuration",
            menu_label="Droits administratifs",
        )
        db_column.update_column(
            "tbl_droits_admin",
            "nomembre",
            new_field_name="membre",
            new_description="Membre",
            new_required=False,
        )
        db_column.update_column(
            "tbl_droits_admin",
            "gestionprofil",
            new_field_name="gestion_profil",
            new_description="Gestion profil",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_droits_admin",
            "gestioncatsouscat",
            new_field_name="gestion_type_service",
            new_description="Gestion type de services",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_droits_admin",
            "gestionoffre",
            new_field_name="gestion_offre",
            new_description="Gestion offre",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_droits_admin",
            "gestionoffremembre",
            new_field_name="gestion_offre_service",
            new_description="Gestion offre de services",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_droits_admin",
            "saisieechange",
            new_field_name="saisie_echange",
            new_description="Saisie échange",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_droits_admin",
            "validation",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_droits_admin",
            "gestiondmd",
            new_field_name="gestion_dmd",
            new_description="Gestion demande de services",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_droits_admin",
            "groupeachat",
            new_field_name="groupe_achat",
            new_description="Groupe d'achat",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_droits_admin",
            "consulterprofil",
            new_field_name="consulter_profil",
            new_description="Consulter profil",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_droits_admin",
            "consulteretatcompte",
            new_field_name="consulter_etat_compte",
            new_description="Consulter état de compte",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_droits_admin",
            "gestionfichier",
            new_field_name="gestion_fichier",
            new_description="Gestion fichier",
            new_type="boolean",
        )

        # tbl_echange_service
        db_table.update_table(
            "tbl_echange_service",
            # new_rec_name="nom",
            new_model_name="organization.echange.service",
            menu_group="Service",
            menu_parent="Service",
            menu_label="Échange de services",
        )
        db_column.update_column(
            "tbl_echange_service",
            "noechangeservice",
            delete=True,
        )
        db_column.update_column(
            "tbl_echange_service",
            "nopointservice",
            new_field_name="point_service",
            new_description="Point de services",
        )
        db_column.update_column(
            "tbl_echange_service",
            "nomembrevendeur",
            new_field_name="membre_vendeur",
            new_description="Membre vendeur",
        )
        db_column.update_column(
            "tbl_echange_service",
            "nomembreacheteur",
            new_field_name="membre_acheteur",
            new_description="Membre acheteur",
        )
        db_column.update_column(
            "tbl_echange_service",
            "nodemandeservice",
            new_field_name="demande_service",
            new_description="Demande de services",
        )
        db_column.update_column(
            "tbl_echange_service",
            "nooffreservicemembre",
            new_field_name="offre_service",
            new_description="Offre de services",
        )
        db_column.update_column(
            "tbl_echange_service",
            "nbheure",
            new_field_name="nb_heure",
            new_description="Nombre d'heure",
            new_help="Nombre d'heure effectué au moment de l'échange.",
            force_widget="float_time",
        )
        db_column.update_column(
            "tbl_echange_service",
            "dateechange",
            new_field_name="date_echange",
            new_description="Date de l'échange",
        )
        db_column.update_column(
            "tbl_echange_service",
            "typeechange",
            new_field_name="type_echange",
            new_description="Type d'échange",
            new_type="selection",
            selection_migration_start_at=1,
            new_selection=(
                "[('offre_ordinaire', 'Offre ordinaire'),"
                "('offre_special', 'Offre spéciale'),"
                "('demande', 'Demande'),"
                "('offre_ponctuel', 'Offre ponctuelle')]"
            ),
        )
        db_column.update_column(
            "tbl_echange_service",
            "remarque",
        )
        db_column.update_column(
            "tbl_echange_service",
            "commentaire",
        )

        # tbl_fichier
        db_table.update_table(
            "tbl_fichier",
            new_rec_name="nom",
            new_model_name="organization.fichier",
            menu_group="Document",
            menu_parent="Organization",
        )
        db_column.update_column(
            "tbl_fichier",
            "id_fichier",
            delete=True,
        )
        db_column.update_column(
            "tbl_fichier",
            "id_typefichier",
            new_field_name="type_fichier",
            new_description="Type fichier",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_fichier",
            "noorganization",
            new_field_name="organization",
            new_description="Organization",
        )
        db_column.update_column(
            "tbl_fichier",
            "nomfichierstokage",
            new_field_name="fichier",
            new_description="Fichier",
            new_type="binary",
            path_binary="/organization_canada/Intranet/document/doc",
        )
        db_column.update_column(
            "tbl_fichier",
            "nomfichieroriginal",
            new_field_name="nom",
            new_description="Nom",
        )
        db_column.update_column(
            "tbl_fichier",
            "si_admin",
            new_type="boolean",
            new_description="Admin",
        )
        db_column.update_column(
            "tbl_fichier",
            "si_organizationlocalseulement",
            new_type="boolean",
            new_field_name="si_organization_local_seulement",
            new_description="Organization local seulement",
        )
        db_column.update_column(
            "tbl_fichier",
            "si_disponible",
            new_type="boolean",
            new_description="Disponible",
        )
        db_column.update_column(
            "tbl_fichier",
            "datemaj_fichier",
            new_field_name="date_mise_a_jour",
            new_description="Dernière mise à jour",
            new_help="Date de la dernière mise à jour",
        )

        # tbl_fournisseur
        db_table.update_table(
            "tbl_fournisseur",
            delete=True,
            # new_rec_name="description",
            # new_model_name="organization.fournisseur",
        )

        # tbl_fournisseur_produit
        db_table.update_table(
            "tbl_fournisseur_produit",
            delete=True,
            # new_rec_name="description",
            # new_model_name="organization.fournisseur.produit",
        )

        # tbl_fournisseur_produit_commande
        db_table.update_table(
            "tbl_fournisseur_produit_commande",
            delete=True,
            # new_rec_name="description",
            # new_model_name="organization.fournisseur.produit.commande",
        )

        # tbl_fournisseur_produit_pointservice
        db_table.update_table(
            "tbl_fournisseur_produit_pointservice",
            delete=True,
            # new_rec_name="description",
            # new_model_name="organization.fournisseur.produit.pointservice",
        )

        # tbl_info_logiciel_bd
        db_table.update_table(
            "tbl_info_logiciel_bd",
            delete=True,
        )

        # tbl_log_acces
        db_table.update_table(
            "tbl_log_acces",
            delete=True,
        )

        # tbl_membre
        db_table.update_table(
            "tbl_membre",
            # new_rec_name="nom_complet",
            new_model_name="organization.membre",
            menu_group="Membre",
            menu_parent="Organization",
        )
        db_column.update_column(
            "tbl_membre",
            "nomembre",
            delete=True,
        )
        db_column.update_column(
            "tbl_membre",
            "nocartier",
            new_field_name="quartier",
            new_description="Quartier",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_membre",
            "noorganization",
            new_field_name="organization",
            new_description="Organization",
            new_help="Organization associée",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_membre",
            "nopointservice",
            new_field_name="point_service",
            new_description="Point de service",
            new_help="Point de service associé",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_membre",
            "notypecommunication",
            new_field_name="type_communication",
            new_description="Type de communications",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_membre",
            "nooccupation",
            new_field_name="occupation",
            new_description="Occupation",
            add_one2many=True,
            is_hide_blacklist_list_view=True,
        )
        db_column.update_column(
            "tbl_membre",
            "noorigine",
            new_field_name="origine",
            new_description="Origine",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_membre",
            "nosituationmaison",
            new_field_name="situation_maison",
            new_description="Situation maison",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_membre",
            "noprovenance",
            new_field_name="provenance",
            new_description="Provenance",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_membre",
            "norevenufamilial",
            new_field_name="revenu_familial",
            new_description="Revenu familial",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_membre",
            "noarrondissement",
            new_field_name="arrondissement",
            new_description="Arrondissement",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_membre",
            "noville",
            new_field_name="ville",
            new_description="Ville",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_membre",
            "noregion",
            new_field_name="region",
            new_description="Région",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_membre",
            "membreca",
            new_field_name="membre_ca",
            new_description="Membre du CA",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_membre",
            "partsocialpaye",
            new_field_name="part_social_paye",
            new_description="Part social payé",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_membre",
            "codepostal",
        )
        db_column.update_column(
            "tbl_membre",
            "dateadhesion",
            new_field_name="date_adhesion",
            new_description="Date de l'adhésion",
        )
        # db_column.update_column(
        #     "tbl_membre",
        #     "nom",
        #     new_required=True,
        # )
        db_column.update_column(
            "tbl_membre",
            "prenom",
            new_description="Prénom",
        )
        db_column.update_column(
            "tbl_membre",
            "adresse",
        )
        db_column.update_column(
            "tbl_membre",
            "telephone1",
            new_field_name="telephone_1",
            new_description="1er téléphone",
        )
        db_column.update_column(
            "tbl_membre",
            "postetel1",
            new_field_name="telephone_poste_1",
            new_description="1er poste téléphone",
        )
        db_column.update_column(
            "tbl_membre",
            "notypetel1",
            new_field_name="telephone_type_1",
            new_description="1er type de téléphones",
            add_one2many=True,
            one2many_description="Membre 1",
        )
        db_column.update_column(
            "tbl_membre",
            "telephone2",
            new_field_name="telephone_2",
            new_description="2e téléphone",
        )
        db_column.update_column(
            "tbl_membre",
            "postetel2",
            new_field_name="telephone_poste_2",
            new_description="2 poste téléphone",
        )
        db_column.update_column(
            "tbl_membre",
            "notypetel2",
            new_field_name="telephone_type_2",
            new_description="2e type de téléphones",
            add_one2many=True,
            one2many_description="Membre 2",
        )
        db_column.update_column(
            "tbl_membre",
            "telephone3",
            new_field_name="telephone_3",
            new_description="3e téléphone",
        )
        db_column.update_column(
            "tbl_membre",
            "postetel3",
            new_field_name="telephone_poste_3",
            new_description="3 poste téléphone",
        )
        db_column.update_column(
            "tbl_membre",
            "notypetel3",
            new_field_name="telephone_type_3",
            new_description="3e type de téléphones",
            add_one2many=True,
            one2many_description="Membre 3",
        )
        db_column.update_column(
            "tbl_membre",
            "courriel",
        )
        db_column.update_column(
            "tbl_membre",
            "achatregrouper",
            new_field_name="achat_regrouper",
            new_description="Achat regroupé",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_membre",
            "pretactif",
            new_field_name="pret_actif",
            new_description="Prêt actif",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_membre",
            "pretradier",
            new_field_name="pret_radier",
            new_description="Prêt radié",
            new_type="boolean",
            ignore_field=True,
        )
        db_column.update_column(
            "tbl_membre",
            "pretpayer",
            new_field_name="pret_payer",
            new_description="Prêt payé",
            new_type="boolean",
            ignore_field=True,
        )
        db_column.update_column(
            "tbl_membre",
            "etatcomptecourriel",
            ignore_field=True,
        )
        db_column.update_column(
            "tbl_membre",
            "bottintel",
            new_field_name="bottin_tel",
            new_description="Bottin téléphone",
            new_type="boolean",
            is_hide_blacklist_list_view=True,
        )
        db_column.update_column(
            "tbl_membre",
            "bottincourriel",
            new_field_name="bottin_courriel",
            new_description="Bottin courriel",
            new_type="boolean",
            is_hide_blacklist_list_view=True,
        )
        db_column.update_column(
            "tbl_membre",
            "membreactif",
            new_field_name="active",
            new_description="Actif",
            new_type="boolean",
            new_default_value="True",
            force_widget="boolean_button",
            new_help=(
                "Lorsque non actif, ce membre n'est plus en"
                " fonction, mais demeure accessible."
            ),
        )
        db_column.update_column(
            "tbl_membre",
            "membreconjoint",
            new_field_name="membre_conjoint",
            new_description="A un membre conjoint",
            new_type="boolean",
            is_hide_blacklist_list_view=True,
        )
        db_column.update_column(
            "tbl_membre",
            "nomembreconjoint",
            new_field_name="membre_conjoint_id",
            new_description="Membre conjoint",
            is_hide_blacklist_list_view=True,
        )
        db_column.update_column(
            "tbl_membre",
            "memo",
            new_description="Mémo",
            is_hide_blacklist_list_view=True,
        )
        db_column.update_column(
            "tbl_membre",
            "sexe",
            new_type="selection",
            is_hide_blacklist_list_view=True,
            # TODO add default pour autre
            new_selection=(
                "[('femme', 'Femme'),('homme', 'Homme'),('autre', 'Autre')]"
            ),
        )
        db_column.update_column(
            "tbl_membre",
            "anneenaissance",
            new_field_name="annee_naissance",
            new_description="Année de naissance",
            is_hide_blacklist_list_view=True,
        )
        db_column.update_column(
            "tbl_membre",
            "precisezorigine",
            ignore_field=True,
        )
        db_column.update_column(
            "tbl_membre",
            "nomutilisateur",
            new_field_name="nom_utilisateur",
            new_description="Nom du compte",
        )
        # Configuration for test
        # db_column.update_column(
        #     "tbl_membre",
        #     "motdepasse",
        #     sql_select_modify=f"DECODE(motdepasse,'{SECRET_PASSWORD}')",
        # )
        # Always keep this configuration
        db_column.update_column(
            "tbl_membre",
            "motdepasse",
            ignore_field=True,
        )
        db_column.update_column(
            "tbl_membre",
            "profilapprouver",
            new_field_name="profil_approuver",
            new_description="Profil approuvé",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_membre",
            "membreprinc",
            new_field_name="membre_principal",
            new_description="Membre principal",
            new_type="boolean",
            is_hide_blacklist_list_view=True,
        )
        db_column.update_column(
            "tbl_membre",
            "nomorganization",
            ignore_field=True,
        )
        db_column.update_column(
            "tbl_membre",
            "recevoircourrielgrp",
            new_field_name="recevoir_courriel_groupe",
            new_description="Veut recevoir courriel de groupes",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_membre",
            "pascommunication",
            new_field_name="pas_communication",
            new_description="Pas de communication",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_membre",
            "descriptionorganizateur",
            new_field_name="description_membre",
            new_description="Description du membre",
            new_type="boolean",
            is_hide_blacklist_list_view=True,
        )
        db_column.update_column(
            "tbl_membre",
            "estunpointservice",
            new_field_name="est_un_point_service",
            new_description="Est un point de service",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_membre",
            "date_maj_membre",
            new_field_name="date_mise_a_jour",
            new_description="Dernière mise à jour",
            new_help="Date de la dernière mise à jour",
        )
        db_column.update_column(
            "tbl_membre",
            "transferede",
            new_field_name="transfert_organization",
            new_description="Transfert d'une Organization",
        )
        # db_column.update_column(
        #     "tbl_membre",
        #     "",
        #     new_field_name="nom_complet",
        #     new_type="char",
        #     new_description="Nom complet",
        #     new_help="TODO",
        #     new_compute="_compute_nom_complet"
        # )

        # tbl_mensualite
        db_table.update_table(
            "tbl_mensualite",
            delete=True,
        )

        # tbl_occupation
        db_table.update_table(
            "tbl_occupation",
            new_rec_name="nom",
            new_model_name="organization.occupation",
            nomenclator=True,
            menu_group="Statistique",
            menu_parent="Organization",
        )
        db_column.update_column(
            "tbl_occupation",
            "nooccupation",
            delete=True,
        )
        db_column.update_column(
            "tbl_occupation",
            "occupation",
            new_field_name="nom",
        )

        # tbl_offre_service_membre
        db_table.update_table(
            "tbl_offre_service_membre",
            new_rec_name="description",
            new_model_name="organization.offre.service",
            menu_group="Service",
            menu_parent="Service",
            menu_label="Offre de services",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "nooffreservicemembre",
            delete=True,
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "nomembre",
            new_field_name="membre",
            new_description="Membre",
            new_help="Membre qui offre le service",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "noorganization",
            new_field_name="organization",
            new_description="Organization",
            new_help="Organization associée",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "nocategoriesouscategorie",
            new_field_name="type_service_id",
            new_description="Type de services",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "titreoffrespecial",
            new_field_name="nom_offre_special",
            new_description="Nom de l'offre spéciale",
            new_help="Nom ou brève description de l'offre spéciale",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "conditionx",
            new_field_name="condition_autre",
            new_description="Condition autres",
            new_help="Autres conditions à informer",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "disponibilite",
            new_description="Disponibilité",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "tarif",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "description",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "dateaffichage",
            new_field_name="date_affichage",
            new_description="Date d'affichage",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "datedebut",
            new_field_name="date_debut",
            new_description="Date de début",
            new_help="Date à partir de laquelle l'offre est valide.",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "datefin",
            new_field_name="date_fin",
            new_description="Date de fin",
            new_help="Date jusqu'à laquelle l'offre est valide.",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "approuve",
            new_field_name="approuve",
            new_description="Approuvé",
            new_type="boolean",
            new_help="Permet d'approuver ce type de services.",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "offrespecial",
            new_field_name="offre_special",
            new_description="Offre spéciale",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "supprimer",
            new_field_name="active",
            new_description="Actif",
            new_type="boolean",
            new_default_value="True",
            force_widget="boolean_button",
            new_help=(
                "Lorsque non actif, cet offre de services n'est plus en"
                " fonction, mais demeure accessible."
            ),
            compute_data_function="""not active""",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "fait",
            new_field_name="accompli",
            new_description="Accomplie",
            new_help="Cette offre de service est réalisée.",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "conditionoffre",
            new_field_name="condition",
            new_description="Conditions",
            new_help="Conditions inhérentes à l'offre",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "nbfoisconsulteroffremembre",
            new_field_name="nb_consultation",
            new_description="Nombre de consultations",
        )
        db_column.update_column(
            "tbl_offre_service_membre",
            "datemaj_servicemembre",
            new_field_name="date_mise_a_jour",
            new_description="Dernière mise à jour",
            new_help="Date de la dernière mise à jour",
        )

        # tbl_origine
        db_table.update_table(
            "tbl_origine",
            new_rec_name="nom",
            new_model_name="organization.origine",
            nomenclator=True,
            menu_group="Statistique",
            menu_parent="Organization",
        )
        db_column.update_column(
            "tbl_origine",
            "noorigine",
            delete=True,
        )
        db_column.update_column(
            "tbl_origine",
            "origine",
            new_field_name="nom",
        )

        # tbl_pointservice
        db_table.update_table(
            "tbl_pointservice",
            new_rec_name="nom",
            new_model_name="organization.point.service",
            menu_group="Organization",
            menu_parent="Organization",
            menu_label="Point de services",
        )
        db_column.update_column(
            "tbl_pointservice",
            "nopointservice",
            delete=True,
        )
        db_column.update_column(
            "tbl_pointservice",
            "nompointservice",
            new_field_name="nom",
            new_description="Nom",
            new_help="Nom du point de service",
        )
        db_column.update_column(
            "tbl_pointservice",
            "ordrepointservice",
            new_field_name="sequence",
            new_description="Séquence",
            new_help="Séquence d'affichage",
            is_hide_blacklist_list_view=True,
        )
        db_column.update_column(
            "tbl_pointservice",
            "notegrpachatpageclient",
            ignore_field=True,
        )
        db_column.update_column(
            "tbl_pointservice",
            "datemaj_pointservice",
            new_field_name="date_mise_a_jour",
            new_description="Dernière mise à jour",
            new_help="Date de la dernière mise à jour",
        )
        db_column.update_column(
            "tbl_pointservice",
            "noorganization",
            new_field_name="organization",
            new_description="Organization",
        )
        # db_column.update_column(
        #     "tbl_pointservice",
        #     "noarrondissement",
        # )
        # db_column.update_column(
        #     "tbl_pointservice",
        #     "noville",
        # )
        # db_column.update_column(
        #     "tbl_pointservice",
        #     "noregion",
        # )
        # db_column.update_column(
        #     "tbl_pointservice",
        #     "codepostale",
        # )
        # db_column.update_column(
        #     "tbl_pointservice",
        #     "dateadhesion",
        # )
        # db_column.update_column(
        #     "tbl_pointservice",
        #     "adresse",
        # )
        # db_column.update_column(
        #     "tbl_pointservice",
        #     "telephone1",
        # )
        # db_column.update_column(
        #     "tbl_pointservice",
        #     "telephone2",
        # )
        # db_column.update_column(
        #     "tbl_pointservice",
        #     "courriel",
        # )
        # db_column.update_column(
        #     "tbl_pointservice",
        #     "recevoircourrielgrp",
        # )

        # tbl_pointservice_fournisseur
        db_table.update_table(
            "tbl_pointservice_fournisseur",
            delete=True,
            # new_rec_name="description",
            # new_model_name="organization.pointservice.fournisseur",
        )

        # tbl_pret
        db_table.update_table(
            "tbl_pret",
            delete=True,
        )

        # tbl_produit
        db_table.update_table(
            "tbl_produit",
            delete=True,
            # new_rec_name="description",
            # new_model_name="organization.produit",
        )

        # tbl_provenance
        db_table.update_table(
            "tbl_provenance",
            new_rec_name="nom",
            new_model_name="organization.provenance",
            nomenclator=True,
            menu_group="Statistique",
            menu_parent="Organization",
        )
        db_column.update_column(
            "tbl_provenance",
            "noprovenance",
            delete=True,
        )
        db_column.update_column(
            "tbl_provenance",
            "provenance",
            new_field_name="nom",
        )

        # tbl_region
        db_table.update_table(
            "tbl_region",
            new_rec_name="nom",
            new_model_name="organization.region",
            nomenclator=True,
            menu_group="Location",
            menu_parent="Configuration",
            menu_label="Région",
        )
        db_column.update_column(
            "tbl_region",
            "noregion",
            new_field_name="code",
            new_description="Code de région",
            new_help="Code de la région administrative",
        )
        db_column.update_column(
            "tbl_region",
            "region",
            new_field_name="nom",
            new_description="Nom",
        )

        # tbl_revenu_familial
        # TODO bug field name est encore là
        db_table.update_table(
            "tbl_revenu_familial",
            new_rec_name="nom",
            new_model_name="organization.revenu.familial",
            nomenclator=True,
            menu_group="Statistique",
            menu_parent="Organization",
        )
        db_column.update_column(
            "tbl_revenu_familial",
            "norevenufamilial",
            delete=True,
        )
        db_column.update_column(
            "tbl_revenu_familial",
            "revenu",
            new_field_name="nom",
        )

        # tbl_situation_maison
        db_table.update_table(
            "tbl_situation_maison",
            new_rec_name="nom",
            new_model_name="organization.situation.maison",
            nomenclator=True,
            menu_group="Statistique",
            menu_parent="Organization",
        )
        db_column.update_column(
            "tbl_situation_maison",
            "nosituationmaison",
            delete=True,
        )
        db_column.update_column(
            "tbl_situation_maison",
            "situation",
            new_field_name="nom",
        )

        # tbl_sous_categorie
        db_table.update_table(
            "tbl_sous_categorie",
            new_model_name="organization.type.service.sous.categorie",
            new_rec_name="nom",
            new_description="Type de services sous-catégorie",
            nomenclator=True,
            menu_group="Catégorie de services",
            menu_parent="Service",
            menu_label="Sous-catégorie de services",
        )
        db_column.update_column(
            "tbl_sous_categorie",
            "nosouscategorieid",
            delete=True,
        )
        db_column.update_column(
            "tbl_sous_categorie",
            "nosouscategorie",
            new_field_name="sous_categorie_service",
            new_description="Sous-catégorie",
        )
        db_column.update_column(
            "tbl_sous_categorie",
            "nocategorie",
            new_field_name="categorie",
            new_description="Catégorie",
            add_one2many=True,
        )
        db_column.update_column(
            "tbl_sous_categorie",
            "titresouscategorie",
            new_field_name="nom",
            new_description="Nom",
            compute_data_function="""nom.replace("&#8217;", "'").strip()""",
        )
        db_column.update_column(
            "tbl_sous_categorie",
            "supprimer",
            new_field_name="active",
            new_description="Actif",
            new_type="boolean",
            new_default_value="True",
            force_widget="boolean_button",
            new_help=(
                "Lorsque non actif, cette sous-catégorie n'est plus en"
                " fonction, mais demeure accessible."
            ),
            compute_data_function="""not active""",
        )
        db_column.update_column(
            "tbl_sous_categorie",
            "approuver",
            new_field_name="approuver",
            new_description="Approuvé",
            new_type="boolean",
            new_help="Permet d'approuver cette sous-catégorie.",
        )

        # tbl_taxe
        db_table.update_table(
            "tbl_taxe",
            delete=True,
            # new_model_name="organization.taxe"
            # "taxe", new_model_name="organization.taxe", new_rec_name="nom_complet"
        )

        # tbl_titre
        db_table.update_table(
            "tbl_titre",
            new_rec_name="nom",
            new_model_name="organization.titre",
            nomenclator=True,
            delete=True,
        )
        db_column.update_column(
            "tbl_titre",
            "notitre",
            delete=True,
        )
        db_column.update_column(
            "tbl_titre",
            "titre",
            new_field_name="nom",
        )
        db_column.update_column(
            "tbl_titre",
            "visible_titre",
        )
        db_column.update_column(
            "tbl_titre",
            "datemaj_titre",
        )

        # tbl_type_communication
        db_table.update_table(
            "tbl_type_communication",
            new_rec_name="nom",
            new_model_name="organization.type.communication",
            nomenclator=True,
            menu_group="Statistique",
            menu_parent="Organization",
            menu_label="Type de communications",
        )
        db_column.update_column(
            "tbl_type_communication",
            "notypecommunication",
            delete=True,
        )
        db_column.update_column(
            "tbl_type_communication",
            "typecommunication",
            new_field_name="nom",
        )

        # tbl_type_compte
        db_table.update_table(
            "tbl_type_compte",
            new_model_name="organization.type.compte",
            menu_group="Configuration",
            menu_parent="Configuration",
            menu_label="Type de comptes membre",
        )
        db_column.update_column(
            "tbl_type_compte",
            "nomembre",
            new_required=False,
            new_field_name="membre",
            new_description="Membre",
        )
        db_column.update_column(
            "tbl_type_compte",
            "organizateursimple",
            new_field_name="organizateur_simple",
            new_description="Organizateur simple",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_type_compte",
            "admin",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_type_compte",
            "adminchef",
            new_field_name="admin_chef",
            new_description="Admin chef",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_type_compte",
            "reseau",
            new_description="Réseau",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_type_compte",
            "spip",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_type_compte",
            "adminpointservice",
            new_field_name="admin_point_service",
            new_description="Administrateur point service",
            new_type="boolean",
        )
        db_column.update_column(
            "tbl_type_compte",
            "adminordpointservice",
            new_field_name="admin_ord_point_service",
            new_description="Administrateur ordinaire point service",
            new_type="boolean",
        )

        # tbl_type_fichier
        db_table.update_table(
            "tbl_type_fichier",
            new_rec_name="nom",
            new_model_name="organization.type.fichier",
            nomenclator=True,
            menu_group="Document",
            menu_parent="Organization",
            menu_label="Type de fichiers",
        )
        db_column.update_column(
            "tbl_type_fichier",
            "id_typefichier",
            delete=True,
        )
        db_column.update_column(
            "tbl_type_fichier",
            "typefichier",
            new_field_name="nom",
            new_description="Nom",
        )
        db_column.update_column(
            "tbl_type_fichier",
            "datemaj_typefichier",
            new_field_name="date_mise_a_jour",
            new_description="Dernière mise à jour",
            new_help="Date de la dernière mise à jour",
        )

        # tbl_type_tel
        db_table.update_table(
            "tbl_type_tel",
            new_rec_name="nom",
            new_model_name="organization.type.telephone",
            nomenclator=True,
            menu_group="Statistique",
            menu_parent="Organization",
            menu_label="Type de téléphones",
        )
        db_column.update_column(
            "tbl_type_tel",
            "notypetel",
            delete=True,
        )
        db_column.update_column(
            "tbl_type_tel",
            "typetel",
            new_field_name="nom",
            new_description="Nom",
        )

        # tbl_versement
        db_table.update_table(
            "tbl_versement",
            delete=True,
        )

        # tbl_ville
        db_table.update_table(
            "tbl_ville",
            new_rec_name="nom",
            new_model_name="organization.ville",
            nomenclator=True,
            menu_group="Location",
            menu_parent="Configuration",
        )
        db_column.update_column(
            "tbl_ville",
            "noville",
            new_field_name="code",
            new_description="Code",
            new_help="Code de la ville",
        )
        db_column.update_column(
            "tbl_ville",
            "ville",
            new_field_name="nom",
            new_description="Nom",
        )
        db_column.update_column(
            "tbl_ville",
            "noregion",
            new_field_name="region",
            new_description="Région",
            add_one2many=True,
        )

        # # vue_membre_qc
        # db_table.update_table(
        #     "Vue_Membre_Qc",
        #     delete=True,
        # )
        #
        # # vue_membre_tr
        # db_table.update_table(
        #     "Vue_Membre_TR",
        #     delete=True,
        # )

        code_generator_db_tables = (
            env["code.generator.db.table"]
            # .search([("name", "in", ("tbl_membre", "tbl_pointservice"))])
            # .search([]).filtered(lambda x: x.name not in lst_table_to_delete)
            .search([])
        )

        # lst_nomenclator = (
        #     # "tbl_organization",
        #     # # "tbl_achat_ponctuel",
        #     # # "tbl_achat_ponctuel_produit",
        #     "tbl_region",
        #     "tbl_ville",
        #     "tbl_arrondissement",
        #     "tbl_cartier",
        #     "tbl_categorie",
        #     "tbl_categorie_sous_categorie",
        #     # # "tbl_commande",
        #     # # "tbl_commande_membre",
        #     # # "tbl_commande_membre_produit",
        #     # # "tbl_commentaire",
        #     # # "tbl_demande_service",
        #     # # "tbl_dmd_adhesion",
        #     # # "tbl_droits_admin",
        #     # # "tbl_echange_service",
        #     # "tbl_fichier",
        #     # # "tbl_fournisseur",
        #     # # "tbl_fournisseur_produit",
        #     # # "tbl_fournisseur_produit_commande",
        #     # # "tbl_fournisseur_produit_pointservice",
        #     # "tbl_info_logiciel_bd",
        #     # # "tbl_log_acces",
        #     # "tbl_membre",
        #     # "tbl_mensualite",
        #     "tbl_occupation",
        #     # # "tbl_offre_service_membre",
        #     "tbl_origine",
        #     # "tbl_pointservice",
        #     # # "tbl_pointservice_fournisseur",
        #     # # "tbl_pret",
        #     # # "tbl_produit",
        #     "tbl_provenance",
        #     "tbl_revenu_familial",
        #     "tbl_situation_maison",
        #     "tbl_sous_categorie",
        #     # "tbl_taxe",
        #     "tbl_titre",
        #     "tbl_type_communication",
        #     # # "tbl_type_compte",
        #     "tbl_type_fichier",
        #     "tbl_type_tel",
        #     # # "tbl_versement",
        # )
        # # lst_nomenclator = []
        #
        # if lst_nomenclator:
        #     for db_table_id in code_generator_db_tables:
        #         if db_table_id.name in lst_nomenclator:
        #             db_table_id.nomenclator = True

        after_time = time.process_time()
        _logger.info(
            "DEBUG time execution hook update model db before generate_module"
            f" {after_time - before_time}"
        )

        lst_code_generator_id = code_generator_db_tables.generate_module(
            code_generator_id=code_generator_id
        )

        lst_value_code = []
        # Add new field tbl_membre nom_complet
        str_code = """for rec in self:
            rec.nom_complet = False
            if rec.est_un_point_service:
                rec.nom_complet = f"Point de service {rec.point_service.nom}"
            else:
                if rec.nom and rec.prenom:
                    rec.nom_complet = f"{rec.prenom} {rec.nom}"
                elif rec.nom:
                    rec.nom_complet = f"{rec.nom}"
                elif rec.prenom:
                    rec.nom_complet = f"{rec.prenom}"
        """
        code_id = generate_rec_name_code_compute(
            env,
            "tbl_membre",
            code_generator_id,
            "nom_complet",
            ("nom", "prenom", "est_un_point_service", "point_service"),
            str_code,
        )
        if code_id:
            lst_value_code.append(code_id)

        # Add new field tbl_droits_admin nom_complet
        str_code = """for rec in self:
            if rec.membre:
                rec.nom_complet = rec.membre.nom_complet
            else:
                rec.nom_complet = False
        """
        code_id = generate_rec_name_code_compute(
            env,
            "tbl_droits_admin",
            code_generator_id,
            "nom_complet",
            "membre",
            str_code,
        )
        if code_id:
            lst_value_code.append(code_id)

        # Add new field tbl_echange_service nom_complet
        str_code = """for rec in self:
            value = ""
            if rec.type_echange:
                value += rec.type_echange
            if rec.point_service and rec.point_service.nom:
                if rec.type_echange:
                    value += " - "
                value += rec.point_service.nom
            if not value:
                value = False
            rec.nom_complet = value
        """
        code_id = generate_rec_name_code_compute(
            env,
            "tbl_echange_service",
            code_generator_id,
            "nom_complet",
            ("type_echange", "point_service"),
            str_code,
        )
        if code_id:
            lst_value_code.append(code_id)

        # Add new field tbl_dmd_adhesion nom_complet
        str_code = """for rec in self:
            if rec.nom and rec.prenom:
                rec.nom_complet = f"{rec.prenom} {rec.nom}"
            elif rec.nom:
                rec.nom_complet = f"{rec.nom}"
            elif rec.prenom:
                rec.nom_complet = f"{rec.prenom}"
            else:
                rec.nom_complet = False
        """
        code_id = generate_rec_name_code_compute(
            env,
            "tbl_dmd_adhesion",
            code_generator_id,
            "nom_complet",
            ("nom", "prenom"),
            str_code,
        )
        if code_id:
            lst_value_code.append(code_id)

        # Add new field tbl_commentaire nom_complet
        str_code = """for rec in self:
            value = ""
            if rec.number:
                value += str(rec.number)
            if rec.number and (rec.type_offre or rec.degre_satisfaction):
                value += " - "
            if rec.type_offre:
                value += str(rec.type_offre)
            if rec.type_offre and rec.degre_satisfaction:
                value += " - "
            if rec.degre_satisfaction:
                value += str(rec.degre_satisfaction)
            if not value:
                value = False
            rec.nom_complet = value
        """
        code_id = generate_rec_name_code_compute(
            env,
            "tbl_commentaire",
            code_generator_id,
            "nom_complet",
            ("type_offre", "number", "degre_satisfaction"),
            str_code,
        )
        if code_id:
            lst_value_code.append(code_id)

        # Add new field tbl_categorie_sous_categorie identifiant
        str_code = """for rec in self:
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
        """
        code_id = generate_rec_name_code_compute(
            env,
            "tbl_categorie_sous_categorie",
            code_generator_id,
            "identifiant",
            ("sous_categorie_id", "sous_categorie_id.categorie", "numero"),
            str_code,
            update_rec_name=False,
        )
        if code_id:
            lst_value_code.append(code_id)

        # Add new field tbl_categorie_sous_categorie nom_complet
        str_code = """for rec in self:
            value = ""
            if rec.identifiant:
               value += rec.identifiant
            if rec.identifiant and rec.nom:
                value += " - "
            if rec.nom:
               value += rec.nom
            rec.nom_complet = value
        """
        code_id = generate_rec_name_code_compute(
            env,
            "tbl_categorie_sous_categorie",
            code_generator_id,
            "nom_complet",
            ("nom", "identifiant"),
            str_code,
        )
        if code_id:
            lst_value_code.append(code_id)

        # Add new field tbl_taxe nom_complet
        # str_code = """for rec in self:
        #     value = ""
        #     if rec.tauxtaxepro:
        #         value += str(rec.tauxtaxepro)
        #     if rec.tauxtaxepro and rec.tauxtaxefed:
        #         value += " - "
        #     if rec.tauxtaxefed:
        #         value += str(rec.tauxtaxefed)
        #     rec.nom_complet = value
        # """
        # code_id = generate_rec_name_code_compute(
        #     env,
        #     "tbl_taxe",
        #     code_generator_id,
        #     "nom_complet",
        #     ("tauxtaxepro", "tauxtaxefed"),
        #     str_code,
        # )
        # if code_id:
        #     lst_value_code.append(code_id)

        # Add new field tbl_type_compte nom_complet
        str_code = """for rec in self:
            value = ""
            if rec.membre:
                value += rec.membre.nom_complet
            if not value:
                value = False
            rec.nom_complet = value
        """
        #  str_code = """for rec in self:
        #     value = ""
        #     value += str(rec.organizateursimple)
        #     value += str(rec.admin)
        #     value += str(rec.adminchef)
        #     value += str(rec.reseau)
        #     value += str(rec.spip)
        #     value += str(rec.adminpointservice)
        #     value += str(rec.adminordpointservice)
        #     rec.nom_complet = value
        # """
        code_id = generate_rec_name_code_compute(
            env,
            "tbl_type_compte",
            code_generator_id,
            "nom_complet",
            # (
            #     "organizateursimple",
            #     "admin",
            #     "adminchef",
            #     "reseau",
            #     "spip",
            #     "adminpointservice",
            #     "adminordpointservice",
            # ),
            "membre",
            str_code,
        )
        if code_id:
            lst_value_code.append(code_id)

        env["code.generator.model.code"].create(lst_value_code)

        # Generate view
        # Action generate view
        wizard_view = env["code.generator.generate.views.wizard"].create(
            {
                "code_generator_id": code_generator_id.id,
                "enable_generate_all": True,
                "portal_enable_create": True,
            }
        )

        wizard_view.button_generate_views()

        # Generate module
        value = {"code_generator_ids": code_generator_id.ids}
        env["code.generator.writer"].create(value)


def generate_rec_name_code_compute(
    env,
    tbl_name,
    code_generator_id,
    new_field_name,
    api_depend,
    str_code,
    ttype="char",
    update_rec_name=True,
):
    model_name = env["code.generator.db.table"].search(
        [("name", "=", tbl_name)]
    )
    model_id = env["ir.model"].search([("model", "=", model_name.model_name)])
    if model_id:
        method_name = f"_compute_{new_field_name}"
        # TODO add variable to create field without export data
        value_field = {
            "name": new_field_name,
            "field_description": new_field_name.replace("_", " ").capitalize(),
            "ttype": ttype,
            "code_generator_compute": method_name,
            "model_id": model_id.id,
        }
        env["ir.model.fields"].create(value_field)
        if update_rec_name:
            model_id.rec_name = new_field_name
        for field_id in model_id.field_id:
            if field_id.name == "name":
                field_id.unlink()
                continue

        # Compute all data
        # TODO don't compute if contain no data
        record_ids = (
            env[model_id.model].with_context(active_test=False).search([])
        )
        if record_ids:
            exec(str_code, {"self": record_ids})

        if type(api_depend) is tuple:
            if len(api_depend) == 1:
                item_decorator = f'("{api_depend[0]}")'
            else:
                item_decorator = api_depend
        elif type(api_depend) is str:
            item_decorator = f'("{api_depend}")'
        else:
            _logger.warning(
                f"Cannot support type '{type(api_depend)}' for api_depend."
            )
            item_decorator = "()"
        decorator = f"@api.depends{item_decorator}"

        return {
            "code": str_code,
            "name": method_name,
            "decorator": decorator,
            "param": "self",
            "sequence": 1,
            "m2o_module": code_generator_id.id,
            "m2o_model": model_id.id,
        }
    else:
        _logger.error(f"Cannot find model from table {tbl_name}")


def uninstall_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        code_generator_id = env["code.generator.module"].search(
            [("name", "=", MODULE_NAME)]
        )
        if code_generator_id:
            code_generator_id.unlink()
