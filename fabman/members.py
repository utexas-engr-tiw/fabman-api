#!/usr/bin/python3
"""This file creates a model for member objects from the Fabman API.
    
    According the the Fabman API documentation, a member object has the following attributes:
    Result[Member%20with%20activity{
        space	integer
            minimum: 1
            maximum: 2147483647
            required if the account has more than one space
        memberNumber	string
            maxLength: 255
        firstName	string
            maxLength: 255
        lastName	string
            maxLength: 255
        gender	stringEnum:
            Array [ 3 ]
        dateOfBirth	string($date)
        emailAddress	string
            maxLength: 255
        company	string
            maxLength: 255
        phone	string
            maxLength: 255
        address	string
            maxLength: 255
        address2	string
            maxLength: 255
        city	string
            maxLength: 255
        zip	string
            maxLength: 255
        countryCode	string
            maxLength: 255
        region	string
            maxLength: 255
        notes	string
        taxExempt	boolean
        hasBillingAddress	boolean
        requireUpfrontPayment	boolean
        upfrontMinimumBalance	number
            minimum: -9999999.99
            maximum: 9999999.99
        billingFirstName	string
            maxLength: 255
        billingLastName	string
            maxLength: 255
        billingCompany	string
            maxLength: 255
        billingAddress	string
            maxLength: 255
        billingAddress2	string
            maxLength: 255
        billingCity	string
            maxLength: 255
        billingZip	string
            maxLength: 255
        billingCountryCode	string
            maxLength: 255
        billingRegion	string
            maxLength: 255
        billingInvoiceText	string
        paidForBy	integer
            minimum: 1
            maximum: 2147483647
        metadata	metadata{...}
        stripeCustomer	string
            maxLength: 255
        language	string
            maxLength: 255
        id*	integer
            minimum: -2147483648
            maximum: 2147483647
        account*	integer
            minimum: -2147483648
            maximum: 2147483647
        state	stringEnum:
            Array [ 3 ]
        allowLogin	boolean
            default: false
        lockVersion*	integer
            minimum: -2147483648
            maximum: 2147483647
        createdAt*	string($date)
        updatedAt*	string($date)
        updatedBy	integer
            minimum: -2147483648
            maximum: 2147483647
        lastActivity*	lastActivity{
            id*	integer
                minimum: -2147483648
                maximum: 2147483647
            at*	string($date)
            resource	Resource%20summary{...}
        }
        _embedded	string
    }]
"""
