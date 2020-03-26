# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Ciclo(models.Model):
    _name = 'gestciclo.ciclo'
    _description = 'Ciclo'

    name = fields.Char()
    descripcion = fields.Text()

class Modulo(models.Model):
    _name = 'gestciclo.modulo'
    _description = 'Módulo'

    name = fields.Char()
    descripcion = fields.Text()
    ciclo_id = fields.Many2one('gestciclo.ciclo', ondelete = 'cascade')

class Profesor(models.Model):
    _name = 'gestciclo.profesor'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    fecha_nacimiento = fields.Date('Fecha de nacimiento')
    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100