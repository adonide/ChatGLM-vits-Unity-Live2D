import sys
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
def a_plus_b(a):
    return a+'python'

print(a_plus_b(sys.argv[1]))