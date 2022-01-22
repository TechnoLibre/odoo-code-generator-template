{
    "name": "Code Generator migrator demo mariadb sql example 1",
    "version": "12.0.1.0",
    "author": "TechnoLibre",
    "license": "AGPL-3",
    "website": "https://technolibre.ca",
    "application": False,
    "depends": [
        "code_generator",
        "code_generator_hook",
        "code_generator_db_servers",
    ],
    "installable": True,
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
