# Extraction record — study PMID_16186171

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 2

## Decisions

## Extraction decisions

### Target markers
Only crt:76 (pfcrt codon 76) is a curated target reported in this paper. The study genotyped only the pfcrt segment containing codon 76 by PCR/restriction digest (ApoI). No other target positions were assayed.

### Counts
Table 1 gives whole-study pfcrt totals: T76/K76 = 122/17 (n=139). No mixed/heterozygous genotypes were found ('No samples were found which contained both pfcrt variants'). So crt:76:T = 122/139 and crt:76:K (wild type) = 17/139.

### Wild-type
crt:76:K is directly reported (17 K76), not imputed. Denominator 139 = number sequenced at codon 76.

### Disaggregation / pooling
Table 1 does provide a per-clinical-subtype breakdown of T76/K76 (A: 54/5; A+: 24/4; C: 25/4; P: 19/4). These are clinical presentation subtypes at a single site and single time window, NOT distinct spatial or temporal breakdowns. Per the resolution rules (finest SPATIAL and TEMPORAL breakdown), clinical subtype is not a spatial/temporal axis, so I did NOT create separate surveys per subtype. I used the single-site pooled totals (122/17). Note: subtype counts sum to 122/17 = 139, matching.

### Geolocation
Single site: Komfo Anokye Teaching Hospital (KATH), Kumasi, Ghana. Placed at KATH/Kumasi coordinates (~6.6975, -1.6244).

### Temporal
One collection window (Nov 2000-Feb 2001); single survey, collection_day set to midpoint (~2000-12-30).

### Not used
Plasma CQ levels, clinical subtypes, deaths, questionnaire data - not target markers. Prior-literature prevalence figures cited in the Discussion (e.g. 65.5%, 63% from other studies) belong to other papers and were not extracted.
