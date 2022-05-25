odoo.define(
    "demo_website_multiple_snippet_list_item_structure_double_short.animation",
    function (require) {
        "use strict";

        let sAnimation = require("website.content.snippets.animation");

        sAnimation.registry.demo_website_multiple_snippet_list_item_structure_double_short =
            sAnimation.Class.extend({
                selector:
                    ".o_demo_website_multiple_snippet_list_item_structure_double_short",

                start: function () {
                    let self = this;
                    this._eventList = this.$(".container");
                    this._originalContent = this._eventList[0].outerHTML;
                    let def = this._rpc({
                        route: "/demo_website_multiple_snippet/dp_dmp_demo_model_portal_and_dp_dm2p_demo_model_2_portal_and_dp_dm3pd_demo_model_3_portal_diagram_list",
                    }).then(function (data) {
                        if (data.error) {
                            return;
                        }

                        if (_.isEmpty(data)) {
                            return;
                        }

                        self._$loadedContent = $(data);
                        self._eventList.replaceWith(self._$loadedContent);
                    });

                    return $.when(this._super.apply(this, arguments), def);
                },
                destroy: function () {
                    this._super.apply(this, arguments);
                    if (this._$loadedContent) {
                        this._$loadedContent.replaceWith(this._originalContent);
                    }
                },
            });
    }
);
