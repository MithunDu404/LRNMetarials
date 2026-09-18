# 8 API Laws of Senior Backend Developer

## 1. Design Around Resources, Not Actions

A common mistake in API design is naming endpoints after actions — things like `getUsers`, `createOrder`, `deleteProduct`. These feel intuitive at first, but they cause a redundancy problem: the URL is describing the action while HTTP itself already has a mechanism for describing actions (the HTTP method). You end up encoding the same information twice.

The cleaner approach is to treat `users`, `orders`, and `products` as resources, and let the HTTP verbs (`GET`, `POST`, `DELETE`, etc.) express what you're doing to them. This scales much better as the API grows, because a single resource can support many operations without needing a new URL invented for each one. For example, an order resource can be retrieved, replaced, or deleted, all through the same `orders` URL, just with a different HTTP method attached.

The core principle: the URL identifies *what* the resource is; the HTTP method identifies *what operation* is being performed on it.

## 2. Make Your URLs Predictable

Consistency in naming resources across the API matters more than it seems. If one part of the API uses `user`, another uses `customers`, and another uses `customer_profiles` for conceptually similar things, each individual endpoint might work fine in isolation, but the API as a whole becomes harder to use — developers have to memorize a different naming rule for every corner of it.

A better-structured API uses one consistent naming pattern for collections (e.g., `users`, `orders`, `products`), and a specific item within a collection is reached via its identifier appended to that collection path. For resources with multi-word names, pick one naming convention (e.g., snake_case or kebab-case) and apply it everywhere — which specific convention you choose matters far less than applying it uniformly.

The underlying idea: a predictable API reduces the amount of documentation a developer needs to keep in their head. If the structure is guessable, it needs fewer instructions to use correctly.

## 3. Use HTTP Methods for Their Actual Purpose

Consider updating a user resource: one API might use `POST` for this, another `PUT`, another `PATCH`. All three might technically function, but each choice forces the client to learn your API's custom, ad hoc rules instead of relying on standard, universally understood HTTP semantics.

The intended purposes of each method:

- **GET** — retrieves data without changing the resource's state.
- **POST** — typically creates a new resource, or triggers some processing that doesn't map cleanly onto updating an existing resource.
- **PUT** — used when replacing the entire representation of a resource.
- **PATCH** — used for partial updates to a resource.
- **DELETE** — removes a resource.

**Idempotency** is the key concept tying this together. An operation is idempotent if performing it multiple times has the same effect as performing it once. Sending the same `GET` request five times should behave the same as sending it once, and the same idea applies to `PUT` and `DELETE`: repeating the request doesn't produce a different or additional effect beyond the first time. `POST` is the exception — sending the same "create" request twice can create two separate resources, since each call is intended to add something new.

This matters practically because networks are unreliable: connections fail, clients retry, requests time out. If your methods honor their proper semantics, the API behaves predictably even when a client resends a request it isn't sure went through. Choosing HTTP methods purely because "it makes the endpoint work" rather than because it matches the method's real semantics undermines this reliability.

## 4. Make Status Codes Useful

A problematic pattern: an API returns `200 OK`, but the response body says the operation actually failed (e.g., "product not found"). This creates a contradiction — the HTTP-level signal says success while the body says failure — and forces the client to check two separate places just to know what happened, which is unnecessary duplication of responsibility.

Status codes should carry the high-level result themselves:

- **200** — a successful read.
- **201** — a resource was successfully created.
- **202** — the request was accepted and will complete asynchronously.
- **204** — a successful operation that returns no response body.

For failures, the numeric family should communicate what kind of failure occurred:

- **400** — invalid request.
- **401** — authentication missing or invalid.
- **403** — authenticated, but lacking permission.
- **404** — the requested resource doesn't exist.
- **409** — the request conflicts with the current state of the resource.
- **422** — the request fails business-level validation.
- **429** — the client is sending too many requests.

The point isn't to memorize the entire status code table — it's to avoid inventing your own parallel error-signaling scheme on top of HTTP when HTTP already has one. The status code should tell the client, on its own, what category of result occurred.

## 5. Keep Errors Consistent

Status codes only tell you the *category* of a failure; clients usually need more detail than that to act on it. Compare a bare error like "something went wrong" against a structured error response that includes an error code, a human-readable message, and the status — the structured version is far more usable for both humans reading it and software reacting to it programmatically: the message can be shown to a user, the error code can drive application logic, and developers can use it to investigate the underlying issue.

