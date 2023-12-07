#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.05 22:00:00                  #
# ================================================== #

from urllib.request import urlopen, Request
from packaging.version import parse as parse_version
import os
import shutil
import json
import ssl
from .utils import trans


class Updater:
    def __init__(self, window=None):
        """
        Updater (patcher)

        :param window: main window
        """
        self.window = window

    def check(self):
        """Checks for updates"""
        print("Checking for updates...")
        url = self.window.website + "/api/version?v=" + str(self.window.version)
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            req = Request(
                url=url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            response = urlopen(req, context=ctx, timeout=3)
            data_json = json.loads(response.read())
            newest_version = data_json["version"]
            newest_build = data_json["build"]

            # changelog
            changelog = ""
            if "changelog" in data_json:
                changelog = data_json["changelog"]

            parsed_newest_version = parse_version(newest_version)
            parsed_current_version = parse_version(self.window.version)
            if parsed_newest_version > parsed_current_version:
                self.show_version_dialog(newest_version, newest_build, changelog)
            else:
                print("No updates available")
        except Exception as e:
            print("Failed to check for updates")
            print(e)

    def show_version_dialog(self, version, build, changelog):
        """
        Displays new version dialog

        :param version: version number
        :param build: build date
        :param changelog: changelog
        """
        txt = trans('update.new_version') + ": " + str(version) + " (" + trans('update.released') + ": " + str(
            build) + ")"
        txt += "\n" + trans('update.current_version') + ": " + self.window.version
        self.window.dialog['update'].changelog.setPlainText(changelog)
        self.window.dialog['update'].message.setText(txt)
        self.window.ui.dialogs.open('update')

    def patch(self):
        """Patch config files to current version"""
        try:
            self.patch_config()
            self.patch_models()
            self.patch_presets()
            # TODO: add context patcher
        except Exception as e:
            print("Failed to patch config files!")
            print(e)

    def patch_dir(self, dirname="", force=False):
        """
        Patches directory
        :param dirname: Directory name
        :param force: Force update
        """
        try:
            # dir
            dst_dir = os.path.join(self.window.config.path, dirname)
            src = os.path.join(self.window.config.get_root_path(), 'data', 'config', dirname)
            for file in os.listdir(src):
                src_file = os.path.join(src, file)
                dst_file = os.path.join(dst_dir, file)
                if not os.path.exists(dst_file) or force:
                    shutil.copyfile(src_file, dst_file)
        except Exception as e:
            print(e)

    def patch_file(self, filename="", force=False):
        """
        Patches file
        :param filename: File name
        :param force: Force update
        """
        try:
            # file
            dst = os.path.join(self.window.config.path, filename)
            if not os.path.exists(dst) or force:
                src = os.path.join(self.window.config.get_root_path(), 'data', 'config', filename)
                shutil.copyfile(src, dst)
        except Exception as e:
            print(e)

    def patch_models(self):
        """Migrates models to current version"""
        data = self.window.config.models
        version = "0.0.0"
        updated = False
        if '__meta__' in data and 'version' in data['__meta__']:
            version = data['__meta__']['version']
        old = parse_version(version)
        current = parse_version(self.window.version)
        if old < current:
            if old < parse_version("2.0.0"):
                self.patch_file('models.json', True)
                updated = True
            if old < parse_version("0.9.1"):
                # apply meta only (not attached in 0.9.0)
                updated = True

        # update file
        if updated:
            data = dict(sorted(data.items()))
            self.window.config.models = data
            self.window.config.save_models()
            print("Migrated models.json.")

    def patch_presets(self):
        """Migrates presets to current version"""
        for k in self.window.config.presets:
            data = self.window.config.presets[k]
            version = "0.0.0"
            updated = False
            if '__meta__' in data and 'version' in data['__meta__']:
                version = data['__meta__']['version']
            old = parse_version(version)
            current = parse_version(self.window.version)
            if old < current:
                if old < parse_version("2.0.0"):
                    self.patch_file('presets', True)

            # update file
            if updated:
                data = dict(sorted(data.items()))
                self.window.config.presets[k] = data
                self.window.config.save_preset(k)
                print("Migrated presets.")

    def patch_config(self):
        """Migrates config to current version"""
        data = self.window.config.data
        version = "0.0.0"
        updated = False
        if '__meta__' in data and 'version' in data['__meta__']:
            version = data['__meta__']['version']
        old = parse_version(version)
        current = parse_version(self.window.version)
        if old < current:
            if old < parse_version("2.0.0"):
                data['theme'] = 'dark_teal'  # force, because removed light themes!
                if 'cmd' not in data:
                    data['cmd'] = True
                if 'stream' not in data:
                    data['stream'] = True
                if 'attachments_send_clear' not in data:
                    data['attachments_send_clear'] = True
                if 'assistant' not in data:
                    data['assistant'] = None
                if 'assistant_thread' not in data:
                    data['assistant_thread'] = None
                updated = True
            if old < parse_version("0.9.6"):
                print("Migrating config from < 0.9.6...")
                data['debug'] = True  # enable debug by default
                updated = True
            if old < parse_version("0.9.4"):
                print("Migrating config from < 0.9.4...")
                if 'plugins' not in data:
                    data['plugins'] = {}
                if 'plugins_enabled' not in data:
                    data['plugins_enabled'] = {}
                updated = True
            if old < parse_version("0.9.2"):
                print("Migrating config from < 0.9.2...")
                keys_to_remove = ['ui.ctx.min_width',
                                  'ui.ctx.max_width',
                                  'ui.toolbox.min_width',
                                  'ui.toolbox.max_width',
                                  'ui.dialog.settings.width',
                                  'ui.dialog.settings.height',
                                  'ui.chatbox.font.color']
                for key in keys_to_remove:
                    if key in data:
                        del data[key]
                if 'theme' not in data:
                    data['theme'] = "dark_teal"
                updated = True

            if old < parse_version("0.9.1"):
                print("Migrating config from < 0.9.1...")
                keys_to_remove = ['user_id', 'custom']  # not needed anymore
                for key in keys_to_remove:
                    if key in data:
                        del data[key]
                keys_to_add = ['organization_key']
                for key in keys_to_add:
                    if key not in data:
                        data[key] = ""
                updated = True

        # update file
        if updated:
            data = dict(sorted(data.items()))
            self.window.config.data = data
            self.window.config.save()
            print("Migrated config.json.")
