/* Freddie Deepak Phase 2 — mock data + feature list (May 2026) */

window.FDPX_DATA = {
  brand: {
    name: "Stride Athletics",
    primary: "#017E89",
    orchestrationRun: "Spring Velocity · Agent run #1842",
    shieldPolicy: "Enterprise · Finance + Healthcare",
    locales: ["en-US", "en-AU", "fr-CA", "de-DE"]
  },

  campaign: {
    name: "Spring Velocity · Volt Runner",
    openRate: "41.2%",
    clickRate: "3.8%",
    revenueAttributed: "$18.4K / 7d",
    anomaly: "Mobile CTR −12% vs cohort"
  },

  features: [
    { num: "01", name: "Agentic Campaign Orchestrator",
      layer: "AI 2.0", surface: "Plan + Journey", sceneCount: 4,
      tagline: "Freddie plans multi-step sends with human approval gates and audit trails." },
    { num: "02", name: "Real-Time Campaign Performance Loop",
      layer: "AI 2.0", surface: "Editor + reporting", sceneCount: 4,
      tagline: "Live metrics beside the canvas; AI proposes fixes when KPIs slip." },
    { num: "03", name: "Send-Time AI Personalization",
      layer: "AI 2.0", surface: "Segment + composer", sceneCount: 4,
      tagline: "Per-recipient assembly within brand + compliance guardrails." },
    { num: "04", name: "Cross-Channel Asset Studio",
      layer: "AI", surface: "Content Studio bridge", sceneCount: 4,
      tagline: "One master asset · crops for email, SMS, social, ads." },
    { num: "05", name: "Compliance-Aware Localization",
      layer: "Governance", surface: "Brand Kit + legal", sceneCount: 4,
      tagline: "Locale packs, mandatory disclaimers, and tone adaptation." },
    { num: "06", name: "AMP for Email",
      layer: "Channel tech", surface: "Builder + preview", sceneCount: 4,
      tagline: "Interactive AMP modules with static fallback in one publish." },
    { num: "07", name: "Mailchimp Shield (governance suite)",
      layer: "Governance", surface: "Workspace admin", sceneCount: 4,
      tagline: "Policy packs, redaction, approvals — before anything ships." },
    { num: "08", name: "Cross-Domain Conversational Agent",
      layer: "AI 2.0", surface: "MCP + partners", sceneCount: 4,
      tagline: "Same Freddie brain in Mailchimp, store, and helpdesk contexts." }
  ],

  scenePayoffs: {
    "s2-menu": "Phase 2 is where sending intelligence compounds — orchestration, feedback loops, and governance.",
    "s2-flowintro": "After Phase 1 creative depth, Phase 2 closes the loop from live performance to compliant send.",
    "s2-flowzen": "All eight capabilities interlock: orchestrate → personalize → localize → govern → extend.",
    "s2-terminal": "Mailchimp wins on send-time truth — not just prettier templates."
  }
};
