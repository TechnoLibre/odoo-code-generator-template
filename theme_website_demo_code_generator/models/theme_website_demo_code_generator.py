from odoo import _, api, fields, models


class ThemeWebsiteDemoCodeGenerator(models.AbstractModel):
    _inherit = "theme.utils"

    def _theme_website_demo_code_generator_post_copy(self, mod):
        self.disable_view("website_theme_install.customize_modal")
