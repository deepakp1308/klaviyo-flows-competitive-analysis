#!/usr/bin/env python3
"""Generate NUNI Template Analysis tab for unified-builder-workflow-health.html."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "unified-builder-workflow-health.html"
START = "<!-- TEMPLATE_ANALYSIS_START -->"
END = "<!-- TEMPLATE_ANALYSIS_END -->"


def panel() -> str:
    return """
<!-- TEMPLATE_ANALYSIS_START -->
<div id="panel-templates" class="tab-panel">
<h1>NUNI / New Builder Template Analysis</h1>
<p class="subtitle">Named template adoption, holiday/seasonal usage, catalog dead weight, VoC gaps, and Klaviyo/Canva competitive coverage &middot; New Builder (NUNI) scope &middot; May 2026</p>

<div class="meta-box">
  <div class="meta-item"><strong>Catalog:</strong> <code>mailchimp.gallery_templates</code> &mdash; 709 named predesigned templates (Christmas, Boutique, Art Newsletter, etc.)</div>
  <div class="meta-item"><strong>Usage (named templates):</strong> <code>bi_reporting.emails_bulk</code> &rarr; <code>user_template_id</code> joined to gallery catalog (actual template SKU per send)</div>
  <div class="meta-item"><strong>Usage (layout skeletons):</strong> <code>emails_bulk.template_id</code> &rarr; <code>mailchimp.templates</code> (1 Column, Sell Products, etc.) &mdash; separate system, dominates volume</div>
  <div class="meta-item"><strong>Paid base:</strong> 1,064,868 customers (Apr 2026, MRR &gt; 0) &middot; HVC = $299+/mo (76,391)</div>
  <div class="meta-item"><strong>VoC:</strong> unitQ Template Management dissatisfaction (+167% YoY) + Builder Workflow Health themes</div>
</div>

<div class="summary-bar">
  <div class="summary-card"><div class="num">709</div><div class="label">Named gallery templates in catalog</div></div>
  <div class="summary-card"><div class="num">388</div><div class="label">Templates with any paid usage (12mo)</div></div>
  <div class="summary-card"><div class="num">321</div><div class="label">Templates with zero paid usage</div></div>
  <div class="summary-card"><div class="num">2.1%</div><div class="label">Paid customers using any named gallery template</div></div>
</div>

<div class="bundle-box" style="background:#fef3c7;border-color:#92400E;">
  <h3>Read this first &mdash; two different &ldquo;template&rdquo; systems</h3>
  <p style="font-size:9pt;line-height:1.55;margin:0;">
    The prior analysis reported &ldquo;79% use paid gallery template&rdquo; from activity <em>flags</em> &mdash; that is not the same as the 709 named designs (Christmas, Halloween, Boutique). In practice:
    <strong>(A) Layout skeletons</strong> (<code>template_id</code> &rarr; 1 Column, Sell Products, Postcard) drive <strong>~87% of paid sending</strong>.
    <strong>(B) Named gallery templates</strong> (<code>user_template_id</code> &rarr; Let It Snow, Art Newsletter) reach only <strong>22,023 paid customers (2.1%)</strong>.
    Top named template = <strong>Event by Jon Hicks at 0.26%</strong> of paid base. This tab reports actual template names and adoption.
  </p>
</div>

<div class="bundle-box">
  <h3>Analysis 1 &mdash; Three synthesis insights (What customers actually use)</h3>
  <ol style="font-size:9pt;line-height:1.55;margin-left:18px;">
    <li><strong>Named gallery templates are barely adopted.</strong> 388/709 have any paid usage; top template (Event by Jon Hicks) = 2,753 customers (0.26%). Most paid senders use generic layout skeletons, not themed gallery designs.</li>
    <li><strong>Holiday catalog is wide but shallow on usage.</strong> 148 holiday templates exist; only 91 saw paid sends. Halloween: 19 templates, 136 paid users total. Christmas: 36 templates, 2,024 users &mdash; concentrated in Let It Snow (501), Giftgiving (392), Snowy Fields (314).</li>
    <li><strong>321 templates are catalog dead weight</strong> (45% of gallery): entire categories at zero &mdash; RSS-To-Email (13), Real Estate (5), Functional (5), Entertainment (4), Technology (29/30 unused).</li>
  </ol>
</div>

