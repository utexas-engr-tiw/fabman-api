#!/usr/bin/python3
"""Main file for the Fabman API library.
"""

import warnings

import requests

from fabman.account import Account
from fabman.api_key import ApiKey
from fabman.booking import Booking
from fabman.charge import Charge
from fabman.invoice import Invoice
from fabman.job import Job
from fabman.member import Member
from fabman.package import Package
from fabman.paginated_list import PaginatedList
from fabman.payment import Payment
from fabman.requester import Requester
from fabman.resource import Resource
from fabman.resource_log import ResourceLog
from fabman.resource_type import ResourceType
from fabman.space import Space
from fabman.training_course import TrainingCourse
from fabman.webhook import Webhook


class Fabman(object):
    """
    The main class to be instantiated to provide access to the Fabman api.
    """

    def __init__(self, access_token: str, base_url="https://fabman.io/api/v1"):
        """Initializes the Fabman class with the given access token and base url.
        All methods take kwargs as their arguments, please refer to the Fabman API
        for more information

        Args:
            access_token (str): The access token to access the API
            base_url (str, optional): The base url of the API. Defaults to
            "https://api.fabman.io/v1".
        """

        if "https://" not in base_url:
            warnings.warn(
                "Please use HTTPS when possible. Fabman API may not respond as intended and user"
                "data will not be secure",
                UserWarning,
            )

        if "://" not in base_url:
            warnings.warn(
                "An invalid `bad_url` provided. Will likely not work as intended.",
                UserWarning,
            )
        if not access_token or access_token == "":
            raise ValueError("No access token provided")

        # sanitize access token and base url
        access_token = access_token.strip()
        if base_url[-1] == "/":
            base_url = base_url[:-1]

        self.__requester = Requester(base_url, access_token)

    def create_api_key(self, **kwargs) -> ApiKey:
        """
        Creates a new API key for a member.

        Calls "POST /api-keys"
        Documentation https://fabman.io/api/v1/documentation#/api-keys/postApikeys
        """

        uri = "/api-keys"
        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return ApiKey(self.__requester, response.json())

    def create_booking(self, **kwargs) -> Booking:
        """
        Creates a new booking in the Fabman database.

        Calls "POST /bookings"
        Documentation https://fabman.io/api/v1/documentation#/bookings/postBookings
        """

        uri = "/bookings"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Booking(self.__requester, response.json())

    def create_charge(self, **kwargs) -> Charge:
        """
        Creates a new charge in the Fabman database.

        Calls "POST /charges"
        Documentation https://fabman.io/api/v1/documentation#/charges/postCharges
        """

        uri = "/charges"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Charge(self.__requester, response.json())

    def create_invoice(self, **kwargs) -> Invoice:
        """
        Creates a new invoice in the Fabman database.

        Calls "POST /invoices"
        Documentation https://fabman.io/api/v1/documentation#/invoices/postInvoices
        """

        uri = "/invoices"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Invoice(self.__requester, response.json())

    def create_key_assignment(self, **kwargs) -> requests.Response:
        """
        Creates a new keycard assignment in the Fabman Database. Note: A better
        method to work with key assignments is to use the Member class and the
        associated MemberKey class that works with the key assignments endpoint.

        Calls "POST /key-assignments"
        Documentation https://fabman.io/api/v1/documentation#/key-assignments/postKeyassignments
        """

        uri = "/key-assignments"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return response.json()

    def create_member(self, **kwargs) -> Member:
        """Creates a new member in the Fabman database.
        Calls "POST /members"
        Documentation: https://fabman.io/api/v1/documentation#/members/postMembers

        Returns:

        """
        uri = "/members"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Member(self.__requester, response.json())

    def create_package(self, **kwargs) -> Package:
        """
        Creates a new package in the Fabman database.

        Calls "POST /packages"
        Documentation: https://fabman.io/api/v1/documentation#/packages/postPackages
        """

        uri = "/packages"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Package(self.__requester, response.json())

    def create_payment(self, **kwargs) -> Payment:
        """
        Creates a new payment in the Fabman database.

        Calls "POST /payments"
        Documentation https://fabman.io/api/v1/documentation#/payments/postPayments
        """

        uri = "/payments"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Payment(self.__requester, response.json())

    def create_resource(self, **kwargs) -> Resource:
        """
        Creates a new resource in the Fabman database.

        Calls "POST /resources"
        Documentation https://fabman.io/api/v1/documentation#/resources/postResources
        """

        uri = "/resources"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Resource(self.__requester, response.json())

    def create_resource_log(self, **kwargs) -> ResourceLog:
        """
        Creates a new resource log in the Fabman database. Use with caution.

        Calls "POST /resource-logs"
        Documentation https://fabman.io/api/v1/documentation#/resource-logs/postResourceLogs
        """
        uri = f"/resource-logs"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return ResourceLog(self.__requester, response.json())

    def create_resource_type(self, **kwargs) -> ResourceType:
        """
        Creates a new resource type in the Fabman database.

        Calls "POST /resource-types"
        Documentation https://fabman.io/api/v1/documentation#/resource-types/postResourceTypes
        """
        uri = "/resource-types"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return ResourceType(self.__requester, response.json())

    def create_space(self, **kwargs) -> Space:
        """
        Creates a new space in the Fabman database.

        Calls "POST /spaces"
        Documentation https://fabman.io/api/v1/documentation#/spaces/postSpaces
        """
        uri = "/spaces"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Space(self.__requester, response.json())

    def create_training_course(self, **kwargs) -> TrainingCourse:
        """
        Creates a new Training course in the Fabman database.

        Calls "POST /training-courses"
        Documentation: https://fabman.io/api/v1/documentation#/training-courses/postTrainingcourses
        """

        uri = "/training-courses"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return TrainingCourse(self.__requester, response.json())

    def create_webhook(self, **kwargs) -> Webhook:
        """
        Creates a new webhook in the Fabman database.

        Calls "POST /webhooks"
        Documentation: https://fabman.io/api/v1/documentation#/webhooks/postWebhooks
        """

        uri = "/webhooks"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Webhook(self.__requester, response.json())

    def get_account(self, account_id, **kwargs) -> Account:
        """
        Get a single account by its ID. Note: for most users, the only account
        retrievable is the account of the API key holder. Majority of endpoints
        are not implemented as they require superuser privileges.

        Calls "GET /accounts/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/accounts/getAccountsId
        """

        uri = f"/accounts/{account_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Account(self.__requester, response.json())

    def get_accounts(self, **kwargs) -> PaginatedList:
        """
        Get a list of accounts. Note, for most users this will only return the account
        of the API key holder. Most documented endpoints are unimplemented as a result.

        Calls "GET /accounts"
        Documentation: https://fabman.io/api/v1/documentation#/accounts/getAccounts
        """
        return PaginatedList(
            Account, self.__requester, "GET", "/accounts", kwargs=kwargs
        )

    def get_api_key(self, key_id, **kwargs) -> ApiKey:
        """
        Get information about a single API key by its ID.

        Calls "GET /api-keys/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/api-keys/getApikeysId
        """

        uri = f"/api-keys/{key_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return ApiKey(self.__requester, response.json())

    def get_api_keys(self, **kwargs) -> PaginatedList:
        """
        Get a list of API keys. Can specify filters, search string, etc.

        Calls "GET /api-keys"
        Documentation: https://fabman.io/api/v1/documentation#/api-keys/getApikeys
        """

        return PaginatedList(
            ApiKey, self.__requester, "GET", "/api-keys", kwargs=kwargs
        )

    def get_booking(self, booking_id, **kwargs) -> Booking:
        """
        Get a single booking by its ID.

        Calls "GET /bookings/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/bookings/getBookingsId
        """
        uri = f"/bookings/{booking_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Booking(self.__requester, response.json())

    def get_bookings(self, **kwargs) -> PaginatedList:
        """
        Retrieves a PaginatedList of bookings from the API. Can specify filters, search
        string, etc.

        Calls "GET /bookings"
        Documentation: https://fabman.io/api/v1/documentation#/bookings/getBookings
        """
        return PaginatedList(
            Booking, self.__requester, "GET", "/bookings", kwargs=kwargs
        )

    def get_charge(self, charge_id: int, **kwargs) -> Charge:
        """
        Retrieves a single Charge given the charge_id.

        Calls "Get /charges/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/charges/getChargesId
        """

        uri = f"/charges/{charge_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Charge(self.__requester, response.json())

    def get_charges(self, **kwargs) -> PaginatedList:
        """
        Retrieves all charges from the API. Can specify filters, search string, etc.

        Calls "GET /charges"
        Documentation: https://fabman.io/api/v1/documentation#/charges/getCharges
        """

        return PaginatedList(Charge, self.__requester, "GET", "/charges", kwargs=kwargs)

    def get_invoice(self, invoice_id, **kwargs) -> Invoice:
        """
        Retrieve information of a single invoice by its ID.

        Calls "GET /invoices/{id}"
        Documentation https://fabman.io/api/v1/documentation#/invoices/getInvoicesId
        """

        uri = f"/invoices/{invoice_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Invoice(self.__requester, response.json())

    def get_invoices(self, **kwargs) -> PaginatedList:
        """
        Retrieves list of all invoices. Can specify filters, search string, etc.

        Calls "GET /invoices"
        Documentation https://fabman.io/api/v1/documentation#/invoices/getInvoices
        """

        return PaginatedList(
            Invoice, self.__requester, "GET", "/invoices", kwargs=kwargs
        )

    def get_job(self, job_id, **kwargs):
        """
        Retrieve a single job from the Fabman API given the job_id.

        Calls "GET /jobs/{id}"
        Documentation https://fabman.io/api/v1/documentation
        """
        uri = f"/jobs/{job_id}"
        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Job(self.__requester, response.json())

    def get_jobs(self, **kwargs):
        """
        Retrieves a list of all jobs. Can specify filters, search string, etc.

        Calls "GET /jobs"
        Documentation https://fabman.io/api/v1/documentation#/jobs/getJobs
        """

        return PaginatedList(Job, self.__requester, "GET", "/jobs", kwargs=kwargs)

    def get_members(self, **kwargs):
        """Get all of the members in the Fabman database. Can specify filters,
        search string, result limits, offsets, and sorting. Refer to the Fabman API
        documentation.

        calls "GET /members"
        documentation https://fabman.io/api/v1/documentation#/members/getMembers
        """

        return PaginatedList(Member, self.__requester, "GET", "/members", kwargs=kwargs)

    def get_member(self, member_id: int, **kwargs):
        """Retrieves a member from the API give their id
        calls "GET /members/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersId

        Args:
            member_id (int): ID of the member to be called
        """
        uri = f"/members/{member_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Member(self.__requester, response.json())

    def get_package(self, package_id: int, **kwargs) -> Package:
        """
        Retrieves a single Package given a package_id

        Calls "GET /packages/{id}"
        Documentation https://fabman.io/api/v1/documentation#/packages/getPackagesId
        """

        uri = f"/packages/{package_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Package(self.__requester, response.json())

    def get_packages(self, **kwargs) -> PaginatedList:
        """
        Retrieves a list of packages. Can specify filters, search string, etc.

        Calls "GET /packages"
        Documentation https://fabman.io/api/v1/documentation#/packages/getPackages
        """

        return PaginatedList(
            Package, self.__requester, "GET", "/packages", kwargs=kwargs
        )

    def get_payment(self, payment_id, **kwargs) -> Payment:
        """
        Retrieves a single payment given a payment_id.

        Calls "GET /payments/{id}"
        Documentation https://fabman.io/api/v1/documentation#/payments/getPaymentsId
        """

        uri = f"/payments/{payment_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Payment(self.__requester, response.json())

    def get_payments(self, **kwargs) -> PaginatedList:
        """
        Retrieves a list of payments. Can specify filters, search string, etc.

        Calls "GET /payments"
        Documentation https://fabman.io/api/v1/documentation#/payments/getPayments
        """

        return PaginatedList(
            Payment, self.__requester, "GET", "/payments", kwargs=kwargs
        )

    def get_resource(self, resource_id: int, **kwargs):
        """
        Get a single resource by its ID. Embed information is also available.

        Calls "GET /resources/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/resources/getResourcesId
        """
        uri = f"/resources/{resource_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Resource(self.__requester, response.json())

    def get_resources(self, **kwargs):
        """
        Get list of available resources (e.g. doors, printers, etc.) Limit, offset,
        and a number of filters are available. Refer to the appropriate documentation.
        calls "GET /resources"
        Documentation: https://fabman.io/api/v1/documentation#/resources/getResources
        """
        raise NotImplementedError(
            "get_resources not implemented yet. Awaiting Pagination"
        )

    def get_resource_log(self, resource_log_id, **kwargs) -> ResourceLog:
        """
        Retrieves a single Resource Log from the API.

        Calls "GET /resource-logs/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/resource-logs/getResourceLogsId
        """

        uri = f"/resource-logs/{resource_log_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return ResourceLog(self.__requester, response.json())

    def get_resource_logs(self, **kwargs) -> PaginatedList:
        """
        Retrieves a list of resource logs. Can specify filters, search string, etc.

        Calls "GET /resource-logs"
        Documentation: https://fabman.io/api/v1/documentation#/resource-logs/getResourceLogs
        """

        return PaginatedList(
            ResourceLog, self.__requester, "GET", "/resource-logs", kwargs=kwargs
        )

    def get_resource_type(self, resource_type_id, **kwargs) -> ResourceType:
        """
        Retrieves a single resource type given a resource_type_id.

        Calls "GET /resource-types/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/resource-types/getResourceTypesId
        """

        uri = f"/resource-types/{resource_type_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return ResourceType(self.__requester, response.json())

    def get_resource_types(self, **kwargs) -> PaginatedList:
        """
        Retrieves a list of resource types. Can specify filters, search string, etc.

        Calls "GET /resource-types"
        Documentation: https://fabman.io/api/v1/documentation#/resource-types/getResourceTypes
        """

        return PaginatedList(
            ResourceType, self.__requester, "GET", "/resource-types", kwargs=kwargs
        )

    def get_space(self, space_id, **kwargs) -> Space:
        """
        Retrieves a single space given a space_id.

        calls "GET /spaces/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/spaces/getSpacesId
        """

        uri = f"/spaces/{space_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Space(self.__requester, response.json())

    def get_spaces(self, **kwargs) -> PaginatedList:
        """
        Retrieves a list of Spaces. Can specify filters, search string, etc.

        Calls "GET /spaces"
        Documentation: https://fabman.io/api/v1/documentation#/spaces/getSpaces
        """

        return PaginatedList(Space, self.__requester, "GET", "/spaces", kwargs=kwargs)

    def get_training_course(self, course_id, **kwargs):
        """
        Retrieve a single TrainingCourse object from the API.

        Calls "GET /training-courses/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/training-courses/getTrainingcoursesId
        """
        uri = f"/training-courses/{course_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return TrainingCourse(self.__requester, response.json())

    def get_training_courses(self, **kwargs):
        """
        Retrieves a PaginatedList of Training Courses available on the api.

        Calls "GET /training-courses"
        Documentation: https://fabman.io/api/v1/documentation#/training-courses/getTrainingcourses
        """
        return PaginatedList(
            TrainingCourse, self.__requester, "GET", "/training-courses", kwargs=kwargs
        )

    def get_user(self, **kwargs):
        """Gets authenticated user information from the API as Member object. Does
        not returns state and superuser information.
        calls "GET /user/me"
        Documentation: https: // fabman.io/api/v1/documentation  # /user/getUserMe
        """
        uri = "/user/me"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Member(self.__requester, response.json()["members"][0])

    def get_webhook(self, webhook_id, **kwargs) -> Webhook:
        """
        Retrieves a single webhook given a webhook_id.

        Calls "GET /webhooks/{id}"
        Documentation https://fabman.io/api/v1/documentation#/webhooks/getWebhooksId
        """

        uri = f"/webhooks/{webhook_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Webhook(self.__requester, response.json())

    def get_webhooks(self, **kwargs) -> PaginatedList:
        """
        Retrieves a list of webhooks. Can specify filters, search string, etc.

        Calls "GET /webhooks"
        Documentation https://fabman.io/api/v1/documentation#/webhooks/getWebhooks
        """

        return PaginatedList(
            Webhook, self.__requester, "GET", "/webhooks", kwargs=kwargs
        )
