odoo.define(
    "demo_mariadb_sql_example_1.demo_mariadb_sql_example_1_portal",
    function (require) {
        "use strict";

        require("web.dom_ready");
        let time = require("web.time");
        let ajax = require("web.ajax");
        let base = require("web_editor.base");
        let context = require("web_editor.context");

        function load_locale() {
            let url = "/web/webclient/locale/" + context.get().lang || "en_US";
            return ajax.loadJS(url);
        }

        let ready_with_locale = $.when(base.ready(), load_locale());
        ready_with_locale.then(function () {
            _.each($(".input-group.date"), function (date_field) {
                let minDate =
                    $(date_field).data("mindate") || moment({ y: 1900 });
                let maxDate =
                    $(date_field).data("maxdate") || moment().add(200, "y");
                let options = {
                    minDate: minDate,
                    maxDate: maxDate,
                    calendarWeeks: true,
                    icons: {
                        time: "fa fa-clock-o",
                        date: "fa fa-calendar",
                        next: "fa fa-chevron-right",
                        previous: "fa fa-chevron-left",
                        up: "fa fa-chevron-up",
                        down: "fa fa-chevron-down",
                    },
                    locale: moment.locale(),
                    allowInputToggle: true,
                    keyBinds: null,
                };
                if ($(date_field).find(".o_website_form_date").length > 0) {
                    options.format = time.getLangDateFormat();
                } else if (
                    $(date_field).find(".o_website_form_clock").length > 0
                ) {
                    // options.format = time.getLangTimeFormat();
                    options.format = "HH:mm";
                    options.defaultDate = moment("00:00", "HH:mm");
                } else {
                    options.format = time.getLangDatetimeFormat();
                }
                $("#" + date_field.id).datetimepicker(options);
            });
        });
    }
);
