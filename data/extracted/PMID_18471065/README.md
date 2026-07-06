# Extraction record — study PMID_18471065

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 2 · Count rows: 26

## Decisions

## Extraction decisions

### Scope
Two surveys created, one per district/health facility (Bufundi/Kabale and Kebisoni/Rukungiri), both collected May-Dec 2005. No pooling; the paper only reports these two sites for its own data. Codon 164 (I164L) is not in the target position list, so it was not extracted despite being the paper's focus. Codon 50 (dhfr) is also not a target. Only target positions from Table 1 were extracted.

### Per-locus vs haplotype choice
Table 1 gives per-locus counts; Table 2 gives haplotype frequencies but with lower denominators (dhfr: Rukungiri 71, Kabale 46; per-locus dhfr totals 72 and 51) and includes codon 164 (not a target). I used the per-locus Table 1 exclusively and did NOT extract haplotype (Table 2) data to avoid double-counting.

### Wild-type imputation
Methods state dhfr codons 51,59,108,164 and dhps codons 436,437,540,581,613 were all screened; Table 1 reports both wild-type and mutant counts directly, so no imputation was needed. For dhps 436 and 613 the paper explicitly states no mutations; reference counts equal full denominators.

### Reconciliation fix (STAVE variant_num<=total_num)
STAVE validates the sum of variant_num across rows sharing (study, survey, variant string) against total_num. For several positions the paper's wild-type + mutant counts sum to MORE than the denominator because mixed (wild-type+mutant) infections were counted in BOTH the wild-type and mutant rows per the paper's methods. These positions are: dhfr:59 (Kabale 6+48=54>51; Rukungiri 3+70=73>72), dhps:437 (Kabale 1+60=61>60), dhps:540 (Kabale 1+60=61>60), dhps:581 (Kabale 44+27=71>60; Rukungiri 41+33=74>72). To satisfy the constraint without fabricating an allocation of the mixed samples, for each of these positions I retained only the WILD-TYPE (reference) count and dropped the separately-reported mutant count (documented in the row notes). The dropped mutant counts are: dhfr:59:R Kabale 48/51 and Rukungiri 70/72; dhps:437:G Kabale 60/60; dhps:540:E Kabale 60/60; dhps:581:G Kabale 27/60 and Rukungiri 33/72. Where wild-type + mutant fit the denominator exactly (dhps:437 Rukungiri 1+71=72; dhps:540 Rukungiri 1+71=72), BOTH rows were retained. Users needing mutant frequencies at the dropped positions can derive approximate values from the reported percentages in Table 1.

### dhps 613 T variant
Table 1 groups 613 S,T together as mutant (0 observed). Both 613:S and 613:T target rows emitted with variant_num=0.

### Geolocation
Bufundi (Kabale District) and Kebisoni (Rukungiri District) placed at approximate subcounty centroids in southwestern Uganda near the Rwandan border; exact coordinates not stated in the paper.
