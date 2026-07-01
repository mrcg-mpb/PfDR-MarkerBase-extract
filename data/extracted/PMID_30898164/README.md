# Extraction record — study PMID_30898164

- Extracted: 2026-07-01
- Model: claude-opus-4-8
- Surveys: 4 · Count rows: 7

## Decisions

# Extraction decisions

## Target markers extracted
Only Pfmdr1 codon 86 (mdr1:86, ref N -> alt Y) falls in the target list among the markers reported per-site. Pfmdr1 184 and 1246 are NOT in the target table and were excluded. Pfk13 non-synonymous mutations reported (R471S, A578S, E433D, I416V, Q613E) do not correspond to any target position and were excluded.

## Pfmdr1:86 counts (Table 4 + footnote)
Table 4 gives per-site N86 (wild-type) prevalence with counts: Kibaha 79/80 (98.8%), Mkuzi 87/88 (98.9%), Mlimba 87/88 (98.9%), Ujiji 88/88 (100%). Pfmdr1 was sequenced for 100% of samples (n=344; per-site totals 80/88/88/88). Denominators therefore taken as the full enrolled samples per site (80, 88, 88, 88).

The footnote states 2 samples had N86Y (one each from Kibaha and Mkuzi) and one sample from Mlimba had N86I. Thus:
- Kibaha: 79 N86 wild-type + 1 N86Y = 80.
- Mkuzi: 87 N86 + 1 N86Y = 88.
- Mlimba: 87 N86 + 1 N86I = 88. (N86I is not a target amino acid but recorded to account for the mutant.)
- Ujiji: 88 N86, no mutants.
These reconcile exactly with the wild-type counts.

## Wild-type imputation
The paper states Pfmdr1 codons were sequenced and reports wild-type (N86, reference) counts directly, so no additional imputation was needed for codon 86. No target Pfk13 codons were reported as mutant in the target list, and although the propeller (440-600) was sequenced (covering many target positions), the paper does not give per-site denominators or wild-type counts for individual target codons — it only reports non-synonymous mutations found. Per rule 3, without clear per-position sequenced denominators by site for the target codons, wild-type was NOT imputed for Pfk13 target positions to avoid fabricating counts. This may bias the extracted data toward the single reported marker (mdr1:86); Pfk13 wild-type frequencies at target codons are therefore absent.

## Haplotype vs per-locus
The Pfmdr1 NFD haplotype (N86/184F/D1246) is reported, but two of its three loci are outside the target set, so the haplotype cannot be encoded meaningfully with target positions only. Per-locus codon 86 data (Table 4) was used instead.

## Spatial
Four sentinel sites geolocated by town centroid: Kibaha (Coast/Pwani), Mkuzi (Muheza, Tanga), Mlimba (Kilombero, Morogoro), Ujiji (Kigoma urban).

## Temporal
Single collection window April-October 2016; each site is one survey with collection_day set to window midpoint (2016-07-16). No pooled national totals extracted (would duplicate site counts).

## Duplicate risk
Samples processed at CDC under PARMA network and data shared with WHO TES monitoring — medium duplicate risk with network datasets, noted for downstream deduplication.
