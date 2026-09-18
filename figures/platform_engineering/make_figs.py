"""Figures for 'Platform Engineering - Lessons from 8 Years at Atlassian'.
03, 07 and 08 are simulations (queueing, token bucket, canary rollout). 09 is a labelled illustrative cost model.
Run:  python figures/platform_engineering/make_figs.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _style import *

OUT = out_dir(__file__)
rng = np.random.default_rng(5)


def node(ax, x, y, text, fc="white", ec=DARK, w=1.8, h=0.8, fs=9, weight="normal"):
    box(ax, x - w / 2, y - h / 2, w, h, text, fc=fc, ec=ec, fs=fs, weight=weight)


# ------------------------------------------------------------------ 01 interview
def fig_interview():
    fig, ax = canvas(13, 3.2, (0, 13), (0, 3.2))
    ax.text(6.5, 2.95, "The interview loop (as it was ~8 years ago)", ha="center", fontsize=12, weight="bold")
    stages = [("① Coding quiz\n(HackerRank)", "tests: basic coding"),
              ("② Tech interview 1\nread a Cloudflare whitepaper\nin 10 min, explain it back", "tests: learning fast,\ncommunication"),
              ("③ Tech interview 2\ninterview the interviewer to\ndebug a past incident", "tests: troubleshooting,\nasking good questions"),
              ("④ Values interview\n\"what must I achieve in\n12 months?\"", "tests: fit, ownership")]
    for i, (s, t) in enumerate(stages):
        x = 1.65 + i * 3.25
        node(ax, x, 1.75, s, fc="#eff6ff", ec=BLUE, w=2.9, h=1.2, fs=8.5)
        ax.text(x, 0.75, t, ha="center", va="top", fontsize=8.5, color=GRAY)
        if i:
            arrow(ax, x - 3.25 + 1.45, 1.75, x - 1.45, 1.75, color=GRAY)
    save(fig, OUT, "01_interview_loop.png")


# ------------------------------------------------------------------ 02 OSB async architecture
def fig_osb():
    fig, ax = canvas(13, 5.0, (0, 13), (0, 5.0))
    ax.text(6.5, 4.75, "Open Service Broker: accept fast, work in the background", ha="center", fontsize=12, weight="bold")
    node(ax, 1.2, 2.6, "config file in\nversion control\n→ build server", fc="#f9fafb", ec=GRAY, w=2.0, h=1.2, fs=8.5)
    node(ax, 4.0, 2.6, "FastAPI broker\n(OSB API)", fc="#eff6ff", ec=BLUE, w=2.0, h=1.0, weight="bold")
    node(ax, 7.0, 3.7, "SQS queue\n(task messages)", fc="#fffbeb", ec=AMBER, w=2.2, h=0.9)
    node(ax, 10.2, 3.7, "worker\n(slow provisioning)", fc="#f5f3ff", ec=PURPLE, w=2.2, h=0.9)
    node(ax, 7.0, 1.3, "DynamoDB\n(job state + results)", fc="#f0fdf4", ec=GREEN, w=2.4, h=0.9)
    node(ax, 12.1, 2.1, "DNS records\nCloudFront\nother AWS APIs", fc="white", ec=GRAY, w=1.6, h=1.1, fs=8)
    arrow(ax, 2.2, 2.95, 3.0, 2.95, color=DARK, text="① PUT provision", fs=8, toff=(0, 0.12))
    arrow(ax, 3.0, 2.6, 2.2, 2.6, color=GREEN)
    ax.text(2.6, 2.4, "② 202 Accepted", fontsize=8, color=GREEN, ha="center", va="top")
    arrow(ax, 2.2, 2.15, 3.0, 2.15, color=BLUE, style="<|-|>", ls="--")
    ax.text(2.6, 1.95, "⑦ poll last_operation\n(repeat until done)", fontsize=8, color=BLUE, ha="center", va="top")
    arrow(ax, 5.0, 2.9, 5.9, 3.6, color=AMBER, text="③ enqueue", fs=8)
    arrow(ax, 8.1, 3.7, 9.1, 3.7, color=AMBER, text="④ pull", fs=8)
    arrow(ax, 11.3, 3.5, 12.1, 2.6, color=PURPLE, text="⑤ do work", fs=8)
    arrow(ax, 10.0, 3.25, 8.0, 1.7, color=PURPLE, text="⑥ write result", fs=8)
    arrow(ax, 5.0, 2.3, 5.8, 1.5, color=GREEN, text="read state", fs=8)
    ax.text(6.5, 0.2, "Iterations: Connexion (routes generated from the OpenAPI spec) → Flask → FastAPI",
            ha="center", fontsize=9, color=GRAY)
    save(fig, OUT, "02_osb_async_architecture.png")


# ------------------------------------------------------------------ 03 sync vs async (queue simulation)
def fig_sync_async():
    n_req, threads, work = 60, 12, 20.0                  # 60 requests arrive within 60 s, each needs ~20 s of work
    arrivals = np.sort(rng.uniform(0, 60, n_req))
    works = rng.lognormal(np.log(work), 0.3, n_req)
    # synchronous: HTTP request holds a server thread for the whole provisioning time
    free = np.zeros(threads); sync_wait = []
    for a, w in zip(arrivals, works):
        i = np.argmin(free); start = max(a, free[i]); free[i] = start + w
        sync_wait.append(start + w - a)                  # client stares at a spinning HTTP call
    # async: HTTP returns in ~50 ms; the same 8 workers drain a queue
    free = np.zeros(threads); done = []
    for a, w in zip(arrivals, works):
        i = np.argmin(free); start = max(a, free[i]); free[i] = start + w
        done.append(start + w - a)
    async_http = np.full(n_req, 0.05)
    fig, axes = plt.subplots(1, 2, figsize=(13, 3.9))
    ax = axes[0]
    ax.plot(arrivals, sync_wait, "o", ms=4, color=RED, label="synchronous API: HTTP call open until work finishes")
    ax.plot(arrivals, async_http, "o", ms=4, color=GREEN, label="async API: HTTP answers 202 immediately")
    ax.axhline(30, color=GRAY, ls="--"); ax.text(1, 32, "typical client / load-balancer timeout (30 s)", fontsize=8, color=GRAY)
    ax.set_yscale("log"); ax.set_xlabel("request arrival time (s)"); ax.set_ylabel("seconds the HTTP call stays open (log)")
    ax.set_title("60 provisioning requests in a minute, 12 workers (simulation)"); ax.legend(fontsize=8, loc="center right")
    ax = axes[1]
    ax.hist(done, bins=25, color=PURPLE, alpha=0.85)
    ax.set_xlabel("seconds until the job is actually finished"); ax.set_ylabel("requests")
    ax.set_title(f"Jobs take the same time either way (median {np.median(done):.0f} s),\n"
                 f"but {np.mean(np.array(sync_wait) > 30)*100:.0f}% of SYNC calls would hit a 30 s timeout")
    save(fig, OUT, "03_sync_vs_async.png")


# ------------------------------------------------------------------ 04 control plane / data plane
def fig_control_plane():
    fig, ax = canvas(13, 5.2, (0, 13), (0, 5.2))
    ax.text(6.5, 4.95, "Control plane (decides) vs data plane (moves bytes): the Sovereign design", ha="center",
            fontsize=12, weight="bold")
    ax.add_patch(FancyBboxPatch((0.2, 0.4), 7.3, 4.1, boxstyle="round,pad=0.03", fc="#f8fafc", ec=BLUE, lw=1.2, ls="--"))
    ax.text(0.4, 4.25, "CONTROL PLANE", color=BLUE, weight="bold", fontsize=9)
    node(ax, 1.5, 3.2, "context source:\nOSB DynamoDB", fc="#f0fdf4", ec=GREEN, w=2.1, h=0.8, fs=8.5)
    node(ax, 1.5, 2.1, "context source:\nS3 bucket", fc="#f0fdf4", ec=GREEN, w=2.1, h=0.8, fs=8.5)
    node(ax, 1.5, 1.0, "templates:\nclusters · routes ·\nlisteners", fc="#fffbeb", ec=AMBER, w=2.1, h=1.0, fs=8.5)
    node(ax, 5.2, 2.1, "Sovereign\n(FastAPI)\nrender template + context\n→ validate\n→ serve config", fc="#eff6ff", ec=BLUE, w=3.2, h=1.9,
         fs=9, weight="bold")
    for y in (3.2, 2.1, 1.0):
        arrow(ax, 2.55, y, 3.6, 2.1 + (y - 2.1) * 0.35, color=GREEN if y > 1.5 else AMBER)
    ax.add_patch(FancyBboxPatch((8.0, 0.4), 4.8, 4.1, boxstyle="round,pad=0.03", fc="#fef2f2", ec=RED, lw=1.2, ls="--"))
    ax.text(8.2, 4.25, "DATA PLANE (~2,000 proxies, ~13 regions)", color=RED, weight="bold", fontsize=9)
    for i, y in enumerate([3.4, 2.4, 1.4]):
        node(ax, 10.4, y, f"Envoy proxy {i+1}\n(hot-reloads config,\nno restart)", fc="white", ec=RED, w=2.6, h=0.8, fs=8.5)
        arrow(ax, 9.1, y, 6.8, 2.1 + (y - 2.4) * 0.4, color=BLUE, ls="--", lw=1)
    ax.text(10.4, 0.6, "…", ha="center", fontsize=14)
    ax.text(7.75, 3.9, "poll /\nstream\nconfig", fontsize=8, color=BLUE, ha="center")
    save(fig, OUT, "04_control_plane_sovereign.png")


# ------------------------------------------------------------------ 05 provisioning pipeline
def fig_pipeline():
    fig, ax = canvas(13.5, 4.4, (0, 13.5), (0, 4.4))
    ax.text(6.75, 4.15, "From config-management code to a live proxy fleet", ha="center", fontsize=12, weight="bold")
    steps = [("SaltStack states", "envoy · logging agent ·\nhardening · network tuning ·\ncontainer runtime · observability", AMBER),
             ("Packer", "boot temp EC2 → apply\nSalt → stop → snapshot", PURPLE),
             ("AMI", "golden machine image\n(immutable)", GRAY),
             ("CloudFormation", "VPC · subnets · IGW · SG ·\nkey pair · IAM role · NLB ·\nACM · Route 53 · ASG→AMI", BLUE),
             ("Auto Scaling Group", "launches EC2 instances,\nreplaces unhealthy ones", BLUE),
             ("Running proxy", "runtime params (secrets) →\npulls config from Sovereign\n→ serves traffic", GREEN)]
    for i, (t, d, c) in enumerate(steps):
        x = 1.1 + i * 2.25
        node(ax, x, 2.95, t, fc="white", ec=c, w=2.0, h=0.7, fs=9, weight="bold")
        ax.text(x, 2.45, d, ha="center", va="top", fontsize=7.8)
        if i:
            arrow(ax, x - 2.25 + 1.0, 2.95, x - 1.0, 2.95, color=GRAY)
    ax.text(6.75, 0.35, "Bake everything slow into the image ('immutable infrastructure'); inject only secrets & config at runtime.",
            ha="center", fontsize=9, color=GRAY)
    save(fig, OUT, "05_provisioning_pipeline.png")


# ------------------------------------------------------------------ 06 edge path with centralized concerns
def fig_edge():
    fig, ax = canvas(13.5, 5.2, (0, 13.5), (0, 5.2))
    ax.text(6.75, 4.95, "Solve cross-cutting concerns ONCE at the edge, not in every service", ha="center", fontsize=12, weight="bold")
    node(ax, 0.9, 2.6, "customer", fc="#f9fafb", ec=GRAY, w=1.4)
    node(ax, 2.9, 2.6, "CloudFront\nDDoS protection", fc="#fffbeb", ec=AMBER, w=1.9, h=1.0, fs=8.5)
    node(ax, 4.9, 2.6, "NLB\n(layer 4)", fc="#f9fafb", ec=GRAY, w=1.4, h=1.0, fs=8.5)
    ax.add_patch(FancyBboxPatch((6.0, 0.5), 3.9, 4.0, boxstyle="round,pad=0.03", fc="#fef2f2", ec=RED, lw=1.4))
    ax.text(7.95, 4.25, "one proxy host (from the AMI)", ha="center", fontsize=8.5, color=RED, weight="bold")
    node(ax, 7.95, 3.4, "Envoy\nrouting · TLS · access logs\n(native filters, templated)", fc="white", ec=RED, w=3.4, h=1.0, fs=8.5)
    for i, (s_, who) in enumerate([("authN", "Rust"), ("authZ", "other team"), ("rate\nlimit", "other team")]):
        node(ax, 6.75 + i * 1.2, 1.4, f"{s_}\nsidecar\n({who})", fc="#eff6ff", ec=BLUE, w=1.15, h=1.3, fs=8)
        arrow(ax, 7.95, 2.9, 6.75 + i * 1.2, 2.0, color=BLUE, lw=1, style="<|-|>")
    for j, y in enumerate([3.8, 2.6, 1.4]):
        node(ax, 11.8, y, f"backend service {j+1}\n(just business logic)", fc="#f0fdf4", ec=GREEN, w=2.6, h=0.8, fs=8.5)
        arrow(ax, 9.65, 3.4, 10.5, y, color=GREEN, lw=1)
    arrow(ax, 1.6, 2.6, 1.95, 2.6); arrow(ax, 3.85, 2.6, 4.2, 2.6); arrow(ax, 5.6, 2.6, 6.25, 3.2)
    ax.text(11.8, 0.55, "…hundreds more", ha="center", fontsize=9, color=GRAY)
    save(fig, OUT, "06_edge_centralized_concerns.png")


# ------------------------------------------------------------------ 07 token bucket simulation
def fig_token_bucket():
    rate, burst = 5.0, 10.0
    t = np.arange(0, 20, 0.01)
    lam = np.where((t > 3) & (t < 6), 25, np.where((t > 12) & (t < 13), 60, 3))    # requests/s
    arrivals = rng.random(len(t)) < lam * 0.01
    tokens, last, allowed, rejected, tok_hist = burst, 0.0, [], [], []
    for ti, a in zip(t, arrivals):
        tokens = min(burst, tokens + (ti - last) * rate); last = ti
        if a:
            if tokens >= 1:
                tokens -= 1; allowed.append(ti)
            else:
                rejected.append(ti)
        tok_hist.append(tokens)
    fig, axes = plt.subplots(2, 1, figsize=(10, 5), sharex=True, gridspec_kw=dict(height_ratios=[1.3, 1]))
    bins = np.arange(0, 20.5, 0.5)
    axes[0].hist([allowed, rejected], bins=bins, stacked=True, color=[GREEN, RED], label=["allowed → backend", "rejected → 429"])
    axes[0].set_ylabel("requests / 0.5 s"); axes[0].legend(fontsize=8)
    axes[0].set_title(f"Token bucket (refill {rate:g}/s, burst {burst:g}) under two traffic spikes (simulation)")
    axes[1].plot(t, tok_hist, color=BLUE); axes[1].set_ylabel("tokens in bucket"); axes[1].set_xlabel("seconds")
    axes[1].axhline(burst, color=GRAY, ls=":")
    save(fig, OUT, "07_token_bucket.png")


# ------------------------------------------------------------------ 08 canary rollout of config
def fig_canary():
    stages = [0.01, 0.05, 0.25, 1.0]
    t = np.arange(0, 60)
    base_err = 0.2
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.8))
    for ax, canary, title in [(axes[0], False, "Push new config to ALL 2,000 proxies at once"),
                              (axes[1], True, "Staged rollout 1% → 5% → 25% → 100%\nwith automatic rollback (caught at the 1% stage)")]:
        err = np.full(len(t), base_err) + rng.normal(0, 0.03, len(t))
        frac = np.zeros(len(t))
        if not canary:
            frac[t >= 10] = 1.0
        else:
            frac[(t >= 10)] = 0.01
            rollback = 13                           # error spike detected on the 1% canary after 3 minutes
            frac[t >= rollback] = 0.0
        bad_err = 35.0                              # the "valid but traffic-destroying" config fails 35% of requests
        total = err * (1 - frac) + bad_err * frac
        ax.plot(t, total, color=RED if not canary else GREEN, lw=2)
        ax.axvline(10, color=GRAY, ls=":"); ax.text(10.5, 30, "bad config\npushed", fontsize=8)
        if canary:
            ax.axvline(13, color=BLUE, ls=":"); ax.text(13.5, 18, "canary (1% of proxies) alarms\n→ auto rollback; peak impact ≈ 0.5%", fontsize=8, color=BLUE)
        ax.set_ylim(0, 40); ax.set_xlabel("minutes"); ax.set_ylabel("% of ALL customer requests failing")
        ax.set_title(title)
    fig.suptitle("A config can be schema-valid and still break traffic: limit the blast radius (simulation)", weight="bold", y=1.04)
    save(fig, OUT, "08_config_canary_rollout.png")


# ------------------------------------------------------------------ 09 centralization economics (illustrative)
def fig_centralize():
    n = np.arange(1, 501)
    concerns = 5
    per_service = 3.0 * concerns          # engineer-weeks per service to build + maintain 5 concerns itself (assumption)
    central_fixed = 150.0                 # platform team build cost (assumption)
    central_marginal = 0.3                # onboarding per service (assumption)
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.plot(n, per_service * n, color=RED, lw=2.5, label="every service implements authN, authZ, rate limits, logs, DDoS")
    ax.plot(n, central_fixed + central_marginal * n, color=GREEN, lw=2.5, label="platform team builds them once at the proxy layer")
    be = central_fixed / (per_service - central_marginal)
    ax.axvline(be, color=GRAY, ls=":"); ax.text(be + 5, 5000, f"break-even ≈ {be:.0f} services", fontsize=9)
    ax.set_xlabel("number of backend services"); ax.set_ylabel("engineer-weeks")
    ax.set_title("Illustrative cost model (assumed numbers): centralization wins as services multiply\n"
                 "(and security becomes consistent instead of 'whatever each team remembered')", fontsize=10)
    ax.legend(fontsize=8.5); ax.grid(alpha=0.3)
    save(fig, OUT, "09_centralization_economics.png")


if __name__ == "__main__":
    fig_interview(); fig_osb(); fig_sync_async(); fig_control_plane(); fig_pipeline(); fig_edge()
    fig_token_bucket(); fig_canary(); fig_centralize()
