from pmdb.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

def project_report(request,Project_id):
    return render_to_response(
        "pmdb/admin/project_report.html",
        {'part_list' : PartChange.objects.filter(Project=Project_id)},
        RequestContext(request, {}),
    )
project_report = staff_member_required(project_report)

