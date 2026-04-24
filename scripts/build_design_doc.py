# -*- coding: utf-8 -*-
"""
Generate the Firefly Rise — Google Ads API Tool Design Document (PDF).
Output: docs/firefly-rise-google-ads-api-tool-design.pdf
"""
import datetime
import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, PageBreak, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "firefly-rise-google-ads-api-tool-design.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

PRIMARY = colors.HexColor("#ff7200")
ACCENT = colors.HexColor("#0a2540")
DARK = colors.HexColor("#2d2d2d")
MUTED = colors.HexColor("#6b6b6b")
BG_GRAY = colors.HexColor("#f2f2f2")
BORDER = colors.HexColor("#e0e0e0")

styles = getSampleStyleSheet()

# Custom styles
H1 = ParagraphStyle("H1", parent=styles["Heading1"],
    fontName="Helvetica-Bold", fontSize=22, leading=28, textColor=DARK,
    spaceBefore=4, spaceAfter=14, alignment=TA_LEFT)
H2 = ParagraphStyle("H2", parent=styles["Heading2"],
    fontName="Helvetica-Bold", fontSize=15, leading=20, textColor=PRIMARY,
    spaceBefore=18, spaceAfter=8, alignment=TA_LEFT)
H3 = ParagraphStyle("H3", parent=styles["Heading3"],
    fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=DARK,
    spaceBefore=10, spaceAfter=4, alignment=TA_LEFT)
BODY = ParagraphStyle("Body", parent=styles["BodyText"],
    fontName="Helvetica", fontSize=10.2, leading=15, textColor=DARK,
    spaceBefore=2, spaceAfter=6, alignment=TA_LEFT)
BULLET = ParagraphStyle("Bullet", parent=BODY,
    leftIndent=14, bulletIndent=2, spaceBefore=1, spaceAfter=1)
META = ParagraphStyle("Meta", parent=BODY, textColor=MUTED, fontSize=9, leading=12)
COVER_TITLE = ParagraphStyle("CoverTitle", parent=H1,
    fontSize=30, leading=36, alignment=TA_LEFT, spaceAfter=8, textColor=DARK)
COVER_SUB = ParagraphStyle("CoverSub", parent=BODY, fontSize=14, leading=20,
    textColor=PRIMARY, alignment=TA_LEFT, spaceAfter=18)
COVER_META = ParagraphStyle("CoverMeta", parent=BODY, fontSize=10, leading=14,
    textColor=MUTED, alignment=TA_LEFT)


def bullet(text):
    return Paragraph(text, BULLET, bulletText=u"\u2022")


def header_footer(canvas, doc):
    canvas.saveState()
    # Header bar (orange accent)
    canvas.setFillColor(PRIMARY)
    canvas.rect(0, LETTER[1] - 0.35 * inch, LETTER[0], 0.06 * inch, stroke=0, fill=1)
    # Footer
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(0.75 * inch, 0.5 * inch,
        "Firefly Rise \u2014 Google Ads API Tool Design Document")
    canvas.drawRightString(LETTER[0] - 0.75 * inch, 0.5 * inch,
        f"Page {doc.page}")
    canvas.restoreState()


def make_doc():
    doc = BaseDocTemplate(
        str(OUT), pagesize=LETTER,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        topMargin=0.7 * inch, bottomMargin=0.8 * inch,
        title="Firefly Rise — Google Ads API Tool Design",
        author="Firefly Rise",
        subject="Google Ads API Developer Token Application",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="default",
        frames=[frame], onPage=header_footer)])
    return doc


story = []