<h2>1. Top 50 Named Gallery Templates (Last 12 Months, Paid Customers)</h2>
<p style="font-size:8.5pt;color:#555;margin-bottom:8px;">From <code>gallery_templates</code> joined on <code>emails_bulk.user_template_id</code>. These are the actual predesigned templates customers pick by name.</p>
<table class="detail-table targeting-table">
  <thead><tr><th>#</th><th>Template name</th><th>Category</th><th>Subcategory</th><th>Paid users</th><th>% of paid base</th><th>Campaigns</th><th>Lifecycle use case</th><th>12mo traction</th></tr></thead>
  <tbody>
    <tr><td>1</td><td><strong>Event by Jon Hicks</strong></td><td>Events</td><td>&mdash;</td><td>2,753</td><td>0.26%</td><td>26,904</td><td>Event invitation / RSVP broadcast</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>2</td><td><strong>Boutique</strong></td><td>E-commerce</td><td>&mdash;</td><td>2,129</td><td>0.20%</td><td>33,426</td><td>Product showcase / boutique retail promo</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>3</td><td><strong>Art Newsletter</strong></td><td>Newsletters</td><td>&mdash;</td><td>1,750</td><td>0.16%</td><td>30,037</td><td>Recurring content / creative newsletter</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>4</td><td><strong>Fall Colors</strong></td><td>Holiday</td><td>Autumn</td><td>1,470</td><td>0.14%</td><td>13,343</td><td>Autumn seasonal promo</td><td><span style="color:#166534;">Gaining</span> (+18% users H2)</td></tr>
    <tr><td>5</td><td><strong>Wide</strong></td><td>Stationery</td><td>&mdash;</td><td>1,280</td><td>0.12%</td><td>20,029</td><td>General announcement / letter layout</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>6</td><td><strong>Appointment Reminder</strong></td><td>Notifications</td><td>&mdash;</td><td>1,215</td><td>0.11%</td><td>23,190</td><td>Appointment / booking reminder</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>7</td><td><strong>reconfirm</strong></td><td>&mdash;</td><td>&mdash;</td><td>1,058</td><td>0.10%</td><td>1,225</td><td>Re-confirmation / opt-in utility</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>8</td><td><strong>Invitation by Terris Kremer</strong></td><td>Events</td><td>&mdash;</td><td>888</td><td>0.08%</td><td>15,506</td><td>Event invitation</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>9</td><td><strong>Invitation by Jon Hicks</strong></td><td>Events</td><td>&mdash;</td><td>670</td><td>0.06%</td><td>10,472</td><td>Event invitation</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>10</td><td><strong>Sophisticated</strong></td><td>E-commerce</td><td>&mdash;</td><td>594</td><td>0.06%</td><td>11,675</td><td>Premium product promo</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>11</td><td><strong>Soft</strong></td><td>E-commerce</td><td>&mdash;</td><td>581</td><td>0.05%</td><td>11,492</td><td>Soft-tone product promo</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>12</td><td><strong>Hero Image</strong></td><td>E-commerce</td><td>&mdash;</td><td>540</td><td>0.05%</td><td>9,187</td><td>Hero-led product sale</td><td><span style="color:#166534;">Gaining</span></td></tr>
    <tr><td>13</td><td><strong>Postcard</strong></td><td>Newsletters</td><td>&mdash;</td><td>507</td><td>0.05%</td><td>5,025</td><td>Short-form newsletter</td><td><span style="color:#B91C1C;">Losing</span></td></tr>
    <tr><td>14</td><td><strong>Let It Snow</strong></td><td>Holiday</td><td>Christmas</td><td>501</td><td>0.05%</td><td>1,269</td><td>Christmas holiday promo</td><td><span style="color:#166534;">Gaining</span> (+1,860% users H2 &mdash; seasonal)</td></tr>
    <tr><td>15</td><td><strong>Sale Announcement</strong></td><td>E-commerce</td><td>&mdash;</td><td>487</td><td>0.05%</td><td>5,951</td><td>Sale / discount blast</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>16</td><td><strong>Newsletter by Terris Kremer</strong></td><td>Newsletters</td><td>&mdash;</td><td>453</td><td>0.04%</td><td>7,535</td><td>Recurring newsletter</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>17</td><td><strong>Pop-up</strong></td><td>Newsletters</td><td>&mdash;</td><td>422</td><td>0.04%</td><td>9,609</td><td>Pop-up event / flash promo</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>18</td><td><strong>Flyer</strong></td><td>E-commerce</td><td>&mdash;</td><td>397</td><td>0.04%</td><td>11,077</td><td>Promotional flyer</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>19</td><td><strong>Giftgiving</strong></td><td>Holiday</td><td>Christmas</td><td>392</td><td>0.04%</td><td>3,978</td><td>Christmas gift promo</td><td><span style="color:#166534;">Gaining</span> (+148% users H2)</td></tr>
    <tr><td>20</td><td><strong>Oceanic</strong></td><td>Newsletters</td><td>&mdash;</td><td>375</td><td>0.04%</td><td>8,237</td><td>Newsletter with visual hero</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>21</td><td><strong>Contrast</strong></td><td>E-commerce</td><td>&mdash;</td><td>373</td><td>0.04%</td><td>7,510</td><td>High-contrast product grid</td><td><span style="color:#B91C1C;">Losing</span></td></tr>
    <tr><td>22</td><td><strong>Nature by 45Royale</strong></td><td>Newsletters</td><td>&mdash;</td><td>363</td><td>0.03%</td><td>4,989</td><td>Nature-themed newsletter</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>23</td><td><strong>Hero Card</strong></td><td>E-commerce</td><td>&mdash;</td><td>338</td><td>0.03%</td><td>4,340</td><td>Card-style product feature</td><td><span style="color:#166534;">Gaining</span></td></tr>
    <tr><td>24</td><td><strong>Monochromic</strong></td><td>E-commerce</td><td>&mdash;</td><td>328</td><td>0.03%</td><td>4,714</td><td>Minimal mono product layout</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>25</td><td><strong>Snowy Fields</strong></td><td>Holiday</td><td>Christmas</td><td>314</td><td>0.03%</td><td>684</td><td>Christmas winter scene promo</td><td><span style="color:#166534;">Gaining</span> (+1,665% users H2 &mdash; seasonal)</td></tr>
    <tr><td>26</td><td><strong>Competition Invitation</strong></td><td>Events</td><td>&mdash;</td><td>297</td><td>0.03%</td><td>2,120</td><td>Contest / competition invite</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>27</td><td><strong>Title Bar</strong></td><td>Newsletters</td><td>&mdash;</td><td>295</td><td>0.03%</td><td>6,320</td><td>Header-led newsletter</td><td><span style="color:#B91C1C;">Losing</span></td></tr>
    <tr><td>28</td><td><strong>GDPR Subscriber Alert</strong></td><td>Subscriber Alerts</td><td>&mdash;</td><td>278</td><td>0.03%</td><td>5,034</td><td>Compliance / consent alert</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>29</td><td><strong>Elegant</strong></td><td>Newsletters</td><td>&mdash;</td><td>276</td><td>0.03%</td><td>5,563</td><td>Elegant newsletter layout</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>30</td><td><strong>Color Box</strong></td><td>E-commerce</td><td>&mdash;</td><td>255</td><td>0.02%</td><td>5,270</td><td>Color-block product promo</td><td><span style="color:#166534;">Gaining</span></td></tr>
    <tr><td>31</td><td><strong>Outdoor Sports</strong></td><td>Newsletters</td><td>&mdash;</td><td>253</td><td>0.02%</td><td>4,000</td><td>Sports / outdoor newsletter</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>32</td><td><strong>New Collection</strong></td><td>E-commerce</td><td>&mdash;</td><td>251</td><td>0.02%</td><td>7,184</td><td>New product drop announcement</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>33</td><td><strong>Bold</strong></td><td>Newsletters</td><td>&mdash;</td><td>245</td><td>0.02%</td><td>3,084</td><td>Bold-type newsletter</td><td><span style="color:#B91C1C;">Losing</span></td></tr>
    <tr><td>34</td><td><strong>Vignelli</strong></td><td>Newsletters</td><td>&mdash;</td><td>239</td><td>0.02%</td><td>5,590</td><td>Design-forward newsletter</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>35</td><td><strong>Rest &amp; Relaxation</strong></td><td>Newsletters</td><td>&mdash;</td><td>231</td><td>0.02%</td><td>5,977</td><td>Wellness / lifestyle newsletter</td><td><span style="color:#B91C1C;">Losing</span></td></tr>
    <tr><td>36</td><td><strong>Subtle</strong></td><td>E-commerce</td><td>&mdash;</td><td>229</td><td>0.02%</td><td>6,816</td><td>Subtle product promo</td><td><span style="color:#B91C1C;">Losing</span></td></tr>
    <tr><td>37</td><td><strong>Monthly Contest</strong></td><td>E-commerce</td><td>&mdash;</td><td>209</td><td>0.02%</td><td>2,740</td><td>Recurring contest promo</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>38</td><td><strong>Caribou Christmas</strong></td><td>Holiday</td><td>Christmas</td><td>207</td><td>0.02%</td><td>430</td><td>Christmas themed promo</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>39</td><td><strong>Neapolitan</strong></td><td>Newsletters</td><td>&mdash;</td><td>200</td><td>0.02%</td><td>2,444</td><td>Multi-section newsletter</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>40</td><td><strong>Postcard</strong> (Photography)</td><td>Photography</td><td>&mdash;</td><td>194</td><td>0.02%</td><td>2,302</td><td>Photo portfolio postcard</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>41</td><td><strong>Multiple Event</strong></td><td>Events</td><td>&mdash;</td><td>191</td><td>0.02%</td><td>2,596</td><td>Multi-event calendar invite</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>42</td><td><strong>Colorfield</strong></td><td>Newsletters</td><td>&mdash;</td><td>190</td><td>0.02%</td><td>2,701</td><td>Color-block newsletter</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>43</td><td><strong>Gift Giving Snowmen</strong></td><td>Holiday</td><td>Christmas</td><td>190</td><td>0.02%</td><td>356</td><td>Christmas gift promo</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>44</td><td><strong>Ticket</strong></td><td>Events</td><td>&mdash;</td><td>184</td><td>0.02%</td><td>1,766</td><td>Ticketing / admission event</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>45</td><td><strong>Minimal</strong></td><td>Newsletters</td><td>&mdash;</td><td>173</td><td>0.02%</td><td>3,435</td><td>Minimal newsletter</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>46</td><td><strong>Event by Veerle Pieters</strong></td><td>Events</td><td>&mdash;</td><td>169</td><td>0.02%</td><td>853</td><td>Event invitation</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>47</td><td><strong>SurveyMonkey Basic</strong></td><td>Integrations</td><td>&mdash;</td><td>167</td><td>0.02%</td><td>1,487</td><td>Survey invitation</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>48</td><td><strong>Independence Rocket</strong></td><td>Holiday</td><td>4th of July</td><td>166</td><td>0.02%</td><td>447</td><td>July 4th promo</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>49</td><td><strong>Recipe by 45Royale</strong></td><td>Newsletters</td><td>&mdash;</td><td>161</td><td>0.02%</td><td>2,620</td><td>Recipe / food newsletter</td><td><span style="color:#555;">Flat</span></td></tr>
    <tr><td>50</td><td><strong>Member Welcome</strong></td><td>E-commerce</td><td>&mdash;</td><td>147</td><td>0.01%</td><td>4,308</td><td>Membership welcome (single send)</td><td><span style="color:#555;">Flat</span></td></tr>
  </tbody>
