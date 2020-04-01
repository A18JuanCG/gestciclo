# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Ciclo(models.Model):
    _name = 'gestciclo.ciclo'
    _description = 'Ciclo'
    _rec_name = 'nombre_ciclo'

    nombre_ciclo = fields.Char(required = True)
    descripcion = fields.Text()
    modulos_ids = fields.One2many('gestciclo.modulo', inverse_name = 'ciclo_id')

    @api.constrains('nombre_ciclo')
    def _check_name(self):
        partner_rec = self.env['gestciclo.ciclo'].search([('nombre_ciclo', '=', self.nombre_ciclo), ('id', '!=', self.id)])
        if partner_rec:
            raise ValueError(('El ciclo ya existe'))

class Modulo(models.Model):
    _name = 'gestciclo.modulo'
    _description = 'Módulo'

    name = fields.Char(required = True)
    descripcion = fields.Text()
    horas = fields.Integer(required = True)
    ciclo_id = fields.Many2one('gestciclo.ciclo', ondelete = 'cascade', required = True)
    modsprof_ids = fields.One2many('gestciclo.modsprof', inverse_name = 'modulo_id')
    faltas_ids = fields.One2many('gestciclo.faltas', inverse_name = 'modulo_id')
    contenidos_ids = fields.One2many('gestciclo.contev', inverse_name = 'modulo_id')
    notas_ids = fields.One2many('gestciclo.notaeval', inverse_name = 'modulo_id')

    @api.constrains('name')
    def _check_name(self):
        partner_rec = self.env['gestciclo.modulo'].search([('name', '=', self.name), ('id', '!=', self.id)])
        if partner_rec:
            raise ValueError(('El módulo ya existe'))

class Profesor(models.Model):
    _name = 'gestciclo.profesor'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', ondelete = 'cascade', required = True)
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

    modulo_id = fields.Many2one('gestciclo.modulo', ondelete = 'cascade', required = True)
    profesor_id = fields.Many2one('gestciclo.profesor', ondelete = 'cascade', required = True)
    curso = fields.Char(required = True)
    ciclo = fields.Char('Ciclo', related = 'modulo_id.ciclo_id.nombre_ciclo', required = True)

class Alumno(models.Model):
    _name = 'gestciclo.alumno'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', ondelete='cascade', required = True)
    modsalum_ids = fields.One2many('gestciclo.modsalum', inverse_name = 'alumno_id')
    faltas_ids = fields.One2many('gestciclo.faltas', inverse_name = 'alumno_id')
    notas_cont_ev_ids = fields.One2many('gestciclo.notacontev', inverse_name = 'alumno_id')
    notas_ids = fields.One2many('gestciclo.notaeval', inverse_name = 'alumno_id')
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

    modulo_id = fields.Many2one('gestciclo.modulo', ondelete = 'cascade', required = True)
    alumno_id = fields.Many2one('gestciclo.alumno', ondelete = 'cascade', required = True)
    curso = fields.Char(required = True)
    ciclo = fields.Char('Ciclo', related = 'modulo_id.ciclo_id.nombre_ciclo', required = True)
    horas = fields.Integer('Horas totales del módulo', related = 'modulo_id.horas')
    horas_para_perd_ev = fields.Integer('Horas permitidas para faltas')
    horas_faltadas = fields.Integer('Total de horas faltadas', compute = 'calcular_faltas')
    perdida_evaluacion = fields.Boolean('Pérdida de evaluación continua', compute = 'calcular_perdida_ev', readonly = True)
    nota_final = fields.Float('Nota final', compute = 'calcular_nota_final', digits = (2,1), readonly = True)

    @api.depends('horas_faltadas', 'horas_para_perd_ev')
    def calcular_perdida_ev(self):
        for record in self:
            record.perdida_evaluacion = record.horas_faltadas >= record.horas_para_perd_ev

    @api.model
    def calcular_faltas(self):
        faltas = self.env['gestciclo.faltas']
        for record in self:
            total_horas = 0
            contador_puntualidad = 0
            for falta in faltas.search([('alumno_id.id', '=', record.alumno_id.id), ('modulo_id.id', '=', record.modulo_id.id)]):
                if falta.tipo == 'puntualidad':
                    contador_puntualidad += 1
                    if contador_puntualidad >= 5:
                        total_horas += 1
                        contador_puntualidad = 0
                else:
                    total_horas += falta.horas
            record.horas_faltadas = total_horas

    @api.model
    def calcular_nota_final(self):
        notas = self.env['gestciclo.notaeval']
        for record in self:
            nota_f = 0
            contador = 0
            for nota in notas.search([('alumno_id.id', '=', record.alumno_id.id), ('modulo_id.id', '=', record.modulo_id.id)]):
                nota_f += nota.nota
                contador += 1
            if contador > 0:
                record.nota_final = nota_f / contador
            else:
                record.nota_final = 0

