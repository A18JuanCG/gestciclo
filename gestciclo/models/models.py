# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Ciclo(models.Model):
    _name = 'gestciclo.ciclo'
    _description = 'Ciclo'
    _rec_name = 'nombre_ciclo'

    nombre_ciclo = fields.Char(required = True)
    descripcion = fields.Text()
    modulos_ids = fields.One2many('gestciclo.modulo', inverse_name = 'ciclo_id')

    @api.constrains('name')
    def _check_name(self):
        partner_rec = self.env['gestciclo.ciclo'].search([('name', '=', self.name), ('id', '!=', self.id)])
        if partner_rec:
            raise ValueError(('El ciclo ya existe'))

class Modulo(models.Model):
    _name = 'gestciclo.modulo'
    _description = 'Módulo'

    name = fields.Char(required = True)
    descripcion = fields.Text()
    ciclo_id = fields.Many2one('gestciclo.ciclo', ondelete = 'cascade')
    modsprof_ids = fields.One2many('gestciclo.modsprof', inverse_name = 'modulo_id')

    @api.constrains('name')
    def _check_name(self):
        partner_rec = self.env['gestciclo.modulo'].search([('name', '=', self.name), ('id', '!=', self.id)])
        if partner_rec:
            raise ValueError(('El módulo ya existe'))

class Profesor(models.Model):
    _name = 'gestciclo.profesor'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', ondelete = 'cascade')
    modsprof_ids = fields.One2many('gestciclo.modsprof', inverse_name = 'profesor_id')
    nif = fields.Char(required = True)
    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')

    @api.constrains('nif')
    def _check_name(self):
        partner_rec = self.env['gestciclo.profesor'].search([('nif', '=', self.nif), ('id', '!=', self.id)])
        if partner_rec:
            raise ValueError(('El NIF ya existe'))

class ModulosProfesor(models.Model):
    _name = 'gestciclo.modsprof'
    _description = 'Módulos impartidos'
    _rec_name = 'modulo_id'

    modulo_id = fields.Many2one('gestciclo.modulo', ondelete = 'cascade')
    profesor_id = fields.Many2one('gestciclo.profesor', ondelete = 'cascade')
    curso = fields.Char()
    ciclo = fields.Char('Ciclo', related = 'modulo_id.ciclo_id.nombre_ciclo')

class Alumno(models.Model):
    _name = 'gestciclo.alumno'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    nif = fields.Char(required = True)
    fecha_nacimiento = fields.Date('Fecha de nacimiento')
    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')

    @api.constrains('nif')
    def _check_name(self):
        partner_rec = self.env['gestciclo.alumno'].search([('nif', '=', self.nif), ('id', '!=', self.id)])
        if partner_rec:
            raise ValueError(('El NIF ya existe'))
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100