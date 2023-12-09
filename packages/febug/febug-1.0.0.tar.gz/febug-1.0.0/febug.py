# SPDX-License-Identifier: 0BSD


import os, sys, struct, socket, array, signal, ctypes

_sysname = os.uname().sysname

SIGNUM = signal.SIGUSR2
SOCKET = "/run/febug.sock" if _sysname == "Linux" else "/var/run/febug.sock"


# struct [[packed]] febug_message {
# 	uint64_t variable_id;
# 	uint64_t variable_type;
# 	uint8_t  signal;
# 	char     name[/* Enough to bring the overall size to 4096. */];
# };
FebugMessage = struct.Struct('=QQB4079s')
assert(FebugMessage.size == 4096)

# struct [[packed]] stop_febug_message {
# 	uint64_t variable_id;
# };
StopFebugMessage = struct.Struct('=Q')
assert(StopFebugMessage.size == 8)

# struct [[packed]] attn_febug_message {
# 	uint64_t variable_id;
# 	uint64_t variable_type;
# };
AttnFebugMessage = struct.Struct('=QQ')
assert(AttnFebugMessage.size == 16)




# GUESS WHAT?? DARWIN DEFINES SOCK_SEQPACKET BUT DOESN'T ACTUALLY FUCKING SUPPORT IT (i.e. socket(2) returns EPROTONOSUPPORT). WHY? BECAUSE FUCK YOU.
_SOCK_SEQPACKET = socket.SOCK_STREAM if _sysname == "Darwin" else socket.SOCK_SEQPACKET

def ControlledSocket(path = SOCKET):
		if "FRBUG_DONT" in os.environ:
			return None

		sock = socket.socket(socket.AF_UNIX, _SOCK_SEQPACKET, 0)

		try:
			sock.connect(os.environ.get("FEBUG_SOCKET", path))
		except Exception as e:
			print("febug.ControlledSocket(): connect:", e, file=sys.stderr)
			return None

		if _sysname in ["Linux", "OpenBSD", "Darwin"]:
			# Handled automatically with SO_PASSCRED, also the manual variant didn't work for some reason
			# Only way is getsockopt(SO_PEERCRED)
			# Only way is getsockopt(LOCAL_PEERCRED)+getsockopt(LOCAL_PEEREPID)
			pass
		elif _sysname == "NetBSD":
			# Correct way is automatically via LOCAL_CREDS
			# However, the message /must/ be sent after the peer sets it; use a sync message from the server for this,
			# otherwise we sent the first febug_message too quickly sometimes
			try:
				assert(len(sock.recv(AttnFebugMessage.size)) == AttnFebugMessage.size)
			except Exception as e:
				print("febug.ControlledSocket(): recv:", e, file=sys.stderr)
				return None
		else:
			# // From FreeBSD 12.1-RELEASE-p7 /usr/include/socket.h:
			# #define CMGROUP_MAX 16
			# /*
			#  * Credentials structure, used to verify the identity of a peer
			#  * process that has sent us a message. This is allocated by the
			#  * peer process but filled in by the kernel. This prevents the
			#  * peer from lying about its identity. (Note that cmcred_groups[0]
			#  * is the effective GID.)
			#  */
			# struct cmsgcred {
			# 	pid_t	cmcred_pid;		/* PID of sending process */
			# 	uid_t	cmcred_uid;		/* real UID of sending process */
			# 	uid_t	cmcred_euid;		/* effective UID of sending process */
			# 	gid_t	cmcred_gid;		/* real GID of sending process */
			# 	short	cmcred_ngroups;		/* number or groups */
			# 	gid_t	cmcred_groups[CMGROUP_MAX];	/* groups */
			# };
			try:
				sock.sendmsg([], [(socket.SOL_SOCKET, socket.SCM_CREDS, bytes(socket.CMSG_SPACE(struct.calcsize("iiiis16i"))))])  # no way to get what size pid_t or gid_t is, assume int
			except Exception as e:
				print("febug.ControlledSocket(): sendmsg:", e, file=sys.stderr)
				return None

		return sock

CONTROLLED_SOCKET = ControlledSocket()


class Wrapper:
	def __init__(self, of, name, signal = SIGNUM):
		self.of = of
		self.name = name
		self.signal = signal

	def __enter__(self):
		if CONTROLLED_SOCKET:
			try:
				CONTROLLED_SOCKET.send(FebugMessage.pack(id(self), 0x57726170706572, self.signal, bytes(self.name, 'UTF-8')))  # 'Wrapper'
			except:
				pass
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if CONTROLLED_SOCKET:
			try:
				CONTROLLED_SOCKET.send(StopFebugMessage.pack(id(self)))
			except:
				pass


def debug_handler(sig, frame):
	if not CONTROLLED_SOCKET:
		return

	fd = array.array("i")
	try:
		afmsg_b, ancdata, flags, addr = CONTROLLED_SOCKET.recvmsg(AttnFebugMessage.size, socket.CMSG_SPACE(fd.itemsize))
	except Exception as e:
		print("febug.debug_handler(): recvmsg:", e, file=sys.stderr)
		return
	(variable_id, variable_type) = AttnFebugMessage.unpack(afmsg_b)
	if variable_type != 0x57726170706572:  # 'Wrapper'
		print("febug.debug_handler(): variable_type != 'Wrapper', dunno what to do", file=sys.stderr)
		return
	if len(ancdata):
		fd.frombytes(ancdata[0][2])
		fd = fd[0]
	else:
		print("febug.debug_handler(): no fd in cmsg", file=sys.stderr)
		return

	with os.fdopen(fd, "w") as retpipe:
		print(ctypes.cast(variable_id, ctypes.py_object).value.of, file=retpipe)
