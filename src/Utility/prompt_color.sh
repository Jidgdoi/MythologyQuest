reset="\033[0m"
First="48" # 38 for foreground color

for i in $(seq 16 255); do
	if (("$(( ${i}%6 ))" == "3")); then
		echo -e "\033[${First};5;${i}m${i} ${reset}"
	else
		echo -en "\033[${First};5;${i}m${i} ${reset}"
	fi
done
