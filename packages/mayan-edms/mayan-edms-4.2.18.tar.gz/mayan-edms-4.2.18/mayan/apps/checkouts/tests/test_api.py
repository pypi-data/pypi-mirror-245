from django.utils.encoding import force_text

from rest_framework import status

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_document_checked_in, event_document_checked_out,
    event_document_forcefully_checked_in
)
from ..permissions import (
    permission_document_check_in, permission_document_check_in_override,
    permission_document_check_out, permission_document_check_out_detail_view
)

from .mixins import (
    DocumentCheckoutsAPIViewTestMixin, DocumentCheckoutTestMixin
)


class CheckoutsAPITestCase(
    DocumentCheckoutsAPIViewTestMixin, DocumentCheckoutTestMixin,
    DocumentTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_document_check_out_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_check_out_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertFalse(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_check_out
        )

        self._clear_events()

        response = self._request_test_document_check_out_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_checked_out.id)

    def test_trashed_document_check_out_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_check_out
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_check_out_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertFalse(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_delete_api_view_no_permission(self):
        self._check_out_test_document()

        self._clear_events()

        response = self._request_test_document_check_out_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_delete_api_view_with_access(self):
        self._check_out_test_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_check_in
        )

        self._clear_events()

        response = self._request_test_document_check_out_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(
            events[0].verb, event_document_checked_in.id
        )

    def test_trashed_document_check_out_delete_api_view_with_access(self):
        self._check_out_test_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_check_in
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_check_out_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_in_forcefull_api_view_no_permission(self):
        self._create_test_user()
        self._check_out_test_document(user=self.test_user)

        self.grant_access(
            obj=self.test_document, permission=permission_document_check_in
        )

        self._clear_events()

        response = self._request_test_document_check_out_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_in_forcefull_api_view_with_access(self):
        self._create_test_user()
        self._check_out_test_document(user=self.test_user)

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_in_override
        )

        self._clear_events()

        response = self._request_test_document_check_out_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(
            events[0].verb, event_document_forcefully_checked_in.id
        )

    def test_trashed_document_check_in_forcefull_api_view_with_access(self):
        self._create_test_user()
        self._check_out_test_document(user=self.test_user)

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_in_override
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_check_out_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_detail_api_view_no_permission(self):
        self._check_out_test_document()

        self._clear_events()

        response = self._request_test_document_check_out_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_detail_api_view_with_check_out_detail_access(self):
        self._check_out_test_document()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        self._clear_events()

        response = self._request_test_document_check_out_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_detail_api_view_with_document_access(self):
        self._check_out_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_check_out_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_detail_api_view_with_full_access(self):
        self._check_out_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        self._clear_events()

        response = self._request_test_document_check_out_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['document']['uuid'],
            force_text(s=self.test_document.uuid)
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_check_out_detail_api_view_with_full_access(self):
        self._check_out_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_check_out_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_list_api_view_no_permission(self):
        self._check_out_test_document()

        self._clear_events()

        response = self._request_test_document_check_out_list_api_view()
        self.assertNotContains(
            response=response, text=self.test_document.uuid,
            status_code=status.HTTP_200_OK
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_list_api_view_with_document_access(self):
        self._check_out_test_document()
        self.grant_access(
            permission=permission_document_view, obj=self.test_document
        )

        self._clear_events()

        response = self._request_test_document_check_out_list_api_view()
        self.assertNotContains(
            response=response, text=self.test_document.uuid,
            status_code=status.HTTP_200_OK
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_list_api_view_with_check_out_detail_access(self):
        self._check_out_test_document()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        self._clear_events()

        response = self._request_test_document_check_out_list_api_view()
        self.assertNotContains(
            response=response, text=self.test_document.uuid,
            status_code=status.HTTP_200_OK
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_list_api_view_with_full_access(self):
        self._check_out_test_document()

        self.grant_access(
            permission=permission_document_view, obj=self.test_document
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        self._clear_events()

        response = self._request_test_document_check_out_list_api_view()
        self.assertContains(
            response=response, text=self.test_document.uuid,
            status_code=status.HTTP_200_OK
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_check_out_list_api_view_with_full_access(self):
        self._check_out_test_document()

        self.grant_access(
            permission=permission_document_view, obj=self.test_document
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_check_out_list_api_view()
        self.assertNotContains(
            response=response, text=self.test_document.uuid,
            status_code=status.HTTP_200_OK
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