</table>

<h2>2. Holiday &amp; Seasonal Named Templates (What You Asked For)</h2>
<p style="font-size:8.5pt;color:#555;">Christmas, Halloween, Valentine&rsquo;s, Thanksgiving, etc. &mdash; actual template names and paid adoption.</p>

<h3>By holiday subcategory (aggregate)</h3>
<table class="detail-table targeting-table">
  <thead><tr><th>Holiday</th><th>Templates in catalog</th><th>Paid users (12mo)</th><th>% of paid base</th><th>Top template</th><th>Verdict</th></tr></thead>
  <tbody>
    <tr><td><strong>Autumn</strong></td><td>1</td><td>1,470</td><td>0.14%</td><td>Fall Colors (1,470)</td><td>Only autumn template; actually used</td></tr>
    <tr><td><strong>Christmas</strong></td><td>36</td><td>2,024</td><td>0.19%</td><td>Let It Snow (501), Giftgiving (392), Snowy Fields (314)</td><td><span style="color:#166534;">Gaining</span> seasonally; 25 Christmas templates near-zero usage</td></tr>
    <tr><td><strong>Valentine&rsquo;s Day</strong></td><td>15</td><td>319</td><td>0.03%</td><td>XO (87), Roses (82), Whale You Be Mine? (50)</td><td>Underused vs 15-template catalog</td></tr>
    <tr><td><strong>Halloween</strong></td><td>19</td><td>136</td><td>0.01%</td><td>Spooky Night (79), Floating Skulls (40)</td><td style="color:#B91C1C;"><strong>Dead catalog</strong> &mdash; 19 templates, 0.01% adoption</td></tr>
    <tr><td><strong>Thanksgiving</strong></td><td>14</td><td>179</td><td>0.02%</td><td>Golden Fields (71), Falling Leaves (15)</td><td>Near-zero despite 14 templates</td></tr>
    <tr><td><strong>4th of July</strong></td><td>6</td><td>325</td><td>0.03%</td><td>Independence Rocket (166), Tricolor Banners (118)</td><td>Moderate; concentrated in 2 templates</td></tr>
    <tr><td><strong>New Year</strong></td><td>12</td><td>72</td><td>0.01%</td><td>Golden Bubbly (16)</td><td>12 templates, minimal traction</td></tr>
    <tr><td><strong>Easter</strong></td><td>9</td><td>12</td><td>&lt;0.01%</td><td>Easter Crosses 1A (2)</td><td style="color:#B91C1C;">Zero meaningful adoption</td></tr>
  </tbody>
