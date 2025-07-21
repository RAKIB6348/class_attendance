# -*- coding: utf-8 -*-
# from odoo import http


# class ClassAttendance(http.Controller):
#     @http.route('/class_attendance/class_attendance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/class_attendance/class_attendance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('class_attendance.listing', {
#             'root': '/class_attendance/class_attendance',
#             'objects': http.request.env['class_attendance.class_attendance'].search([]),
#         })

#     @http.route('/class_attendance/class_attendance/objects/<model("class_attendance.class_attendance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('class_attendance.object', {
#             'object': obj
#         })

