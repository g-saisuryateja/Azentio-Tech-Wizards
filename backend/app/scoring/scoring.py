# Risk scoring engine

# score = clamp( sum(weight × confidence) + combination_bonus - sum(mitigations), 0, 100 )
#
# Risk bands: Low (0-39), Medium (40-69), High (70-100)
#
# Components:
# - indicators:   Weighted fraud indicators
# - scorer:       Score computation with combination bonus
# - explain:      Human-readable score explanations