# ── Cover ─────────────────────────────────────────────────────────────────────
story += [
    Spacer(1, 1.0 * inch),
    Paragraph("Google Ads API Tool", COVER_SUB),
    Paragraph("Design Documentation", COVER_TITLE),
    Spacer(1, 0.2 * inch),
    Paragraph(
        "<b>Firefly Rise</b> &mdash; a US digital marketing agency that works exclusively "
        "with home-service contractors. This document describes the design of the "
        "internal campaign-management tool that uses the Google Ads API.",
        BODY),
    Spacer(1, 0.6 * inch),
    Paragraph("<b>Company:</b> Firefly Rise", COVER_META),
    Paragraph("<b>Website:</b> https://fireflyrise.com", COVER_META),
    Paragraph("<b>Tool name:</b> Firefly Rise Campaign Manager (FRCM)", COVER_META),
    Paragraph("<b>Document version:</b> 1.0", COVER_META),
    Paragraph(f"<b>Last updated:</b> {datetime.date.today().strftime('%B %d, %Y')}",
        COVER_META),
    PageBreak(),
]

# ── 1. Tool Overview ──────────────────────────────────────────────────────────
story += [
    Paragraph("1. Tool Overview", H1),
    Paragraph(
        "<b>Firefly Rise Campaign Manager (FRCM)</b> is an internal web-based tool "
        "used exclusively by Firefly Rise account managers, strategists, and analysts "
        "to plan, launch, monitor, optimize, and report on Google Ads campaigns "
        "operated on behalf of home-service contractor clients (plumbers, HVAC, "
        "electricians, roofers, landscapers, painters, garage-door specialists, and "
        "similar trades).",
        BODY),
    Paragraph(
        "The tool is not exposed to clients. Clients receive scheduled, read-only "
        "weekly performance reports generated by the tool but do not log in or "
        "interact with it. The tool is not a self-service ad platform, does not "
        "resell ad inventory, and does not allow third parties to manage ad "
        "campaigns through it.",
        BODY),
    Paragraph("Primary objectives", H3),
    bullet("Manage many client Google Ads accounts efficiently from a single dashboard."),
    bullet("Automate routine reporting and surface optimization opportunities so account managers spend more time on strategy and less on data wrangling."),
    bullet("Tie Google Ads performance to actual phone calls and booked jobs (via call-tracking integrations) for transparent client reporting."),
    bullet("Enforce a consistent campaign-build playbook across the home-service vertical."),
]

# ── 2. Architecture ───────────────────────────────────────────────────────────
story += [
    Paragraph("2. Architecture", H1),
    Paragraph(
        "FRCM is a server-rendered web application with an internal-only frontend, "
        "a Python backend, a relational database for client and campaign metadata, "
        "and a data warehouse for historical Google Ads performance data.",
        BODY),
    Paragraph("Stack", H3),
]

stack_data = [
    ["Layer", "Technology"],
    ["Frontend (internal)", "Server-rendered HTML, vanilla JS, no public exposure"],
    ["Backend API", "Python 3.11+ with FastAPI"],
    ["Google Ads client", "Official google-ads Python library (gRPC)"],
    ["Database", "PostgreSQL (client metadata, audit log, jobs)"],
    ["Warehouse", "BigQuery or PostgreSQL (cached API responses, history)"],
    ["Job scheduler", "APScheduler / Celery for periodic syncs and reports"],
    ["Auth", "OAuth 2.0 (Google) + internal SSO for staff users"],
    ["Hosting", "Private VPC behind a VPN; no public ingress"],
]
stack_table = Table(stack_data, colWidths=[1.7 * inch, 4.6 * inch])
stack_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_GRAY]),
    ("LINEBELOW", (0, 0), (-1, 0), 1, PRIMARY),
    ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
]))
story += [stack_table, Spacer(1, 6)]

story += [
    Paragraph("High-level component diagram", H3),
    Paragraph(
        "<font face='Courier' size='9'>"
        "[Internal user]&nbsp;&nbsp;&rarr;&nbsp;&nbsp;[FRCM Web UI]&nbsp;&nbsp;&rarr;&nbsp;&nbsp;"
        "[FastAPI backend]&nbsp;&nbsp;&rarr;&nbsp;&nbsp;[google-ads Python client]"
        "<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&darr;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;[Google Ads API (gRPC)]<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&darr;<br/>"
        "[PostgreSQL]&nbsp;&nbsp;&larr;&nbsp;&nbsp;[Job scheduler]&nbsp;&nbsp;&rarr;&nbsp;&nbsp;"
        "[BigQuery / data warehouse]&nbsp;&nbsp;&rarr;&nbsp;&nbsp;[Weekly client report PDFs]"
        "</font>",
        BODY),
]

