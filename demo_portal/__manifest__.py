{
    "name": "Demo Portal",
    "category": "Uncategorized",
    "version": "12.0.1.0",
    "author": "TechnoLibre",
    "license": "AGPL-3",
    "website": "https://technolibre.ca",
    "application": True,
    "depends": [
        "website",
        "mail",
        "portal",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/demo_model_2_portal.xml",
        "views/demo_portal_templates.xml",
        "views/demo_model_3_portal_diagram.xml",
        "views/demo_model_portal.xml",
        "views/menu.xml",
        "views/snippets.xml",
    ],
    "installable": True,
}
