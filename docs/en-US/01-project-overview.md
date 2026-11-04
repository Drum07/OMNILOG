# Project Vision — OMNILOG HUB

## 1. Purpose
Build an integrated platform for order management, inventory, warehousing, transportation, deliveries, and omnichannel e-commerce.

## 2. Actors
- Customer: browses the catalog, places orders, and tracks deliveries.
- Warehouse Operator: records stock movements, picking, and product allocation.
- Logistics Manager: monitors KPIs, routes, fleet, and deliveries.
- System Administrator: manages users, roles, settings, and audit records.

## 3. Initial functional requirements
- FR001: authenticate users according to their roles.
- FR002: manage customers and addresses.
- FR003: manage products and categories.
- FR004: check stock availability by warehouse.
- FR005: create and track orders.
- FR006: record payments and payment states.
- FR007: allocate products to warehouse locations.
- FR008: plan routes and assign deliveries, vehicles, and drivers.
- FR009: track shipments using a tracking code.
- FR010: record relevant events in an audit trail.
- FR011: generate management indicators.
- FR012: manage users and roles.

## 4. Initial non-functional requirements
- NFR001: expose an OpenAPI-documented API.
- NFR002: common queries should respond in under 2 seconds in a defined reference environment and test workload.
- NFR003: passwords must only be stored as secure hashes.
- NFR004: personal data must have a defined purpose, restricted access, retention, and LGPD-aligned safeguards.
- NFR005: critical stock and order operations must use database transactions.
- NFR006: source code must be version-controlled with Git and reviewed through pull requests.
- NFR007: automated tests must cover critical business rules.
- NFR008: backups must be validated through restoration tests, not merely generated.

## 5. Assumptions and boundaries
This is an academic project using fictional data. Real payment, carrier, and mapping integrations will be simulated until authorized credentials and environments are available.
