# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Ciclo(models.Model):
    _name = 'gestciclo.ciclo'
    _description = 'Ciclo'

    nombre = fields.Char()
    descripcion = fields.Text()

class Modulo(models.Model):
    _name = 'gestciclo.modulo'
    _description = 'Módulo'

    nombre = fields.Char()
    descripcion = fields.Text()
    ciclo_id = fields.Many2one('gestciclo.ciclo', ondelete = 'cascade')
    
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100