# ── 3. Users & UI ─────────────────────────────────────────────────────────────
story += [
    Paragraph("3. Users and User Interface", H1),
    Paragraph(
        "FRCM is used only by Firefly Rise employees. There are three internal roles:",
        BODY),
    bullet("<b>Account Manager</b> &mdash; primary user. Reviews client performance, applies optimization recommendations, generates and approves weekly reports."),
    bullet("<b>Strategist</b> &mdash; builds new campaigns and ad groups, edits keyword lists, writes ad copy variants, configures conversion tracking."),
    bullet("<b>Analyst / Owner</b> &mdash; agency-wide reporting, P&amp;L by client, hiring decisions, portfolio health checks."),

    Paragraph("Main views", H3),
    bullet("<b>Client portfolio</b> &mdash; one row per client, with health-check indicators (account status, conversion-tracking validity, week-over-week trends)."),
    bullet("<b>Client detail</b> &mdash; full Google Ads structure (campaigns &rarr; ad groups &rarr; ads / keywords) with performance side-by-side."),
    bullet("<b>Recommendations queue</b> &mdash; ranked list of suggested optimizations (negative keywords to add, low-performing ads to pause, budget shifts) generated from API data."),
    bullet("<b>Report builder</b> &mdash; renders branded weekly PDF and HTML reports tying spend to phone calls and booked jobs (data from call-tracking partners merged with Google Ads conversion data)."),
    bullet("<b>Audit log</b> &mdash; every API mutation made through the tool is logged with timestamp, internal user, target client account, and the request payload (sanitized)."),
]

# ── 4. Data Flow ──────────────────────────────────────────────────────────────
story += [
    Paragraph("4. Data Flow", H1),
    Paragraph("Read path (reporting and dashboard)", H3),
    Paragraph(
        "1. Scheduled job runs nightly (and on-demand from the dashboard) and "
        "iterates over the list of active client accounts under our Manager Account.<br/>"
        "2. For each client, the tool calls the Google Ads API "
        "(<i>GoogleAdsService.SearchStream</i>) to pull the prior-day performance data "
        "for campaigns, ad groups, ads, keywords, and search terms.<br/>"
        "3. Responses are stored in the data warehouse with a per-client partition.<br/>"
        "4. The dashboard queries the warehouse (not the API directly) for fast loads.",
        BODY),
    Paragraph("Write path (campaign management)", H3),
    Paragraph(
        "1. An internal user takes an action in the dashboard "
        "(e.g. apply an optimization recommendation, pause an ad group, edit a budget).<br/>"
        "2. The backend constructs the corresponding mutate request "
        "(<i>CampaignService.MutateCampaigns</i>, <i>AdGroupService.MutateAdGroups</i>, etc.).<br/>"
        "3. The request is sent to the Google Ads API with the appropriate "
        "<i>login_customer_id</i> (the Manager Account) and <i>customer_id</i> (the client).<br/>"
        "4. The response is logged to the audit log and the local cache is invalidated "
        "for the affected entity.",
        BODY),
    Paragraph("Client report path", H3),
    Paragraph(
        "1. Every Monday at 06:00 local time, the report job runs for each client.<br/>"
        "2. The job reads the prior 7 days of Google Ads performance from the warehouse, "
        "merges it with call-tracking data (calls, recordings, booked-job attribution), "
        "and renders a branded report.<br/>"
        "3. Reports are emailed to the client and archived in the warehouse for "
        "12 months.",
        BODY),
]

# ── 5. API Operations ─────────────────────────────────────────────────────────
story += [
    Paragraph("5. Google Ads API Operations Used", H1),
    Paragraph(
        "FRCM uses the standard Google Ads API (current version) via the official "
        "<i>google-ads</i> Python client library. The following services and operations "
        "are used:",
        BODY),
]

