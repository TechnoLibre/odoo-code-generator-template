odoo.define(
    "demo_website_multiple_snippet_Individual_item_content.animation",
    function (require) {
        "use strict";

        let sAnimation = require("website.content.snippets.animation");

        sAnimation.registry.demo_website_multiple_snippet_Individual_item_content =
            sAnimation.Class.extend({
                selector:
                    ".o_demo_website_multiple_snippet_Individual_item_content",

                start: function () {
                    let self = this;
                    this._eventList = this.$(".container");
                    this._originalContent = this._eventList[0].outerHTML;
                    let def = this._rpc({
                        route: "/demo_website_multiple_snippet/get_last_item",
                    }).then(function (data) {
                        if (data.error) {
                            return;
                        }

                        self._$loadedContent = $(data);

                        if (_.isEmpty(data)) {
                            self.$(
                                ".o_loading_demo_website_multiple_snippet_Individual_item_content"
                            ).text("NO DATA");
                            return;
                        }

                        if (data["demo_binary"]) {
                            self.$(".demo_binary_value").text(
                                data["demo_binary"]
                            );
                        }
                        if (data["demo_binary_image"]) {
                            self.$(".demo_binary_image_value").text(
                                data["demo_binary_image"]
                            );
                        }
                        if (data["demo_boolean"]) {
                            self.$(".demo_boolean_value").text(
                                data["demo_boolean"]
                            );
                        }
                        if (data["demo_char"]) {
                            self.$(".demo_char_value").text(data["demo_char"]);
                        }
                        if (data["demo_date"]) {
                            self.$(".demo_date_value").text(data["demo_date"]);
                        }
                        if (data["demo_date_time"]) {
                            self.$(".demo_date_time_value").text(
                                data["demo_date_time"]
                            );
                        }
                        if (data["demo_external_link"]) {
                            self.$(".demo_external_link_value").text(
                                data["demo_external_link"]
                            );
                        }
                        if (data["demo_float"]) {
                            self.$(".demo_float_value").text(
                                data["demo_float"]
                            );
                        }
                        if (data["demo_float_time"]) {
                            self.$(".demo_float_time_value").text(
                                data["demo_float_time"]
                            );
                        }
                        if (data["demo_html"]) {
                            self.$(".demo_html_value").text(data["demo_html"]);
                        }
                        if (data["demo_integer"]) {
                            self.$(".demo_integer_value").text(
                                data["demo_integer"]
                            );
                        }
                        if (data["demo_many2many"]) {
                            self.$(".demo_many2many_value").text(
                                data["demo_many2many"]
                            );
                        }
                        if (data["demo_one2many_dst"]) {
                            self.$(".demo_one2many_dst_value").text(
                                data["demo_one2many_dst"]
                            );
                        }
                        if (data["demo_one2many_src"]) {
                            self.$(".demo_one2many_src_value").text(
                                data["demo_one2many_src"]
                            );
                        }
                        if (data["demo_selection"]) {
                            self.$(".demo_selection_value").text(
                                data["demo_selection"]
                            );
                        }
                        if (data["demo_text"]) {
                            self.$(".demo_text_value").text(data["demo_text"]);
                        }
                        if (data["diagram_id"]) {
                            self.$(".diagram_id_value").text(
                                data["diagram_id"]
                            );
                        }
                        if (data["name"]) {
                            self.$(".name_value").text(data["name"]);
                        }
                        if (data["xpos"]) {
                            self.$(".xpos_value").text(data["xpos"]);
                        }
                        if (data["ypos"]) {
                            self.$(".ypos_value").text(data["ypos"]);
                        }
                        self.$(
                            ".o_loading_demo_website_multiple_snippet_Individual_item_content"
                        ).remove();
                    });

                    return $.when(this._super.apply(this, arguments), def);
                },
                destroy: function () {
                    this._super.apply(this, arguments);
                    if (this._$loadedContent) {
                        this._eventList.replaceWith(this._originalContent);
                    }
                },
            });
    }
);
