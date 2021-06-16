# Copyright 2019 Coop IT Easy SCRLfs
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import os

from odoo import http
import odoo.addons.hw_proxy.controllers.main as hw_proxy
from odoo.http import request
from odoo.modules.module import get_module_path
from odoo.tools.config import config

from checksumdir import dirhash

CERT_DIR = config.get('certified_modules_directory', 'hw_certified_modules')
USER_DIR = os.path.expanduser("~")


class ModuleHashPage(hw_proxy.Proxy):
    @http.route("/hw_proxy/module_hash", type="http", auth="none", cors="*")
    def modules_hash(self):

        base_dir = self.get_certified_modules_directory()
        dir_hash = dirhash(base_dir, "sha256", excluded_extensions=["pyc"])

        res = """
              <!DOCTYPE HTML>
              <html>
                  <head>
                      <title>Hardware Hash Certification (hw_hash_cert) : v12.0.1.0</title>
                      <style>
                      body {{
                          width: 800px;
                          margin: 60px auto;
                          font-family: sans-serif;
                          text-align: justify;
                          color: #6B6B6B;
                      }}
                      </style>
                  </head>
                  <body>
                      <h1>Hardware Hash Certification (hw_hash_cert) : v12.0.1.0</h1>
                      <div>
                        <p>
                        {}
                        </p>
                      </div>
                  </body>
              </html>
        """.format(
            dir_hash
        )
        return request.make_response(
            res,
            {
                "Cache-Control": "no-cache",
                "Content-Type": "text/html; charset=utf-8",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
            },
        )

    def get_certified_modules_directory(self):

        start_dir = os.path.dirname(os.path.realpath(__file__))
        last_root = start_dir
        current_root = start_dir
        found_cert_dir = None

        while found_cert_dir is None and current_root != USER_DIR:
            pruned = False
            for root, dirs, files in os.walk(current_root):
                if not pruned:
                    try:
                        # Remove the part of the tree we already searched
                        del dirs[dirs.index(os.path.basename(last_root))]
                        pruned = True
                    except ValueError:
                        pass
                if CERT_DIR in dirs:
                    # found the directory, stop
                    found_cert_dir = os.path.join(root, CERT_DIR)
                    break
                # Otherwise, pop up a level, search again
            last_root = current_root
            current_root = os.path.dirname(last_root)

        if found_cert_dir:
            return found_cert_dir
        return os.path.dirname(get_module_path("hw_hash_cert"))
