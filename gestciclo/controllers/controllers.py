# -*- coding: utf-8 -*-
from odoo import http

# class Gestciclo(http.Controller):
#     @http.route('/gestciclo/gestciclo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestciclo/gestciclo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestciclo.listing', {
#             'root': '/gestciclo/gestciclo',
#             'objects': http.request.env['gestciclo.gestciclo'].search([]),
#         })

#     @http.route('/gestciclo/gestciclo/objects/<model("gestciclo.gestciclo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestciclo.object', {
#             'object': obj
#         })