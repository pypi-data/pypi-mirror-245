# febug [![builds.sr.ht badge](//builds.sr.ht/~nabijaczleweli/febug.svg)](//builds.sr.ht/~nabijaczleweli/febug)
anyway, here's user-space debugfs

## [Debian  manpages](//srhtcdn.githack.com/~nabijaczleweli/febug/blob/man/Debian/index.0.html)  ([PDF](//srhtcdn.githack.com/~nabijaczleweli/febug/blob/man/Debian.pdf))
## [FreeBSD manpages](//srhtcdn.githack.com/~nabijaczleweli/febug/blob/man/FreeBSD/index.0.html) ([PDF](//srhtcdn.githack.com/~nabijaczleweli/febug/blob/man/FreeBSD.pdf))
## [NetBSD  manpages](//srhtcdn.githack.com/~nabijaczleweli/febug/blob/man/NetBSD/index.0.html)  ([PDF](//srhtcdn.githack.com/~nabijaczleweli/febug/blob/man/NetBSD.pdf))
## [OpenBSD manpages](//srhtcdn.githack.com/~nabijaczleweli/febug/blob/man/OpenBSD/index.0.html) ([PDF](//srhtcdn.githack.com/~nabijaczleweli/febug/blob/man/OpenBSD.pdf))
## [MacOS   manpages](//srhtcdn.githack.com/~nabijaczleweli/febug/blob/man/MacOS/index.0.html)   ([PDF](//srhtcdn.githack.com/~nabijaczleweli/febug/blob/man/MacOS.pdf))
## [Library rustdoc ](//srhtcdn.githack.com/~nabijaczleweli/febug/blob/rustdoc/febug/index.html)

### What?

Co-operative (between the program and you) debugging:

<!-- remember to sync this to febug(8) -->
```
# systemctl start febug
$ findmnt /run/febug
/run/febug febug  fuse.febug rw,nosuid,nodev,relatime,user_id=0,group_id=0,default_permissions,allow_other
$ ./out/examples/vector-sort &
[1] 1409
$ LD_LIBRARY_PATH=out ./out/examples/string-qsort &
[2] 1410
$ ls /run/febug/
1409    1410
$ ls -l /run/febug/
dr-xr-x--- 4 nabijaczleweli users 0 Jan 15 19:52 1409
dr-xr-x--- 3 nabijaczleweli users 0 Jan 15 19:52 1410
$ ls /run/febug/1409/
comparisons     cool_data
$ cat /run/febug/1409/*
24
-3 -2 -3 -2 -3 -2 3 -1 -2 -3 0 1 2 3 -1 -2 -3 0 1 2 3 -1 -2 -3 0 1 2 3 -1 2 1 0 1 2 3 -1 0 -1 0 1 2 3
$ cat /run/febug/1409/*
45
-3 -2 -3 -2 -3 -2 -3 -2 -2 -3 -3 -2 -1 3 -1 1 0 0 1 2 3 2 -1 3 0 1 2 3 -1 2 1 0 1 2 3 -1 0 -1 0 1 2 3
$ grep . /run/febug/*/*
/run/febug/1409/comparisons:71
/run/febug/1409/cool_data:-3 -3 -3 -3 -3 -3 -2 -2 -2 -2 -2 -2 -1 3 -1 1 0 0 1 2 3 2 -1 3 0 1 2 3 -1 2 1 0 1 2 3 -1 0 -1 0 1 2 3
/run/febug/1410/cool_data:3012987654ACEFOLJKODNIEMIGHBPPbdWwnfTpXQcreRlVvUSitZQWjRTYUazuqwertyuiopoxyhmYsgkq
$ kill %1
$ ls /run/febug/
1410
```

### How?