</table>

<h3>Individual holiday templates (top by subcategory)</h3>
<table class="detail-table targeting-table">
  <thead><tr><th>Template name</th><th>Holiday</th><th>Paid users</th><th>% paid base</th><th>12mo traction</th></tr></thead>
  <tbody>
    <tr><td><strong>Fall Colors</strong></td><td>Autumn</td><td>1,470</td><td>0.14%</td><td>Gaining</td></tr>
    <tr><td><strong>Let It Snow</strong></td><td>Christmas</td><td>501</td><td>0.05%</td><td>Gaining (seasonal spike Nov&ndash;Apr)</td></tr>
    <tr><td><strong>Giftgiving</strong></td><td>Christmas</td><td>392</td><td>0.04%</td><td>Gaining</td></tr>
    <tr><td><strong>Snowy Fields</strong></td><td>Christmas</td><td>314</td><td>0.03%</td><td>Gaining (seasonal)</td></tr>
    <tr><td><strong>Caribou Christmas</strong></td><td>Christmas</td><td>207</td><td>0.02%</td><td>Flat</td></tr>
    <tr><td><strong>Gift Giving Snowmen</strong></td><td>Christmas</td><td>190</td><td>0.02%</td><td>Flat</td></tr>
    <tr><td><strong>Independence Rocket</strong></td><td>4th of July</td><td>166</td><td>0.02%</td><td>Flat</td></tr>
    <tr><td><strong>XO</strong></td><td>Valentine&rsquo;s</td><td>87</td><td>0.01%</td><td>Flat</td></tr>
    <tr><td><strong>Roses</strong></td><td>Valentine&rsquo;s</td><td>82</td><td>0.01%</td><td>Flat</td></tr>
    <tr><td><strong>Spooky Night</strong></td><td>Halloween</td><td>79</td><td>0.01%</td><td>Flat</td></tr>
    <tr><td><strong>Golden Fields</strong></td><td>Thanksgiving</td><td>71</td><td>0.01%</td><td>Flat</td></tr>
    <tr><td><strong>Whale You Be Mine?</strong></td><td>Valentine&rsquo;s</td><td>50</td><td>&lt;0.01%</td><td>Flat</td></tr>
    <tr><td><strong>Floating Skulls</strong></td><td>Halloween</td><td>40</td><td>&lt;0.01%</td><td>Flat</td></tr>
    <tr><td><strong>Heart Of Flowers</strong></td><td>Valentine&rsquo;s</td><td>39</td><td>&lt;0.01%</td><td>Flat</td></tr>
    <tr><td><strong>Christmas Postcard</strong></td><td>Christmas</td><td>9</td><td>&lt;0.01%</td><td style="color:#B91C1C;">Near-zero despite being in catalog since 2009</td></tr>
    <tr><td><strong>Thanksgiving</strong></td><td>Thanksgiving</td><td>7</td><td>&lt;0.01%</td><td style="color:#B91C1C;">Named template essentially unused</td></tr>
  </tbody>
</table>

