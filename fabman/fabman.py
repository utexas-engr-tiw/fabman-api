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
        """
        Initializes the Fabman class with the given access token and base url.
        All methods take kwargs as their arguments, please refer to the Fabman API
        for more information

        Args:
            :access_token (str): The access token to access the API
            :base_url (str, optional): The base url of the API. Defaults to
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

        :calls: "POST /api-keys" \
        <https://fabman.io/api/v1/documentation#/api-keys/postApikeys>
        
        :returns: :code:`ApiKey` object if successful
        :rtype: :code:`fabman.ApiKey`
        """

        uri = "/api-keys"
        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return ApiKey(self.__requester, response.json())

    def create_booking(self, **kwargs) -> Booking:
        """
        Creates a new booking in the Fabman database.

        :calls: "POST /bookings" \
		<https://fabman.io/api/v1/documentation#/bookings/postBookings>
  
        :returns: :code:`Booking` object if successful
        :rtype: :code:`fabman.Booking`
        """

        uri = "/bookings"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Booking(self.__requester, response.json())

    def create_charge(self, **kwargs) -> Charge:
        """
        Creates a new charge in the Fabman database.

        :calls: "POST /charges" \
		<https://fabman.io/api/v1/documentation#/charges/postCharges>
  
        :returns: :code:`Charge` object if successful
        :rtype: :code:`fabman.Charge`
        """

        uri = "/charges"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Charge(self.__requester, response.json())

    def create_invoice(self, **kwargs) -> Invoice:
        """
        Creates a new invoice in the Fabman database.

        :calls: "POST /invoices" \
		<https://fabman.io/api/v1/documentation#/invoices/postInvoices>
  
        :returns: :code:`Invoice` object if successful
        :rtype: :code:`fabman.Invoice`
        """

        uri = "/invoices"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Invoice(self.__requester, response.json())

    def create_key_assignment(self, **kwargs) -> requests.Response:
        """
        Creates a new keycard assignment in the Fabman Database. Note: A better
        method to work with key assignments is to use the Member class and the
        associated MemberKey class that works with the key assignments endpoint.

        :calls: "POST /key-assignments" \
		<https://fabman.io/api/v1/documentation#/key-assignments/postKeyassignments>
  
        :returns: :code:`requests.Response` object if successful
        :rtype: :code:`requests.Response`
        """

        uri = "/key-assignments"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return response

    def create_member(self, **kwargs) -> Member:
        """
        Creates a new member in the Fabman database.

        :calls: "POST /members" \
        <https://fabman.io/api/v1/documentation#/members/postMembers>

        :returns: :code:`Member` object if successful
        :rtype: :code:`fabman.Member`

        """
        uri = "/members"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Member(self.__requester, response.json())

    def create_package(self, **kwargs) -> Package:
        """
        Creates a new package in the Fabman database.

        :calls: "POST /packages" \
        <https://fabman.io/api/v1/documentation#/packages/postPackages>
        
        :returns: :code:`Package` object if successful
        :rtype: :code:`fabman.Package`
        """

        uri = "/packages"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Package(self.__requester, response.json())

    def create_payment(self, **kwargs) -> Payment:
        """
        Creates a new payment in the Fabman database.

        :calls: "POST /payments" \
		<https://fabman.io/api/v1/documentation#/payments/postPayments>
  
        :returns: :code:`Payment` object if successful
        :rtype: :code:`fabman.Payment`
        """

        uri = "/payments"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Payment(self.__requester, response.json())

    def create_resource(self, **kwargs) -> Resource:
        """
        Creates a new resource in the Fabman database.

        :calls: "POST /resources" \
		<https://fabman.io/api/v1/documentation#/resources/postResources>
  
        :returns: :code:`Resource` object if successful
        :rtype: :code:`fabman.Resource`
        """

        uri = "/resources"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Resource(self.__requester, response.json())

    def create_resource_log(self, **kwargs) -> ResourceLog:
        """
        Creates a new resource log in the Fabman database. Use with caution.

        :calls: "POST /resource-logs" \
		<https://fabman.io/api/v1/documentation#/resource-logs/postResourcelogs>
  
        :returns: :code:`ResourceLog` object if successful
        :rtype: :code:`fabman.ResourceLog`
        """
        uri = "/resource-logs"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return ResourceLog(self.__requester, response.json())

    def create_resource_type(self, **kwargs) -> ResourceType:
        """
        Creates a new resource type in the Fabman database.

        :calls: "POST /resource-types" \
		<https://fabman.io/api/v1/documentation#/resource-types/postResourcetypes>
  
        :returns: :code:`ResourceType` object if successful
        :rtype: :code:`fabman.ResourceType`
        """
        uri = "/resource-types"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return ResourceType(self.__requester, response.json())

    def create_space(self, **kwargs) -> Space:
        """
        Creates a new space in the Fabman database.

        :calls: "POST /spaces" \
		<https://fabman.io/api/v1/documentation#/spaces/postSpaces>
  
        :returns: :code:`Space` object if successful
        :rtype: :code:`fabman.Space`
        """
        uri = "/spaces"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Space(self.__requester, response.json())

    def create_training_course(self, **kwargs) -> TrainingCourse:
        """
        Creates a new Training course in the Fabman database.

        :calls: "POST /training-courses" \
        <https://fabman.io/api/v1/documentation#/training-courses/postTrainingcourses>
        
        :returns: :code:`TrainingCourse` object if successful
        :rtype: :code:`fabman.TrainingCourse`
        """

        uri = "/training-courses"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return TrainingCourse(self.__requester, response.json())

    def create_webhook(self, **kwargs) -> Webhook:
        """
        Creates a new webhook in the Fabman database.

        :calls: "POST /webhooks" \
        <https://fabman.io/api/v1/documentation#/webhooks/postWebhooks>
        
        :returns: :code:`Webhook` object if successful
        :rtype: :code:`fabman.Webhook`
        """

        uri = "/webhooks"

        response = self.__requester.request("POST", uri, _kwargs=kwargs)

        return Webhook(self.__requester, response.json())

    def get_account(self, account_id, **kwargs) -> Account:
        """
        Get a single account by its ID. Note: for most users, the only account
        retrievable is the account of the API key holder. Majority of endpoints
        are not implemented as they require superuser privileges.

        :calls: "GET /accounts/{account_id}" \
        <https://fabman.io/api/v1/documentation#/accounts/getAccountsId>
        
        :param account_id: The id of the account to retrieve
        :type account_id: int
        :returns: :code:`Account` object if successful
        :rtype: :code:`fabman.Account`
        """

        uri = f"/accounts/{account_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Account(self.__requester, response.json())

    def get_accounts(self, **kwargs) -> PaginatedList:
        """
        Get a list of accounts. Note, for most users this will only return the account
        of the API key holder. Most documented endpoints are unimplemented as a result.

        :calls: "GET /accounts" \
        <https://fabman.io/api/v1/documentation#/accounts/getAccounts>
        
        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """
        return PaginatedList(Account, self.__requester, "GET", "/accounts", **kwargs)

    def get_api_key(self, key_id, **kwargs) -> ApiKey:
        """
        Get information about a single API key by its ID.

        :calls: "GET /api-keys/{key_id}" \
        <https://fabman.io/api/v1/documentation#/api-keys/getApikeysId>
        
        :param key_id: The id of the API key to retrieve
        :type key_id: int
        :returns: :code:`ApiKey` object if successful
        :rtype: :code:`fabman.ApiKey`
        """

        uri = f"/api-keys/{key_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return ApiKey(self.__requester, response.json())

    def get_api_keys(self, **kwargs) -> PaginatedList:
        """
        Get a list of API keys. Can specify filters, search string, etc.

        :calls: "GET /api-keys" \
		<https://fabman.io/api/v1/documentation#/api-keys/getApikeys>
  
        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """

        return PaginatedList(ApiKey, self.__requester, "GET", "/api-keys", **kwargs)

    def get_booking(self, booking_id, **kwargs) -> Booking:
        """
        Get a single booking by its ID.

        :calls: "GET /bookings/{id}" \
		<https://fabman.io/api/v1/documentation#/bookings/getBookingsId>

        :param booking_id: The id of the booking to retrieve
        :type booking_id: int
        :returns: :code:`Booking` object if successful
        :rtype: :code:`fabman.Booking`
        """
        uri = f"/bookings/{booking_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Booking(self.__requester, response.json())

    def get_bookings(self, **kwargs) -> PaginatedList:
        """
        Retrieves a PaginatedList of bookings from the API. Can specify filters, search
        string, etc.

        :calls: "GET /bookings" \
		<https://fabman.io/api/v1/documentation#/bookings/getBookings>
  
        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """
        return PaginatedList(Booking, self.__requester, "GET", "/bookings", **kwargs)

    def get_charge(self, charge_id: int, **kwargs) -> Charge:
        """
        Retrieves a single Charge given the charge_id.

        :calls: "Get /charges/{id}" \
		<https://fabman.io/api/v1/documentation#/charges/getChargesId>

        :param charge_id: The id of the charge to retrieve
        :type charge_id: int
        :returns: :code:`Charge` object if successful
        :rtype: :code:`fabman.Charge`
        """

        uri = f"/charges/{charge_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Charge(self.__requester, response.json())

    def get_charges(self, **kwargs) -> PaginatedList:
        """
        Retrieves all charges from the API. Can specify filters, search string, etc.

        :calls: "GET /charges" \
		<https://fabman.io/api/v1/documentation#/charges/getCharges>
  
        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """

        return PaginatedList(Charge, self.__requester, "GET", "/charges", **kwargs)

    def get_invoice(self, invoice_id, **kwargs) -> Invoice:
        """
        Retrieve information of a single invoice by its ID.

        :calls: "GET /invoices/{id}" \
		<https://fabman.io/api/v1/documentation#/invoices/getInvoicesId>
  
        :param invoice_id: The id of the invoice to retrieve
        :type invoice_id: int
        :returns: :code:`Invoice` object if successful
        :rtype: :code:`fabman.Invoice`
        """

        uri = f"/invoices/{invoice_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Invoice(self.__requester, response.json())

    def get_invoices(self, **kwargs) -> PaginatedList:
        """
        Retrieves list of all invoices. Can specify filters, search string, etc.

        :calls: "GET /invoices" \
		<https://fabman.io/api/v1/documentation#/invoices/getInvoices>
  
        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """

        return PaginatedList(Invoice, self.__requester, "GET", "/invoices", **kwargs)

    def get_job(self, job_id, **kwargs) -> Job:
        """
        Retrieve a single job from the Fabman API given the job_id.

        :calls: "GET /jobs/{id}" \
		<https://fabman.io/api/v1/documentation#/jobs/getJobsId>
  
        :param job_id: The id of the job to retrieve
        :type job_id: int
        :returns: :code:`Job` object if successful
        :rtype: :code:`Job`
        """
        uri = f"/jobs/{job_id}"
        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Job(self.__requester, response.json())

    def get_jobs(self, **kwargs) -> PaginatedList:
        """
        Retrieves a list of all jobs. Can specify filters, search string, etc.

        :calls: "GET /jobs" \
		<https://fabman.io/api/v1/documentation#/jobs/getJobs>
  
        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """

        return PaginatedList(Job, self.__requester, "GET", "/jobs", **kwargs)

    def get_member(self, member_id: int, **kwargs):
        """Retrieves a member from the API give their id
        :calls: "GET /members/{id}" \
		<https://fabman.io/api/v1/documentation#/members/getMembersId>

        :param member_id: The id of the member to retrieve
        :type member_id: int
        :returns: :code:`Member` object if successful
        """
        uri = f"/members/{member_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Member(self.__requester, response.json())

    def get_members(self, **kwargs):
        """Get all of the members in the Fabman database. Can specify filters,
        search string, result limits, offsets, and sorting. Refer to the Fabman API
        documentation.

        :calls: "GET /members" \
		<https://fabman.io/api/v1/documentation#/members/getMembers>

        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """

        return PaginatedList(Member, self.__requester, "GET", "/members", **kwargs)

    def get_package(self, package_id: int, **kwargs) -> Package:
        """
        Retrieves a single Package given a package_id

        :calls: "GET /packages/{id}" \
		<https://fabman.io/api/v1/documentation#/packages/getPackagesId>
  
        :param package_id: The id of the package to retrieve
        :type package_id: int
        :returns: :code:`Package` object if successful
        :rtype: :code:`fabman.Package`
        """

        uri = f"/packages/{package_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Package(self.__requester, response.json())

    def get_packages(self, **kwargs) -> PaginatedList:
        """
        Retrieves a list of packages. Can specify filters, search string, etc.

        :calls: "GET /packages" \
		<https://fabman.io/api/v1/documentation#/packages/getPackages>
  
        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """

        return PaginatedList(Package, self.__requester, "GET", "/packages", **kwargs)

    def get_payment(self, payment_id, **kwargs) -> Payment:
        """
        Retrieves a single payment given a payment_id.

        :calls: "GET /payments/{id}" \
		<https://fabman.io/api/v1/documentation#/payments/getPaymentsId>

        :param payment_id: The id of the payment to retrieve
        :type payment_id: int
        :returns: :code:`Payment` object if successful
        :rtype: :code:`fabman.Payment`
        """

        uri = f"/payments/{payment_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Payment(self.__requester, response.json())

    def get_payments(self, **kwargs) -> PaginatedList:
        """
        Retrieves a list of payments. Can specify filters, search string, etc.

        :calls: "GET /payments" \
		<https://fabman.io/api/v1/documentation#/payments/getPayments>

        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """

        return PaginatedList(Payment, self.__requester, "GET", "/payments", **kwargs)

    def get_resource(self, resource_id: int, **kwargs):
        """
        Get a single resource by its ID. Embed information is also available.

        :calls: "GET /resources/{id}" \
		<https://fabman.io/api/v1/documentation#/resources/getResourcesId>

        :param resource_id: The id of the resource to retrieve
        :type resource_id: int
        :returns: :code:`Resource` object if successful
        :rtype: :code:`fabman.Resource`
        """
        uri = f"/resources/{resource_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Resource(self.__requester, response.json())

    def get_resources(self, **kwargs) -> PaginatedList:
        """
        Get list of available resources (e.g. doors, printers, etc.) Limit, offset,
        and a number of filters are available. Refer to the appropriate documentation.

        :calls: "GET /resources" \
		<https://fabman.io/api/v1/documentation#/resources/getResources>
  
        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """
        return PaginatedList(
            Resource,
            self.__requester,
            "GET",
            "/resources",
            **kwargs,
        )

    def get_resource_log(self, resource_log_id, **kwargs) -> ResourceLog:
        """
        Retrieves a single Resource Log from the API.

        :calls: "GET /resource-logs/{id}" \
		<https://fabman.io/api/v1/documentation#/resource-logs/getResourcelogsId>

        :param resource_log_id: The id of the resource log to retrieve
        :type resource_log_id: int
        :returns: :code:`ResourceLog` object if successful
        :rtype: :code:`fabman.ResourceLog`
        """

        uri = f"/resource-logs/{resource_log_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return ResourceLog(self.__requester, response.json())

    def get_resource_logs(self, **kwargs) -> PaginatedList:
        """
        Retrieves a list of resource logs. Can specify filters, search string, etc.

        :calls: "GET /resource-logs" \
		<https://fabman.io/api/v1/documentation#/resource-logs/getResourcelogs>
  
        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """

        return PaginatedList(
            ResourceLog, self.__requester, "GET", "/resource-logs", **kwargs
        )

    def get_resource_types(self, **kwargs) -> PaginatedList:
        """
        Retrieves a list of resource types. Can specify filters, search string, etc.

        :calls: "GET /resource-types" \
		<https://fabman.io/api/v1/documentation#/resource-types/getResourcetypes>
  
        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """

        return PaginatedList(
            ResourceType, self.__requester, "GET", "/resource-types", **kwargs
        )

    def get_space(self, space_id, **kwargs) -> Space:
        """
        Retrieves a single space given a space_id.

        :calls: "GET /spaces/{id}" \
		<https://fabman.io/api/v1/documentation#/spaces/getSpacesId>

        :param space_id: The id of the space to retrieve
        :type space_id: int
        :returns: :code:`Space` object if successful
        :rtype: :code:`fabman.Space`
        """

        uri = f"/spaces/{space_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Space(self.__requester, response.json())

    def get_spaces(self, **kwargs) -> PaginatedList:
        """
        Retrieves a list of Spaces. Can specify filters, search string, etc.

        :calls: "GET /spaces" \
		<https://fabman.io/api/v1/documentation#/spaces/getSpaces>
  
        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """

        return PaginatedList(Space, self.__requester, "GET", "/spaces", **kwargs)

    def get_training_course(self, course_id, **kwargs):
        """
        Retrieve a single TrainingCourse object from the API.

        :calls: "GET /training-courses/{id}" \
		<https://fabman.io/api/v1/documentation#/training-courses/getTrainingcoursesId>
  
        :param course_id: The id of the training course to retrieve
        :type course_id: int
        :returns: :code:`TrainingCourse` object if successful
        :rtype: :code:`fabman.TrainingCourse`
        """
        uri = f"/training-courses/{course_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return TrainingCourse(self.__requester, response.json())

    def get_training_courses(self, **kwargs):
        """
        Retrieves a PaginatedList of Training Courses available on the api.

        :calls: "GET /training-courses" \
		<https://fabman.io/api/v1/documentation#/training-courses/getTrainingcourses>
  
        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """
        return PaginatedList(
            TrainingCourse, self.__requester, "GET", "/training-courses", **kwargs
        )

    def get_user(self, **kwargs) -> Member:
        """Gets authenticated user information from the API as Member object. Does
        not returns state and superuser information.
        :calls: "GET /user/me" \
		<https://fabman.io/api/v1/documentation#/user/getUserMe>

        :returns: :code:`Member` object if successful
        :rtype: :code:`fabman.Member`
        """
        uri = "/user/me"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Member(self.__requester, response.json()["members"][0])

    def get_webhook(self, webhook_id, **kwargs) -> Webhook:
        """
        Retrieves a single webhook given a webhook_id.

        :calls: "GET /webhooks/{id}" \
		<https://fabman.io/api/v1/documentation#/webhooks/getWebhooksId>
  
        :param webhook_id: The id of the webhook to retrieve
        :type webhook_id: int
        :returns: :code:`Webhook` object if successful
        :rtype: :code:`fabman.Webhook`
        """

        uri = f"/webhooks/{webhook_id}"

        response = self.__requester.request("GET", uri, _kwargs=kwargs)

        return Webhook(self.__requester, response.json())

    def get_webhooks(self, **kwargs) -> PaginatedList:
        """
        Retrieves a list of webhooks. Can specify filters, search string, etc.

        :calls: "GET /webhooks" \
		<https://fabman.io/api/v1/documentation#/webhooks/getWebhooks>
  
        :returns: :code:`PaginatedList` object if successful
        :rtype: :code:`fabman.PaginatedList`
        """

        return PaginatedList(Webhook, self.__requester, "GET", "/webhooks", **kwargs)
