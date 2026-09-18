# I Was Laid Off by Atlassian — Study Notes

## Context and Purpose

The speaker worked at Atlassian for roughly eight years and was recently affected by layoffs. This video is a retrospective on the systems he built there, organized so viewers can jump to whichever section interests them. Most of the content is technical (the architecture of a self-service load balancing platform he built from scratch), with a final section on non-technical lessons (mentoring, conflict, maintenance).

## The Interview Process

The speaker still remembers the process clearly, even though it no longer matches how Atlassian interviews today. It had several stages:

- **Coding quiz on HackerRank** — he scored full marks.
- **First technical interview (two interviewers)** — he was handed a whitepaper (Cloudflare's paper on custom domains), given about 10 minutes alone to read it, and then asked to explain its contents back to the interviewers. This was followed by questions on architectural topics like microservices and containers.
- **Second technical interview — a troubleshooting exercise.** He had to interview the interviewer to gather information and diagnose a real past Atlassian incident: an application bug that caused a denial-of-service condition. He was also asked how latency-based DNS routing works. He reasoned about it from first principles and guessed that AWS Route 53 measured actual client latency directly (e.g., via triangulation), but the more accurate answer is that this kind of routing typically relies on a geolocation database rather than real-time latency measurement. His answer was called "not accurate, but acceptable" — a good example of reasoning that's plausible but not quite matching the real mechanism.
- **Values interview.** He doesn't recall most of it, but he remembers asking the interviewers a specific question: "Looking back 12 months from now, what would I need to have achieved for you to say hiring me was a good decision?" Their answer became his actual first assignment: build a self-service load-balancing system for Atlassian's internal developers — conceptually similar to AWS's Application Load Balancer, but for internal platform use. He didn't know the specific framework involved, but expressed confidence based on his experience building Python web apps, and that confidence was enough to get him hired.

## First Project: The Open Service Broker (OSB)

### What an Open Service Broker Is

An Open Service Broker is a web application with a standardized API for provisioning resources onto a platform — commonly used in Kubernetes ecosystems. The OSB spec (published on GitHub, with an OpenAPI document) defines endpoints such as:

- A **catalog endpoint** that lists available services and plans (with metadata) — this is what a self-service console UI would query to let developers browse and request resources.
- **Provisioning endpoints** (PUT/PATCH for creating/updating, DELETE for removing) that bind a resource (e.g., a database) to a consumer (a pod or cloud instance), abstracting away the underlying implementation (e.g., the developer just gets "a SQL-compatible database," not necessarily raw MySQL).

At Atlassian, provisioning requests didn't come from a UI — they came from configuration files committed to version control, which a build server then pushed through as deployment requests.

### Building It

The speaker built his own OSB implementation in Python, evolving through three iterations:
1. **Connexion** — a Python library that generates API route handlers directly from an OpenAPI document.
2. **Flask** — migrated to a plain Flask app.
3. **FastAPI** — the final and (as far as he knows) still-current implementation.

### Internal Architecture

The broker followed an asynchronous task pattern:

- A **FastAPI web app** receives a client's provisioning request (e.g., "provision a load balancer for me").
- Rather than doing the work itself, it drops a task description onto an **SQS queue**.
- A **worker** process picks up the task and performs the actual provisioning work — e.g., creating DNS records, creating a CloudFront distribution, or making other API calls.
- Results are written to a **DynamoDB** database.
- Meanwhile, the client polls the web app repeatedly ("is it ready yet?"); the web app checks the database and reports back success or failure once the worker finishes.

This separation (fast API layer, async worker, shared database, message queue) let the system accept requests quickly while doing potentially slow provisioning work in the background.

## Second Project: Replacing Load Balancers with Envoy

### Motivation

An architect proposed replacing Atlassian's existing enterprise load balancers — which carried real licensing costs — with an open-source, cloud-native, "commodity" proxy. The chosen technology was **Envoy Proxy**, which the speaker describes as similar in purpose to Nginx but more modern. The underlying goal was the same self-service philosophy as the OSB: developers shouldn't need to talk to the platform team just to get their load balancing configured.

### Why Envoy Fit This Model

Envoy exposes an API for **dynamic configuration** — its behavior can be reloaded at runtime without restarting the process. This meant the team could run a fleet of Envoy proxies continuously, and whenever a developer's service needed different routing/config, that change could be pushed out live rather than requiring a redeploy of the proxy itself.

### The Envoy Control Plane ("Sovereign")

To manage this dynamic configuration, the speaker built what the team called the **Envoy control plane**, later open-sourced under the name **Sovereign** (hosted on Bitbucket). Its design:

- It's another FastAPI app.
- It's configured with **templates** and **context**.
- Templates correspond to Envoy resource types — **clusters**, **routes**, **listeners**, etc.
- On startup, it loads templates and context and exposes them as APIs that Envoy proxies poll.
- When an Envoy instance requests configuration, Sovereign renders the templates using the current context and returns the resulting Envoy configuration.

The key design idea is **where the context comes from**: it's pulled dynamically from multiple sources — the OSB's database (the same DynamoDB used by the broker/worker system) and other stores, such as an S3 bucket holding data that changes over time. As that underlying data changes, the templates re-render, and Envoy's live configuration changes with it.

### The Full Request Flow (Broker + Control Plane + Proxy)

Putting the two systems together:
1. Client sends a provisioning request to the broker.
2. The worker performs the provisioning task and writes new data to the database.
3. The Sovereign control plane polls that data (and other sources) and generates new Envoy configuration from templates.
4. That configuration is delivered to the Envoy proxy, which changes its behavior accordingly.

This is presented as the second major building block, sitting logically "underneath" the client/broker relationship described earlier.

## Third Project: Provisioning the Proxy Infrastructure

Having a control plane and Envoy doesn't answer the question of how the actual Envoy machines come into existence. This required two more pieces.

### Infrastructure as Code via CloudFormation

The proxy fleet (the speaker mentions roughly 2,000 proxies across around 13 regions) was provisioned using **AWS CloudFormation** templates — infrastructure-as-code that creates the same resources a human would otherwise create manually through the AWS console. The components involved, walked through as they'd be built "from scratch," included:
- A VPC and subnet
- An internet gateway
- A security group
- A key pair
- An IAM role
- An **Auto Scaling Group (ASG)**, which is what actually creates the EC2 instances
- An **AMI** referenced by the ASG (so it knows what image to boot)
- A **Network Load Balancer (NLB)** — a layer-4 proxy in front of the fleet
- Some **ACM** (AWS Certificate Manager) usage
- Some **Route 53** DNS records for supporting purposes
- **Parameters** — passed in at instance runtime for secrets, keys, and other per-environment values

The IAM role, key pair, and security group all attach to the EC2 instances (inherited via the ASG). Note that the AMI itself isn't created by this template — it's only *referenced*, which motivates the next piece.

### Building the AMI with Packer and SaltStack

To produce the actual machine image used by the ASG, the team used:
- **HashiCorp Packer**, using its EC2 provisioner, to spin up a temporary EC2 instance in a dev account.
- **SaltStack** for configuration management — functionally comparable to Puppet, Ansible, or Chef. The speaker's plain-language definition of configuration management tools: they let you declaratively specify which packages get installed, which files get placed, and which services get run, in a specific order, rather than doing it by hand.

The process: Packer creates a live EC2 instance, uploads the SaltStack configuration, runs the provisioning step, then shuts the instance down and snapshots it into an AMI.

The resulting AMI baked in several categories of SaltStack "states" (install + configure steps), including:
- Envoy itself
- Logging agents
- Security/hardening
- Network tuning
- Container runtime support
- An observability agent (covering logging, tracing, and metrics)

So the overall chain is: SaltStack states → Packer builds an AMI → CloudFormation template references that AMI → ASG boots EC2 instances from it → instances receive runtime parameters (secrets/keys) → the resulting proxies pull their live configuration from Sovereign and start serving traffic.

The speaker notes this entire body of work — broker, control plane, and proxy provisioning pipeline — represented roughly the first two years of his time on the team.

## Migration Phase

With the foundation in place, the next major phase (spanning a couple of years) was twofold:

1. **Onboarding large products** — getting big Atlassian products (Jira, Confluence, Bitbucket, Status Page, and others) to actually use the new centralized load-balancing platform. This required building out many additional features to support the special cases these larger products needed, since the platform had to remain generic and multi-tenant while still serving very different products.
2. **Forced migration of all microservices** — this was comparatively easier because it could be mandated at the platform level. Previously, every service got very basic load balancing by default from the platform, and a service could become publicly accessible somewhat by accident, without much protection. The platform team changed this: after the migration, a service could no longer be exposed publicly through the old basic load balancer — teams had to explicitly configure the new centralized infrastructure, which forced developers to consciously signal that they intended a service to be public, closing an accidental-exposure gap.

## Deeper Envoy Configuration and Centralizing Cross-Cutting Concerns

### Why Envoy's Configuration Surface Is Large

The speaker walks through Envoy's configuration model to illustrate its complexity: a **virtual host** lets you configure which domains to accept traffic for; **routes** let you match requests in various ways and take actions — forwarding, direct responses, redirects, adding/removing headers, or sending traffic to *any* cluster configured on the proxy. That last point matters a lot at scale: if a proxy fleet serves potentially a thousand different services (each with its own cluster), and any route can point at any cluster, then the platform team's templating and validation logic becomes critical — it has to guarantee that the parameters developers submit always produce *valid* Envoy resources, since an invalid or a "valid but traffic-destroying" configuration is a real operational risk. A large share of the team's engineering effort went into this validation and templating logic for exactly this reason.

Envoy also supports **extensions** attached to listeners and clusters — for example, various **network filters**, the most heavily used being the **HTTP Connection Manager**, which handles routing, proxying behavior, and WebSocket support. Beyond that, Envoy supports **external processing** and **external authorization** hooks, which sets up the next idea.

### The Case for Centralizing Concerns at the Edge

The speaker's core architectural insight: once you have dynamic, template-driven configuration flowing to a proxy layer that sits between every customer and every backend service, you've created an opportunity to solve certain problems *once*, at the proxy layer, instead of separately inside every individual backend service.

He illustrates the request path: customer → NLB → Envoy proxy fleet → backend service (and the response flows back the same way). Concerns like **authentication, authorization, DDoS protection, rate limiting, and access logging** all need to happen somewhere. If Atlassian has (hypothetically) "a bazillion" backend services, each maintaining its own version of these concerns independently would be a massive duplication of engineering effort, would slow down feature delivery, and would ultimately hurt the customer, since teams would be spending time on undifferentiated infrastructure work rather than on their actual product. Centralizing these concerns at the shared proxy layer avoids that duplicated cost entirely.

### How Each Concern Was Actually Implemented

- **DDoS protection** — handled upstream by **CloudFront**, sitting in front of the NLB/proxy layer. This piece was primarily built by a colleague of the speaker's.
- **Access logging** — implemented natively inside Envoy itself, using Envoy's built-in access log network filter (configured through the HTTP Connection Manager). Because all of this configuration is templated and dynamic, a developer just submits a small piece of JSON describing what they want, and the templating system produces the full access-log configuration for them automatically — no manual Envoy config authoring required.
- **Authentication, authorization, and rate limiting** — these were too complex to express purely as native Envoy filter configuration, so they were implemented via a **sidecar model**: additional local processes/containers running alongside Envoy on the same proxy instance, which Envoy talks to over the network locally. 
  - The **authentication sidecar** was written by the speaker himself, in **Rust** (which he jokingly calls "the Lord's language").
  - The **authorization sidecar** was contributed by another team.
  - The **rate limiting sidecar** was also contributed by another team.
  
  These sidecars were installed and configured as part of the same AMI-provisioning pipeline described earlier (Packer + SaltStack), and — importantly — they too could receive their own dynamic configuration over the wire, independent of Envoy's own configuration. This made the whole proxy host "programmable" at multiple layers: the proxy itself, plus each sidecar, all reconfigurable live.

The net effect: authentication, authorization, DDoS protection, rate limiting, and access logging are all resolved before a request ever reaches a backend service, and backend teams don't need to think about any of it.

## Later Work: Compliance

After the technical buildout and migrations were largely complete, the team took on **compliance requirements** — verifying that the existing systems met various compliance standards. The speaker found this phase tedious and unrewarding compared to the earlier building work, describing it as "boring checklist ticking" rather than construction of new systems.

## Non-Technical Lessons from Eight Years

### Skills Gained Beyond Engineering

The speaker highlights several non-technical capabilities he developed that aren't usually discussed alongside technical portfolio work: diplomacy, conflict avoidance and resolution, persuasion, proposing ideas, and teaching/mentoring.

### On Maintenance

He draws a distinction between the difficulty of *building* something and the difficulty of *maintaining* it over time.

- At the start of a project, there's a burst of necessary work: onboarding new contributors, writing documentation, training people to debug and operate the system, and making sure people going on call know what can go wrong — which log messages matter, which metrics to watch, and what those metrics imply. He gives concrete failure scenarios he had to think through: what happens if AWS has an outage and the database becomes unreachable? What if SQS goes down and no provisioning tasks can run — what's the downstream impact on services waiting for resources? What if a proxy receives configuration that is technically valid but nonetheless breaks the traffic flowing through it — how would you detect that?
- Over a longer time horizon, the harder problem emerges: people join and leave, onboarding has to happen repeatedly, and each new contributor brings their own opinions about how the code should be restructured or improved. This produces **churn** in the codebase. The speaker frames the location of that churn as a diagnostic signal — a "smell": wherever churn concentrates is often an early indicator that a section of the system is going to keep growing in size or complexity, and that something structural needs to be addressed before it gets worse.
- His broader generalization: building something is comparatively easy; keeping it *changeable* over time is the hard part, because every change tends to add coupling, so that later changes in one area unexpectedly ripple into another, and someone eventually has to spend effort "detangling" that coupling.
- He raises an open question about AI-assisted/"vibe coded" software: since so much code is now being produced by people who may not deeply understand what they generated, it remains to be seen how the maintenance burden will show up over time — that burden doesn't appear immediately, only after enough changes have accumulated. He notes some optimism that LLMs might also be usable to help identify and perform the detangling work itself, but says he doesn't want to be overly optimistic about that yet.

### On Interpersonal Conflict and Diplomacy

Working under many different managers and alongside many different colleagues over eight years exposed him to a wide range of personalities and working styles, and inevitably to some conflicts — even with people he otherwise respected. His conclusion is that this kind of mismatch is somewhat inevitable, and the best available response is developing self-awareness, awareness of the other person, and some understanding of psychology, so that you can anticipate friction before it escalates and take responsibility for managing the relationship. He's candid that this was a genuine source of stress that at times affected his performance — and because it affected his performance, he took it seriously enough to consciously work on it, and believes he'd handle similar situations better in the future.

### On Mentoring vs. Teaching

He separates two skills he considers distinct: 

- **Teaching/training colleagues** — breaking down complex systems into simple mental models for others — which he describes as something he's good at and which effectively became his main activity in the second half of his time at Atlassian (pairing with colleagues, walking through problems together). Feedback he consistently received was that he was always available to help and good at making difficult topics understandable.
- **Mentoring** (in the specific sense of guiding an intern) — which he found genuinely difficult. The specific tension he describes is calibrating how much help to give: not wanting to simply hand over answers, but also not wanting the mentee to get stuck to the point of frustration. He mentored an intern who ultimately received the highest possible internship rating and a guaranteed return offer, and whose project was very impressive — but he's reluctant to credit himself fully for that outcome, since the intern also drew on help from other colleagues with expertise the speaker himself lacked, and did the bulk of the actual implementation, testing, and design work independently. He adds that part of his uncertainty about his own mentoring ability stems from never having been mentored himself, so he has no personal reference point for what "good mentoring" is supposed to feel like from the other side.

---

Source: [I was laid off by Atlassian](https://youtu.be/55pTFVoclvE?si=KMmeZ_0K8pEoHUae) — Vasilios Syrakis