<div class="bundle-box">
  <h3>Analysis 2 &mdash; Three synthesis insights (Holiday templates)</h3>
  <ol style="font-size:9pt;line-height:1.55;margin-left:18px;">
    <li><strong>We have 148 holiday templates but customers use ~5.</strong> Fall Colors + top 4 Christmas templates account for most holiday sends. 57/148 holiday templates had zero paid usage in 12 months.</li>
    <li><strong>Halloween is a catalog failure:</strong> 19 templates, 136 total paid users (0.01% of base). Customers aren&rsquo;t finding or choosing these &mdash; likely buried in gallery browse.</li>
    <li><strong>Christmas templates spike seasonally (Let It Snow: 25 users H1 &rarr; 490 H2)</strong> but absolute numbers remain tiny vs layout skeletons. Seasonal investment ROI is low unless paired with goal-based surfacing at send time.</li>
  </ol>
</div>

<h2>3. Layout Skeleton Templates (What Most Paid Customers Actually Use)</h2>
<p style="font-size:8.5pt;color:#555;">These are <em>not</em> in the 709 gallery catalog. They are structural layouts from <code>mailchimp.templates</code> joined via <code>template_id</code>. This is why &ldquo;79% paid gallery&rdquo; from activity flags was misleading.</p>
<table class="detail-table targeting-table">
  <thead><tr><th>Layout template name</th><th>Paid users (12mo)</th><th>% of paid base</th><th>Campaigns</th><th>What it is</th></tr></thead>
  <tbody>
    <tr><td><strong>1:2 columns:3 columns</strong></td><td>318,963</td><td>29.95%</td><td>7.2M</td><td>Multi-column general layout</td></tr>
    <tr><td><strong>Postcard - Old2</strong></td><td>147,823</td><td>13.88%</td><td>2.6M</td><td>Legacy postcard layout</td></tr>
    <tr><td><strong>1 Column</strong></td><td>94,417</td><td>8.87%</td><td>2.8M</td><td>Single-column basic layout</td></tr>
    <tr><td><strong>Sell Products</strong></td><td>53,661</td><td>5.04%</td><td>1.2M</td><td>E-commerce product grid skeleton</td></tr>
    <tr><td><strong>Make an Announcement</strong></td><td>41,444</td><td>3.89%</td><td>733K</td><td>Announcement layout</td></tr>
    <tr><td><strong>Right Column</strong></td><td>34,677</td><td>3.26%</td><td>339K</td><td>Sidebar-right layout</td></tr>
    <tr><td><strong>Left Column</strong></td><td>31,722</td><td>2.98%</td><td>291K</td><td>Sidebar-left layout</td></tr>
    <tr><td><strong>Simple Text</strong></td><td>23,597</td><td>2.22%</td><td>646K</td><td>Plain text email</td></tr>
    <tr><td><strong>Tell A Story</strong></td><td>17,729</td><td>1.66%</td><td>284K</td><td>Storytelling layout</td></tr>
    <tr><td><strong>Educate</strong></td><td>11,862</td><td>1.11%</td><td>170K</td><td>Educational content layout</td></tr>
    <tr><td><strong>Follow Up</strong></td><td>11,164</td><td>1.05%</td><td>148K</td><td>Follow-up message layout</td></tr>
  </tbody>
</table>
<p class="note">Top 3 layout skeletons alone = <strong>52.7%</strong> of paid base. Named gallery templates combined = <strong>2.1%</strong>. Product strategy must address both layers.</p>

<h2>4. Catalog Health: Category Adoption &amp; Dead Weight</h2>
<table class="detail-table targeting-table">
  <thead><tr><th>Category</th><th>Templates in catalog</th><th>Templates with paid usage</th><th>Templates unused</th><th>Paid users (any template in category)</th><th>Insight</th></tr></thead>
  <tbody>
    <tr><td><strong>Newsletters</strong></td><td>96</td><td>69</td><td>27</td><td>10,565</td><td>Largest usage; Art Newsletter leads</td></tr>
    <tr><td><strong>E-commerce</strong></td><td>47</td><td>32</td><td>15</td><td>9,685</td><td>Boutique, Sophisticated, Hero Image top</td></tr>
    <tr><td><strong>Events</strong></td><td>29</td><td>26</td><td>3</td><td>7,458</td><td>Event by Jon Hicks dominates</td></tr>
    <tr><td><strong>Holiday</strong></td><td>148</td><td>91</td><td>57</td><td>5,271</td><td>148 templates, concentrated in 5&ndash;10 names</td></tr>
    <tr><td><strong>Stationery</strong></td><td>16</td><td>11</td><td>5</td><td>2,504</td><td>Wide is primary</td></tr>
    <tr><td><strong>Notifications</strong></td><td>3</td><td>3</td><td>0</td><td>2,441</td><td>Appointment Reminder carries category</td></tr>
    <tr><td><strong>Nonprofit</strong></td><td>21</td><td>8</td><td>13</td><td>20</td><td style="color:#B91C1C;">21 templates, 20 paid users total</td></tr>
    <tr><td><strong>Technology</strong></td><td>30</td><td>1</td><td>29</td><td>1</td><td style="color:#B91C1C;">97% dead catalog</td></tr>
    <tr><td><strong>Sports</strong></td><td>51</td><td>18</td><td>33</td><td>58</td><td>Vertical d&eacute;cor, near-zero adoption</td></tr>
    <tr><td><strong>RSS-To-Email</strong></td><td>13</td><td>0</td><td>13</td><td>0</td><td style="color:#B91C1C;">100% unused</td></tr>
    <tr><td><strong>Real Estate</strong></td><td>5</td><td>0</td><td>5</td><td>0</td><td style="color:#B91C1C;">100% unused</td></tr>
    <tr><td><strong>AutoConnect</strong></td><td>22</td><td>3</td><td>19</td><td>7</td><td>Integration templates barely used</td></tr>
  </tbody>
