from odoo import _, api, models, fields, SUPERUSER_ID

import os

MODULE_NAME = "auto_backup"


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # The path of the actual file
        path_module_generate = os.path.normpath(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "OCA_server-tools"
            )
        )

        short_name = MODULE_NAME.replace("_", " ").title()

        # Add code generator
        categ_id = env["ir.module.category"].search([("name", "=", "Tools")])
        value = {
            "shortdesc": "Database Auto-Backup",
            "name": "auto_backup",
            "header_manifest": """
# Copyright 2004-2009 Tiny SPRL (<http://tiny.be>).
# Copyright 2015 Agile Business Group <http://www.agilebg.com>
# Copyright 2016 Grupo ESOC Ingenieria de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
            """,
            "license": "AGPL-3",
            "category_id": categ_id.id,
            "summary": "Backups database",
            "author": (
                "Yenthe Van Ginneken, "
                "Agile Business Group, "
                "Grupo ESOC Ingenieria de Servicios, "
                "LasLabs, "
                "AdaptiveCity, "
                "Odoo Community Association (OCA)"
            ),
            "website": "https://github.com/OCA/server-tools/",
            "application": False,
            "enable_sync_code": True,
            "path_sync_code": path_module_generate,
            "icon": os.path.join(
                os.path.dirname(__file__),
                "static",
                "description",
                "code_generator_icon.png",
            ),
        }

        # TODO HUMAN: enable your functionality to generate
        value["enable_sync_template"] = True
        value["ignore_fields"] = ""
        value["post_init_hook_show"] = False
        value["uninstall_hook_show"] = False
        value["post_init_hook_feature_code_generator"] = False
        value["uninstall_hook_feature_code_generator"] = False

        value["hook_constant_code"] = f'MODULE_NAME = "{MODULE_NAME}"'

        code_generator_id = env["code.generator.module"].create(value)

        # Add Db Backup
        value = {
            "name": "db_backup",
            "model": "db.backup",
            "m2o_module": code_generator_id.id,
            "rec_name": None,
            "nomenclator": True,
        }
        model_db_backup = env["ir.model"].create(value)

        # Model Inherit
        dependency_ids = env["ir.module.module"].search(
            [("name", "=", "mail")]
        )
        for dependency in dependency_ids:
            value = {
                "module_id": code_generator_id.id,
                "depend_id": dependency.id,
                "name": code_generator_id.display_name,
            }
            env["code.generator.module.dependency"].create(value)
        inherit_model = env["ir.model"].search([("model", "=", "mail.thread")])
        model_db_backup.m2o_inherit_model = inherit_model.id

        # External dependencies
        value = {
            "module_id": code_generator_id.id,
            "depend": "pysftp",
            "application_type": "python",
        }
        env["code.generator.module.external.dependency"].create(value)

        ##### Cron
        value = {
            "m2o_module": code_generator_id.id,
            "name": "Backup Scheduler",
            "user_id": env.ref("base.user_root").id,
            "interval_number": 1,
            "interval_type": "days",
            "numbercall": -1,
            "nextcall_template": (
                "(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d"
                " 03:00:00')"
            ),
            "model_id": model_db_backup.id,
            "state": "code",
            "code": "model.action_backup_all()",
        }
        cron_id = env["ir.cron"].create(value)

        value = {
            "name": "ir_cron_backup_scheduler_0",
            "model": "ir.cron",
            "module": MODULE_NAME,
            "res_id": cron_id.id,
            "noupdate": True,
        }
        env["ir.model.data"].create(value)

        ##### Begin Field
        value_field_backup_format = {
            "name": "backup_format",
            "model": "db.backup",
            "field_description": "Backup Format",
            "code_generator_sequence": 14,
            "ttype": "selection",
            "selection": (
                "[('zip', 'zip (includes filestore)'), ('dump', 'pg_dump"
                " custom format (without filestore)')]"
            ),
            "model_id": model_db_backup.id,
            "default": "zip",
            "help": "Choose the format for this backup.",
        }
        env["ir.model.fields"].create(value_field_backup_format)

        value_field_days_to_keep = {
            "name": "days_to_keep",
            "model": "db.backup",
            "field_description": "Days To Keep",
            "code_generator_sequence": 6,
            "ttype": "integer",
            "model_id": model_db_backup.id,
            "required": True,
            "help": (
                "Backups older than this will be deleted automatically. Set 0"
                " to disable autodeletion."
            ),
        }
        env["ir.model.fields"].create(value_field_days_to_keep)

        value_field_folder = {
            "name": "folder",
            "model": "db.backup",
            "field_description": "Folder",
            "code_generator_sequence": 5,
            "ttype": "char",
            "model_id": model_db_backup.id,
            "default": "lambda self: self._default_folder()",
            "required": True,
            "help": "Absolute path for storing the backups",
        }
        env["ir.model.fields"].create(value_field_folder)

        value_field_method = {
            "name": "method",
            "model": "db.backup",
            "field_description": "Method",
            "code_generator_sequence": 7,
            "ttype": "selection",
            "selection": (
                "[('local', 'Local disk'), ('sftp', 'Remote SFTP server')]"
            ),
            "model_id": model_db_backup.id,
            "default": "local",
            "help": "Choose the storage method for this backup.",
        }
        env["ir.model.fields"].create(value_field_method)

        value_field_name = {
            "name": "name",
            "model": "db.backup",
            "field_description": "Name",
            "code_generator_sequence": 4,
            "ttype": "char",
            "model_id": model_db_backup.id,
            "store": True,
            "code_generator_compute": "_compute_name",
            "help": "Summary of this backup process",
        }
        env["ir.model.fields"].create(value_field_name)

        value_field_sftp_host = {
            "name": "sftp_host",
            "model": "db.backup",
            "field_description": "SFTP Server",
            "code_generator_sequence": 8,
            "ttype": "char",
            "model_id": model_db_backup.id,
            "help": (
                "The host name or IP address from your remote server. For"
                " example 192.168.0.1"
            ),
        }
        env["ir.model.fields"].create(value_field_sftp_host)

        value_field_sftp_password = {
            "name": "sftp_password",
            "model": "db.backup",
            "field_description": "SFTP Password",
            "code_generator_sequence": 11,
            "ttype": "char",
            "model_id": model_db_backup.id,
            "help": (
                "The password for the SFTP connection. If you specify a"
                " private key file, then this is the password to decrypt it."
            ),
        }
        env["ir.model.fields"].create(value_field_sftp_password)

        value_field_sftp_port = {
            "name": "sftp_port",
            "model": "db.backup",
            "field_description": "SFTP Port",
            "code_generator_sequence": 9,
            "ttype": "integer",
            "model_id": model_db_backup.id,
            "default": 22,
            "help": "The port on the FTP server that accepts SSH/SFTP calls.",
        }
        env["ir.model.fields"].create(value_field_sftp_port)

        value_field_sftp_private_key = {
            "name": "sftp_private_key",
            "model": "db.backup",
            "field_description": "Private key location",
            "code_generator_sequence": 12,
            "ttype": "char",
            "model_id": model_db_backup.id,
            "help": (
                "Path to the private key file. Only the Odoo user should have"
                " read permissions for that file."
            ),
        }
        env["ir.model.fields"].create(value_field_sftp_private_key)

        value_field_sftp_public_host_key = {
            "name": "sftp_public_host_key",
            "model": "db.backup",
            "field_description": "Public host key",
            "code_generator_sequence": 13,
            "ttype": "char",
            "model_id": model_db_backup.id,
            "help": (
                "Verify SFTP server's identity using its public rsa-key. The"
                " host key verification protects you from man-in-the-middle"
                " attacks. Can be generated with command 'ssh-keyscan -p PORT"
                " -H HOST/IP' and the right key is immediately after the words"
                " 'ssh-rsa'."
            ),
        }
        env["ir.model.fields"].create(value_field_sftp_public_host_key)

        value_field_sftp_user = {
            "name": "sftp_user",
            "model": "db.backup",
            "field_description": "Username in the SFTP Server",
            "code_generator_sequence": 10,
            "ttype": "char",
            "model_id": model_db_backup.id,
            "help": (
                "The username where the SFTP connection should be made with."
                " This is the user on the external server."
            ),
        }
        env["ir.model.fields"].create(value_field_sftp_user)

        # Hack to solve field name
        field_x_name = env["ir.model.fields"].search(
            [("model_id", "=", model_db_backup.id), ("name", "=", "x_name")]
        )
        field_x_name.unlink()
        model_db_backup.rec_name = "name"
        ##### End Field

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """# Copyright 2004-2009 Tiny SPRL (<http://tiny.be>).
# Copyright 2015 Agile Business Group <http://www.agilebg.com>
# Copyright 2016 Grupo ESOC Ingenieria de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import os
import shutil
import traceback
from contextlib import contextmanager
from datetime import datetime, timedelta
from glob import iglob
import base64
import paramiko

from odoo import _, api, exceptions, fields, models, tools
from odoo.service import db

_logger = logging.getLogger(__name__)
try:
    import pysftp
except ImportError:  # pragma: no cover
    _logger.debug("Cannot import pysftp")""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_db_backup.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": '''"""Default to ``backups`` folder inside current server datadir."""
return os.path.join(
    tools.config["data_dir"], "backups", self.env.cr.dbname
)''',
                    "name": "_default_folder",
                    "decorator": "@api.model",
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_db_backup.id,
                },
                {
                    "code": '''"""Get the right summary for this job."""
for rec in self:
    if rec.method == "local":
        rec.name = "%s @ localhost" % rec.folder
    elif rec.method == "sftp":
        rec.name = "sftp://%s@%s:%d%s" % (
            rec.sftp_user,
            rec.sftp_host,
            rec.sftp_port,
            rec.folder,
        )''',
                    "name": "_compute_name",
                    "decorator": (
                        '@api.multi;@api.depends("folder", "method",'
                        ' "sftp_host", "sftp_port", "sftp_user")'
                    ),
                    "param": "self",
                    "sequence": 1,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_db_backup.id,
                },
                {
                    "code": '''"""Do not use the filestore or you will backup your backups."""
for record in self:
    if record.method == "local" and record.folder.startswith(
        tools.config.filestore(self.env.cr.dbname)
    ):
        raise exceptions.ValidationError(
            _(
                "Do not save backups on your filestore, or you will "
                "backup your backups too!"
            )
        )''',
                    "name": "_check_folder",
                    "decorator": (
                        '@api.multi;@api.constrains("folder", "method")'
                    ),
                    "param": "self",
                    "sequence": 2,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_db_backup.id,
                },
                {
                    "code": '''"""Check if the SFTP settings are correct."""
try:
    # Just open and close the connection
    with self.sftp_connection():
        raise exceptions.Warning(_("Connection Test Succeeded!"))
except (
    pysftp.CredentialException,
    pysftp.ConnectionException,
    pysftp.SSHException,
):
    _logger.info("Connection Test Failed!", exc_info=True)
    raise exceptions.Warning(_("Connection Test Failed!"))''',
                    "name": "action_sftp_test_connection",
                    "decorator": "@api.multi",
                    "param": "self",
                    "sequence": 3,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_db_backup.id,
                },
                {
                    "code": '''"""Run selected backups."""
backup = None
successful = self.browse()

# Start with local storage
for rec in self.filtered(lambda r: r.method == "local"):
    filename = self.filename(datetime.now(), ext=rec.backup_format)
    with rec.backup_log():
        # Directory must exist
        try:
            os.makedirs(rec.folder)
        except OSError:
            pass

        with open(os.path.join(rec.folder, filename), "wb") as destiny:
            # Copy the cached backup
            if backup:
                with open(backup) as cached:
                    shutil.copyfileobj(cached, destiny)
            # Generate new backup
            else:
                db.dump_db(
                    self.env.cr.dbname,
                    destiny,
                    backup_format=rec.backup_format,
                )
                backup = backup or destiny.name
        successful |= rec

# Ensure a local backup exists if we are going to write it remotely
sftp = self.filtered(lambda r: r.method == "sftp")
if sftp:
    for rec in sftp:
        filename = self.filename(datetime.now(), ext=rec.backup_format)
        with rec.backup_log():

            cached = db.dump_db(
                self.env.cr.dbname,
                None,
                backup_format=rec.backup_format,
            )

            with cached:
                with rec.sftp_connection() as remote:
                    # Directory must exist
                    try:
                        remote.makedirs(rec.folder)
                    except pysftp.ConnectionException:
                        pass

                    # Copy cached backup to remote server
                    with remote.open(
                        os.path.join(rec.folder, filename), "wb"
                    ) as destiny:
                        shutil.copyfileobj(cached, destiny)
                successful |= rec

# Remove old files for successful backups
successful.cleanup()''',
                    "name": "action_backup",
                    "decorator": "@api.multi",
                    "param": "self",
                    "sequence": 4,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_db_backup.id,
                },
                {
                    "code": '''"""Run all scheduled backups."""
return self.search([]).action_backup()''',
                    "name": "action_backup_all",
                    "decorator": "@api.model",
                    "param": "self",
                    "sequence": 5,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_db_backup.id,
                },
                {
                    "code": '''"""Log a backup result."""
try:
    _logger.info("Starting database backup: %s", self.name)
    yield
except Exception:
    _logger.exception("Database backup failed: %s", self.name)
    escaped_tb = tools.html_escape(traceback.format_exc())
    self.message_post(  # pylint: disable=translation-required
        body="<p>%s</p><pre>%s</pre>"
        % (_("Database backup failed."), escaped_tb),
        subtype=self.env.ref(
            "auto_backup.mail_message_subtype_failure"
        ),
    )
else:
    _logger.info("Database backup succeeded: %s", self.name)
    self.message_post(body=_("Database backup succeeded."))''',
                    "name": "backup_log",
                    "decorator": "@api.multi;@contextmanager",
                    "param": "self",
                    "sequence": 6,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_db_backup.id,
                },
                {
                    "code": '''"""Clean up old backups."""
now = datetime.now()
for rec in self.filtered("days_to_keep"):
    with rec.cleanup_log():
        oldest = self.filename(now - timedelta(days=rec.days_to_keep))

        if rec.method == "local":
            for name in iglob(os.path.join(rec.folder, "*.dump.zip")):
                if os.path.basename(name) < oldest:
                    os.unlink(name)

        elif rec.method == "sftp":
            with rec.sftp_connection() as remote:
                for name in remote.listdir(rec.folder):
                    if (
                        name.endswith(".dump.zip")
                        and os.path.basename(name) < oldest
                    ):
                        remote.unlink("%s/%s" % (rec.folder, name))''',
                    "name": "cleanup",
                    "decorator": "@api.multi",
                    "param": "self",
                    "sequence": 7,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_db_backup.id,
                },
                {
                    "code": '''"""Log a possible cleanup failure."""
self.ensure_one()
try:
    _logger.info(
        "Starting cleanup process after database backup: %s", self.name
    )
    yield
except Exception:
    _logger.exception("Cleanup of old database backups failed: %s")
    escaped_tb = tools.html_escape(traceback.format_exc())
    self.message_post(  # pylint: disable=translation-required
        body="<p>%s</p><pre>%s</pre>"
        % (_("Cleanup of old database backups failed."), escaped_tb),
        subtype=self.env.ref("auto_backup.failure"),
    )
else:
    _logger.info(
        "Cleanup of old database backups succeeded: %s", self.name
    )''',
                    "name": "cleanup_log",
                    "decorator": "@api.multi;@contextmanager",
                    "param": "self",
                    "sequence": 8,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_db_backup.id,
                },
                {
                    "code": '''"""Generate a file name for a backup.

