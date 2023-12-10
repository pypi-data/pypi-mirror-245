from django.conf.urls import url

from .api_views import (
    APIEventListView, APIEventTypeListView, APIEventTypeNamespaceDetailView,
    APIEventTypeNamespaceEventTypeListView, APIEventTypeNamespaceListView,
    APINotificationListView, APIObjectEventListView
)
from .views.clear_views import (
    EventListClearView, ObjectEventClearView, VerbEventClearView
)
from .views.event_views import (
    EventListView, ObjectEventListView, VerbEventListView
)
from .views.export_views import (
    EventListExportView, ObjectEventExportView, VerbEventExportView
)
from .views.notification_views import (
    NotificationListView, NotificationMarkRead, NotificationMarkReadAll
)
from .views.subscription_views import (
    EventTypeSubscriptionListView, ObjectEventTypeSubscriptionListView
)


urlpatterns_events = [
    url(regex=r'^events/$', name='events_list', view=EventListView.as_view()),
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/events/$',
        name='events_for_object', view=ObjectEventListView.as_view()
    ),
    url(
        regex=r'^verbs/(?P<verb>[\w\-\.]+)/$', name='events_by_verb',
        view=VerbEventListView.as_view(),
    )
]

urlpatterns_events_clear = [
    url(
        regex=r'^events/clear/$', name='events_list_clear',
        view=EventListClearView.as_view()
    ),
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/events/clear/$',
        name='events_for_object_clear', view=ObjectEventClearView.as_view()
    ),
    url(
        regex=r'^verbs/(?P<verb>[\w\-\.]+)/clear/$', name='events_by_verb_clear',
        view=VerbEventClearView.as_view(),
    )
]

urlpatterns_events_export = [
    url(
        regex=r'^events/export/$', name='events_list_export',
        view=EventListExportView.as_view()
    ),
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/events/export/$',
        name='events_for_object_export', view=ObjectEventExportView.as_view()
    ),
    url(
        regex=r'^verbs/(?P<verb>[\w\-\.]+)/export/$', name='events_by_verb_export',
        view=VerbEventExportView.as_view(),
    )
]

urlpatterns_notification = [
    url(
        regex=r'^user/notifications/$', name='user_notifications_list',
        view=NotificationListView.as_view()
    ),
    url(
        regex=r'^user/notifications/(?P<notification_id>\d+)/mark_read/$',
        name='notification_mark_read', view=NotificationMarkRead.as_view()
    ),
    url(
        regex=r'^user/notifications/all/mark_read/$',
        name='notification_mark_read_all',
        view=NotificationMarkReadAll.as_view()
    ),
]

urlpatterns_subscriptions = [
    url(
        regex=r'^user/event_types/subscriptions/$',
        name='event_types_user_subscriptions_list',
        view=EventTypeSubscriptionListView.as_view()
    ),
    url(
        regex=r'^user/object/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/subscriptions/$',
        name='object_event_types_user_subscriptions_list',
        view=ObjectEventTypeSubscriptionListView.as_view()
    ),
]

urlpatterns = []
urlpatterns.extend(urlpatterns_events)
urlpatterns.extend(urlpatterns_events_clear)
urlpatterns.extend(urlpatterns_events_export)
urlpatterns.extend(urlpatterns_notification)
urlpatterns.extend(urlpatterns_subscriptions)

api_urls = [
    url(
        regex=r'^event_type_namespaces/(?P<name>[-\w]+)/$',
        name='event-type-namespace-detail',
        view=APIEventTypeNamespaceDetailView.as_view()
    ),
    url(
        regex=r'^event_type_namespaces/(?P<name>[-\w]+)/event_types/$',
        name='event-type-namespace-event-type-list',
        view=APIEventTypeNamespaceEventTypeListView.as_view()
    ),
    url(
        regex=r'^event_type_namespaces/$',
        name='event-type-namespace-list',
        view=APIEventTypeNamespaceListView.as_view()
    ),
    url(
        regex=r'^event_types/$', name='event-type-list',
        view=APIEventTypeListView.as_view()
    ),
    url(
        regex=r'^events/$', name='event-list', view=APIEventListView.as_view()
    ),
    url(
        regex=r'^notifications/$', name='notification-list',
        view=APINotificationListView.as_view()
    ),
    url(
        regex=r'^objects/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/events/$',
        name='object-event-list', view=APIObjectEventListView.as_view()
    ),
]
