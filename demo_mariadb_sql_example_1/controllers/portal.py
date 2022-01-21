from collections import OrderedDict
from operator import itemgetter

from odoo import _, http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.osv.expression import OR
from odoo.tools import groupby as groupbyelem


class DemoMariadbSqlExample1Controller(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super(
            DemoMariadbSqlExample1Controller, self
        )._prepare_portal_layout_values()
        values["organization_arrondissement_count"] = request.env[
            "organization.arrondissement"
        ].search_count([])
        values["organization_commentaire_count"] = request.env[
            "organization.commentaire"
        ].search_count([])
        values["organization_demande_adhesion_count"] = request.env[
            "organization.demande.adhesion"
        ].search_count([])
        values["organization_demande_service_count"] = request.env[
            "organization.demande.service"
        ].search_count([])
        values["organization_droits_admin_count"] = request.env[
            "organization.droits.admin"
        ].search_count([])
        values["organization_echange_service_count"] = request.env[
            "organization.echange.service"
        ].search_count([])
        values["organization_fichier_count"] = request.env[
            "organization.fichier"
        ].search_count([])
        values["organization_membre_count"] = request.env[
            "organization.membre"
        ].search_count([])
        values["organization_occupation_count"] = request.env[
            "organization.occupation"
        ].search_count([])
        values["organization_offre_service_count"] = request.env[
            "organization.offre.service"
        ].search_count([])
        values["organization_organization_count"] = request.env[
            "organization.organization"
        ].search_count([])
        values["organization_origine_count"] = request.env[
            "organization.origine"
        ].search_count([])
        values["organization_point_service_count"] = request.env[
            "organization.point.service"
        ].search_count([])
        values["organization_provenance_count"] = request.env[
            "organization.provenance"
        ].search_count([])
        values["organization_quartier_count"] = request.env[
            "organization.quartier"
        ].search_count([])
        values["organization_region_count"] = request.env[
            "organization.region"
        ].search_count([])
        values["organization_revenu_familial_count"] = request.env[
            "organization.revenu.familial"
        ].search_count([])
        values["organization_situation_maison_count"] = request.env[
            "organization.situation.maison"
        ].search_count([])
        values["organization_type_communication_count"] = request.env[
            "organization.type.communication"
        ].search_count([])
        values["organization_type_compte_count"] = request.env[
            "organization.type.compte"
        ].search_count([])
        values["organization_type_fichier_count"] = request.env[
            "organization.type.fichier"
        ].search_count([])
        values["organization_type_service_count"] = request.env[
            "organization.type.service"
        ].search_count([])
        values["organization_type_service_categorie_count"] = request.env[
            "organization.type.service.categorie"
        ].search_count([])
        values["organization_type_service_sous_categorie_count"] = request.env[
            "organization.type.service.sous.categorie"
        ].search_count([])
        values["organization_type_telephone_count"] = request.env[
            "organization.type.telephone"
        ].search_count([])
        values["organization_ville_count"] = request.env[
            "organization.ville"
        ].search_count([])
        return values

    # ------------------------------------------------------------
    # My Organization Arrondissement
    # ------------------------------------------------------------
    def _organization_arrondissement_get_page_view_values(
        self, organization_arrondissement, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_arrondissement",
            "organization_arrondissement": organization_arrondissement,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_arrondissement,
            access_token,
            values,
            "my_organization_arrondissements_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_arrondissements",
            "/my/organization_arrondissements/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_arrondissements(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationArrondissement = request.env["organization.arrondissement"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.arrondissement", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_arrondissements count
        organization_arrondissement_count = (
            OrganizationArrondissement.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/organization_arrondissements",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_arrondissement_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_arrondissements = OrganizationArrondissement.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_arrondissements_history"
        ] = organization_arrondissements.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_arrondissements": organization_arrondissements,
                "page_name": "organization_arrondissement",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_arrondissements",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_arrondissements",
            values,
        )

    @http.route(
        [
            "/my/organization_arrondissement/<int:organization_arrondissement_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_arrondissement(
        self, organization_arrondissement_id=None, access_token=None, **kw
    ):
        try:
            organization_arrondissement_sudo = self._document_check_access(
                "organization.arrondissement",
                organization_arrondissement_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_arrondissement_get_page_view_values(
            organization_arrondissement_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_arrondissement",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Commentaire
    # ------------------------------------------------------------
    def _organization_commentaire_get_page_view_values(
        self, organization_commentaire, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_commentaire",
            "organization_commentaire": organization_commentaire,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_commentaire,
            access_token,
            values,
            "my_organization_commentaires_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_commentaires",
            "/my/organization_commentaires/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_commentaires(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationCommentaire = request.env["organization.commentaire"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.commentaire", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_commentaires count
        organization_commentaire_count = OrganizationCommentaire.search_count(
            domain
        )
        # pager
        pager = portal_pager(
            url="/my/organization_commentaires",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_commentaire_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_commentaires = OrganizationCommentaire.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_commentaires_history"
        ] = organization_commentaires.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_commentaires": organization_commentaires,
                "page_name": "organization_commentaire",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_commentaires",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_commentaires",
            values,
        )

    @http.route(
        ["/my/organization_commentaire/<int:organization_commentaire_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_commentaire(
        self, organization_commentaire_id=None, access_token=None, **kw
    ):
        try:
            organization_commentaire_sudo = self._document_check_access(
                "organization.commentaire",
                organization_commentaire_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_commentaire_get_page_view_values(
            organization_commentaire_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_commentaire",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Demande Adhesion
    # ------------------------------------------------------------
    def _organization_demande_adhesion_get_page_view_values(
        self, organization_demande_adhesion, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_demande_adhesion",
            "organization_demande_adhesion": organization_demande_adhesion,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_demande_adhesion,
            access_token,
            values,
            "my_organization_demande_adhesions_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_demande_adhesions",
            "/my/organization_demande_adhesions/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_demande_adhesions(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationDemandeAdhesion = request.env[
            "organization.demande.adhesion"
        ]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.demande.adhesion", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_demande_adhesions count
        organization_demande_adhesion_count = (
            OrganizationDemandeAdhesion.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/organization_demande_adhesions",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_demande_adhesion_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_demande_adhesions = OrganizationDemandeAdhesion.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_demande_adhesions_history"
        ] = organization_demande_adhesions.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_demande_adhesions": organization_demande_adhesions,
                "page_name": "organization_demande_adhesion",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_demande_adhesions",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_demande_adhesions",
            values,
        )

    @http.route(
        [
            "/my/organization_demande_adhesion/<int:organization_demande_adhesion_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_demande_adhesion(
        self, organization_demande_adhesion_id=None, access_token=None, **kw
    ):
        try:
            organization_demande_adhesion_sudo = self._document_check_access(
                "organization.demande.adhesion",
                organization_demande_adhesion_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_demande_adhesion_get_page_view_values(
            organization_demande_adhesion_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_demande_adhesion",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Demande Service
    # ------------------------------------------------------------
    def _organization_demande_service_get_page_view_values(
        self, organization_demande_service, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_demande_service",
            "organization_demande_service": organization_demande_service,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_demande_service,
            access_token,
            values,
            "my_organization_demande_services_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_demande_services",
            "/my/organization_demande_services/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_demande_services(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationDemandeService = request.env[
            "organization.demande.service"
        ]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.demande.service", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_demande_services count
        organization_demande_service_count = (
            OrganizationDemandeService.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/organization_demande_services",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_demande_service_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_demande_services = OrganizationDemandeService.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_demande_services_history"
        ] = organization_demande_services.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_demande_services": organization_demande_services,
                "page_name": "organization_demande_service",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_demande_services",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_demande_services",
            values,
        )

    @http.route(
        [
            "/my/organization_demande_service/<int:organization_demande_service_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_demande_service(
        self, organization_demande_service_id=None, access_token=None, **kw
    ):
        try:
            organization_demande_service_sudo = self._document_check_access(
                "organization.demande.service",
                organization_demande_service_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_demande_service_get_page_view_values(
            organization_demande_service_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_demande_service",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Droits Admin
    # ------------------------------------------------------------
    def _organization_droits_admin_get_page_view_values(
        self, organization_droits_admin, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_droits_admin",
            "organization_droits_admin": organization_droits_admin,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_droits_admin,
            access_token,
            values,
            "my_organization_droits_admins_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_droits_admins",
            "/my/organization_droits_admins/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_droits_admins(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationDroitsAdmin = request.env["organization.droits.admin"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.droits.admin", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_droits_admins count
        organization_droits_admin_count = OrganizationDroitsAdmin.search_count(
            domain
        )
        # pager
        pager = portal_pager(
            url="/my/organization_droits_admins",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_droits_admin_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_droits_admins = OrganizationDroitsAdmin.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_droits_admins_history"
        ] = organization_droits_admins.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_droits_admins": organization_droits_admins,
                "page_name": "organization_droits_admin",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_droits_admins",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_droits_admins",
            values,
        )

    @http.route(
        ["/my/organization_droits_admin/<int:organization_droits_admin_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_droits_admin(
        self, organization_droits_admin_id=None, access_token=None, **kw
    ):
        try:
            organization_droits_admin_sudo = self._document_check_access(
                "organization.droits.admin",
                organization_droits_admin_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_droits_admin_get_page_view_values(
            organization_droits_admin_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_droits_admin",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Echange Service
    # ------------------------------------------------------------
    def _organization_echange_service_get_page_view_values(
        self, organization_echange_service, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_echange_service",
            "organization_echange_service": organization_echange_service,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_echange_service,
            access_token,
            values,
            "my_organization_echange_services_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_echange_services",
            "/my/organization_echange_services/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_echange_services(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationEchangeService = request.env[
            "organization.echange.service"
        ]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.echange.service", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_echange_services count
        organization_echange_service_count = (
            OrganizationEchangeService.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/organization_echange_services",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_echange_service_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_echange_services = OrganizationEchangeService.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_echange_services_history"
        ] = organization_echange_services.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_echange_services": organization_echange_services,
                "page_name": "organization_echange_service",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_echange_services",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_echange_services",
            values,
        )

    @http.route(
        [
            "/my/organization_echange_service/<int:organization_echange_service_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_echange_service(
        self, organization_echange_service_id=None, access_token=None, **kw
    ):
        try:
            organization_echange_service_sudo = self._document_check_access(
                "organization.echange.service",
                organization_echange_service_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_echange_service_get_page_view_values(
            organization_echange_service_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_echange_service",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Fichier
    # ------------------------------------------------------------
    def _organization_fichier_get_page_view_values(
        self, organization_fichier, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_fichier",
            "organization_fichier": organization_fichier,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_fichier,
            access_token,
            values,
            "my_organization_fichiers_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_fichiers",
            "/my/organization_fichiers/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_fichiers(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationFichier = request.env["organization.fichier"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.fichier", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_fichiers count
        organization_fichier_count = OrganizationFichier.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/organization_fichiers",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_fichier_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_fichiers = OrganizationFichier.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_fichiers_history"
        ] = organization_fichiers.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_fichiers": organization_fichiers,
                "page_name": "organization_fichier",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_fichiers",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_fichiers",
            values,
        )

    @http.route(
        ["/my/organization_fichier/<int:organization_fichier_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_fichier(
        self, organization_fichier_id=None, access_token=None, **kw
    ):
        try:
            organization_fichier_sudo = self._document_check_access(
                "organization.fichier", organization_fichier_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_fichier_get_page_view_values(
            organization_fichier_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_fichier", values
        )

    # ------------------------------------------------------------
    # My Organization Membre
    # ------------------------------------------------------------
    def _organization_membre_get_page_view_values(
        self, organization_membre, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_membre",
            "organization_membre": organization_membre,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_membre,
            access_token,
            values,
            "my_organization_membres_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_membres",
            "/my/organization_membres/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_membres(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationMembre = request.env["organization.membre"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.membre", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_membres count
        organization_membre_count = OrganizationMembre.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/organization_membres",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_membre_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_membres = OrganizationMembre.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_membres_history"
        ] = organization_membres.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_membres": organization_membres,
                "page_name": "organization_membre",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_membres",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_membres", values
        )

    @http.route(
        ["/my/organization_membre/<int:organization_membre_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_membre(
        self, organization_membre_id=None, access_token=None, **kw
    ):
        try:
            organization_membre_sudo = self._document_check_access(
                "organization.membre", organization_membre_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_membre_get_page_view_values(
            organization_membre_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_membre", values
        )

    # ------------------------------------------------------------
    # My Organization Occupation
    # ------------------------------------------------------------
    def _organization_occupation_get_page_view_values(
        self, organization_occupation, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_occupation",
            "organization_occupation": organization_occupation,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_occupation,
            access_token,
            values,
            "my_organization_occupations_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_occupations",
            "/my/organization_occupations/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_occupations(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationOccupation = request.env["organization.occupation"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.occupation", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_occupations count
        organization_occupation_count = OrganizationOccupation.search_count(
            domain
        )
        # pager
        pager = portal_pager(
            url="/my/organization_occupations",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_occupation_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_occupations = OrganizationOccupation.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_occupations_history"
        ] = organization_occupations.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_occupations": organization_occupations,
                "page_name": "organization_occupation",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_occupations",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_occupations",
            values,
        )

    @http.route(
        ["/my/organization_occupation/<int:organization_occupation_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_occupation(
        self, organization_occupation_id=None, access_token=None, **kw
    ):
        try:
            organization_occupation_sudo = self._document_check_access(
                "organization.occupation",
                organization_occupation_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_occupation_get_page_view_values(
            organization_occupation_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_occupation",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Offre Service
    # ------------------------------------------------------------
    def _organization_offre_service_get_page_view_values(
        self, organization_offre_service, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_offre_service",
            "organization_offre_service": organization_offre_service,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_offre_service,
            access_token,
            values,
            "my_organization_offre_services_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_offre_services",
            "/my/organization_offre_services/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_offre_services(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationOffreService = request.env["organization.offre.service"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.offre.service", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_offre_services count
        organization_offre_service_count = (
            OrganizationOffreService.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/organization_offre_services",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_offre_service_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_offre_services = OrganizationOffreService.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_offre_services_history"
        ] = organization_offre_services.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_offre_services": organization_offre_services,
                "page_name": "organization_offre_service",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_offre_services",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_offre_services",
            values,
        )

    @http.route(
        ["/my/organization_offre_service/<int:organization_offre_service_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_offre_service(
        self, organization_offre_service_id=None, access_token=None, **kw
    ):
        try:
            organization_offre_service_sudo = self._document_check_access(
                "organization.offre.service",
                organization_offre_service_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_offre_service_get_page_view_values(
            organization_offre_service_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_offre_service",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Organization
    # ------------------------------------------------------------
    def _organization_organization_get_page_view_values(
        self, organization_organization, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_organization",
            "organization_organization": organization_organization,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_organization,
            access_token,
            values,
            "my_organization_organizations_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_organizations",
            "/my/organization_organizations/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_organizations(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationOrganization = request.env["organization.organization"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.organization", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_organizations count
        organization_organization_count = (
            OrganizationOrganization.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/organization_organizations",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_organization_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_organizations = OrganizationOrganization.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_organizations_history"
        ] = organization_organizations.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_organizations": organization_organizations,
                "page_name": "organization_organization",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_organizations",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_organizations",
            values,
        )

    @http.route(
        ["/my/organization_organization/<int:organization_organization_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_organization(
        self, organization_organization_id=None, access_token=None, **kw
    ):
        try:
            organization_organization_sudo = self._document_check_access(
                "organization.organization",
                organization_organization_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_organization_get_page_view_values(
            organization_organization_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_organization",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Origine
    # ------------------------------------------------------------
    def _organization_origine_get_page_view_values(
        self, organization_origine, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_origine",
            "organization_origine": organization_origine,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_origine,
            access_token,
            values,
            "my_organization_origines_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_origines",
            "/my/organization_origines/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_origines(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationOrigine = request.env["organization.origine"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.origine", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_origines count
        organization_origine_count = OrganizationOrigine.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/organization_origines",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_origine_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_origines = OrganizationOrigine.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_origines_history"
        ] = organization_origines.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_origines": organization_origines,
                "page_name": "organization_origine",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_origines",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_origines",
            values,
        )

    @http.route(
        ["/my/organization_origine/<int:organization_origine_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_origine(
        self, organization_origine_id=None, access_token=None, **kw
    ):
        try:
            organization_origine_sudo = self._document_check_access(
                "organization.origine", organization_origine_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_origine_get_page_view_values(
            organization_origine_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_origine", values
        )

    # ------------------------------------------------------------
    # My Organization Point Service
    # ------------------------------------------------------------
    def _organization_point_service_get_page_view_values(
        self, organization_point_service, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_point_service",
            "organization_point_service": organization_point_service,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_point_service,
            access_token,
            values,
            "my_organization_point_services_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_point_services",
            "/my/organization_point_services/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_point_services(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationPointService = request.env["organization.point.service"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.point.service", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_point_services count
        organization_point_service_count = (
            OrganizationPointService.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/organization_point_services",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_point_service_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_point_services = OrganizationPointService.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_point_services_history"
        ] = organization_point_services.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_point_services": organization_point_services,
                "page_name": "organization_point_service",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_point_services",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_point_services",
            values,
        )

    @http.route(
        ["/my/organization_point_service/<int:organization_point_service_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_point_service(
        self, organization_point_service_id=None, access_token=None, **kw
    ):
        try:
            organization_point_service_sudo = self._document_check_access(
                "organization.point.service",
                organization_point_service_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_point_service_get_page_view_values(
            organization_point_service_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_point_service",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Provenance
    # ------------------------------------------------------------
    def _organization_provenance_get_page_view_values(
        self, organization_provenance, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_provenance",
            "organization_provenance": organization_provenance,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_provenance,
            access_token,
            values,
            "my_organization_provenances_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_provenances",
            "/my/organization_provenances/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_provenances(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationProvenance = request.env["organization.provenance"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.provenance", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_provenances count
        organization_provenance_count = OrganizationProvenance.search_count(
            domain
        )
        # pager
        pager = portal_pager(
            url="/my/organization_provenances",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_provenance_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_provenances = OrganizationProvenance.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_provenances_history"
        ] = organization_provenances.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_provenances": organization_provenances,
                "page_name": "organization_provenance",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_provenances",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_provenances",
            values,
        )

    @http.route(
        ["/my/organization_provenance/<int:organization_provenance_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_provenance(
        self, organization_provenance_id=None, access_token=None, **kw
    ):
        try:
            organization_provenance_sudo = self._document_check_access(
                "organization.provenance",
                organization_provenance_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_provenance_get_page_view_values(
            organization_provenance_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_provenance",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Quartier
    # ------------------------------------------------------------
    def _organization_quartier_get_page_view_values(
        self, organization_quartier, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_quartier",
            "organization_quartier": organization_quartier,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_quartier,
            access_token,
            values,
            "my_organization_quartiers_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_quartiers",
            "/my/organization_quartiers/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_quartiers(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationQuartier = request.env["organization.quartier"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.quartier", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_quartiers count
        organization_quartier_count = OrganizationQuartier.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/organization_quartiers",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_quartier_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_quartiers = OrganizationQuartier.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_quartiers_history"
        ] = organization_quartiers.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_quartiers": organization_quartiers,
                "page_name": "organization_quartier",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_quartiers",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_quartiers",
            values,
        )

    @http.route(
        ["/my/organization_quartier/<int:organization_quartier_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_quartier(
        self, organization_quartier_id=None, access_token=None, **kw
    ):
        try:
            organization_quartier_sudo = self._document_check_access(
                "organization.quartier", organization_quartier_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_quartier_get_page_view_values(
            organization_quartier_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_quartier",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Region
    # ------------------------------------------------------------
    def _organization_region_get_page_view_values(
        self, organization_region, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_region",
            "organization_region": organization_region,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_region,
            access_token,
            values,
            "my_organization_regions_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_regions",
            "/my/organization_regions/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_regions(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationRegion = request.env["organization.region"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.region", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_regions count
        organization_region_count = OrganizationRegion.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/organization_regions",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_region_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_regions = OrganizationRegion.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_regions_history"
        ] = organization_regions.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_regions": organization_regions,
                "page_name": "organization_region",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_regions",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_regions", values
        )

    @http.route(
        ["/my/organization_region/<int:organization_region_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_region(
        self, organization_region_id=None, access_token=None, **kw
    ):
        try:
            organization_region_sudo = self._document_check_access(
                "organization.region", organization_region_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_region_get_page_view_values(
            organization_region_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_region", values
        )

    # ------------------------------------------------------------
    # My Organization Revenu Familial
    # ------------------------------------------------------------
    def _organization_revenu_familial_get_page_view_values(
        self, organization_revenu_familial, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_revenu_familial",
            "organization_revenu_familial": organization_revenu_familial,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_revenu_familial,
            access_token,
            values,
            "my_organization_revenu_familials_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_revenu_familials",
            "/my/organization_revenu_familials/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_revenu_familials(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationRevenuFamilial = request.env[
            "organization.revenu.familial"
        ]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.revenu.familial", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_revenu_familials count
        organization_revenu_familial_count = (
            OrganizationRevenuFamilial.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/organization_revenu_familials",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_revenu_familial_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_revenu_familials = OrganizationRevenuFamilial.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_revenu_familials_history"
        ] = organization_revenu_familials.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_revenu_familials": organization_revenu_familials,
                "page_name": "organization_revenu_familial",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_revenu_familials",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_revenu_familials",
            values,
        )

    @http.route(
        [
            "/my/organization_revenu_familial/<int:organization_revenu_familial_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_revenu_familial(
        self, organization_revenu_familial_id=None, access_token=None, **kw
    ):
        try:
            organization_revenu_familial_sudo = self._document_check_access(
                "organization.revenu.familial",
                organization_revenu_familial_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_revenu_familial_get_page_view_values(
            organization_revenu_familial_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_revenu_familial",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Situation Maison
    # ------------------------------------------------------------
    def _organization_situation_maison_get_page_view_values(
        self, organization_situation_maison, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_situation_maison",
            "organization_situation_maison": organization_situation_maison,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_situation_maison,
            access_token,
            values,
            "my_organization_situation_maisons_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_situation_maisons",
            "/my/organization_situation_maisons/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_situation_maisons(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationSituationMaison = request.env[
            "organization.situation.maison"
        ]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.situation.maison", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_situation_maisons count
        organization_situation_maison_count = (
            OrganizationSituationMaison.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/organization_situation_maisons",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_situation_maison_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_situation_maisons = OrganizationSituationMaison.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_situation_maisons_history"
        ] = organization_situation_maisons.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_situation_maisons": organization_situation_maisons,
                "page_name": "organization_situation_maison",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_situation_maisons",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_situation_maisons",
            values,
        )

    @http.route(
        [
            "/my/organization_situation_maison/<int:organization_situation_maison_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_situation_maison(
        self, organization_situation_maison_id=None, access_token=None, **kw
    ):
        try:
            organization_situation_maison_sudo = self._document_check_access(
                "organization.situation.maison",
                organization_situation_maison_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_situation_maison_get_page_view_values(
            organization_situation_maison_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_situation_maison",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Type Communication
    # ------------------------------------------------------------
    def _organization_type_communication_get_page_view_values(
        self, organization_type_communication, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_type_communication",
            "organization_type_communication": organization_type_communication,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_type_communication,
            access_token,
            values,
            "my_organization_type_communications_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_type_communications",
            "/my/organization_type_communications/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_type_communications(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationTypeCommunication = request.env[
            "organization.type.communication"
        ]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.type.communication", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_type_communications count
        organization_type_communication_count = (
            OrganizationTypeCommunication.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/organization_type_communications",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_type_communication_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_type_communications = (
            OrganizationTypeCommunication.search(
                domain,
                order=order,
                limit=self._items_per_page,
                offset=pager["offset"],
            )
        )
        request.session[
            "my_organization_type_communications_history"
        ] = organization_type_communications.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_type_communications": organization_type_communications,
                "page_name": "organization_type_communication",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_type_communications",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_type_communications",
            values,
        )

    @http.route(
        [
            "/my/organization_type_communication/<int:organization_type_communication_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_type_communication(
        self, organization_type_communication_id=None, access_token=None, **kw
    ):
        try:
            organization_type_communication_sudo = self._document_check_access(
                "organization.type.communication",
                organization_type_communication_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_type_communication_get_page_view_values(
            organization_type_communication_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_type_communication",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Type Compte
    # ------------------------------------------------------------
    def _organization_type_compte_get_page_view_values(
        self, organization_type_compte, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_type_compte",
            "organization_type_compte": organization_type_compte,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_type_compte,
            access_token,
            values,
            "my_organization_type_comptes_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_type_comptes",
            "/my/organization_type_comptes/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_type_comptes(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationTypeCompte = request.env["organization.type.compte"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.type.compte", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_type_comptes count
        organization_type_compte_count = OrganizationTypeCompte.search_count(
            domain
        )
        # pager
        pager = portal_pager(
            url="/my/organization_type_comptes",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_type_compte_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_type_comptes = OrganizationTypeCompte.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_type_comptes_history"
        ] = organization_type_comptes.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_type_comptes": organization_type_comptes,
                "page_name": "organization_type_compte",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_type_comptes",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_type_comptes",
            values,
        )

    @http.route(
        ["/my/organization_type_compte/<int:organization_type_compte_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_type_compte(
        self, organization_type_compte_id=None, access_token=None, **kw
    ):
        try:
            organization_type_compte_sudo = self._document_check_access(
                "organization.type.compte",
                organization_type_compte_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_type_compte_get_page_view_values(
            organization_type_compte_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_type_compte",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Type Fichier
    # ------------------------------------------------------------
    def _organization_type_fichier_get_page_view_values(
        self, organization_type_fichier, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_type_fichier",
            "organization_type_fichier": organization_type_fichier,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_type_fichier,
            access_token,
            values,
            "my_organization_type_fichiers_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_type_fichiers",
            "/my/organization_type_fichiers/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_type_fichiers(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationTypeFichier = request.env["organization.type.fichier"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.type.fichier", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_type_fichiers count
        organization_type_fichier_count = OrganizationTypeFichier.search_count(
            domain
        )
        # pager
        pager = portal_pager(
            url="/my/organization_type_fichiers",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_type_fichier_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_type_fichiers = OrganizationTypeFichier.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_type_fichiers_history"
        ] = organization_type_fichiers.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_type_fichiers": organization_type_fichiers,
                "page_name": "organization_type_fichier",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_type_fichiers",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_type_fichiers",
            values,
        )

    @http.route(
        ["/my/organization_type_fichier/<int:organization_type_fichier_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_type_fichier(
        self, organization_type_fichier_id=None, access_token=None, **kw
    ):
        try:
            organization_type_fichier_sudo = self._document_check_access(
                "organization.type.fichier",
                organization_type_fichier_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_type_fichier_get_page_view_values(
            organization_type_fichier_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_type_fichier",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Type Service
    # ------------------------------------------------------------
    def _organization_type_service_get_page_view_values(
        self, organization_type_service, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_type_service",
            "organization_type_service": organization_type_service,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_type_service,
            access_token,
            values,
            "my_organization_type_services_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_type_services",
            "/my/organization_type_services/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_type_services(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationTypeService = request.env["organization.type.service"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.type.service", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_type_services count
        organization_type_service_count = OrganizationTypeService.search_count(
            domain
        )
        # pager
        pager = portal_pager(
            url="/my/organization_type_services",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_type_service_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_type_services = OrganizationTypeService.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_type_services_history"
        ] = organization_type_services.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_type_services": organization_type_services,
                "page_name": "organization_type_service",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_type_services",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_type_services",
            values,
        )

    @http.route(
        ["/my/organization_type_service/<int:organization_type_service_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_type_service(
        self, organization_type_service_id=None, access_token=None, **kw
    ):
        try:
            organization_type_service_sudo = self._document_check_access(
                "organization.type.service",
                organization_type_service_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_type_service_get_page_view_values(
            organization_type_service_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_type_service",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Type Service Categorie
    # ------------------------------------------------------------
    def _organization_type_service_categorie_get_page_view_values(
        self, organization_type_service_categorie, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_type_service_categorie",
            "organization_type_service_categorie": organization_type_service_categorie,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_type_service_categorie,
            access_token,
            values,
            "my_organization_type_service_categories_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_type_service_categories",
            "/my/organization_type_service_categories/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_type_service_categories(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationTypeServiceCategorie = request.env[
            "organization.type.service.categorie"
        ]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.type.service.categorie", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_type_service_categories count
        organization_type_service_categorie_count = (
            OrganizationTypeServiceCategorie.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/organization_type_service_categories",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_type_service_categorie_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_type_service_categories = (
            OrganizationTypeServiceCategorie.search(
                domain,
                order=order,
                limit=self._items_per_page,
                offset=pager["offset"],
            )
        )
        request.session[
            "my_organization_type_service_categories_history"
        ] = organization_type_service_categories.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_type_service_categories": organization_type_service_categories,
                "page_name": "organization_type_service_categorie",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_type_service_categories",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_type_service_categories",
            values,
        )

    @http.route(
        [
            "/my/organization_type_service_categorie/<int:organization_type_service_categorie_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_type_service_categorie(
        self,
        organization_type_service_categorie_id=None,
        access_token=None,
        **kw,
    ):
        try:
            organization_type_service_categorie_sudo = (
                self._document_check_access(
                    "organization.type.service.categorie",
                    organization_type_service_categorie_id,
                    access_token,
                )
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = (
            self._organization_type_service_categorie_get_page_view_values(
                organization_type_service_categorie_sudo, access_token, **kw
            )
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_type_service_categorie",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Type Service Sous Categorie
    # ------------------------------------------------------------
    def _organization_type_service_sous_categorie_get_page_view_values(
        self, organization_type_service_sous_categorie, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_type_service_sous_categorie",
            "organization_type_service_sous_categorie": organization_type_service_sous_categorie,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_type_service_sous_categorie,
            access_token,
            values,
            "my_organization_type_service_sous_categories_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_type_service_sous_categories",
            "/my/organization_type_service_sous_categories/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_type_service_sous_categories(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationTypeServiceSousCategorie = request.env[
            "organization.type.service.sous.categorie"
        ]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.type.service.sous.categorie", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_type_service_sous_categories count
        organization_type_service_sous_categorie_count = (
            OrganizationTypeServiceSousCategorie.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/organization_type_service_sous_categories",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_type_service_sous_categorie_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_type_service_sous_categories = (
            OrganizationTypeServiceSousCategorie.search(
                domain,
                order=order,
                limit=self._items_per_page,
                offset=pager["offset"],
            )
        )
        request.session[
            "my_organization_type_service_sous_categories_history"
        ] = organization_type_service_sous_categories.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_type_service_sous_categories": organization_type_service_sous_categories,
                "page_name": "organization_type_service_sous_categorie",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_type_service_sous_categories",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_type_service_sous_categories",
            values,
        )

    @http.route(
        [
            "/my/organization_type_service_sous_categorie/<int:organization_type_service_sous_categorie_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_type_service_sous_categorie(
        self,
        organization_type_service_sous_categorie_id=None,
        access_token=None,
        **kw,
    ):
        try:
            organization_type_service_sous_categorie_sudo = (
                self._document_check_access(
                    "organization.type.service.sous.categorie",
                    organization_type_service_sous_categorie_id,
                    access_token,
                )
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_type_service_sous_categorie_get_page_view_values(
            organization_type_service_sous_categorie_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_type_service_sous_categorie",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Type Telephone
    # ------------------------------------------------------------
    def _organization_type_telephone_get_page_view_values(
        self, organization_type_telephone, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_type_telephone",
            "organization_type_telephone": organization_type_telephone,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_type_telephone,
            access_token,
            values,
            "my_organization_type_telephones_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/organization_type_telephones",
            "/my/organization_type_telephones/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_type_telephones(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationTypeTelephone = request.env["organization.type.telephone"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "organization.type.telephone", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_type_telephones count
        organization_type_telephone_count = (
            OrganizationTypeTelephone.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/organization_type_telephones",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_type_telephone_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_type_telephones = OrganizationTypeTelephone.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_type_telephones_history"
        ] = organization_type_telephones.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_type_telephones": organization_type_telephones,
                "page_name": "organization_type_telephone",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_type_telephones",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_type_telephones",
            values,
        )

    @http.route(
        [
            "/my/organization_type_telephone/<int:organization_type_telephone_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_type_telephone(
        self, organization_type_telephone_id=None, access_token=None, **kw
    ):
        try:
            organization_type_telephone_sudo = self._document_check_access(
                "organization.type.telephone",
                organization_type_telephone_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_type_telephone_get_page_view_values(
            organization_type_telephone_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_type_telephone",
            values,
        )

    # ------------------------------------------------------------
    # My Organization Ville
    # ------------------------------------------------------------
    def _organization_ville_get_page_view_values(
        self, organization_ville, access_token, **kwargs
    ):
        values = {
            "page_name": "organization_ville",
            "organization_ville": organization_ville,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            organization_ville,
            access_token,
            values,
            "my_organization_villes_history",
            False,
            **kwargs,
        )

    @http.route(
        ["/my/organization_villes", "/my/organization_villes/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_organization_villes(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        OrganizationVille = request.env["organization.ville"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups("organization.ville", domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # organization_villes count
        organization_ville_count = OrganizationVille.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/organization_villes",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=organization_ville_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        organization_villes = OrganizationVille.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_organization_villes_history"
        ] = organization_villes.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "organization_villes": organization_villes,
                "page_name": "organization_ville",
                "archive_groups": archive_groups,
                "default_url": "/my/organization_villes",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_villes", values
        )

    @http.route(
        ["/my/organization_ville/<int:organization_ville_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_organization_ville(
        self, organization_ville_id=None, access_token=None, **kw
    ):
        try:
            organization_ville_sudo = self._document_check_access(
                "organization.ville", organization_ville_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._organization_ville_get_page_view_values(
            organization_ville_sudo, access_token, **kw
        )
        return request.render(
            "demo_mariadb_sql_example_1.portal_my_organization_ville", values
        )
