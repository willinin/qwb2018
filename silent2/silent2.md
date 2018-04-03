#qwbctf  silent2  wp

这道题只有一个uaf漏洞，没有溢出，申请的堆块不能是`fastbin chunk`。
几个比较关键的点是：

* 堆的地址在数据段，unlink的提示
* chunk在改写的时候，长度判断是`strlen`，所以正常情况下只能改写`fd`，不能unsortbin attack.

这里简单说下这题的利用思路，很明显这题能构造`chunk overlap`去`creat a fake freed chunk`，但是怎么使得下一个`used chunk`的`pre_used`标志位为0是一个当时搞不定的问题。

而且`actual chunk and fake chunk`只能是紧紧包含的关系，否则就没有p指针。

方法大概是这样的：

* free 掉3个chunk，形成一个大的chunk
* 然后改写大chunk的数据，改写大chunk里第2个chunk的大小，使之变大
* 试想一下，这时如果free掉第2个小chunk，再free掉第一个小chunk
* unsortbin 里面就有大chunk和改写了大小的第2个小chunk
* 这个时候申请一个chunk，使得大chunk分割，分割剩下的chunk刚好是之前第3个chunk的数据段。
* 这个时候  下个chunkd的`pre_used`还是不会置位。但是，这时候我们在创建一个chunk，就会申请到第2个小chunk(已经在smallbin里)，通过改写第2个小chunk，就能改变第3个chunk的数据。

总结起来就是通过改变size和free操作，使得unsortbin里的chunk overlap，然后你malloc其中一个，使之分割，但使用另外一个chunk去改写数据。



