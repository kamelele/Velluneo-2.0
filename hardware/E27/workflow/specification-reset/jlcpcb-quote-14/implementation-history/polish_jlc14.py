from pathlib import Path
import json
W=Path(__file__).resolve().parent;D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/jlcpcb-quote-14';H=D/'support';A=D/'assembly-feasibility'
def txt(p,s):p.write_text(s,encoding='utf-8')
txt(D/'START_HERE_PL.txt','''VELLUNEO JLC14 — JAK UZYSKAĆ WYCENĘ JLCPCB

Pakiet obejmuje wycenę PCB oraz osobną ocenę możliwości montażu. Niczego jeszcze
nie wysłano, nie wgrano na konto JLCPCB ani nie zamówiono.

1. Rozpakuj Velluneo_JLC14_Quote_Handoff.zip.
2. Otwórz https://cart.jlcpcb.com/quote. W polu „Add gerber file” wybierz tylko
   Velluneo_JLC14_Gerber_Upload.zip. Nie wgrywaj tam całego pakietu zapytania.
3. Ustaw: FR-4; 4 warstwy; 45 × 60 mm; 5 sztuk; Industrial/Consumer electronics;
   1 projekt; Single PCB; 1.6 mm; Green; White; ENIG; Outer Copper 1 oz;
   Inner Copper 0.5 oz; Remove Mark; Flying Probe Fully Test.
   Poproś o dokładny stack JLC04161H-7628 i FR-4 Tg155. Szczegóły są również
   w quote-settings.json. Jeśli opcja nie jest dostępna, uzgodnij ją z obsługą.
4. Via Covering: „Epoxy-Filled & Capped”. Wszystkie 17 przelotek Ø0.300 mm
   mają być wypełnione nieprzewodzącym epoksydem i zamknięte miedzią z obu stron.
   Wszystkie 25 otworów do montażu elementów pozostaje otwartych.
5. Wklej PCB-REMARK-PASTE.txt do „PCB Remark”. Jeśli pole nie mieści tekstu,
   użyj PCB-REMARK-SHORT.txt i przekaż pełny opis obsłudze technicznej.
   Nie pomijaj wymagań. JLCPCB zastrzega, że opisy PDF/TXT/Excel ukryte
   w archiwum Gerber mogą być pomijane. Dlatego są też w uwagach i zapytaniu.
6. Sprawdź podgląd: 4 warstwy miedzi, jeden obrys 45 × 60 mm i 42 otwory.
   Nie ma otworów NPTH ani szczelin. „Velluneo_JLC14.sk” to pomocnicza mapa
   17 przelotek do wypełnienia, a nie kolejna warstwa miedzi lub drugi obrys.
   Przy błędnym rozpoznaniu plików przerwij ten krok i skontaktuj się z obsługą.
7. Wyślij przygotowane zapytanie z JLCPCB-ENQUIRY-UNSENT.txt do support@jlcpcb.com,
   gdy zdecydujesz się skontaktować z wykonawcą. Załącz pakiet zapytania lub
   osobno Gerber ZIP oraz pliki support/ i assembly-feasibility/.
   Zalecana jest ręczna ocena techniczna: standardowa tolerancja otworów JLCPCB
   nie spełnia wymagania T1. Potrzebna jest pisemna odpowiedź na listę pytań.
8. Dla osobnej wyceny gołego PCB pozostaw PCB Assembly i Stencil wyłączone.
   Montaż wyceń osobno: 26 elementów SMT z obu stron oraz możliwość wykonania
   5 operacji THT i 2 operacji przewodów. JLCPCB ma potwierdzić dokładne części,
   dostępność, koszty i proces; nie zatwierdzono żadnych zamienników.
9. Montaż dwustronny wymaga Standard PCBA oraz panelu technologicznego minimum
   70 × 70 mm, szyn i znaczników pozycjonujących. Docelowa płytka nadal ma
   45 × 60 mm. Wykonawca ma przedstawić panel, sposób rozdzielenia płytek,
   liczbę dostarczonych sztuk i koszt do sprawdzenia.
10. BOM/CPL w assembly-feasibility/ są plikami referencyjnymi do ręcznej wyceny.
    Nagłówki odpowiadają JLCPCB, ale numery LCSC i korekty centroidów/obrotów
    pod konkretne części nie są potwierdzone. Nie traktuj ich jako gotowego
    zlecenia automatycznego montażu. Poproś o dokładne dopasowanie MPN/LCSC,
    kontrolę polaryzacji i podgląd rozmieszczenia przed przyszłym montażem.

WAŻNE WYMAGANIE OTWORÓW
T1: 10 gotowych otworów 1.350 mm, wymagany zakres 1.300–1.400 mm.
Standard JLCPCB +0.13/−0.08 mm daje 1.270–1.480 mm i nie jest zaakceptowany.
Prosimy o dokładniejszą usługę ±0.050 mm dla wszystkich 25 otworów elementów
oraz uzgodnienie rejestracji otworów i pól. Nazwa usługi może zawierać „Press-fit”,
ale nasze otwory służą elementom lutowanym — nie złączom wciskanym.

To zapytanie, nie zamówienie. Sama cena kalkulatora ani przyjęcie ZIP nie oznacza
potwierdzenia specjalnych wymagań. Nie aktywuj płatnego doboru części bez osobnej
decyzji. Nie przechodź do płatności ani zatwierdzenia produkcji.

Jeśli później zamówienie zostanie zatwierdzone, wybierz „Confirm Production File”
bez automatycznej akceptacji. JLCPCB zwykle przygotowuje te pliki po etapie
zamówienia/płatności. Wcześniejszą ocenę DFM i ewentualną opłatę trzeba uzgodnić
osobno; nie obiecujemy bezpłatnych filmów produkcyjnych przed zamówieniem.
''')
txt(D/'README.md','''# JLC14 — JLCPCB quotation handoff

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
''')
txt(D/'PCB-REMARK-PASTE.txt','''JLC14: QUOTATION/DFM ONLY. 45x60mm, 4L, 1.6mm, ENIG; exact JLC04161H-7628 requested. Velluneo_JLC14.sk is AUXILIARY VIA-FILL SELECTION, NOT COPPER/OUTLINE: nonconductive epoxy-fill and copper-cap BOTH ends of all 17 marked 0.300mm vias only; leave all 25 component PTH open. Ten T1 finished holes: target1.350mm, REQUIRED1.300-1.400mm. Request tighter +/-0.050mm service for all 25 listed insertion holes; standard +0.13/-0.08 is NOT accepted for T1. These are soldered insertion holes, not press-fit terminals. Requested hole/land registration<=0.025mm and finished ring/cap limits require written capability response. No added copper, tooling, thieving or marks in output Y37.865-47.100mm across X0-45 on any copper layer. Confirm actual laminate/CTI/RTI and minimum pressed dielectrics. Return infeasible requirements as redlines. If a later order is authorized, confirm production files before manufacture; no automatic acceptance. Discuss all requirements with technical support; attachments alone are not authorization.
''')
txt(D/'PCB-REMARK-SHORT.txt','''JLC14 QUOTE/DFM ONLY. Velluneo_JLC14.sk selects all17 0.300mm vias: nonconductive epoxy fill + copper cap BOTH ends;25 component holes OPEN. T1 finished1.350mm REQUIRED1.300-1.400; standard tolerance NOT accepted. Exact JLC04161H-7628. Full hole/registration/material/isolation requirements need written technical-support confirmation. No automatic production-file acceptance. See full technical enquiry.
''')
txt(A/'READ_BEFORE_ASSEMBLY_QUOTE.txt','''JLC14 — MANUAL ASSEMBLY FEASIBILITY / QUOTATION

Please quote five finished individual boards separately from the bare-PCB quote.
Option A: 26 SMT components on BOTH sides. Option B: also assess five THT parts
and two wire operations, each conditional on exact construction acceptance.
The full 33-part MPN list identifies these scopes. J1/J2 are wire pads, not defined
connectors; no wire construction or length has been invented. F1 and C4 are SMT.
T1 is a complete custom winding assembly, not a stock bobbin/core substitute.

The 26-SMT BOM and CPL have matching designators, JLC-style headers, millimetres
and Top/Bottom sides. LCSC IDs remain blank because matching has not been verified.
Use the exact manufacturer part numbers for manual matching and return C-numbers,
suffixes, packages, ratings and availability for review. No substitutions or paid
parts-selection service are authorized. These files are QUOTE_REFERENCE, not an
approved automatic PCBA order. State any selection-service fee before activation.

Coordinates are native footprint origins: X=x-77.5, Y=130-y. Both faces use the
same top-view XY frame. Native export angles are normalized to 0..360 degrees;
no guessed bottom mirror or feeder correction is applied. Actual centroids,
part-specific offsets, pin 1, polarity and reel/feed rotations must be checked
after exact component matching in the placement preview. Return corrections for
review before machine use. The full 33-position file is engineering reference,
not a claim that custom THT/wire operations are automated placement tasks.

Double-sided placement requires Standard PCBA. JLC lists a 70x70mm minimum
handling size and requires rails/fiducials. Please return a panel/tooling proposal
for the individual 45x60mm board; adding 5mm rails alone does not meet both 70mm
dimensions. Quote actual panels, delivered units, rails, depanelization, stencil,
setup, sourcing and labor separately. Keep added tooling off the finished board
and preserve its outline, isolation band and all component positions.

For SMT-only work, leave all 25 insertion holes open and unsoldered. Retain the
17 filled/capped vias. For later THT/wire work, return the soldering/masking and
inspection process, transformer construction and formed-part/vent clearances.
Finished insulation and energized functional testing require a separate qualified
basis; this enquiry grants no manufacturing, assembly or testing authorization.
''')
txt(D/'JLCPCB-ENQUIRY-UNSENT.txt','''To: support@jlcpcb.com
Subject: DFM/quotation and separate assembly feasibility — Velluneo JLC14

Dear JLCPCB Technical Support,

Please review the attached JLC14 handoff. This is a technical enquiry, not an
order or authorization to activate a paid service, manufacture or assemble.

1. BARE PCB: please quote five finished individual 45x60mm, four-layer FR-4
boards, nominal1.6mm, Tg155 request, ENIG, green/white, outer1oz/inner0.5oz.
Request exact JLC04161H-7628 construction. Please identify the actual laminate,
CTI/RTI, minimum pressed dielectrics and finished copper guarantees.

The Gerber ZIP contains one GKO, four copper layers, two mask, two legends,
two paste layers, Excellon XLN, a drill map and Velluneo_JLC14.sk. The sk is
AUXILIARY VIA-FILL SELECTION, not copper or outline: epoxy-fill and copper-cap
BOTH ends of all 17 marked 0.300mm vias. Leave all 25 component holes open.

T1's ten finished holes target1.350mm and must be1.300-1.400mm. Your standard
+0.13/-0.08 tolerance is not acceptable here. Please quote tighter +/-0.050mm
service for all 25 listed insertion holes. These are soldered insertion holes,
not press-fit connector terminals. Requested hole/land registration<=0.025mm
also needs explicit agreement. Please return guaranteed hole/ring/cap/planarity
limits and any infeasible requirement as a redline before an order.

No copper, tooling, thieving or marks may be added in the protected band across
X0-45mm, outputY37.865-47.100mm, on any copper layer. Please answer the technical
response checklist. An online calculator figure is not process confirmation.

2. SEPARATE ASSEMBLY FEASIBILITY/COST: please assess 26 SMT parts on BOTH sides
using the exact 33-part MPN list and the 26-SMT quote-reference BOM/CPL. Return
exact matching LCSC numbers, suffixes/packages/ratings, availability and any
selection-service fee before activation. No substitutions are authorized.
Also assess the five THT parts and two wire operations separately. Custom T1
and formed parts require accepted drawings, construction and first articles.

We understand that two-sided placement requires Standard PCBA and a handling
panel at least70x70mm with rails/fiducials. Please return the panel proposal,
actual unit/panel quantities and separate tooling, stencil, setup, parts, labor,
depanelization and lead-time figures. Keep additions off the finished board and
preserve its isolation band. The reference CPL has no verified feeder/centroid
corrections; please return placement corrections/preview for review before use.

Please advise what preliminary DFM is available before ordering and any fee
requiring separate approval. For a later authorized order we will request
Confirm Production File without automatic confirmation; we understand processed
films normally follow that order/payment stage. No paid service, shipping order,
payment or production authorization is supplied by this enquiry. Shipping can
be quoted separately when destination details are provided.

Regards,
Velluneo project — prepared draft, not yet sent
''')
txt(H/'FABRICATION-REQUIREMENTS.txt','''JLC14 — FABRICATION REQUIREMENTS FOR TECHNICAL QUOTATION

Unchanged source: RFQ13 isolated driver,45x60mm,4layers,33parts. No order.

Files: oneGKO outline; GTL/G2L/G3L/GBL copper; two masks; two legends; two paste;
Excellon XLN; drillmap; auxiliary Velluneo_JLC14.sk selecting17 filled vias.
The SK is not copper, outline or a second drilling operation. No duplicate GM
outline, native PCB, PDF, BOM or nested archive is inside the upload ZIP.
Paste layers are assembly reference, not an instruction to purchase a stencil.

All CAM/SK/CPL share native plot datum(77.5,130)mm: outputX=x-77.5, Y=130-y.
Bounds0..45x0..60mm. The tutorial's Absolute-origin example is deliberately
adapted to the same retained plot datum for Gerber AND drill. No bottom mirror.

Quote5 individual boards: FR-4 nominal1.6mm(+/-10%), Tg155 request, ENIG,
green/white, outer1oz and inner0.5oz. Request exactJLC04161H-7628 construction;
source foil/core/prepreg numbers are nominal construction inputs, not guaranteed
minimum finished copper or dielectric. Return actual laminate/CTI/RTI and limits.

Epoxy-fill and copper-cap BOTH ends of ALL17 marked0.300mm through-vias. Leave
all25 component holes open. No other design hole is0.300mm. Component targets
are1.000..1.600mm. Ordinary tenting or ink plugging is not an acceptable substitute.

Component sizes mean FINISHED plated-hole targets, not uncompensated tool sizes.
Request+/-0.050mm for all25 listed holes; tenT1 holes1.350mm must be1.300..1.400mm.
Standard JLC+0.13/-0.08 gives1.270..1.480mm and is not accepted forT1. Please quote
the tighter-hole service; these are soldered insertion holes, not press-fit terminals.
Hole/land registration<=0.025mm requires written capability agreement. The public
position tolerance+/-0.075mm does not establish this requested registration limit.
Return actual finished rings, hole position, cap thickness and planarity limits.

Protected band: outputX0..45, Y37.865..47.100mm, on all four copper layers.
No added copper, tooling, thieving, marks, slots or changes without reviewed redlines.
There are no mounting holes or slots on the individual finished board. Source
projected P/S coppergap>=10.725mm; proposed0.35mm/domain finishing budget remains
conditional and does not qualify finished transformer insulation.

Critical requirements belong in PCBRemark and the manual technical enquiry;
the JLC ordering guide says PDF/text/Excel hidden in the upload ZIP may be ignored.
Please state preliminary DFM availability and any engineering charge separately.
Confirm Production File normally follows a later order/payment; no free pre-order
films or supplier process acceptance are claimed. No manufacture is authorized.
''')
print('Polished owner instructions and professional supplier-facing draft/requirements')
