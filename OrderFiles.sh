awk 'BEGIN {
  FS = ","
  OFS = "\t"
  while ("ls g*" | getline)
  {
    a = $1
    getline < a
    getline < a 
    c = ($2 == "X"? 99 : $2)
    printf("%02d\t%09d\t%s\n",c,$3,a)
    close(a)
  }
}' | sort | awk -v FS="," -v OFS="\t" -v F="GnomAD_patho.txt" '{
  split($0,A,/\t/)
  a = g = A[3]
  sub(/.csv$/,"",g)
  g = substr(g,15)
  getline < a
  if (!first)
    print $2, $3, $5, $6, "gene", $14, $15, $20 > F
  while (getline < a)
    print "chr" $2, $3, $5, $6, g,  $14, $15, sprintf("%7.4f",log($20)/log(10)) >> F
  close(a)
  first = 1
}'