:param datetime.datetime when:
    Use this datetime instead of :meth:`datetime.datetime.now`.
:param str ext: Extension of the file. Default: dump.zip
"""
return "{:%Y_%m_%d_%H_%M_%S}.{ext}".format(
    when, ext="dump.zip" if ext == "zip" else ext
)''',
                    "name": "filename",
                    "decorator": "@staticmethod",
                    "param": "when, ext='zip'",
                    "sequence": 9,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_db_backup.id,
                },
                {
                    "code": '''"""Return a new SFTP connection with found parameters."""
self.ensure_one()
params = {
    "host": self.sftp_host,
    "username": self.sftp_user,
    "port": self.sftp_port,
}

# not empty sftp_public_key means that we should verify sftp server with it
cnopts = pysftp.CnOpts()
if self.sftp_public_host_key:
    key = paramiko.RSAKey(
        data=base64.b64decode(self.sftp_public_host_key)
    )
    cnopts.hostkeys.add(self.sftp_host, "ssh-rsa", key)
else:
    cnopts.hostkeys = None

_logger.debug(
    "Trying to connect to sftp://%(username)s@%(host)s:%(port)d",
    extra=params,
)
if self.sftp_private_key:
    params["private_key"] = self.sftp_private_key
    if self.sftp_password:
        params["private_key_pass"] = self.sftp_password
else:
    params["password"] = self.sftp_password

return pysftp.Connection(**params, cnopts=cnopts)''',
                    "name": "sftp_connection",
                    "decorator": "@api.multi",
                    "param": "self",
                    "sequence": 10,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_db_backup.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add constraint
        if True:
            lst_value = [
                {
                    "name": "db_backup_name_unique",
                    "definition": "UNIQUE(name)",
                    "message": "Cannot duplicate a configuration.",
                    "type": "u",
                    "code_generator_id": code_generator_id.id,
                    "module": code_generator_id.id,
                    "model": model_db_backup.id,
                },
                {
                    "name": "db_backup_days_to_keep_positive",
                    "definition": "CHECK(days_to_keep >= 0)",
                    "message": (
                        "I cannot remove backups from the future. Ask Doc for"
                        " that."
                    ),
                    "type": "u",
                    "code_generator_id": code_generator_id.id,
                    "module": code_generator_id.id,
                    "model": model_db_backup.id,
                },
            ]
            env["ir.model.constraint"].create(lst_value)

        # Generate view
        ##### Begin Views
        lst_view_id = []
        # form view
        if True:
            lst_item_view = []
            # HEADER
            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "header",
                    "item_type": "button",
                    "action_name": "action_backup",
                    "button_type": "oe_highlight",
                    "label": "Execute backup",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            # TITLE
            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "title",
                    "item_type": "field",
                    "action_name": "name",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            # BODY
            view_item_body_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "group",
                    "label": "Basic backup configuration",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_1.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "folder",
                    "parent_id": view_item_body_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "days_to_keep",
                    "parent_id": view_item_body_1.id,
                    "sequence": 2,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "method",
                    "parent_id": view_item_body_1.id,
                    "sequence": 3,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "backup_format",
                    "parent_id": view_item_body_1.id,
                    "sequence": 4,
                }
            )
            lst_item_view.append(view_item.id)

            view_item_body_2 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "div",
                    "attrs": "{'invisible': [('method', '!=', 'sftp')]}",
                    "sequence": 2,
                }
            )
            lst_item_view.append(view_item_body_2.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "html",
                    "background_type": "bg-warning",
                    "label": (
                        "Use SFTP with caution! This writes files to external"
                        " servers under the path you specify."
                    ),
                    "parent_id": view_item_body_2.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item_body_2 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "group",
                    "label": "SFTP Settings",
                    "parent_id": view_item_body_2.id,
                    "sequence": 2,
                }
            )
            lst_item_view.append(view_item_body_2.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "sftp_host",
                    "placeholder": "sftp.example.com",
                    "parent_id": view_item_body_2.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "sftp_port",
                    "parent_id": view_item_body_2.id,
                    "sequence": 2,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "sftp_user",
                    "placeholder": "john",
                    "parent_id": view_item_body_2.id,
                    "sequence": 3,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "sftp_password",
                    "password": True,
                    "parent_id": view_item_body_2.id,
                    "sequence": 4,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "sftp_private_key",
                    "placeholder": "/home/odoo/.ssh/id_rsa",
                    "parent_id": view_item_body_2.id,
                    "sequence": 5,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "sftp_public_host_key",
                    "placeholder": "AAAA...",
                    "parent_id": view_item_body_2.id,
                    "sequence": 6,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "button",
                    "action_name": "action_sftp_test_connection",
                    "icon": "fa-television",
                    "label": "Test SFTP Connection",
                    "parent_id": view_item_body_2.id,
                    "sequence": 7,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "html",
                    "colspan": 2,
                    "label": """
                    Automatic backups of the database can be scheduled as follows:
                    <ol>
                    <li>Go to Settings / Technical / Automation / Scheduled Actions.</li>
                    <li>Search the action named 'Backup scheduler'.</li>
                    <li>Set the scheduler to active and fill in how often you want backups generated.</li>
                    </ol>
                    """,
                    "is_help": True,
                    "sequence": 4,
                }
            )
            lst_item_view.append(view_item.id)

            view_code_generator = env["code.generator.view"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "view_type": "form",
                    # "view_name": "view_backup_conf_form",
                    "m2o_model": model_db_backup.id,
                    "view_item_ids": [(6, 0, lst_item_view)],
                    "id_name": "view_backup_conf_form",
                }
            )
            lst_view_id.append(view_code_generator.id)

        # tree view
        if True:
            lst_item_view = []
            # BODY
            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "name",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "folder",
                    "sequence": 2,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "days_to_keep",
                    "sequence": 3,
                }
            )
            lst_item_view.append(view_item.id)

            view_code_generator = env["code.generator.view"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "view_type": "tree",
                    # "view_name": "view_backup_conf_form",
                    "m2o_model": model_db_backup.id,
                    "view_item_ids": [(6, 0, lst_item_view)],
                    "id_name": "view_backup_conf_tree",
                }
            )
            lst_view_id.append(view_code_generator.id)

        # search view
        if True:
            lst_item_view = []
            # BODY
            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "name",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "folder",
                    "sequence": 2,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "action_name": "sftp_host",
                    "sequence": 3,
                }
            )
            lst_item_view.append(view_item.id)

            view_code_generator = env["code.generator.view"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "view_type": "search",
                    # "view_name": "view_backup_conf_form",
                    "m2o_model": model_db_backup.id,
                    "view_item_ids": [(6, 0, lst_item_view)],
                    "id_name": "view_backup_conf_search",
                }
            )
            lst_view_id.append(view_code_generator.id)

        # act_window view
        if True:
            action_backup_conf_form = env["code.generator.act_window"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "name": "Automated Backups",
                    "id_name": "action_backup_conf_form",
                }
            )

        # menu view
        if True:
            env["code.generator.menu"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "id_name": "backup_conf_menu",
                    "parent_id_name": "base.next_id_9",
                    "m2o_act_window": action_backup_conf_form.id,
                }
            )
        ##### End Views

        # Generate server action
        # action_server view
        if True:
            act_server_id = env["ir.actions.server"].create(
                {
                    "name": "Execute backup(s)",
                    "model_id": model_db_backup.id,
                    "binding_model_id": model_db_backup.id,
                    "state": "code",
                    "code": "records.action_backup()",
                    "comment": 'Execute backup from "More" menu',
                }
            )

            # Add record id name
            env["ir.model.data"].create(
                {
                    "name": "action_server_backup",
                    "model": "ir.actions.server",
                    "module": "auto_backup",
                    "res_id": act_server_id.id,
                    "noupdate": True,
                }
            )

        # Action generate view
        wizard_view = env["code.generator.generate.views.wizard"].create(
            {
                "code_generator_id": code_generator_id.id,
                "enable_generate_all": False,
                "code_generator_view_ids": [(6, 0, lst_view_id)],
            }
        )

        wizard_view.button_generate_views()

        # Generate module
        value = {"code_generator_ids": code_generator_id.ids}
        env["code.generator.writer"].create(value)


def uninstall_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        code_generator_id = env["code.generator.module"].search(
            [("name", "=", MODULE_NAME)]
        )
        if code_generator_id:
            code_generator_id.unlink()
