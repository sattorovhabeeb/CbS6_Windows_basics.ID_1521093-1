#!/bin/bash

if [ "$EUID" -ne 0 ]; then
   echo "Zapuskayte ot root: sudo ./get_all_info.sh"
   exit 1
fi


OUTPUT_FILE="info"
rm -f "$OUTPUT_FILE" OS_RESULT.tar

echo "Sobiraem informaciyu..."
echo "=== USTONOVLENNYE PAKETY ===" >> "$OUTPUT_FILE"
dpkg -l >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"


echo "=== ZAPUSHENNYE PROCESSY ===" >> "$OUTPUT_FILE"

ps aux >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"


echo "=== OTKRYTYE PORTY ===" >> "$OUTPUT_FILE"

echo "TCP LISTEN: " >> "$OUTPUT_FILE"
ss -tln >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "USP UNCONN: " >> "$OUTPUT_FILE"
ss -uln >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "=== USTANAVLIVAEM COWSAY I SL ===" >> "$OUTPUT_FILE"
apt update >> "$OUTPUT_FILE" 2>&1
apt install -y sowsay sl >> "$OUTPUT_FILE" 2>&1
echo "Ustanovka zavershina" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "=== SISTEMA I YADRO ===" >> "$OUTPUT_FILE"
echo "YADRO:" >> "$OUTPUT_FILE"
uname -r >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "OC:" >> "$OUTPUT_FILE"
cat /etc/os-release >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

tar -cf OS_RESAULT.tar "$OUTPUT_FILE"

echo "GOTOVO! Sozdan arxiv s faylom info"
