fld  f1, 100(x7)
fmul f2, f2, f1
fadd f2, f1, f3
fld  f9, 0(x3)
fdiv f3, f9, f7
fmul f7, f3, f2
fsub f2, f4, f4
fsd  f2, 50(x11)
fdiv f1, f5, f2
fsd  f1, 50(x11)
fadd f4, f1, f2
