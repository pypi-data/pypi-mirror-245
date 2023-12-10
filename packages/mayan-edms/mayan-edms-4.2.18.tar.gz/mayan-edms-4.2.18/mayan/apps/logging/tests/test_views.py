from mayan.apps.testing.tests.base import GenericViewTestCase

from ..permissions import permission_error_log_view

from .mixins import (
    ErrorLoggingTextMixin, ErrorLoggingViewTestMixin,
    GlobalErrorLogViewTestMixin
)


class GlobalErrorLogViewTestCase(
    ErrorLoggingTextMixin, GlobalErrorLogViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_error_log_test_object()
        self._create_error_log_entry()

    def test_global_error_log_partition_entry_list_view_no_permission(self):
        response = self._request_global_error_log_partition_entry_list_view()
        self.assertNotContains(
            response=response, text=self._test_error_log_entry.text,
            status_code=200
        )

    def test_global_error_log_partition_entry_list_view_with_access(self):
        self.grant_access(
            obj=self.test_object, permission=permission_error_log_view
        )

        response = self._request_global_error_log_partition_entry_list_view()
        self.assertContains(
            response=response, text=self._test_error_log_entry.text,
            status_code=200
        )


class ErrorLoggingViewTestCase(
    ErrorLoggingTextMixin, ErrorLoggingViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_error_log_test_object()
        self._create_error_log_entry()

    def test_object_error_list_view_no_permission(self):
        response = self._request_object_error_log_list_view()
        self.assertNotContains(
            response=response, text=self._test_error_log_entry.text,
            status_code=404
        )

    def test_object_error_list_view_with_access(self):
        self.grant_access(
            obj=self.test_object, permission=permission_error_log_view
        )

        response = self._request_object_error_log_list_view()
        self.assertContains(
            response=response, text=self._test_error_log_entry.text,
            status_code=200
        )

    def test_object_error_list_clear_view_no_permission(self):
        response = self._request_object_error_log_list_clear_view()
        self.assertEqual(response.status_code, 404)

        self.assertNotEqual(self.test_object.error_log.count(), 0)

    def test_object_error_list_clear_view_with_access(self):
        self.grant_access(
            obj=self.test_object, permission=permission_error_log_view
        )

        response = self._request_object_error_log_list_clear_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_object.error_log.count(), 0)