api_data = [
    ["Category", "Services / methods"],
    ["Reporting (read)",
        "GoogleAdsService.SearchStream queries against campaign, ad_group, ad_group_ad, "
        "keyword_view, search_term_view, geographic_view, customer, and customer_client resources"],
    ["Campaign management",
        "CampaignService.MutateCampaigns (create, update, pause, resume); "
        "CampaignBudgetService.MutateCampaignBudgets"],
    ["Ad group management",
        "AdGroupService.MutateAdGroups; AdGroupCriterionService.MutateAdGroupCriteria"],
    ["Ad management",
        "AdGroupAdService.MutateAdGroupAds (create / update / pause); "
        "AssetService for sitelinks, callouts, structured snippets"],
    ["Keyword management",
        "AdGroupCriterionService for keyword adds, bid adjustments, status changes; "
        "CampaignCriterionService and CustomerNegativeCriterionService for negatives"],
    ["Conversion tracking",
        "ConversionActionService (read), ConversionUploadService (when offline conversions "
        "from call tracking need to be uploaded)"],
    ["Account management",
        "CustomerService and CustomerClientService for reading account-level metadata "
        "and verifying manager-link status"],
    ["Recommendations",
        "RecommendationService (read) to surface Google's own recommendations to internal users"],
]
api_table = Table(api_data, colWidths=[1.6 * inch, 4.7 * inch])
api_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_GRAY]),
    ("LINEBELOW", (0, 0), (-1, 0), 1, PRIMARY),
    ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
]))
story += [api_table]

# ── 6. Authentication ─────────────────────────────────────────────────────────
story += [
    Paragraph("6. Authentication and Authorization", H1),
    Paragraph(
        "Every client whose Google Ads account is managed by Firefly Rise has linked "
        "their account to the Firefly Rise Google Ads Manager Account (MCC) under a "
        "signed service agreement. The MCC linkage is performed in Google Ads using "
        "Google's standard manager-link request/accept flow; clients always retain "
        "ownership of their account, billing, and historical data.",
        BODY),
    Paragraph("OAuth flow", H3),
    bullet("Firefly Rise holds a single OAuth 2.0 client (client ID + secret) for FRCM, scoped to <i>https://www.googleapis.com/auth/adwords</i>."),
    bullet("Once per Firefly Rise authorized internal user, an offline-access OAuth grant produces a refresh token tied to our Manager Account login."),
    bullet("Refresh tokens are stored encrypted at rest (AES-256, key managed by our cloud KMS); short-lived access tokens are kept in memory only."),
    bullet("All API calls include both a <i>login_customer_id</i> header (set to the MCC) and the target <i>customer_id</i> in the request payload to scope access."),
    bullet("Developer token is loaded from a secret store; it is never logged, committed, or transmitted to client browsers."),

    Paragraph("Authorization", H3),
    bullet("Internal users authenticate to FRCM via SSO (Google Workspace) and are mapped to one of the three roles described in section 3."),
    bullet("Account Manager and Strategist roles can perform read and mutate operations against any linked client account."),
    bullet("Analyst role is read-only."),
    bullet("Every API mutation is recorded in the audit log with the internal user and the target client."),
]

# ── 7. Use Cases ──────────────────────────────────────────────────────────────
story += [
    Paragraph("7. Representative Use Cases", H1),
    Paragraph("7.1 Daily portfolio sync", H3),
    Paragraph(
        "A scheduled job pulls prior-day performance for every linked client account, "
        "stores it in the warehouse, and updates a green/yellow/red health status for "
        "each client. Triggers an internal alert when an account drops to red.",
        BODY),
    Paragraph("7.2 Weekly client report", H3),
    Paragraph(
        "Every Monday morning, a job aggregates the prior 7 days of Google Ads "
        "performance, merges it with call-tracking data (calls received, calls "
        "answered, calls converted to a booked job), renders a branded PDF, and emails "
        "it to the client. The client sees exactly which keywords and campaigns "
        "produced calls and booked jobs that week.",
        BODY),
    Paragraph("7.3 Optimization recommendation queue", H3),
    Paragraph(
        "FRCM analyzes recent search-term reports and surfaces high-cost / "
        "low-conversion search terms that should become negative keywords. An account "
        "manager reviews the queue, approves recommended actions in bulk, and the tool "
        "applies them to the client account via the API. Every change is captured in "
        "the audit log.",
        BODY),
    Paragraph("7.4 Bulk campaign launch", H3),
    Paragraph(
        "When onboarding a new client, a strategist applies a vertical-specific "
        "campaign template (e.g. \"emergency plumbing &mdash; metro market\") that "
        "creates the full campaign &rarr; ad group &rarr; ad &rarr; keyword structure "
        "via the Google Ads API, against the new linked client account. This replaces "
        "what used to be a multi-day manual setup.",
        BODY),
    Paragraph("7.5 Conversion validation", H3),
    Paragraph(
        "Before a campaign is allowed to scale, FRCM verifies via the API that "
        "conversion actions are configured correctly, are firing within expected "
        "thresholds, and are linked to the right click sources. This catches broken "
        "tracking before significant ad spend is wasted.",
        BODY),
]

