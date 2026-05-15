#!/bin/bash
# composite-zone-glyphs.sh — Overlay numogram zone glyphs onto NoobAI wallpaper images.
# Preserves originals. Outputs to ~/Pictures/Wall/zones-glyphed/
#
# Usage:
#   bash composite-zone-glyphs.sh          # All zones
#   bash composite-zone-glyphs.sh 6        # Single zone
#   bash composite-zone-glyphs.sh 0 3 6 9  # Specific zones

set -euo pipefail

SRC_DIR="$HOME/Pictures/Wall/zones"
OUT_DIR="$HOME/Pictures/Wall/zones-glyphed"
mkdir -p "$OUT_DIR"

# Zone colors (matching manim-numogram palette)
declare -A ZONE_COLOR=(
    [0]="#444444" [1]="#FFD700" [2]="#FF8C00" [3]="#FF00FF"
    [4]="#00FFFF" [5]="#00FF00" [6]="#0080FF" [7]="#FF3333"
    [8]="#C0A0FF" [9]="#9900FF"
)

# Zone names
declare -A ZONE_NAME=(
    [0]="VOID" [1]="SURGE" [2]="DOUBLE" [3]="TRIANGLE"
    [4]="GATE" [5]="CENTER" [6]="HINGE" [7]="CUT"
    [8]="VORTEX" [9]="PLEX"
)

# Syzygy pairs
declare -A ZONE_SYZYGY=(
    [0]="0 :: 9" [1]="1 :: 8" [2]="2 :: 7" [3]="3 :: 6"
    [4]="4 :: 5" [5]="5 :: 4" [6]="6 :: 3" [7]="7 :: 2"
    [8]="8 :: 1" [9]="9 :: 0"
)

# AQ values for zone names
declare -A ZONE_AQ=(
    [0]="V=111 O=40 I=24 D=14" [1]="S=44 U=46 R=33 G=22 E=15"
    [2]="D=14 O=40 U=46 B=12 L=27 E=15"
    [3]="T=45 R=33 I=24 A=11 N=29 G=22 L=27 E=15"
    [4]="G=22 A=11 T=45 E=15"
    [5]="C=13 E=15 N=29 T=45 E=15 R=33"
    [6]="H=23 I=24 N=29 G=22 E=15"
    [7]="C=13 U=46 T=45"
    [8]="V=111 O=40 R=33 T=45 E=15 X=69"
    [9]="P=41 L=27 E=15 X=69"
)

# Zone numbers to process
ZONES=("$@")
if [ ${#ZONES[@]} -eq 0 ]; then
    ZONES=(0 1 2 3 4 5 6 7 8 9)
fi

for ZONE in "${ZONES[@]}"; do
    SRC="$SRC_DIR/zone${ZONE}.png"
    OUT="$OUT_DIR/zone${ZONE}-glyphed.png"

    if [ ! -f "$SRC" ]; then
        echo "SKIP: $SRC not found"
        continue
    fi

    COLOR="${ZONE_COLOR[$ZONE]}"
    NAME="${ZONE_NAME[$ZONE]}"
    SYZYGY="${ZONE_SYZYGY[$ZONE]}"

    echo "Compositing Zone $ZONE ($NAME)..."

    # Get image dimensions
    W=$(identify -format "%w" "$SRC")
    H=$(identify -format "%h" "$SRC")

    # Font size proportional to image height
    BIG_FONT=$((H / 6))
    MED_FONT=$((H / 20))
    SMALL_FONT=$((H / 30))
    TINY_FONT=$((H / 40))

    # Position calculations
    RIGHT_X=$((W - W / 10))
    BOTTOM_Y=$((H - H / 8))
    BOTTOM_Y2=$((H - H / 12))
    BOTTOM_Y3=$((H - H / 18))
    BOTTOM_Y4=$((H - H / 28))
    TOP_RIGHT_Y=$((H / 12))

    # Build composite using magick
    magick "$SRC" \
        \
        -font "Adwaita-Mono-Bold" \
        \
        -gravity Southwest \
        -fill "$COLOR" -stroke black -strokewidth 3 \
        -pointsize "$BIG_FONT" -annotate "+$((W/10))+$((H/8))" "$ZONE" \
        \
        -stroke none \
        -fill "$COLOR" -stroke black -strokewidth 2 \
        -pointsize "$MED_FONT" -annotate "+$((W/10))+$((H/14))" "$NAME" \
        \
        -stroke none \
        -fill "white" -stroke black -strokewidth 1 \
        -pointsize "$SMALL_FONT" -annotate "+$((W/10))+$((H/22))" "SYZYGY $SYZYGY" \
        \
        -stroke none \
        -fill "white" -alpha set -channel A -evaluate set 50% +channel \
        -pointsize "$TINY_FONT" -annotate "+$((W/10))+$((H/35))" "ZONE $ZONE · NUMOGRAM" \
        \
        -gravity Northeast \
        -fill "$COLOR" -alpha set -channel A -evaluate set 30% +channel \
        -stroke none \
        -pointsize "$((TINY_FONT * 3/4))" -annotate "+$((W/20))+$((H/10))" "☿" \
        \
        -alpha off \
        \
        "$OUT"

    echo "  Saved: $OUT"
done

echo ""
echo "Done. Glyphed wallpapers at: $OUT_DIR"
echo "Originals preserved in: $SRC_DIR"
echo ""
echo "To use as wallpapers, copy to ~/Pictures/Wall/:"
echo "  cp $OUT_DIR/zone*-glyphed.png ~/Pictures/Wall/"
