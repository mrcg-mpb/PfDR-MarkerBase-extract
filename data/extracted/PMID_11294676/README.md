# Extraction record — study PMID_11294676

- Extracted: 2026-07-06
- Model: claude-opus-4-8
- Surveys: 1 · Count rows: 2

## Decisions

# Extraction decisions

## Target markers
Only pfcrt codon 76 (K76T) is a curated target position reported in this paper. The paper also mentions M74I and N75E changes (crt:74, crt:75 are targets), but these are described as part of the complex mutation accompanying K76T and no independent count/denominator is given for them separately, so they are NOT extracted (no uniquely determinable counts).

## Counts and denominators
Two denominators appear:
- Text: 51/56 pretreatment samples had T76 (85%), 4 of which were mixed. Mixed infections were treated by the authors as single mutated-allele infections.
- Table 1: among the 50 subjects who completed 14-day follow-up, 45 T76 and 5 K76.

I used the full pretreatment denominator of 56 (the molecular-genotyping population) as it is the primary reported frequency (85%). variant_num(crt:76:T)=51, total=56. Wild-type crt:76:K imputed as 56-51=5, total=56.

I did NOT additionally extract the Table 1 counts (45/50, 5/50) because they represent an overlapping subset of the same samples — extracting both would double-count. The 56-sample figure is chosen as it is the larger/complete pretreatment population.

## Mixed infections
4 mixed (K76/T76) infections were folded into the mutant count by the authors; I follow their allocation rather than creating a separate mixed-call count, to avoid double representation.

## Geolocation
Manhiça, Maputo Province, southern Mozambique — placed at the town centroid (~-25.402, 32.808).

## Temporal
Single survey: May–July 1999, midpoint 1999-06-15.

## Single survey
One site, one time window -> survey_id = study_id.
