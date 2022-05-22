{
    "name": "Demo website attachments data",
    "category": "Website",
    "summary": "Exported Data from website with attachments.",
    "version": "12.0.1.0",
    "author": "TechnoLibre",
    "license": "AGPL-3",
    "website": "https://technolibre.ca",
    "depends": ["website"],
    "data": [
        "data/ir_attachment.xml",
        "data/ir_ui_view.xml",
        "data/website_page.xml",
        "data/website_menu.xml",
    ],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
}