</table>
<p class="note"><strong>Zero new gallery templates added since July 2019.</strong> Catalog is frozen; FY27 lifecycle library would be net-new SKUs, not refreshes of existing holiday skins.</p>

<h2>5. Segment Cuts: HVC vs Sub-$299 on Top Named Templates</h2>
<table class="detail-table targeting-table">
  <thead><tr><th>Template name</th><th>HVC ($299+) users</th><th>Sub-$299 users</th><th>HVC share of template users</th><th>Insight</th></tr></thead>
  <tbody>
    <tr><td>Event by Jon Hicks</td><td>288</td><td>2,497</td><td>10.5%</td><td>Mass-market event template</td></tr>
    <tr><td>Boutique</td><td>277</td><td>1,892</td><td>13.0%</td><td>E-com d&eacute;cor; sub-$299 heavy</td></tr>
    <tr><td>Art Newsletter</td><td>190</td><td>1,586</td><td>10.9%</td><td>Newsletter staple for SMB</td></tr>
    <tr><td>Fall Colors</td><td>149</td><td>1,348</td><td>10.1%</td><td>Seasonal; broad SMB</td></tr>
    <tr><td>reconfirm</td><td>280</td><td>824</td><td>26.5%</td><td>Utility template; HVC over-indexes</td></tr>
    <tr><td>Let It Snow</td><td>64</td><td>448</td><td>12.8%</td><td>Christmas; SMB seasonal</td></tr>
    <tr><td>Sale Announcement</td><td>69</td><td>424</td><td>14.2%</td><td>Promo; moderate HVC</td></tr>
  </tbody>
</table>
<p class="note">HVC customers are <strong>not</strong> driving named gallery adoption (10&ndash;14% of template users). They use layout skeletons + custom saved templates instead.</p>

<h2>6. New Paid Customers: Top Named Templates in First 30 Days</h2>
<p style="font-size:8.5pt;color:#555;">Paid customers who converted since May 2025; gallery template usage in first 30 days of paid tenure.</p>
<table class="detail-table targeting-table">
  <thead><tr><th>Template name</th><th>Category</th><th>New paid users</th><th>Campaigns in first 30d</th><th>Lifecycle moment</th></tr></thead>
  <tbody>
    <tr><td><strong>reconfirm</strong></td><td>Utility</td><td>198</td><td>198</td><td>Compliance / list hygiene on conversion</td></tr>
    <tr><td><strong>Art Newsletter</strong></td><td>Newsletters</td><td>110</td><td>235</td><td>First newsletter send</td></tr>
    <tr><td><strong>Boutique</strong></td><td>E-commerce</td><td>106</td><td>310</td><td>First product promo</td></tr>
    <tr><td><strong>Event by Jon Hicks</strong></td><td>Events</td><td>93</td><td>195</td><td>First event invite</td></tr>
    <tr><td><strong>Wide</strong></td><td>Stationery</td><td>54</td><td>108</td><td>General first send</td></tr>
    <tr><td><strong>Fall Colors</strong></td><td>Holiday/Autumn</td><td>53</td><td>97</td><td>Seasonal first send</td></tr>
    <tr><td><strong>Appointment Reminder</strong></td><td>Notifications</td><td>41</td><td>77</td><td>Service business first send</td></tr>
    <tr><td><strong>Sale Announcement</strong></td><td>E-commerce</td><td>22</td><td>45</td><td>First sale blast</td></tr>
    <tr><td><strong>GDPR Subscriber Alert</strong></td><td>Compliance</td><td>12</td><td>47</td><td>EU compliance on signup</td></tr>
  </tbody>
</table>
<p class="note">No Halloween, Valentine&rsquo;s, or Christmas templates in top first-30-day picks except Fall Colors (seasonal timing). New paid customers start with utility + newsletter + e-com basics.</p>

<h2>7. VoC-Requested Templates Not in Catalog (or Not Surfaced)</h2>
<p style="font-size:8.5pt;color:#555;">unitQ category <strong>Template Management::Dissatisfaction With Template Quality And Availability</strong> (+167% YoY) + Builder Workflow Health. Mapped to specific missing template <em>types</em>, not flags.</p>
<table class="detail-table targeting-table">
  <thead><tr><th>Requested template type</th><th>Example Klaviyo/Canva has</th><th>Mailchimp named template today</th><th>Gap</th></tr></thead>
  <tbody>
    <tr><td><strong>Abandoned cart email series</strong></td><td>Klaviyo: browse/cart/checkout abandon templates</td><td>No named template; Sell Products layout only</td><td style="color:#B91C1C;">Missing lifecycle series</td></tr>
    <tr><td><strong>Welcome series (3&ndash;5 emails)</strong></td><td>Klaviyo: welcome flow template set</td><td>Member Welcome (147 users) &mdash; single send only</td><td style="color:#B91C1C;">Missing multi-email kit</td></tr>
    <tr><td><strong>Win-back / re-engagement</strong></td><td>Klaviyo: win-back, sunset templates</td><td>Follow Up layout skeleton (not gallery)</td><td style="color:#B91C1C;">Missing</td></tr>
    <tr><td><strong>B2B / ProServ newsletter</strong></td><td>Canva: 1,700+ vertical newsletter designs</td><td>Nonprofit: 20 paid users; no ProServ gallery</td><td style="color:#B91C1C;">Missing vertical</td></tr>
    <tr><td><strong>Post-purchase / review request</strong></td><td>Klaviyo: post-purchase, review request</td><td>No named template</td><td style="color:#B91C1C;">Missing</td></tr>
    <tr><td><strong>Goal-filtered browse</strong> (not category d&eacute;cor)</td><td>Klaviyo: filter by welcome, promo, lifecycle</td><td>Category browse: Holiday, E-com, etc.</td><td style="color:#B91C1C;">Discoverability gap</td></tr>
    <tr><td><strong>Store-connected product blocks</strong></td><td>Klaviyo: live SKU blocks in templates</td><td>Boutique, Hero Image &mdash; static layouts</td><td style="color:#92400E;">Partial</td></tr>
    <tr><td><strong>SMS/WhatsApp matching templates</strong></td><td>Klaviyo: multi-channel canvas templates</td><td>Email-only gallery (709 templates)</td><td style="color:#B91C1C;">Missing channel parity</td></tr>
  </tbody>
