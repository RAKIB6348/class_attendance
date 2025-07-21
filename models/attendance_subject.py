from odoo import models, fields


class AttendanceSubject(models.Model):
    _name = "attendance.subject"
    _description = "Attendance Subject"

    name = fields.Char(string="Subject Name", required=True)
    code = fields.Char(string="Subject Code", required=True)