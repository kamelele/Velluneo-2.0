# JLC14 — JLCPCB quotation handoff

Prepared against official JLCPCB pages checked on 20 November 2026. The owner
selected a bare-PCB quote plus a separate assembly-feasibility quote. Production
CAD is the unchanged RFQ13 isolated 45 × 60 mm, four-layer, 33-part driver.

## Use the correct archive

- Velluneo_JLC14_Gerber_Upload.zip: only the manufacturing/reference CAM files
  for Add gerber file at https://cart.jlcpcb.com/quote.
- Velluneo_JLC14_Quote_Handoff.zip: the complete manual technical enquiry,
  including the upload ZIP, settings, remarks, drawings and assembly references.
  Do not upload this complete handoff as Gerbers.

START_HERE_PL.txt gives the owner the exact sequence. JLCPCB-ENQUIRY-UNSENT.txt
is the ready English draft addressed to the official quotation-support contact.
No account was accessed, upload made, message sent, service activated or order placed.

## Applied JLCPCB instructions

The upload has one GKO outline, four named copper layers, two mask layers, two
legends, two paste layers, an Excellon XLN and the recommended human drill map.
The auxiliary sk layer explicitly identifies all 17 vias requiring epoxy filling
and copper caps. Its role is stated in PCB Remark and the enquiry; it is not a
copper layer or another outline. All 25 component insertion holes remain open.
Critical requirements are in the form instructions and PCB Remark, rather than
relying on PDF/text hidden inside the upload ZIP being read by production staff.

The native export uses Protel-style names, mask subtraction and a checked common
plot datum. The tutorial's Absolute-origin example is deliberately adapted to the
retained RFQ13 datum for Gerber, drill, SK and CPL together; this avoids mixed
coordinates or a mirrored bottom side. New files are independently parsed and
compared with the nine already-reviewed RFQ13 artwork layers. No routing, pin,
component, library, rule, requirement, approval or toolkit change is introduced.

## Exact scope of readiness

The package is prepared for quotation; it has not been accepted by the live JLCPCB
importer or a supplier engineer. Hole accuracy, registration, material and filling
requirements need written capability confirmation. The calculator price alone
cannot establish that. Processed production files normally follow a later order
and payment; preliminary DFM and any engineering charge must be agreed separately.

The 26-SMT BOM/CPL use JLC-style headers but remain QUOTE_REFERENCE files. Exact
LCSC matching, availability and part-specific centroid/feeder rotation checks are
not invented. The full 33-part MPN list and seven manual operations are included
for support to assess sourcing and assembly feasibility. Two-sided assembly needs
Standard PCBA and a handling panel at least 70 × 70 mm, rails and fiducials. Ask for
a panel proposal while retaining the finished 45 × 60 mm outline and isolation band.

RFQ13's finished-transformer, formed-part, insulation, functional, fault, thermal
and genuine human stage/release holds remain. This packet authorizes none of those
operations and does not activate a paid parts-selection service.
