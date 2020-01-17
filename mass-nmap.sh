#!/bin/bash
domain=$1
# define testcontent
content=$(cat ./$domain/massg.txt)

# declare associative array
declare -A dict 

# loop over all ip lines
while read -r ip port; do
   # save ports
   dict[$ip]+="$port "
         # ignore lines start with #, grep ip an port from content 
done < <(sed '/^#/d;s/.*Host: \([^ ]*\).*Ports: \([0-9]*\).*/\1 \2/' <<< "$content") 
mkdir ./$domain/xml
# loop over assocative array
for key in  "${!dict[@]}"; do

   # sort ports in string
   sorted=$(echo "${dict[$key]}" | tr " " "\n" | sort -n | tr "\n" ,)

   # extract leading ,
   ports="${sorted#*,}"
   #echo $ports	
   #if  [[ ${ports[*]}  =~ 8009 ]]; then
#	   echo "$key" "http"
#   fi
	   # print key an ports without tailing ,
   #printf "%s %s\n" "$key" "${ports%,*}"

   echo "-sV --script vulners -p$ports -oX ./$domain/xml/$domain.$key.xml $key"
done  | parallel -debug "nmap {}"

