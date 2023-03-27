import sys
import io
import time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

def something(content):
    time.sleep(5)
    print(content+'aaa')

def main():
    while True:
        content = input('输入：')
        something(content)

if __name__ == '__main__':
    main()
