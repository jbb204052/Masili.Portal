# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from . import models


admin.site.register(models.Hotline)
admin.site.register(models.Resident)
admin.site.register(models.BarangayOfficial)
# admin.site.register(models.EmergencyContact)
# admin.site.register(models.Purok)
admin.site.register(models.BrgyOrganization)
admin.site.register(models.OrgMember)

# BLOTTER
admin.site.register(models.Blotter)
admin.site.register(models.Complainant)
admin.site.register(models.Respondent)
admin.site.register(models.Hearing)


# ANNOUNCEMENT
admin.site.register(models.Announcement)
admin.site.register(models.NotificationsCTA)



admin.site.register(models.Gallery)


admin.site.register(models.Ordinance)

admin.site.register(models.Session)

admin.site.register(models.CertificateRequest)

admin.site.register(models.News)
admin.site.register(models.BusinessPermit)