</table>

<div class="bundle-box">
  <h3>Analysis 3 &mdash; Three synthesis insights (VoC &amp; competitive gaps)</h3>
  <ol style="font-size:9pt;line-height:1.55;margin-left:18px;">
    <li><strong>Customers aren&rsquo;t asking for more Halloween skins.</strong> They want lifecycle-named templates (Abandoned Cart, Welcome Series, Win-Back) that Klaviyo ships as goal-filtered sets. We have 148 holiday d&eacute;cor templates and zero abandoned-cart named templates.</li>
    <li><strong>Canva wins on vertical newsletter breadth; Klaviyo wins on lifecycle depth.</strong> Mailchimp&rsquo;s named gallery sits between them on d&eacute;cor (Boutique, Art Newsletter) but loses on both goal-filtering and multi-step series.</li>
    <li><strong>321 zero-usage templates create findability noise.</strong> Retire or hide dead SKUs (Technology, RSS, Real Estate, 57 holiday) before adding FY27 lifecycle library &mdash; otherwise new templates get buried too.</li>
  </ol>
</div>

<h2>8. Competitive Gap: Klaviyo &amp; Canva vs Mailchimp Named Templates</h2>
<table class="detail-table targeting-table">
  <thead><tr><th>Template capability</th><th>Klaviyo</th><th>Canva</th><th>Mailchimp (this analysis)</th><th>Specific gap</th></tr></thead>
  <tbody>
    <tr><td>Named templates with measurable adoption</td><td>160+; filtered by lifecycle goal</td><td>1,700+ email newsletters by vertical</td><td>709 catalog; 388 used; top = 0.26% adoption</td><td>Catalog bloat + no goal filter</td></tr>
    <tr><td>Christmas / holiday</td><td>Seasonal + lifecycle holiday flows</td><td>100s of holiday newsletter designs</td><td>36 Christmas templates; Let It Snow = 501 users (0.05%)</td><td>Exists but invisible/unused</td></tr>
    <tr><td>Halloween / Valentine&rsquo;s</td><td>Seasonal campaign templates</td><td>Vertical holiday browse</td><td>Halloween: 19 templates, 136 users total</td><td style="color:#B91C1C;">Catalog without demand</td></tr>
    <tr><td>Newsletter starters</td><td>Welcome, newsletter, digest templates</td><td>1,700+ newsletter templates</td><td>Art Newsletter (1,750 users) leads; 96 in catalog</td><td>Moderate; no goal tag</td></tr>
    <tr><td>E-commerce lifecycle</td><td>Abandoned cart, post-purchase, win-back series</td><td>Product promo designs (manual)</td><td>Boutique, Sale Announcement &mdash; single-send promo only</td><td style="color:#B91C1C;">No lifecycle series</td></tr>
    <tr><td>Universal content blocks</td><td>Reusable blocks across templates</td><td>Brand kits + shared elements</td><td>Template-scoped; UC on Q1&ndash;Q2 roadmap</td><td style="color:#B91C1C;">Portability gap</td></tr>
    <tr><td>Multi-channel templates</td><td>Email + SMS + push in flow canvas</td><td>Email design export only</td><td>709 email gallery templates only</td><td style="color:#B91C1C;">SMS/WhatsApp separate</td></tr>
  </tbody>
</table>

<h2>9. Microsegment Impact (Unified Builder Customer Targeting Clusters)</h2>
<table class="detail-table targeting-table">
  <thead><tr><th>Template action</th><th>Named templates affected / proposed</th><th>Primary clusters</th><th>Expected impact</th></tr></thead>
  <tbody>
    <tr><td>Retire 321 zero-usage SKUs; surface top 50 by adoption</td><td>Hide Technology, RSS, Real Estate, unused Halloween</td><td>C9 High-Friction, C8, C0 Dormant Paid</td><td>Findability fix before net-new design</td></tr>
    <tr><td>Launch lifecycle-named template series</td><td>Abandoned Cart, Welcome (3-email), Win-Back</td><td>C4 Growing-but-Incomplete, C2 High-MRR</td><td>Closes Klaviyo gap; ~34% pack EV to C4</td></tr>
    <tr><td>Seasonal surfacing at send time</td><td>Let It Snow, Fall Colors, Spooky Night triggered by calendar</td><td>C11 Rising-Usage, C1 Reliable Mid-Market</td><td>Activates existing holiday catalog without new SKUs</td></tr>
    <tr><td>B2B/ProServ named gallery</td><td>Consulting Newsletter, SaaS Update, Client Onboarding</td><td>C1, C11, C7 Dormant Free</td><td>Nonprofit template proof: 21 SKUs &rarr; 20 users</td></tr>
    <tr><td>Store-connected Boutique/Hero Image preview</td><td>Upgrade existing e-com named templates with live SKUs</td><td>C4, C2, C12 AI-Ready Mid-Market</td><td>~68% combined cluster EV</td></tr>
  </tbody>
