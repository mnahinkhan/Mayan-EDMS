from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.permissions import (
    permission_document_create, permission_document_new_version
)
from mayan.apps.navigation import Link

from .icons import (
    icon_document_create_multiple, icon_log, icon_source_list,
    icon_source_create
)
from .literals import (
    SOURCE_CHOICE_EMAIL_IMAP, SOURCE_CHOICE_EMAIL_POP3,
    SOURCE_CHOICE_SANE_SCANNER, SOURCE_CHOICE_STAGING, SOURCE_CHOICE_WATCH,
    SOURCE_CHOICE_WEB_FORM
)
from .permissions import (
    permission_sources_create, permission_sources_delete,
    permission_sources_edit, permission_sources_view
)


def condition_check_document_creation_acls(context):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )

    return AccessControlList.objects.restrict_queryset(
        permission=permission_document_create,
        queryset=DocumentType.objects.all(), user=context['user']
    ).exists()


def document_new_version_not_blocked(context):
    NewVersionBlock = apps.get_model(
        app_label='checkouts', model_name='NewVersionBlock'
    )

    return not NewVersionBlock.objects.is_blocked(context['object'])


link_document_create_multiple = Link(
    condition=condition_check_document_creation_acls,
    icon_class=icon_document_create_multiple, text=_('New document'),
    view='sources:document_create_multiple'
)
link_source_check_now = Link(
    kwargs={'source_id': 'resolved_object.pk'},
    permissions=(permission_sources_edit,), text=_('Check now'),
    view='sources:source_check'
)
link_source_create_imap_email = Link(
    icon_class=icon_source_create,
    kwargs={'source_type': '"%s"' % SOURCE_CHOICE_EMAIL_IMAP},
    permissions=(permission_sources_create,),
    text=_('Add new IMAP email'), view='sources:source_create'
)
link_source_create_pop3_email = Link(
    icon_class=icon_source_create,
    kwargs={'source_type': '"%s"' % SOURCE_CHOICE_EMAIL_POP3},
    permissions=(permission_sources_create,),
    text=_('Add new POP3 email'), view='sources:source_create'
)
link_source_create_staging_folder = Link(
    icon_class=icon_source_create,
    kwargs={'source_type': '"%s"' % SOURCE_CHOICE_STAGING},
    permissions=(permission_sources_create,),
    text=_('Add new staging folder'), view='sources:source_create'
)
link_source_create_watch_folder = Link(
    icon_class=icon_source_create,
    kwargs={'source_type': '"%s"' % SOURCE_CHOICE_WATCH},
    permissions=(permission_sources_create,),
    text=_('Add new watch folder'), view='sources:source_create'
)
link_source_create_webform = Link(
    icon_class=icon_source_create,
    kwargs={'source_type': '"%s"' % SOURCE_CHOICE_WEB_FORM},
    permissions=(permission_sources_create,),
    text=_('Add new webform source'), view='sources:source_create'
)
link_source_create_sane_scanner = Link(
    icon_class=icon_source_create,
    kwargs={'source_type': '"%s"' % SOURCE_CHOICE_SANE_SCANNER},
    permissions=(permission_sources_create,),
    text=_('Add new SANE scanner'), view='sources:source_create'
)
link_source_delete = Link(
    kwargs={'source_id': 'resolved_object.pk'},
    permissions=(permission_sources_delete,), tags='dangerous',
    text=_('Delete'), view='sources:source_delete'
)
link_source_edit = Link(
    kwargs={'source_id': 'resolved_object.pk'},
    permissions=(permission_sources_edit,), text=_('Edit'),
    view='sources:source_edit'
)
link_source_list = Link(
    icon_class=icon_source_list,
    permissions=(permission_sources_view,), text=_('Sources'),
    view='sources:source_list'
)
link_source_logs = Link(
    icon_class=icon_log, kwargs={'source_id': 'resolved_object.pk'},
    permissions=(permission_sources_view,), text=_('Logs'),
    view='sources:source_logs'
)
link_staging_file_delete = Link(
    keep_query=True, kwargs={
        'staging_file_pk': 'source.pk',
        'encoded_filename': 'object.encoded_filename'
    }, permissions=(permission_document_new_version, permission_document_create),
    tags='dangerous', text=_('Delete'), view='sources:staging_file_delete'
)
link_upload_version = Link(
    condition=document_new_version_not_blocked,
    kwargs={'document_pk': 'resolved_object.pk'},
    permissions=(permission_document_new_version,),
    text=_('Upload new version'), view='sources:upload_version'
)
