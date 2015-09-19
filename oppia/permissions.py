# oppia/permissions.py

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse

from itertools import chain

from oppia.models import Course, Participant

def can_upload(request):
    if settings.OPPIA_STAFF_ONLY_UPLOAD is True and not request.user.is_staff and request.user.userprofile.can_upload is False:
        return False
    else:
        return True
           
def check_owner(request,id):
    try:
        # check only the owner can view 
        if request.user.is_staff:
            course = Course.objects.get(pk=id)
        else:
            try:
                course = Course.objects.get(pk=id,user=request.user)
            except Course.DoesNotExist:
                course = Course.objects.get(pk=id,coursemanager__course__id=id, coursemanager__user = request.user)
    except Course.DoesNotExist:
        raise Http404
    return course

def get_user(request, view_user_id):
    if request.user.is_staff or (request.user.id == int(view_user_id)):
        try:
            view_user = User.objects.get(pk=view_user_id)
            return view_user, None
        except User.DoesNotExist:
            raise Http404()
    else: 
        try:
            view_user = User.objects.get(pk=view_user_id)
            courses = Course.objects.filter(coursecohort__cohort__participant__user=view_user, 
                                        coursecohort__cohort__participant__role=Participant.STUDENT) \
                                .filter(coursecohort__cohort__participant__user=request.user, 
                                        coursecohort__cohort__participant__role=Participant.TEACHER).count()
            if courses > 0:
                return view_user, None
            else:
                return None, HttpResponse('Unauthorized', status=401)
        except User.DoesNotExist:
            return None, HttpResponse('Unauthorized', status=401)



def get_user_courses(request, view_user):
    
    if request.user.is_staff or request.user == view_user:
        # get all courses user has taken part in
        # plus all those they are students on
        cohort_courses = Course.objects.filter(coursecohort__cohort__participant__user=view_user, 
                                        coursecohort__cohort__participant__role=Participant.STUDENT).distinct().order_by('title')
        other_courses = Course.objects.filter(tracker__user=view_user).exclude(pk__in=cohort_courses.values_list('id', flat=True)).distinct().order_by('title')
    else:
        cohort_courses = Course.objects.filter(coursecohort__cohort__participant__user=view_user, 
                                        coursecohort__cohort__participant__role=Participant.STUDENT) \
                                .filter(coursecohort__cohort__participant__user=request.user, 
                                        coursecohort__cohort__participant__role=Participant.TEACHER).distinct().order_by('title')
        other_courses = None
        
    all_courses = list(chain(cohort_courses, other_courses))    
    return cohort_courses, other_courses, all_courses

def is_manager(course_id,user):
    try:
        # check only the owner can view 
        if user.is_staff:
            return True
        else:
            try:
                course = Course.objects.get(pk=course_id,user=user)
                return True
            except Course.DoesNotExist:
                course = Course.objects.get(pk=course_id,coursemanager__course__id=course_id, coursemanager__user = user)
                return True
    except Course.DoesNotExist:
        return False


def course_can_view(request,id):
    try:
        if request.user.is_staff:
            course = Course.objects.get(pk=id)
        else:
            try:
                course = Course.objects.get(pk=id,is_draft=False,is_archived=False)
            except Course.DoesNotExist:
                course = Course.objects.get(pk=id,is_draft=False,is_archived=False, coursemanager__course__id=id, coursemanager__user = request.user)
    except Course.DoesNotExist:
        raise Http404
    return course