# ── 8. Security & Privacy ─────────────────────────────────────────────────────
story += [
    Paragraph("8. Security and Privacy", H1),
    bullet("All credentials (developer token, OAuth client secret, refresh tokens) are stored encrypted at rest in a managed secret store; never committed to source control."),
    bullet("All network traffic uses TLS 1.2+; the FRCM web UI is reachable only over HTTPS, behind a VPN, with no public ingress."),
    bullet("Internal users authenticate via Google Workspace SSO with mandatory 2FA."),
    bullet("PostgreSQL and warehouse instances run in a private VPC; backups are encrypted."),
    bullet("Audit log captures every API mutation, OAuth grant, and admin action; retained for at least 12 months."),
    bullet("Client data is never shared with third parties beyond the cloud-provider sub-processors required to operate the platform (hosting, email delivery, error tracking)."),
    bullet("Client-account access is removed within one business day of the end of an engagement; the corresponding Google Ads manager-link is cancelled and refresh tokens are revoked."),
    bullet("Annual internal security review of access lists, secret rotation, and audit-log integrity."),
]

# ── 9. Compliance ─────────────────────────────────────────────────────────────
story += [
    Paragraph("9. Compliance with Google Ads API Policies", H1),
    Paragraph(
        "FRCM is intended to comply with the Google Ads API Terms and the Required "
        "Minimum Functionality (RMF) for tools that manage Google Ads accounts on "
        "behalf of advertisers:",
        BODY),
    bullet("<b>Manager-account model.</b> Every client account is owned by the client and linked to our MCC under a signed service agreement."),
    bullet("<b>Internal-only tool.</b> FRCM is not exposed to clients or third parties; it is not a self-service ad platform."),
    bullet("<b>No reselling.</b> Firefly Rise does not resell Google Ads inventory; clients are billed by Google directly for their ad spend."),
    bullet("<b>Reporting fidelity.</b> Performance metrics surfaced to clients (impressions, clicks, conversions, cost) come directly from the Google Ads API and are not modified or recombined in misleading ways."),
    bullet("<b>Required functionality.</b> The tool supports campaign creation, ad-group and ad management, keyword and negative-keyword management, budget and bid adjustments, and reporting at the campaign, ad-group, ad, and keyword level &mdash; covering the RMF set for tools targeting search advertising."),
    bullet("<b>Token usage.</b> Our Google Ads API developer token is used only by Firefly Rise from FRCM; it is not embedded in client-facing software, browser extensions, or distributed binaries."),
    bullet("<b>No prohibited use cases.</b> FRCM does not perform automated account creation, mass-edits unrelated to legitimate optimization, click-fraud detection-as-a-service, or any other use case prohibited by the Google Ads API policy."),

    Paragraph("Contact", H3),
    Paragraph(
        "Questions about this design document or Firefly Rise's use of the Google Ads "
        "API should be directed to the Firefly Rise team via the contact channels on "
        "https://fireflyrise.com.",
        BODY),
]


def main():
    doc = make_doc()
    doc.build(story)
    size = OUT.stat().st_size / 1024
    print(f"Wrote {OUT} ({size:.0f} KB, ~{doc.page} pages)")


if __name__ == "__main__":
    main()
