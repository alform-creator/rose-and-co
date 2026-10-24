# Rose & Co — Gifts, Delivery & Real Reviews

The website is published from the \`main\` branch by \`.github/workflows/deploy.yml\`.
The site is regenerated from ZIP archives plus installer scripts on every deploy.

## Interactive tools
- Secret love letter (live envelope preview, add to custom bouquet, or submit an enquiry through WhatsApp)
- Surprise delivery (recipient, phone optional, address, preferred date/daypart, instructions)
- Bouquet recommendation quiz (3 questions → appropriate existing catalogue category)
- Delivery estimator (zone-aware and displays **only confirmed fees**)
- Customer reviews (displays **only approved and genuine entries**)

All functions are provided in **Armenian, Russian and English**. The mobile layout uses the same components.

## Set real shipping rates

Open and edit \`.github/rose-services-data.json\` in GitHub and change \`fee_amd\` for a zone from \`null\` to an actual integer amount after verifying the tariff. Example:
\`"fee_amd": 1500\` would display 1,500 AMD for that zone. This number is **an example**, not an existing Rose & Co rate. \`0\` is an explicitly confirmed free delivery tariff; do not enter zero unless free delivery is actually offered.

Until configured, the site transparently displays "price upon request" and opens a WhatsApp enquiry. Shipping availability and total order prices still need confirmation.

## Publish real reviews

Reviews begin intentionally empty. Do not invent customer testimonials.
Once you have a genuine, permissioned testimonial, add an entry to the \`reviews\` array:

\`\`\`json
{
  "name": "First name or approved display name",
  "rating": 5,
  "quote": {
    "hy": "Authentic Armenian translation",
    "ru": "Authentic Russian translation",
    "en": "Authentic English translation"
  },
  "approved": true
}
\`\`\`

Only use the person's approved display name, do not publish their phone number, and keep written permission for publication. Reviews arriving via WhatsApp **do not publish automatically**, because this is a static GitHub Pages site without a moderation backend.

## Privacy and booking

- Every submission is a WhatsApp enquiry; no forms store names, phone numbers, or messages on GitHub Pages.
- Submission is not a confirmed order, delivery time, or price.
- Preferred surprise-delivery dates cannot be before today; time of day remains subject to business confirmation.
- The builder and new tools preserve original products, localizations, navigation and the existing opening animation.

To update services: \`.github/scripts/install-rose-services.py\`.
To verify automated deployment: GitHub Actions → **Prepare Rose & Co website**, then **pages build and deployment**.
