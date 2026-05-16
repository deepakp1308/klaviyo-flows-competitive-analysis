/* =========================================================================
   Freddie Deepak's Phase 1 Prototype — Mock Data
   v1.0 · May 2026

   Single source-of-truth object tree consumed by every scene.
   - Brand: "Stride Athletics" — synthetic demo DTC (see synthetic-demo-pack/)
   - Email narrative aligns with Spring Velocity / Volt Runner campaign copy
   - Memories, connectors, research, MCP token are all plausible
     placeholders kept short enough to fit a scene

   Edit copy here, not inline in scenes (Rule R7: no invented copy in
   scene markup; all visible product copy comes from this file).
   ========================================================================= */

window.FDPX_DATA = {
  brand: {
    name: "Stride Athletics",
    primary: "#017E89",
    accent: "#F4EFE6",
    fontHead: "Means Web",
    fontBody: "Graphik Web",
    voiceProfile: {
      active: "Default",
      available: ["Default", "Holiday", "Launch"]
    },
    intelligence: {
      tone: "warm, confident",
      voice: "first-person plural",
      avoid: "jargon, em-dashes",
      sentenceLength: "8–18 words avg",
      lastScan: "last week"
    },
    staleDraftCount: 12
  },

  email: {
    subject: "Spring Velocity: Volt Runner ships free this week",
    heroLine: "Train in rhythm this spring",
    recipientList: "New email subscribers",
    recipientCount: 2150,
    promoCode: "SPRINGVEL · bundle ship-free + Volt at $128",
    focusMetric: "Revenue",
    products: ["Stride Volt Runner (SA-VOLT-M-001)", "Stride Life Bundle"],
    bodyBlocks: [
      { id: "b1", type: "Header", text: "Stride Athletics" },
      { id: "b2", type: "Hero",    text: "Train in rhythm this spring" },
      { id: "b3", type: "Body",    text: "Spring Velocity is here — Volt Runner ($128), City Pierce Jacket, and the Life Bundle ($198) with free ground shipping through Sunday." },
      { id: "b4", type: "Coupon",  text: "SPRINGVEL · extra savings on bundles + Volt launch" },
      { id: "b5", type: "Body",    text: "Every mile earns its rest: Flow Mat + Sunrise Hood pair with the Volt for recovery days." },
      { id: "b6", type: "CTA",     text: "Shop Spring Velocity" },
      { id: "b7", type: "Footer",  text: "stride-athletics.example.com · Demo addresses only · Unsubscribe" }
    ]
  },

  memories: [
    { id: "m1",  text: "Customers respond best to social-proof framing", category: "Style" },
    { id: "m2",  text: "Tuesday 10am AEST highest engagement",            category: "Cadence" },
    { id: "m3",  text: "Spring Velocity is the hero launch tag",                category: "Inventory" },
    { id: "m4",  text: "Hero CTAs work best in active voice",             category: "Style" },
    { id: "m5",  text: "Single CTA outperforms 2-CTA by 15% CTR",         category: "Performance" },
    { id: "m6",  text: "Audience prefers warmth over urgency",            category: "Brand voice" },
    { id: "m7",  text: "Avoid red on hero CTAs (brand mismatch)",         category: "Style" },
    { id: "m8",  text: "Email subjects under 50 chars perform best",      category: "Performance" },
    { id: "m9",  text: "First-time buyers convert on free shipping",      category: "Audience" },
    { id: "m10", text: "Sunday sends slip 22% — avoid",                   category: "Cadence" },
    { id: "m11", text: "Product photos > illustrations for ecom",         category: "Style" },
    { id: "m12", text: "Re-engagement works best at day 45",              category: "Cadence" }
  ],

  connectors: {
    slack: {
      enabled: true,
      lastSync: "2m ago",
      channel: "#marketing-launches",
      excerpt: "Q3 launch goes live Tuesday · hero copy approved by Sarah"
    },
    drive: {
      enabled: true,
      lastSync: "11m ago",
      excerpt: "Brand guidelines v4.pdf — fonts updated to Graphik 500"
    },
    notion: {
      enabled: true,
      lastSync: "3m ago",
      page: "Q3 launch brief",
      excerpt: "Target: existing customers + warm leads · tone: confident, not pushy"
    },
    zoom:     { enabled: false, lastSync: null, excerpt: null },
    calendar: { enabled: false, lastSync: null, excerpt: null }
  },

  research: {
    depth: "Quick",
    findings: [
      { source: "Q3 2025 email benchmark report",
        insight: "Industry avg open rate for welcome = 47% (your benchmark)" },
      { source: "Reddit r/emailmarketing",
        insight: "Single-CTA welcome emails outperform 2-CTA by ~15% CTR" },
      { source: "Mailchimp internal benchmarks",
        insight: "Top welcome emails reference signup source in first 3 lines" }
    ],
    sourcesIndexed: 12
  },

  mcp: {
    enabled: true,
    token: "mc_live_a8f3b9c2e7d6f1...",
    tokenMasked: "mc_live_••••••••••••f1...",
    lastUsed: "4 minutes ago by Claude 4.5 (Cursor)"
  },

  // The 10 features — used by the menu (S-MENU) and per-feature intros
  features: [
    { num: "01", name: "AI Image Manipulation Suite",
      layer: "AI",     surface: "Design editor",   sceneCount: 6,
      tagline: "Edit images inline. Brush-replace, subject-extract, frame-extend, themed effects." },
    { num: "02", name: "Dream Lab",
      layer: "AI",     surface: "Manual rail",     sceneCount: 5,
      tagline: "Generate high-fidelity branded imagery from prompt + style reference." },
    { num: "03", name: "Conversational Design Editing",
      layer: "AI 2.0", surface: "Chat composer",   sceneCount: 4,
      tagline: "Drive the whole builder from plain English. 'Make the hero more professional.'" },
    { num: "04", name: "Magic Layers",
      layer: "AI 2.0", surface: "Composer attach", sceneCount: 4,
      tagline: "Drop a flat image or PDF. We reconstruct editable layers." },
    { num: "05", name: "Brand Voice 2.0 + Brand Intelligence",
      layer: "AI 2.0", surface: "Brand Kit",       sceneCount: 5,
      tagline: "Save voice profiles. Auto-update old templates to the latest brand." },
    { num: "06", name: "Mailchimp Memory",
      layer: "AI 2.0", surface: "Sidebar",         sceneCount: 5,
      tagline: "AI remembers what works for your team across campaigns." },
    { num: "07", name: "Live-Context Connectors",
      layer: "AI 2.0", surface: "Settings",        sceneCount: 5,
      tagline: "Slack, Drive, Notion, Zoom, Calendar feed live context into the brief." },
    { num: "08", name: "AI Sticker / GIF / Animation",
      layer: "AI",     surface: "Manual rail",     sceneCount: 5,
      tagline: "Branded sticker packs + one-click hero animation." },
    { num: "09", name: "Web Research Integration",
      layer: "AI 2.0", surface: "Strategy panel",  sceneCount: 3,
      tagline: "AI scans the web for competitive + seasonal context before generating." },
    { num: "10", name: "ChatGPT & Claude MCP Bridge",
      layer: "AI 2.0", surface: "Settings",        sceneCount: 3,
      tagline: "Expose Mailchimp as an MCP server. Drive campaigns from external AI clients." }
  ],

  /** Short value lines for the sticky chrome (overrides auto-generated payoff text). */
  scenePayoffs: {
    "s-menu": "Choose any Phase 1 capability—or walk all ten in order for the full story.",
    "s-flowintro": "One path from plan to send: every new AI surface is switched on along the way.",
    "s-flowzen": "All ten extensions compose: connectors, memory, brand voice, design AI, and MCP—together.",
    "s-send-confirm": "Final checklist before ship: channel parity, brand version, and AI traces reviewed.",
    "s-terminal": "You stayed inside Mailchimp for the whole creative loop—no Canva round-trip."
  }
};
