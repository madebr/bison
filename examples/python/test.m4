xx
yy
include(m4sugar.m4)
m4_divert(-1)
m4_undivert()
m4_divert(0)
zz

 abc
 m4_define([b4_rhs_value], [rhs$1])
 m4_define([b4_lhs_value], [dest])


 m4_define([USER1], [        { print(]b4_rhs_value(1, 1, orig 7, [])[) }]) })dnl
 m4_define([USER2],[             { # Generates an empty list }])dnl
 m4_define([USER3],[             { ]b4_lhs_value(orig 7, [])[ = ]b4_rhs_value(2, 1, orig 7, [])[; ]b4_lhs_value(orig 7, [])[.append(]b4_rhs_value(2, 2, orig 8, [])[) }])],
 [[list: list item]])dnl
 m4_define([USER4],[          {
     my_numbers = @{1, 2, 3@}
     if ]b4_rhs_value(1, 1, 4, [])[ in my_numbers:
       print("I know this number!")
     print("Received {}", ]b4_rhs_value(1, 1, 4, [])[)
     print("{} ** 2 -> {}", ]b4_rhs_value(1, 1, 4, [])[, ]b4_rhs_value(1, 1, 4, [])[*]b4_rhs_value(1, 1, 4, [])[)
     ]b4_lhs_value(orig 8, [])[ = str(]b4_rhs_value(1, 1, 4, [])[)
   }])dnl

 [x1]

 #USER1


 [x2]d

 #USER2


 [x3]

 #USER3


 [x4]

 USER4


 [START]

 ->[]USER1[]<-

  [CODE]

dnl index([USER1], [{])
dnl index([USER1], [
dnl ])
dnl index([USER2], [{])
dnl index([USER3], [{])
dnl index(expand(USER4), [{])
dnl index(m4_expand([[USER4]]), [{])

m4_strip([  a  b  c  ])

m4_define([CODE], [m4_joinall([OPENBRACES], USER4)])
[xx]

p
q m4_index(CODE,[{])

m4_bpatsubst([CODE], [m])
