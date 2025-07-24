from odoo import models, fields


class AttendanceClassroom(models.Model):
    _name = "attendance.classroom"
    _description = "Attendance Classroom"

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Classroom name must be unique!')
    ]