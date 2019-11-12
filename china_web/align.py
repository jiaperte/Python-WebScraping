a = ['asdfasd', 'asdf', 'sdfsdf']
b = ['1232', '213', '23']
print("左对齐")
for i in range(3):
    print(a[i].ljust(10), b[i])
print()
print("右对齐")
for i in range(3):
    print(a[i].rjust(10), b[i])
