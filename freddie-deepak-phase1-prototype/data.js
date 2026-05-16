/* =========================================================================
   Freddie Deepak's Phase 1 Prototype — Mock Data
   v1.0 · May 2026

   Single source-of-truth object tree consumed by every scene.
   - Brand: "Bright Light Co." (a fictional DTC brand consistent with the
     baseline content inventory from ai-email-generator-decomp/docs/09)
   - Email content reuses the "Welcome to the Community" baseline string
   - Memories, connectors, research, MCP token are all plausible
     placeholders kept short enough to fit a scene

   Edit copy here, not inline in scenes (Rule R7: no invented copy in
   scene markup; all visible product copy comes from this file).
   ========================================================================= */

window.FDPX_DATA = {
  brand: {
    name: "Bright Light Co.",
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
    subject: "Welcome to the Community",
    heroLine: "Designed by hand, made for you",
    recipientList: "New email subscribers",
    recipientCount: 2150,
    promoCode: "Welcome guide + first-week bonus",
    focusMetric: "Revenue",
    products: ["Product 1", "Product 2"],
    bodyBlocks: [
      { id: "b1", type: "Header", text: "Bright Light Co." },
      { id: "b2", type: "Hero",    text: "Designed by hand, made for you" },
      { id: "b3", type: "Body",    text: "Welcome to the family. Here's a small thank-you for joining." },
      { id: "b4", type: "Coupon",  text: "WELCOME15 · 15% off your first order" },
      { id: "b5", type: "Body",    text: "We hand-pick every product. Browse the collection at your pace." },
      { id: "b6", type: "CTA",     text: "Shop now" },
      { id: "b7", type: "Footer",  text: "123 Main St, Suite 100, New York, NY 10001 · Unsubscribe" }
    ]
  },

  memories: [
    { id: "m1",  text: "Customers respond best to social-proof framing", category: "Style" },
    { id: "m2",  text: "Tuesday 10am AEST highest engagement",            category: "Cadence" },
    { id: "m3",  text: "Spring Refresh is the launch tag",                category: "Inventory" },
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
  ]
};
