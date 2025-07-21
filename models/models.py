# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class class_attendance(models.Model):
#     _name = 'class_attendance.class_attendance'
#     _description = 'class_attendance.class_attendance'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

