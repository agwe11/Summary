#!/bin/bash

if [[ ! $@ =~ ^\-.+ ]];
then
  echo "Use -d domain.com or -i IP address"
  exit
fi

while getopts "d:i:" opt; do
	case $opt in 
		d)
		  	domain=$OPTARG
		  	mkdir $domain
			#amass passive
			echo "amass passive enum"
			amass enum --passive -d $domain -o ./$domain/amasslst &
			#commonspeak
			echo "Appending Commonspeak list"
			cat /usr/share/wordlists/subdomains.txt|while read line;do echo "$line.$domain" >> ./$domain/commonspeaklst;done &
			#rapid7
			echo "Appending rapid7 FDNS lookup"
			pv /usr/share/rapid7/2019-09-27-1569542663-fdns_any.json.gz| pigz -dc | grep -F '.'$domain\"'' | tee ./$domain/rapid7.txt &
			wait
			jq -r 'select(.type=="a")|.name' ./$domain/rapid7.txt >> ./$domain/lst
			cat ./$domain/rapid7.txt | grepcidr -v 10.0.0.0/8,172.16.0.0/12,192.168.0.0/16|  jq -r 'select(.type=="a")|.name' >> ./$domain/lst
			cat ./$domain/amasslst >> ./$domain/lst
			cat ./$domain/commonspeaklst >> ./$domain/lst
			#find possible wildcard domain????

			#massdns
			echo "1st massdns"
			sort -u -o lst lst
			massdns -r /opt/massdns/lists/resolvers.txt -t A  -o S -w ./$domain/online.txt ./$domain/lst
			cat ./$domain/online.txt | awk -F ". " '{print $1}' > ./$domain/domains.txt
			#altdns
			echo "altdns online domains"
			altdns -i ./$domain/domains.txt -o ./$domain/altdnsout -w /usr/share/wordlists/words.txt
			#massdns
			echo "2nd massdns"
			massdns -r /opt/massdns/lists/resolvers.txt -t A  -o S -w ./$domain/alt-online.txt ./$domain/altdnsout
			#create domain only list
			echo "create domain only list"
			cat ./$domain/alt-online.txt >> ./$domain/online.txt #;rm ./$domain/alt-online.txt
			cat ./$domain/online.txt |  awk -F ". " '{print $1}'  > ./$domain/domains.txt
			#create ip list
			echo "create IP only list"
			cat ./$domain/online.txt | awk -F ". " '{print $3}'| grepcidr -v 10.0.0.0/8,172.16.0.0/12,192.168.0.0/16 | sort -u > ./$domain/ips.txt

			#remove private IPs from online.txt
			cat ./$domain/online.txt | grepcidr  -v 10.0.0.0/8,172.16.0.0/12,192.168.0.0/16 > ./$domain/temp;mv ./$domain/temp ./$domain/online.txt 
			#masscan
			sudo masscan --ports 80,443  -iL ./$domain/ips.txt -oG ./$domain/masscang.txt
			#geturls
			content=$(cat ./$domain/domains.txt)

			while IFS= read line
			do
				if [[ $(wget -S --spider  https://$line -t 1 -T 2 2>&1 | grep 'HTTP/1.1') ]]; then
	       				echo "https://$line" | tee -a ./$domain/urls.txt;
				elif [[ $(wget -S --spider  http://$line -t 1 -T 2 2>&1 | grep 'HTTP/1.1') ]]; then
	       				echo "http://$line"| tee -a ./$domain/urls.txt;

				fi
			done < ./$domain/domains.txt

			#wapp
			cat ./$domain/urls.txt | while read line; do docker run --rm wappalyzer/cli $line  >> ./$domain/wapp.txt;done
			#ssllab
			ssllabs-scan --ignore-mismatch --usecache  --grade  --hostfile  ./$domain/domains.txt > ./$domain/ssltemp.txt ; cat ./$domain/ssltemp.txt|grepcidr 0.0.0.0/0 > ./$domain/ssl.txt;rm ./$domain/ssltemp.txt
			#jsearch
			#cat urls.txt|while read line; do python /opt/jsearch/jsearch.py -u $line -n hyundai | grep --line-buffered -e 'DOMAIN INFO' -e 'NAME INFO' |tee -a jsearch.txt;done
			#aquatone
			#cat ./$domain/urls.txt | aquatone -scan-timeout 1000 -out ./$domain/aquatone
			
			;;
		i)
			ip=$OPTARG
			whois -h whois.cymru.com $ip | sed -n '2p' | awk '{print $1}' | xargs -I {} sh -c "whois -h whois.radb.net -- '-i origin {}'" |grep -e descr: -e route: -e origin:
			echo "grep keyword: "
			read keyword
			whois -h whois.cymru.com $ip | sed -n '2p' | awk '{print $1}' | xargs -I {} sh -c "whois -h whois.radb.net -- '-i origin {}'" | grep --color=always -i $keyword -B 1 #| grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}\/[0-9]{1,2}" | sort -u
 			;;
		\?)
			echo "Missing argument"
			;;
		esac
	done

#if [ -z "${domain// }" ] || [ -z "${ip// }"];
#then 
#	echo "Use -d example.com or -i IP address"
#	exit 
#fi