</table>

<hr style="border:none;border-top:3px solid #1a3a5c;margin:28px 0;">

<h2>Executive Summary</h2>
<div class="bundle-box" style="background:#eef2ff;border-color:#1a3a5c;">
  <ol style="font-size:9.5pt;line-height:1.6;margin-left:18px;">
    <li><strong>The 709 named gallery templates are not what most paid customers use.</strong> Only 22,023 paid customers (2.1%) sent from any named gallery template in 12 months. Most use layout skeletons (1 Column, Sell Products) at 30&times; higher adoption.</li>
    <li><strong>You asked for Christmas, Halloween, Valentine&rsquo;s &mdash; here are the numbers:</strong> Let It Snow (501 users), Giftgiving (392), Spooky Night (79), XO (87). Halloween: 19 templates, 136 users total. Holiday catalog is 148 templates wide, ~5 templates deep in actual usage.</li>
    <li><strong>321 templates (45%) have zero paid usage.</strong> Entire categories (RSS, Real Estate, Technology) are dead weight. No new gallery templates since 2019.</li>
    <li><strong>Top named templates:</strong> Event by Jon Hicks (0.26%), Boutique (0.20%), Art Newsletter (0.16%), Fall Colors (0.14%). These are the actual templates with measurable adoption.</li>
    <li><strong>Competitive gap is lifecycle naming, not holiday d&eacute;cor.</strong> Klaviyo ships Abandoned Cart, Welcome Series, Win-Back as named template sets. Mailchimp has Sell Products layout and Member Welcome (147 users). VoC +167% aligns with this gap.</li>
    <li><strong>Recommended sequence:</strong> (1) Hide dead catalog, (2) Surface top 50 + seasonal triggers, (3) Ship lifecycle-named series Q2, (4) B2B/ProServ gallery. Do not add more Halloween skins.</li>
  </ol>
</div>

<h3>What to do next</h3>
<table class="detail-table targeting-table">
  <thead><tr><th>Priority</th><th>Action</th><th>Why</th></tr></thead>
  <tbody>
    <tr><td><strong>P0</strong></td><td>Hide/retire 321 zero-usage named templates from gallery browse</td><td>45% dead catalog causes &ldquo;can&rsquo;t find the right template&rdquo; VoC</td></tr>
    <tr><td><strong>P0</strong></td><td>Add goal-based filters: Welcome, Promo, Abandoned Cart, Win-Back, Seasonal</td><td>Matches Klaviyo browse; maps to lifecycle not d&eacute;cor</td></tr>
    <tr><td><strong>P1</strong></td><td>Calendar-triggered seasonal surfacing (Let It Snow in Nov, Spooky Night in Oct)</td><td>Activates existing holiday templates without new design</td></tr>
    <tr><td><strong>P1</strong></td><td>Ship 12-template ecommerce lifecycle library with named SKUs (Q2 roadmap)</td><td>Closes #1 Klaviyo gap; C4 cluster EV</td></tr>
    <tr><td><strong>P2</strong></td><td>B2B/ProServ named gallery (not more Nonprofit d&eacute;cor)</td><td>Nonprofit proof: 21 templates &rarr; 20 users</td></tr>
    <tr><td><strong>Measure</strong></td><td>Track <code>user_template_id</code> adoption monthly by template name</td><td>Replace misleading activity flags with SKU-level ranking</td></tr>
  </tbody>
</table>

<p class="note">Analysis regenerated May 26, 2026. Usage from <code>bi_reporting.emails_bulk</code> (template_id + user_template_id joins). Paid base Apr 2026. Traction = H1 (May&ndash;Oct 2025) vs H2 (Nov 2025&ndash;Apr 2026) user counts per template.</p>
</div>
<!-- TEMPLATE_ANALYSIS_END -->
"""


def patch_html(content: str) -> str:
    panel_html = panel().strip()
    if START in content and END in content:
        pre, rest = content.split(START, 1)
        _, post = rest.split(END, 1)
        content = pre + panel_html + post
    else:
        anchor = '<script>\nfunction showPageTab'
        if anchor not in content:
            raise SystemExit("Could not find script anchor in HTML")
        content = content.replace(anchor, panel_html + "\n\n" + anchor)

    content = content.replace(
        '  <a href="#targeting" id="tab-link-targeting" onclick="return showPageTab(\'targeting\')">$21M Customer Targeting</a>\n</div>',
        '  <a href="#targeting" id="tab-link-targeting" onclick="return showPageTab(\'targeting\')">$21M Customer Targeting</a>\n'
        '  <a href="#templates" id="tab-link-templates" onclick="return showPageTab(\'templates\')">NUNI Template Analysis</a>\n</div>',
    )

    content = content.replace(
        "  if (hash === 'targeting' || hash === 'workflow') showPageTab(hash);",
        "  if (hash === 'targeting' || hash === 'workflow' || hash === 'templates') showPageTab(hash);",
    )
    content = content.replace(
        "    if (h === 'targeting' || h === 'workflow') showPageTab(h);",
        "    if (h === 'targeting' || h === 'workflow' || h === 'templates') showPageTab(h);",
    )
    return content


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    HTML.write_text(patch_html(text), encoding="utf-8")
    print(f"Updated {HTML}")


if __name__ == "__main__":
    main()
