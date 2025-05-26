perl -pi -e 's/c3 /C.3/' $1
perl -pi -e 's/c2 /C.2/' $1
perl -pi -e 's/c[e-g] /C.2/' $1
perl -pi -e 's/c1 /C.1/' $1
perl -pi -e 's/n1 /N.1/' $1
perl -pi -e 's/n2 /N.2/' $1
perl -pi -e 's/nv   /N.pl3/' $1
perl -pi -e 's/nu   /N.pl3/' $1
perl -pi -e 's/n[e-h] /N.2/' $1
perl -pi -e 's/n[a-d]  /N.ar/' $1
perl -pi -e 's/ns  /N.ar/' $1
perl -pi -e 's/n3 /N.3/' $1
perl -pi -e 's/p5 /P.3/' $1
perl -pi -e 's/c[a-d]  /C.ar/' $1
perl -pi -e 's/oh /O.3/' $1
perl -pi -e 's/os /O.3/' $1
perl -pi -e 's/h[0-9] /H  /' $1
perl -pi -e 's/h[a-z] /H  /' $1
perl -pi -e 's/o  /O.2/' $1
perl -pi -e 's/n   /N.am/' $1
perl -pi -e 's/c  /C.2/' $1
perl -pi -e 's/f  /F  /' $1
perl -pi -e 's/s6  /S.O2/' $1
perl -pi -e 's/sy  /S.O2/' $1
perl -pi -e 's/ss /S.3/' $1
perl -pi -e 's/sh /S.3/' $1
