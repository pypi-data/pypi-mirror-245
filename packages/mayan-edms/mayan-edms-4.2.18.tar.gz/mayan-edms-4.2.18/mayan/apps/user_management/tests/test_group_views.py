from django.contrib.auth.models import Group

from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.metadata.permissions import permission_document_metadata_edit
from mayan.apps.metadata.tests.mixins import MetadataTypeTestMixin
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_group_created, event_group_edited
from ..permissions import (
    permission_group_create, permission_group_delete, permission_group_edit,
    permission_group_view, permission_user_edit
)

from .mixins import (
    GroupTestMixin, GroupUserViewTestMixin, GroupViewTestMixin
)


class GroupViewsTestCase(
    GroupTestMixin, GroupViewTestMixin, GenericViewTestCase
):
    def test_group_create_view_no_permission(self):
        group_count = Group.objects.count()

        self._clear_events()

        response = self._request_test_group_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Group.objects.count(), group_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_create_view_with_permission(self):
        self.grant_permission(permission=permission_group_create)

        group_count = Group.objects.count()

        self._clear_events()

        response = self._request_test_group_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Group.objects.count(), group_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_group)
        self.assertEqual(events[0].verb, event_group_created.id)

    def test_group_delete_single_view_no_permission(self):
        self._create_test_group()

        group_count = Group.objects.count()

        self._clear_events()

        response = self._request_test_group_delete_single_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Group.objects.count(), group_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_delete_single_view_with_access(self):
        self._create_test_group()
        self.grant_access(
            obj=self.test_group, permission=permission_group_delete
        )

        group_count = Group.objects.count()

        self._clear_events()

        response = self._request_test_group_delete_single_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Group.objects.count(), group_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_delete_multiple_view_no_permission(self):
        self._create_test_group()

        group_count = Group.objects.count()

        self._clear_events()

        response = self._request_test_group_delete_multiple_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Group.objects.count(), group_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_delete_multiple_view_with_access(self):
        self._create_test_group()

        group_count = Group.objects.count()

        self.grant_access(
            obj=self.test_group, permission=permission_group_delete
        )

        self._clear_events()

        response = self._request_test_group_delete_multiple_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Group.objects.count(), group_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_edit_view_no_permission(self):
        self._create_test_group()

        group_name = self.test_group.name

        self._clear_events()

        response = self._request_test_group_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_group.refresh_from_db()
        self.assertEqual(self.test_group.name, group_name)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_edit_view_with_access(self):
        self._create_test_group()
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        group_name = self.test_group.name

        self._clear_events()

        response = self._request_test_group_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_group.refresh_from_db()
        self.assertNotEqual(self.test_group.name, group_name)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_group)
        self.assertEqual(events[0].verb, event_group_edited.id)

    def test_group_list_view_no_permission(self):
        self._create_test_group()

        self._clear_events()

        response = self._request_test_group_list_view()
        self.assertNotContains(
            response=response, text=self.test_group.name, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_list_view_with_permission(self):
        self._create_test_group()

        self.grant_access(
            obj=self.test_group, permission=permission_group_view
        )

        self._clear_events()

        response = self._request_test_group_list_view()
        self.assertContains(
            response=response, text=self.test_group.name, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class GroupAddRemoveUserViewTestCase(
    GroupTestMixin, GroupUserViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_group()
        self._create_test_user()

    def test_group_user_add_remove_get_view_no_permission(self):
        self.test_user.groups.add(self.test_group)

        self._clear_events()

        response = self._request_test_group_user_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_user),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_group),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_remove_get_view_with_user_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_user),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_group),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_remove_get_view_with_group_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_user),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_group),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_remove_get_view_with_full_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self.test_user),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_group),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_view_no_permission(self):
        self._clear_events()

        response = self._request_test_group_user_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_user not in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_view_with_user_access(self):
        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_user not in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_view_with_group_access(self):
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_user not in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_view_with_full_access(self):
        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_user in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_user)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_group)
        self.assertEqual(events[0].verb, event_group_edited.id)

    def test_group_user_remove_view_no_permission(self):
        self.test_user.groups.add(self.test_group)

        self._clear_events()

        response = self._request_test_group_user_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_user in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_remove_view_with_user_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_group_user_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_user in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_remove_view_with_group_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_user_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_user in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_remove_view_with_full_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_user_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_user not in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_user)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_group)
        self.assertEqual(events[0].verb, event_group_edited.id)


class SuperUserGroupAddRemoveViewTestCase(
    GroupTestMixin, GroupUserViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_group()
        self._create_test_superuser()
        self.test_user = self.test_superuser

    def test_group_user_add_remove_get_view_no_permission(self):
        self.test_user.groups.add(self.test_group)

        self._clear_events()

        response = self._request_test_group_user_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_user),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_group),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_remove_get_view_with_user_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_user),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_group),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_remove_get_view_with_group_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_user),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_group),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_remove_get_view_with_full_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_user),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_group),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_view_no_permission(self):
        self._clear_events()

        response = self._request_test_group_user_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_user not in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_view_with_user_access(self):
        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_user not in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_view_with_group_access(self):
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_user not in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_view_with_full_access(self):
        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_user not in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_remove_view_no_permission(self):
        self.test_user.groups.add(self.test_group)

        self._clear_events()

        response = self._request_test_group_user_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_user in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_remove_view_with_user_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_group_user_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_user in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_remove_view_with_group_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_user_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_user in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_remove_view_with_full_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_user_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_user in self.test_group.user_set.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class MetadataLookupIntegrationTestCase(
    MetadataTypeTestMixin, GenericDocumentViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_metadata_type()
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )

    def test_group_list_lookup_render(self):
        self.test_metadata_type.lookup = '{{ groups }}'
        self.test_metadata_type.save()
        self.test_document.metadata.create(
            metadata_type=self.test_metadata_type
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        self._clear_events()

        response = self.get(
            viewname='metadata:metadata_edit', kwargs={
                'document_id': self.test_document.pk
            }
        )

        self.assertContains(
            response=response, text='<option value="{}">{}</option>'.format(
                self._test_case_group.name, self._test_case_group.name
            ), status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