class Faltas(models.Model):
    _name = 'gestciclo.faltas'
    _description = 'Faltas del alumno'
    _rec_name = 'modulo_id'

    modulo_id = fields.Many2one('gestciclo.modulo', ondelete = 'cascade', required = True)
    alumno_id = fields.Many2one('gestciclo.alumno', ondelete = 'cascade', required = True)
    tipo = fields.Selection([('asistencia', 'Asistencia'), ('puntualidad', 'Puntualidad')], required = True)
    fecha = fields.Date()
    horas = fields.Integer()

    @api.constrains('modulo_id')
    def _check_name(self):
        modulos = self.env['gestciclo.modsalum']
        for record in self:
            if len(modulos.search([('modulo_id.id', '=', record.modulo_id.id), ('alumno_id.id', '=', record.alumno_id.id)])) == 0:
                raise ValueError(('El alumno no está matriculado en el módulo'))

class Evaluacion(models.Model):
    _name = 'gestciclo.evaluacion'

    name = fields.Selection([(1, '1ª Evaluación'), (2, '2ª Evaluación'), (3, '3ª Evaluación')], 'Evaluación', required = True)
    contenidos_ids = fields.One2many('gestciclo.contev', inverse_name = 'evaluacion_id')
    notas_ids = fields.One2many('gestciclo.notaeval', inverse_name = 'evaluacion_id')

class ContenidosEvaluables(models.Model):
    _name = 'gestciclo.contev'

    name = fields.Char('Nombre', required = True)
    ciclo = fields.Char('Ciclo', related = 'modulo_id.ciclo_id.nombre_ciclo', required = True)
    modulo_id = fields.Many2one('gestciclo.modulo', ondelete = 'cascade', required = True)
    evaluacion_id = fields.Many2one('gestciclo.evaluacion', ondelete = 'cascade', required = True)
    notas_ids = fields.One2many('gestciclo.notacontev', inverse_name = 'cont_ev_id')
    descripcion = fields.Text()
    tipo = fields.Selection([(1, 'Tarea'), (2, 'Examen')], required = True)
    porcentaje = fields.Integer('Porcent. en cálculo nota', required = True)

class NotaContEv(models.Model):
    _name = 'gestciclo.notacontev'
    _rec_name = 'alumno_id'

    alumno_id = fields.Many2one('gestciclo.alumno', ondelete = 'cascade', required = True)
    cont_ev_id = fields.Many2one('gestciclo.contev', ondelete = 'cascade', required = True)
    ciclo = fields.Char('Ciclo', related = 'cont_ev_id.modulo_id.ciclo_id.nombre_ciclo', required = True)
    modulo = fields.Char('Módulo', related = 'cont_ev_id.modulo_id.name', required = True)
    nota = fields.Float(digits = (2,1))
    fecha = fields.Date()

class NotaEvaluacion(models.Model):
    _name = 'gestciclo.notaeval'
    _rec_name = 'alumno_id'

    alumno_id = fields.Many2one('gestciclo.alumno', ondelete = 'cascade', required = True)
    evaluacion_id = fields.Many2one('gestciclo.evaluacion', ondelete = 'cascade', required = True)
    modulo_id = fields.Many2one('gestciclo.modulo', ondelete = 'cascade', required = True)

    fecha = fields.Date()
    curso = fields.Char(required = True)
    nota = fields.Float(compute = 'calcular_nota_eval', digits = (2,1), readonly = True)

    @api.model
    def calcular_nota_eval(self):
        notas = self.env['gestciclo.notacontev']
        for record in self:
            total = 0
            for nota in notas.search([('alumno_id.id', '=', record.alumno_id.id),
                                    ('cont_ev_id.evaluacion_id.id', '=', record.evaluacion_id.id),
                                    ('cont_ev_id.modulo_id.id', '=', record.modulo_id.id)]):
                total += (nota.nota * nota.cont_ev_id.porcentaje) / 100
            record.nota = total