For validation errors specifically, a good API returns exactly which fields failed and why, rather than a generic "invalid request." The precise JSON shape used for errors can vary between systems — what matters is that it is structured and predictable across the whole API, so clients never have to guess what went wrong from a single opaque string.

## 6. Don't Put Everything Into the URL Path

A pattern that starts reasonably but grows out of control: a `products` endpoint that gradually has category, stock status, price, search terms, and sorting all folded into the path itself. Eventually the URL becomes unwieldy and hard to manage.

The fix is to separate concerns: the **path** should identify the resource (or collection), while **query parameters** should be used for filtering and other optional refinements to that resource.

However, query parameters should not be used to smuggle in actions. For example, sending a `GET` request with a parameter like `action=delete` is confusing, because now the HTTP method in the request no longer honestly reflects what the request does — the method says "read," but the parameter says "delete."

The responsibilities should stay cleanly separated:
- Paths identify resources.
- Query parameters refine/filter them.
- HTTP methods describe the operation being performed.

## 7. Treat API Changes Carefully

APIs evolve — a response shape that looks correct today may need new fields, a different structure, or a field whose meaning needs correcting six months from now. The danger isn't change itself, it's making a **breaking** change without considering the clients already depending on the old shape.

Example: an earlier API version returns a simple `price` field, and later the team wants to replace it with a richer pricing structure (e.g., an object with currency, discounts, etc.). This isn't just "adding a field" — it's a structural change, and existing clients that expect `price` to be a simple value will break.

The first question to ask before any change is whether it actually requires a new version:
- Adding a new, non-required field generally does **not** require breaking existing clients — they can simply ignore the field they don't recognize.
- Changing or removing existing behavior/fields generally **does** risk breaking them.

When versioning genuinely is needed, the important thing is that the strategy is obvious and applied consistently — whether that's a version segment in the URL, a request header, or some other established mechanism. The specific mechanism matters less than picking one approach and sticking to it, while giving API consumers a clear path to migrate to the new version.

The underlying goal: API evolution shouldn't turn existing, well-behaved clients into collateral damage.

## 8. Keep Request and Response Formats Consistent

A subtle but underestimated problem: if one endpoint returns a timestamp field as `createdAt`, another as `created_at`, and another as `created`, all three are individually valid, but now every client integrating with the API has to remember which naming convention applies to which specific endpoint. The same inconsistency problem can show up in date formats, pagination structures, error response shapes, property naming, and general response structure.

The fix is simply to pick conventions once and apply them everywhere: use one data format (e.g., JSON) consistently, choose a single naming convention for JSON properties, standardize how errors are structured across all endpoints, and make pagination and filtering behave the same way no matter which resource you're querying.

The goal isn't to produce an exhaustive rulebook that every endpoint must be checked against — it's that once a developer learns how *one* endpoint in your API behaves, they should be able to correctly guess how the *next* endpoint behaves without reading new documentation. Consistency itself is one of the most valuable properties an API can have.

## Closing Point: REST Compliance Isn't the Real Goal

Many developers focus heavily on whether an API technically conforms to REST conventions. That's a useful lens, but it isn't the ultimate goal. Simply using `GET`, `POST`, `PUT`, and `DELETE` correctly doesn't automatically make an API *good*.

A genuinely good API is one that clients can understand and use correctly without constantly consulting documentation: resource names are sensible, methods behave the way their semantics promise, status codes actually mean something, errors follow one consistent structure, filtering works the same way across every endpoint, and changes don't unexpectedly break the clients already built against it.

The practical implication for designing a new REST API is to not start by building endpoints one at a time. Instead, start by defining the patterns the whole API will follow: how resources will be named, how collections will be represented, how filtering will work, which HTTP methods will be used for which operations, how errors will look, how status codes will be handled, and how the API will evolve over time. Once those rules are settled, building out individual endpoints becomes straightforward — because a good REST API doesn't just return the right data, it makes the *correct way to use it* obvious.

---

Source: [8 API Laws of Senior Backend Developer](https://youtu.be/-40xErgJIBg?si=nxSdS1lhc_PbHyLD) — Cloud X Berry
