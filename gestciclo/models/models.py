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
    horas = fields.Integer(required = True)
    ciclo_id = fields.Many2one('gestciclo.ciclo', ondelete = 'cascade')
    modsprof_ids = fields.One2many('gestciclo.modsprof', inverse_name = 'modulo_id')
    faltas_ids = fields.One2many('gestciclo.faltas', inverse_name = 'modulo_id')

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

    @api.constrains('nif')
    def _check_name(self):
        partner_rec = self.env['gestciclo.profesor'].search([('nif', '=', self.nif), ('id', '!=', self.id)])
        if partner_rec:
            raise ValueError(('El NIF ya existe'))

class ModulosProfesor(models.Model):
    _name = 'gestciclo.modsprof'
    _description = 'Módulos impartidos'
    _rec_name = 'modulo_id'
    #poner valor default
    modulo_id = fields.Many2one('gestciclo.modulo', ondelete = 'cascade')
    profesor_id = fields.Many2one('gestciclo.profesor', ondelete = 'cascade')
    curso = fields.Char(required = True)
    ciclo = fields.Char('Ciclo', related = 'modulo_id.ciclo_id.nombre_ciclo')

class Alumno(models.Model):
    _name = 'gestciclo.alumno'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    modsalum_ids = fields.One2many('gestciclo.modsalum', inverse_name = 'alumno_id')
    faltas_ids = fields.One2many('gestciclo.faltas', inverse_name = 'alumno_id')
    nif = fields.Char(required = True)
    fecha_nacimiento = fields.Date('Fecha de nacimiento')

    @api.constrains('nif')
    def _check_name(self):
        partner_rec = self.env['gestciclo.alumno'].search([('nif', '=', self.nif), ('id', '!=', self.id)])
        if partner_rec:
            raise ValueError(('El NIF ya existe'))

class ModulosAlumno(models.Model):
    _name = 'gestciclo.modsalum'
    _description = 'Módulos matriculado'
    _rec_name = 'modulo_id'

    modulo_id = fields.Many2one('gestciclo.modulo', ondelete = 'cascade')
    alumno_id = fields.Many2one('gestciclo.alumno', ondelete = 'cascade')
    curso = fields.Char(required = True)
    ciclo = fields.Char('Ciclo', related = 'modulo_id.ciclo_id.nombre_ciclo')
    horas = fields.Integer('Horas totales del módulo', related = 'modulo_id.horas')
    horas_para_perd_ev = fields.Integer('Horas permitidas para faltas')
    horas_faltadas = fields.Integer('Total de horas faltadas', compute = 'calcular_faltas')
    perdida_evaluacion = fields.Boolean('Pérdida de evaluación continua', compute = 'calcular_perdida_ev', readonly = True)

    @api.depends('horas_faltadas', 'horas_para_perd_ev')
    def calcular_perdida_ev(self):
        for record in self:
            record.perdida_evaluacion = record.horas_faltadas >= record.horas_para_perd_ev

    @api.model
    def calcular_faltas(self):
        faltas = self.env['gestciclo.faltas']
        for record in self:
            total_horas = 0
            for falta in faltas.search([('alumno_id.id', '=', record.alumno_id.id), ('modulo_id.id', '=', record.modulo_id.id)]):
                total_horas += falta.horas
            record.horas_faltadas = total_horas
        #return sum(self.env['gestciclo.faltas'].search[('alumno_id.id', '=', self.alumno_id.id), ('modulo_id.id', '=', self.modulo_id.id)]).mapped('horas')

class Faltas(models.Model):
    _name = 'gestciclo.faltas'
    _description = 'Faltas del alumno'
    _rec_name = 'modulo_id'

    modulo_id = fields.Many2one('gestciclo.modulo', ondelete = 'cascade')
    alumno_id = fields.Many2one('gestciclo.alumno', ondelete = 'cascade')
    tipo = fields.Selection([('asistencia', 'Asistencia'), ('puntualidad', 'Puntualidad')])
    fecha = fields.Date()
    horas = fields.Integer()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100