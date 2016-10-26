import datetime
import os
import sys
import string
import subprocess
import signal

from django.core import mail
from pprint import pprint as pp


def to_select(data, key, value, default='---------', type=None):
    if default==None:
        if type=='date':
            return [(x[key], x[value].strftime('%d-%b-%Y')) for x in data]
        else:
            return [(x[key], x[value]) for x in data]
    else:
        if type=='date':
            return [('', default)] + [(x[key], x[value].strftime('%d-%b-%Y')) for x in data]
        else:
            return [('', default)] + [(x[key], x[value]) for x in data]

def instance_dict(instance, key_format=None):
    "Returns a dictionary containing field names and values for the given instance"
    from django.db.models.fields.related import ForeignKey
    from django.core.exceptions import ObjectDoesNotExist

    if key_format:
        assert '%s' in key_format, 'key_format must contain a %s'

    key = lambda key: key_format and key_format % key or key

    d = {}

    for field in instance._meta.fields:
        attr = field.name

        try:
            value = getattr(instance, attr)
        except ObjectDoesNotExist:
            value = None

        if value is not None and isinstance(field, ForeignKey):
            value = value._get_pk_val()

        d[key(attr)] = value

    for field in instance._meta.many_to_many:
        d[key(field.name)] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]

    return d

def map_to_key(data, key='id'):
    d = {}
    for x in data:
        d[x[key]] = x

    return d
    #return [{x[key]: x} for x in data]

def map_to_key_object(data, key='id'):
    d = {}
    for x in data:
        d[getattr(x,key)] = x

    return d
   
def has_permission(request, permission, project=None):
    project_name = project
    if project == None:
        project_name = request.info.get('current_projectname')
        
    if permission in request.user.get('perms'):
        if project_name == None:
            return True
            
        else:
            for proj in request.user.get('perms')[permission]:
                if project_name == proj:
                    return True                       
            
    return False

def sort_by_key(d):
    temp = SortedDict() 
    for key in sorted(d.iterkeys()):
        temp[key] = d[key]

    return temp

def send_email(subject, body, to, from_email, files=[]):
    email = mail.EmailMessage(subject, body, from_email, to, attachments=files)
    email.content_subtype = "html"
    email.send()

def send_email_to_role(subject, body, from_email, role, project):
    con = pyodbc.connect(ZIMDBCONNSTR)
    cur = con.cursor()
    sql = 'EXEC [zim].[XSP_Get_Users_By_Role_In_Project] \'{0}\', \'{1}\''.format(role, project)
    cur.execute(sql)
    rows = dictfetchall(cur)
    logins = [x['vcAD_LOGIN'] for x in rows]

    users = search_ad(logins)
    emails = [x['email'] for x in users]
    send_email(subject, body, emails, from_email)


def mount(unc, mountpoint='/mnt/tmp', cred_path='/root/.smbcred_ccmask'):

    '''mounts a cifs unc.
        on success, returns the local mountpoint
        on failure, raises an exception'''
    try:
        os.mkdir(mountpoint)
    except OSError:
        pass  # OSError is raised on "Already Exists"

    cmd = '/usr/bin/mount.cifs {0} {1} -o credentials={2}'
    cmd = cmd.format(unc, mountpoint, cred_path)
    pp('DEBUG: executing "{0}"'.format(cmd))

    # send an alarm after 30s
    signal.alarm(30)
    ##TODO: Fix time out code.
    # try:
    subprocess.check_call(cmd, shell=True)
    signal.alarm(0)  # clear alarm
    # except signal.Alarm:
    #     print('timeout!')
    
    return mountpoint
    
def umount(mountpoint='/mnt/tmp'):
    '''unmounts a mountpoint'''
    cmd = '/bin/umount {0}'.format(mountpoint)
    ##TODO: Stop failing if nothing to unmount.
    return subprocess.check_call(cmd, shell=True)
                                                                                                        
if __name__ == '__main__':
    get_contractors_by_permission()