1. UNIX-domain SOCK_SEQPACKET (or SOCK_STREAM, if not available) at `[/var]/run/febug.sock` by default, with a corresponding mount at `[/var]/run/febug`
2. Debuggable client connects
4. When credentials are available, a directory appears, à la procfs
3. When client wants a variable debugged it sends a `febug_message` (`variable_id`, `variable_type`, `signal`, and `name` (see `febug-abi.h`)) – `name` gets a file under the directory
4. On `open()` of the file, the client is sent an `attn_febug_message` (`variable_id` and `variable_type`) and the write end of a pipe and (if `signal` wasn't `SIGKILL`) notified
5. `read()`s copy directly from the corresponding end of the pipe – the client *must* `close()` it by the time it returns from the signal handler (or, if using some other mechanism, when otherwise done representing)
6. When the variable goes out of scope, the client sends a `stop_febug_message` (`variable_id`) to deregister, disappearing the file
7. When client hangs up, its directory disappears

Or, perhaps (server is box, program is oval, user is trapezium):
[![graphviz diagram](how.png)](how.dot)

### Building

For a Linux system: [![builds.sr.ht status for sid](//builds.sr.ht/~nabijaczleweli/febug/commits/sid.yml.svg)](//builds.sr.ht/~nabijaczleweli/febug/commits/sid.yml)
  * install `libfuse3-dev`, `pkg-config`, and `mandoc`
  * `make`

For FreeBSD: [![builds.sr.ht status for latest FreeBSD](//builds.sr.ht/~nabijaczleweli/febug/commits/freebsd-latest.yml.svg)](//builds.sr.ht/~nabijaczleweli/febug/commits/freebsd-latest.yml)
  * install `gmake`, `fusefs-libs3`, and `pkgconf`
  * `gmake`

For NetBSD:
  * install `devel/gmake`
  * `gmake LTO=n`

For OpenBSD: [![builds.sr.ht status for latest OpenBSD](//builds.sr.ht/~nabijaczleweli/febug/commits/openbsd-latest.yml.svg)](//builds.sr.ht/~nabijaczleweli/febug/commits/openbsd-latest.yml)
  * install `gmake`
  * `gmake CXX=c++ LTO=n`

For the Macintosh:
  * install macFUSE and mandoc
  * `make`

For other platforms:
  * ports welcome!

To build the Rust crate, its examples, and documentation, install `cargo`/`rust`/`lang/rust[-bin]`/`rust` and run `[g]make rust-build rust-doc`,
but that is irrelevant to the casual builder.

The Python package can be installed by either copying `febug.py` to the PYTHONPATH,
or by running `[g]make python-build` (this requires python3) and installing packages out of `out/febug.py/dist/`.

dot(1) from graphviz is also needed to regenerate the diagram. though that itself is optional.

#### (End-user-visible) platform differences

When built for Linux, the default socket path is `/run/febug.sock`, otherwise it's `/var/run/febug.sock`.

On OpenBSD and Darwin the processes are authenticated by their effective UID/GID/PID.

Darwin doesn't support SOCK_SEQPACKET, SOCK_STREAM is used instead.

### Running

For a system-wide instance, run `febug /run/febug/ &` (or `/var/run/febug/`, or wherever else, as the case may be) as root.

To run a user-local instance, the `fusermount3` helper is required, and `export FEBUG_SOCKET=/run/user/$(id -u)/febug.sock`
followed by `febug /run/user/$(id -u)/febug/ &` should work for programs using libfebug and libfebug++;
programs using a different ABI wrapper are encouraged to respect this environment variable as well.

`init/` contains systemd units for these two use-cases (though that path has to be set manually in the debugged programs' environment),
FreeBSD/NetBSD and OpenBSD rc.d scripts for the global one.

See the files in `out/examples/`, which sort with sleeps in comparison functions, for how they operate.

### Installation

#### From Debian repository

The following line in `/etc/apt/sources.list` or equivalent:
```apt
deb [signed-by=/etc/apt/keyrings/nabijaczleweli.asc] https://debian.nabijaczleweli.xyz sid main
```

With [my PGP key](//nabijaczleweli.xyz/pgp.txt) (the two URLs are interchangeable):
```sh
sudo wget -O/etc/apt/keyrings/nabijaczleweli.asc https://debian.nabijaczleweli.xyz/nabijaczleweli.gpg.key
sudo wget -O/etc/apt/keyrings/nabijaczleweli.asc https://nabijaczleweli.xyz/pgp.txt
```
(you may need to create /etc/apt/keyrings on apt <2.4.0 (<=bullseye) manually).

Then the usual
```sh
sudo apt update
sudo apt install febug libfebug0 libfebug-dev libfebug++-dev
```
will work on amd64, x32, and i386.

See the [repository README](//debian.nabijaczleweli.xyz/README) or [the source package](//git.sr.ht/~nabijaczleweli/febug.deb) for more information.

#### From pkgsrc

```sh
git clone https://git.sr.ht/~nabijaczleweli/febug-pkgsrc /usr/pkgsrc/devel/febug  # or, indeed, where-ever the pkgsrc root is
```

And `make install` under `devel/febug` will work out-of-box on NetBSD and OpenBSD, but will need `pkg install fusefs-libs3` on FreeBSD.

#### From tar-ball

Release tarballs are signed with <nabijaczleweli@nabijaczleweli.xyz> (pull with WKD, but `7D69 474E 8402 8C5C C0C4  4163 BCFD 0B01 8D26 58F1`).
аnd stored in git notes as-if via [the example program](//man.sr.ht/git.sr.ht/#signing-tagsx27-tarballs)
and are thus available on the [refs listing](https://git.sr.ht/~nabijaczleweli/febug/refs)/tag page as .tar.gz.asc.

## Reporting bugs

There's [the tracker](//todo.sr.ht/~nabijaczleweli/febug), but also see the list below.

## Contributing

Send a patch inline, as an attachment, or a git link and a ref to pull from to [the list](//lists.sr.ht/~nabijaczleweli/febug)
([~nabijaczleweli/febug@lists.sr.ht](mailto:~nabijaczleweli/febug@lists.sr.ht)) or [me](mailto:nabijaczleweli@nabijaczleweli.xyz)
directly. I'm not picky, just please include the repo name in the subject prefix.

## Discussion

Please use the tracker, the list, or [mastussy](//101010.pl/@nabijaczleweli) (formerly [Twitter](//lfs.nabijaczleweli.xyz/0017-twitter-export#1349450713563279361)).

## Special thanks

To all who support further development on Patreon, in particular:
  * ThePhD
  * Embark Studios
  * Lars Strojny
  * EvModder
