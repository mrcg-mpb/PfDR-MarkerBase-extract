# Extraction record — study PMID_15814601

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 4 · Count rows: 12

## Decisions

## Target markers
Only pfcrt codon 76 (K76T) was assayed by PCR-RFLP. Encoded as crt:76:T (mutant), crt:76:K (wild-type), crt:76:K/T (mixed). No other curated positions reported.

## Wild-type encoding
The RFLP assay directly distinguishes wild-type (K), mutant (T) and mixed. Pure wild-type counts are reported explicitly, so crt:76:K counts are directly from the paper (not imputed). No wild-type imputation needed. No other target positions were sequenced, so no imputation elsewhere.

## Survey resolution
The paper reports several distinct groups that are NOT pooled here:
- Non-pregnant controls (n=49).
- Pregnant women during pregnancy, peripheral blood (n=62 infected before delivery).
- Pregnant women at delivery, peripheral blood (n=58).
- Pregnant women at delivery, placental blood (n=67).
These represent different populations/sample types/time points and are treated as separate surveys. Note the pregnant-women groups derive from the same 69-woman cohort followed longitudinally, so peripheral/placental at delivery and mid-pregnancy samples partially overlap in individuals (but are different sampling events/blood compartments). This overlap is documented; counts are not summed across them.

## Counts reconciliation
Controls: 26+6+17=49 = reported total. OK.
During pregnancy: 47+11+4=62 = reported infected before delivery. OK.
Delivery peripheral: 50+3+5=58. OK.
Delivery placental: 57+2+8=67. OK.
All counts reconcile with stated denominators.

## Not used
Subgroup breakdowns (primigravidae vs multigravidae; chloroquine compliance groups) overlap with the main delivery counts and would duplicate samples, so were not extracted separately. Figure 1 percentages are consistent with the text counts.

## Geolocation
All samples from the rural maternity hospital of Thiadiaye, Senegal. Coordinates (~14.4667 N, -16.75 E) are the approximate Thiadiaye town centroid. Controls enrolled 'in the same area'.

## Temporal
Women delivering Oct 2001 - Jun 2002. No finer per-time-bin breakdown given, so all surveys share this window with midpoint 2002-02-14. Mid-pregnancy samples were the earliest infected samples within this cohort window.
