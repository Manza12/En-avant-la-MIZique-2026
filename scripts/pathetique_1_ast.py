from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch

###############
# Definitions #
###############

# Time
## Note values
t_dotted_whole = Texture(Rhythm(Hit('0', '3/2')))
t_dotted_half = Texture(Rhythm(Hit('0', '3/4')))
t_half = Texture(Rhythm(Hit('0', '1/2')))
t_quarter = Texture(Rhythm(Hit('0', '1/4')))
t_eighth = Texture(Rhythm(Hit('0', '1/8')))

## Textures
t_pedal = Texture(
    Rhythm(Hit('0/8', '1/8'), Hit('2/8', '1/8')),
    Rhythm(Hit('1/8', '1/8'), Hit('3/8', '1/8')),
)

t_melody_1_head_1 = t_dotted_half * t_quarter
t_melody_1_head_2 = t_quarter * t_half * t_quarter
t_melody_1_tail = t_quarter ** 4

# Frequency
## Pitches and degrees
tonic = Pitch(60)

ton = Chord({0})
sup = Chord({2})
mdm = Chord({3})
mdM = Chord({4})
sub = Chord({5})
tri = Chord({6})
dom = Chord({7})
smm = Chord({8})
smM = Chord({9})
sbt = Chord({10})
ldt = Chord({11})

## Harmonies
### Length 1
#### Density 1
h_Ton = Harmony.from_chord(ton)        # ({0})
h_Sup = Harmony.from_chord(sup)        # ({2})
h_Min = Harmony.from_chord(mdm)        # ({3})
h_Sub = Harmony.from_chord(sub)        # ({5})
h_Tri = Harmony.from_chord(tri)        # ({6})
h_Dom = Harmony.from_chord(dom)        # ({7})
h_Smm = Harmony.from_chord(smm)        # ({8})
h_SmM = Harmony.from_chord(smM)        # ({9})

#### Density 2
h_Min_6M = Harmony(mdm | (ton + 12))    # ({3, 12})
h_Maj_6m = Harmony(mdM | (ton + 12))    # ({4, 12})
h_Sub_4A = Harmony(sbt | (mdM + 12))    # ({10, 16})
h_Smm_6M = Harmony(smm | (sub + 12))    # ({8, 17})
h_Maj_3m = Harmony(mdM | dom)           # ({4, 7})
h_Sub_3m = Harmony(sub | smm)           # ({5, 8})   
h_Sup_6M = Harmony(sup | ldt)           # ({2, 11})

#### Density 3
h_viio36 = Harmony(sup | sub | ldt)                 # ({2, 5, 11})
h_i46 = Harmony(dom | (ton + 12) | (mdm + 12))      # ({7, 12, 15})
h_iio36 = Harmony(sub | smm | (sup + 12))           # ({5, 8, 14})

#### Density 4
h_i358 = Harmony(ton | mdm | dom | (ton + 12))          # ({0, 3, 7, 12})
h_V378 = Harmony(dom | ldt | (sub + 12) | (dom + 12))   # ({7, 11, 17, 19})

### Length 2
h_Ton_2 = Harmony.from_chord(ton | ton + 12)                        # ({0}, {12})
h_Sup_2 = Harmony.from_chord(sup | sup + 12)              # ({2}, {14})
h_Min_2 = Harmony.from_chord(mdm | mdm + 12)        # ({3}, {15})
h_Sub_2 = Harmony.from_chord(sub | sub + 12)            # ({5}, {17})
h_Tri_2 = Harmony.from_chord(tri | tri + 12)                    # ({6}, {18})
h_Dom_2 = Harmony.from_chord(dom | dom + 12)                  # ({7}, {19})
h_Smm_2 = Harmony.from_chord(smm | smm + 12)  # ({8}, {20})

#############
# Structure #
#############

## Exposition
### Theme P
#### Phrase 1
##### Measure 11-12
m11_bass = (t_pedal * 2) @ (h_Ton_2 - 12 * 2)
m11_12_bass = m11_bass ** 2

m11_melody = t_melody_1_head_1 @ (h_Ton + (h_Sub_4A - 12))
m12_melody = t_melody_1_tail @ ((h_Smm_6M - 12) + h_Maj_3m + h_Sub_3m + h_Sup_6M)
m11_12_melody = m11_melody * m12_melody

m11_12 = m11_12_bass + m11_12_melody

##### Measure 13
m13_14_bass = m11_bass ** 2

m13_melody = t_melody_1_head_2 @ (h_Min_6M + h_Maj_6m + h_Sub_4A)
m14_melody = m12_melody + 12
m13_14_melody = m13_melody * m14_melody

m13_14 = m13_14_bass + m13_14_melody

phrase_1 = m11_12 * m13_14

#### Phrase 2
###### Bass
m15_1_bass = t_pedal @ (h_Ton_2 - 12 * 2)
m15_2_bass = t_pedal @ (h_Sup_2 - 12 * 2)
m16_1_bass = t_pedal @ (h_Min_2 - 12 * 2)
m16_2_bass = t_pedal @ (h_Sub_2 - 12 * 2)
m17_1_bass = t_pedal @ (h_Dom_2 - 12 * 2)
m17_2_bass = t_pedal @ (h_Smm_2 - 12 * 2)
m18_1_bass = t_pedal @ (h_Tri_2 - 12 * 2)
m18_2_bass = t_pedal @ (h_Dom_2 - 12 * 2)

###### Melody
m15_1_melody = t_half @ (h_i358 + 12)
m15_2_melody = t_half @ h_V378
m16_1_melody = t_half @ h_i46
m16_2_melody = t_half @ h_iio36

m17_18_1_melody_1 = t_dotted_whole @ h_Min_6M
m17_18_1_melody_2 = (t_half ** 3) @ (h_Dom + h_Tri + h_SmM)
m17_18_1_melody = m17_18_1_melody_1 + m17_18_1_melody_2

m18_2_melody = t_half @ h_viio36

m15_1 = m15_1_bass + m15_1_melody
m15_2 = m15_2_bass + m15_2_melody
m16_1 = m16_1_bass + m16_1_melody
m16_2 = m16_2_bass + m16_2_melody
m17_18_1 = (m17_1_bass * m17_2_bass * m18_1_bass) + m17_18_1_melody
m18_2 = m18_2_bass + m18_2_melody

phrase_2 = m15_1 * m15_2 * m16_1 * m16_2 * m17_18_1 * m18_2

theme_p = phrase_1 * phrase_2

exposition = theme_p

piece = tonic + exposition