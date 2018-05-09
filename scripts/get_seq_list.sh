awk 'NR>1 {for(i=1;i<=length($0);i++)print i, substr($0,i,1)}' $1
