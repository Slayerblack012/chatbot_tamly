# An Nhiên visual design system

## Brand color rule

The An Nhiên brand palette is a fixed product invariant. Do not change its hues, token values, or brand accents during UI refreshes, responsive work, refactors, or feature development. New interface elements—including legal pages, dialogs, and notifications—must use this palette rather than introducing a separate color identity.

Light and dark modes may use their approved surface and contrast values below. Switching modes is allowed; replacing the approved palette is not. The explicit accessibility high-contrast option is an accessibility override and must not redefine the base brand tokens. Danger and warning colors remain limited to their semantic status messages.

## Approved tokens

| Token | Light | Dark |
| --- | --- | --- |
| Primary | `#137A63` | `#5CC7A4` |
| Primary hover | `#0F6653` | `#78D8B8` |
| Primary light | `#E8F4EF` | `#203D33` |
| Primary soft | `#DCEFE7` | `#284B3E` |
| Page background | `#F4F7F5` | `#101914` |
| Solid card | `#FFFFFF` | `#1B2620` |
| Border | `#DDE6E1` | `#35473C` |
| Main text | `#1D2A24` | `#EDF4EF` |
| Muted text | `#607068` | `#B0BDB5` |

## Implementation rules

- Treat the light and dark tokens in [`style.css`](../static/css/style.css) as the source of truth for the application.
- Keep the matching legal-page tokens in [`legal.css`](../static/css/legal.css) synchronized with the approved values above.
- Use existing CSS custom properties for new UI. Do not hard-code unrelated blue, purple, or other decorative brand accents.
- Only change this palette when the user explicitly asks to change An Nhiên's brand colors. If approved, update this document, both theme token sets, and their visual regression checks together.
