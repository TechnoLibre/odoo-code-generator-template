{
    "name": "Demo website leaflet",
    "category": "Website",
    "summary": "Leaflet integration in website",
    "version": "12.0.1.0",
    "author": "TechnoLibre",
    "license": "AGPL-3",
    "website": "https://technolibre.ca",
    "application": True,
    "depends": [
        "website",
        "base_geoengine",
    ],
    "external_dependencies": {
        "python": ["pyproj"],
    },
    "data": [
        "security/ir.model.access.csv",
        "views/demo_website_leaflet_map.xml",
        "views/demo_website_leaflet_map_feature.xml",
        "views/demo_website_leaflet_category.xml",
        "views/menu.xml",
        "views/geoengine.xml",
        "views/snippets.xml",
    ],
    "installable": True,
}
