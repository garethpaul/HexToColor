/^[[:space:]]+iPhone/ && length($2) == 36 && $2 ~ /^[0-9A-Fa-f-]+$/ {
    print $2
    exit
}
