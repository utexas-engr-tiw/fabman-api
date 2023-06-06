#!/usr/bin/python3
"""This file creates a model for resoure-logs objects from the Fabman API.
    
    According the the Fabman API documentation, a resour-logs object has the following attributes:
    Log record {
        id*	integer
            minimum: -2147483648
            maximum: 2147483647
        account*	integer
            minimum: -2147483648
            maximum: 2147483647
        resource*	integer
            minimum: -2147483648
            maximum: 2147483647
        type*	stringEnum:
            Array [ 9 ]
        member	integer
            minimum: -2147483648
            maximum: 2147483647
        originalMember	integer
            minimum: -2147483648
            maximum: 2147483647
        stoppedAt	string($date)
        lockVersion*	integer
            minimum: -2147483648
            maximum: 2147483647
        createdAt*	string($date)
        updatedAt*	string($date)
        updatedBy	integer
            minimum: -2147483648
            maximum: 2147483647
        stopType	stringEnum:
            Array [ 7 ]
        idleDurationSeconds	integer
            minimum: -2147483648
            maximum: 2147483647
        reason	stringEnum:
            Array [ 14 ]
        notes	string
        metadata	metadata{...}
        extraChargeDescription	string
            maxLength: 255
        extraChargeDetails	string
        extraChargePrice	number
            minimum: -9999999.99
            maximum: 9999999.99
        extraChargeTaxPercent	number
            minimum: 0
            maximum: 100
        _embedded	metadata{...}
    }
"""